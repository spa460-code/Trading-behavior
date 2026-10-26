"""
TB51 — Round-number crossing, forced sell/buy decision + continuation belief.

Flow:
  Qualtrics  --redirect-->  THIS APP  --redirect-->  Qualtrics
  (consent, checks)        (12 trials, 2 screens each)   (demographics, Prolific completion)

Each trial has two screens: ACTION (sell vs buy + strength 1-7) and BELIEF
(1 reverse ... 7 continue). Screen order is counterbalanced between
participants (belief_first = 0/1), assigned at random on entry, or forced
with ?bf=0 / ?bf=1 in the entry link if Qualtrics does the randomizing.

Run locally:
    pip install -r requirements.txt
    python app.py
    # open http://127.0.0.1:5000/?PROLIFIC_PID=TEST123

Data:
    - trading_sim.sqlite on the server (one row per trial). NOTE: on Render's
      free tier the disk is wiped on every deploy, so the Qualtrics copy is the
      one that counts. /export?key=EXPORT_KEY downloads the sqlite log as CSV.
    - Every trial's answers are passed back to Qualtrics as URL parameters:
        ch_t<id>  choice: S (sell) or B (buy)
        st_t<id>  strength 1-7
        sg_t<id>  signed strength: -7..-1 sell, +1..+7 buy
        bl_t<id>  belief 1-7
        rta_t<id> / rtb_t<id>  reaction times (ms)
        belief_first, task_complete
"""

import os, io, csv, json, random, sqlite3
from datetime import datetime, timezone
from urllib.parse import urlencode
from flask import Flask, request, session, redirect, render_template, g, abort, url_for, Response

from stimuli import TRIALS, SHARES_OWNED, STRENGTH_MIN, STRENGTH_MAX, BELIEF_MIN, BELIEF_MAX

# ---------------------------------------------------------------- config
QUALTRICS_RETURN_URL = os.environ.get("QUALTRICS_RETURN_URL",
    "https://uky.az1.qualtrics.com/jfe/form/SV_REPLACE_ME")
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-to-a-long-random-string")
EXPORT_KEY = os.environ.get("EXPORT_KEY", "change-me-too")
DB_PATH = os.path.join(os.path.dirname(__file__), "trading_sim.sqlite")
REVEAL_MS = 700   # delay between the three prices appearing

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------------------------------------------------------------- database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH); g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None: db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS participants (
        pid TEXT PRIMARY KEY, started_at TEXT, finished_at TEXT,
        belief_first INTEGER, plan TEXT);
    CREATE TABLE IF NOT EXISTS trials (
        pid TEXT, trial_index INTEGER, trial_id INTEGER, cond TEXT, direction TEXT,
        level REAL, end_dist INTEGER, prices TEXT,
        choice TEXT, strength INTEGER, signed INTEGER, belief INTEGER,
        rt_action_ms INTEGER, rt_belief_ms INTEGER, answered_at TEXT,
        PRIMARY KEY (pid, trial_id));
    """)
    db.commit(); db.close()

init_db()   # gunicorn never runs __main__, so init here

# ---------------------------------------------------------------- helpers
TRIAL_BY_ID = {t["trial_id"]: t for t in TRIALS}

def current_trial(n):
    plan = session.get("plan")
    if plan is None or n < 0 or n >= len(plan): return None
    return TRIAL_BY_ID[plan[n]]

def pages_for(session_):
    return ["belief", "action"] if session_["belief_first"] else ["action", "belief"]

def upsert_trial(n, trial, **fields):
    db = get_db()
    db.execute("INSERT OR IGNORE INTO trials (pid, trial_index, trial_id, cond, direction, level, end_dist, prices) VALUES (?,?,?,?,?,?,?,?)",
               (session["pid"], n, trial["trial_id"], trial["cond"], trial["direction"], trial["level"], trial["end_dist"], json.dumps(trial["prices"])))
    sets = ", ".join(f"{k}=?" for k in fields)
    db.execute(f"UPDATE trials SET {sets}, answered_at=? WHERE pid=? AND trial_id=?",
               (*fields.values(), datetime.now(timezone.utc).isoformat(), session["pid"], trial["trial_id"]))
    db.commit()

# ---------------------------------------------------------------- routes
@app.route("/")
def entry():
    pid = request.args.get("PROLIFIC_PID") or request.args.get("pid")
    if not pid:
        return ("Missing participant ID. This page must be reached from the survey link with ?PROLIFIC_PID=...", 400)
    bf = request.args.get("bf")
    belief_first = int(bf) if bf in ("0", "1") else random.choice([0, 1])
    plan = [t["trial_id"] for t in TRIALS]; random.shuffle(plan)

    db = get_db()
    db.execute("INSERT OR REPLACE INTO participants (pid, started_at, belief_first, plan) VALUES (?,?,?,?)",
               (pid, datetime.now(timezone.utc).isoformat(), belief_first, json.dumps(plan)))
    db.commit()

    session.clear()
    session["pid"] = pid; session["plan"] = plan; session["belief_first"] = belief_first
    return render_template("instructions.html", n_trials=len(plan), shares=SHARES_OWNED)

@app.route("/trial/<int:n>/<page>", methods=["GET", "POST"])
def trial(n, page):
    if "pid" not in session: abort(403)
    trial = current_trial(n)
    if trial is None: return redirect(url_for("finish"))
    order = pages_for(session)
    if page not in order: abort(404)

    if request.method == "POST":
        if page == "action":
            choice = request.form.get("choice")
            strength = request.form.get("strength", type=int)
            if choice not in ("S", "B") or strength is None or not (STRENGTH_MIN <= strength <= STRENGTH_MAX): abort(400)
            signed = strength if choice == "B" else -strength
            upsert_trial(n, trial, choice=choice, strength=strength, signed=signed,
                         rt_action_ms=request.form.get("rt_ms", type=int))
        else:
            belief = request.form.get("belief", type=int)
            if belief is None or not (BELIEF_MIN <= belief <= BELIEF_MAX): abort(400)
            upsert_trial(n, trial, belief=belief, rt_belief_ms=request.form.get("rt_ms", type=int))
        # next screen: second page of this trial, or first page of the next trial
        if page == order[0]:
            return redirect(url_for("trial", n=n, page=order[1]))
        return redirect(url_for("trial", n=n + 1, page=order[0]))

    tmpl = "trial_action.html" if page == "action" else "trial_belief.html"
    return render_template(tmpl, n=n, total=len(session["plan"]), prices=trial["prices"],
                           decimals=trial["decimals"], shares=SHARES_OWNED, reveal_ms=REVEAL_MS,
                           smin=STRENGTH_MIN, smax=STRENGTH_MAX, bmin=BELIEF_MIN, bmax=BELIEF_MAX,
                           first_page=(page == order[0]))

@app.route("/finish")
def finish():
    if "pid" not in session: abort(403)
    pid = session["pid"]; db = get_db()
    db.execute("UPDATE participants SET finished_at=? WHERE pid=?", (datetime.now(timezone.utc).isoformat(), pid))
    db.commit()
    rows = db.execute("SELECT * FROM trials WHERE pid=?", (pid,)).fetchall()
    params = {"PROLIFIC_PID": pid, "task_complete": 1, "belief_first": session["belief_first"]}
    for r in rows:
        t = r["trial_id"]
        params[f"ch_t{t}"] = r["choice"] or ""
        params[f"st_t{t}"] = r["strength"] if r["strength"] is not None else ""
        params[f"sg_t{t}"] = r["signed"] if r["signed"] is not None else ""
        params[f"bl_t{t}"] = r["belief"] if r["belief"] is not None else ""
        params[f"rta_t{t}"] = r["rt_action_ms"] or ""
        params[f"rtb_t{t}"] = r["rt_belief_ms"] or ""
    session.clear()
    return redirect(f"{QUALTRICS_RETURN_URL}?{urlencode(params)}")

@app.route("/export")
def export():
    if request.args.get("key") != EXPORT_KEY: abort(403)
    db = get_db()
    rows = db.execute("SELECT t.*, p.belief_first, p.started_at, p.finished_at FROM trials t JOIN participants p USING (pid) ORDER BY pid, trial_index").fetchall()
    buf = io.StringIO(); w = csv.writer(buf)
    if rows: w.writerow(rows[0].keys())
    for r in rows: w.writerow(tuple(r))
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=tb51_trials.csv"})

if __name__ == "__main__":
    app.run(debug=True)
