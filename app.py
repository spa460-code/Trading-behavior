"""
TB51 — Round-number crossing, forced sell/buy decision.

Flow:
  Qualtrics  --redirect-->  THIS APP  --redirect-->  Qualtrics
  (consent, checks)        (12 trials, 2 screens each)   (demographics, Prolific completion)

Each trial is ONE screen: all three prices shown at once, then
"Sell some of my shares" vs "Buy more shares". Nothing else.

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
        rt_t<id>  reaction time (ms)
        task_complete
"""

import os, io, csv, json, random, sqlite3
from datetime import datetime, timezone
from urllib.parse import urlencode
from flask import Flask, request, session, redirect, render_template, g, abort, url_for, Response

from stimuli import TRIALS

# ---------------------------------------------------------------- config
QUALTRICS_RETURN_URL = os.environ.get("QUALTRICS_RETURN_URL",
    "https://uky.az1.qualtrics.com/jfe/form/SV_REPLACE_ME")
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-to-a-long-random-string")
EXPORT_KEY = os.environ.get("EXPORT_KEY", "change-me-too")
DB_PATH = os.path.join(os.path.dirname(__file__), "trading_sim.sqlite")

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
        pid TEXT PRIMARY KEY, started_at TEXT, finished_at TEXT, plan TEXT);
    CREATE TABLE IF NOT EXISTS trials (
        pid TEXT, trial_index INTEGER, trial_id INTEGER, cond TEXT, direction TEXT,
        level REAL, end_dist INTEGER, prices TEXT,
        choice TEXT, rt_ms INTEGER, answered_at TEXT,
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
    plan = [t["trial_id"] for t in TRIALS]; random.shuffle(plan)

    db = get_db()
    db.execute("INSERT OR REPLACE INTO participants (pid, started_at, plan) VALUES (?,?,?)",
               (pid, datetime.now(timezone.utc).isoformat(), json.dumps(plan)))
    db.commit()

    session.clear()
    session["pid"] = pid; session["plan"] = plan
    return render_template("instructions.html", n_trials=len(plan))

@app.route("/trial/<int:n>", methods=["GET", "POST"])
def trial(n):
    if "pid" not in session: abort(403)
    trial = current_trial(n)
    if trial is None: return redirect(url_for("finish"))

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice not in ("S", "B"): abort(400)
        upsert_trial(n, trial, choice=choice, rt_ms=request.form.get("rt_ms", type=int))
        return redirect(url_for("trial", n=n + 1))

    return render_template("trial.html", n=n, total=len(session["plan"]), prices=trial["prices"],
                           decimals=trial["decimals"])

@app.route("/finish")
def finish():
    if "pid" not in session: abort(403)
    pid = session["pid"]; db = get_db()
    db.execute("UPDATE participants SET finished_at=? WHERE pid=?", (datetime.now(timezone.utc).isoformat(), pid))
    db.commit()
    rows = db.execute("SELECT * FROM trials WHERE pid=?", (pid,)).fetchall()
    params = {"PROLIFIC_PID": pid, "task_complete": 1}
    for r in rows:
        t = r["trial_id"]
        params[f"ch_t{t}"] = r["choice"] or ""
        params[f"rt_t{t}"] = r["rt_ms"] or ""
    session.clear()
    return redirect(f"{QUALTRICS_RETURN_URL}?{urlencode(params)}")

@app.route("/export")
def export():
    if request.args.get("key") != EXPORT_KEY: abort(403)
    db = get_db()
    rows = db.execute("SELECT t.*, p.started_at, p.finished_at FROM trials t JOIN participants p USING (pid) ORDER BY pid, trial_index").fetchall()
    buf = io.StringIO(); w = csv.writer(buf)
    if rows: w.writerow(rows[0].keys())
    for r in rows: w.writerow(tuple(r))
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=tb51_trials.csv"})

if __name__ == "__main__":
    app.run(debug=True)
