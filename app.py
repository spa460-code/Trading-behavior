"""
Round-number crossing — head-to-head allocation study (external simulator).

Flow:
  Qualtrics  --redirect-->  THIS APP  --redirect-->  Qualtrics
  (front end)              (6 trials)                (finish + payment)

Run locally:
    pip install -r requirements.txt
    python app.py
    # open http://127.0.0.1:5000/?PROLIFIC_PID=TEST123

Data:
    - Full log written to trading_sim.sqlite (one row per stock-allocation).
    - Results also passed back to Qualtrics in the return URL as embedded data.

EDIT ME:
    - QUALTRICS_RETURN_URL  (below) -> your survey's continue/return link
    - SECRET_KEY            (below) -> any long random string before deploying
"""

import os
import json
import random
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlencode

from flask import (
    Flask, request, session, redirect, render_template, g, abort, url_for
)

from stimuli import PAIRS, TOKENS_PER_TRIAL, MOMENTUM_MIN, MOMENTUM_MAX

# ---------------------------------------------------------------- config
QUALTRICS_RETURN_URL = "https://YOUR-UNIVERSITY.qualtrics.com/jfe/form/SV_XXXX"
SECRET_KEY = "change-me-to-a-long-random-string-before-deploying"
DB_PATH = os.path.join(os.path.dirname(__file__), "trading_sim.sqlite")

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------------------------------------------------------------- database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS participants (
        pid          TEXT PRIMARY KEY,
        started_at   TEXT,
        finished_at  TEXT,
        plan         TEXT          -- JSON: randomized trial order + side assignment
    );
    CREATE TABLE IF NOT EXISTS trials (
        pid            TEXT,
        trial_index    INTEGER,    -- order the participant saw it (0..N-1)
        pair_id        INTEGER,
        round_number   REAL,
        crossing_side  TEXT,       -- 'left' or 'right'
        alloc_left     INTEGER,
        alloc_right    INTEGER,
        crossing_share INTEGER,    -- tokens on the crossing stock (the DV)
        rt_ms          INTEGER,
        answered_at    TEXT
    );
    """)
    db.commit()
    db.close()

# ---------------------------------------------------------------- helpers
def build_plan():
    """Randomize pair order and, per pair, which side the crossing stock is on."""
    order = list(range(len(PAIRS)))
    random.shuffle(order)
    plan = []
    for pair_idx in order:
        side = random.choice(["left", "right"])
        plan.append({"pair_idx": pair_idx, "crossing_side": side})
    return plan

def trial_stimulus(step):
    """Return the two stocks for a given plan step, labelled only Stock A/B."""
    pair = PAIRS[step["pair_idx"]]
    if step["crossing_side"] == "left":
        left, right = pair["crossing"], pair["noncrossing"]
    else:
        left, right = pair["noncrossing"], pair["crossing"]
    return pair, left, right

# ---------------------------------------------------------------- routes
@app.route("/")
def entry():
    # Accept either Prolific's PROLIFIC_PID or a generic pid=
    pid = request.args.get("PROLIFIC_PID") or request.args.get("pid")
    if not pid:
        return ("Missing participant ID. This page must be reached from the "
                "survey link with ?PROLIFIC_PID=..."), 400

    plan = build_plan()
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO participants (pid, started_at, plan) VALUES (?,?,?)",
        (pid, datetime.now(timezone.utc).isoformat(), json.dumps(plan)),
    )
    db.commit()

    session.clear()
    session["pid"] = pid
    session["plan"] = plan
    return render_template("instructions.html",
                           n_trials=len(plan), tokens=TOKENS_PER_TRIAL)

@app.route("/trial/<int:n>", methods=["GET", "POST"])
def trial(n):
    if "pid" not in session:
        abort(403)
    plan = session["plan"]
    if n < 0 or n >= len(plan):
        return redirect(url_for("finish"))

    step = plan[n]
    pair, left, right = trial_stimulus(step)

    if request.method == "POST":
        try:
            alloc_left = int(request.form["alloc_left"])
        except (KeyError, ValueError):
            abort(400)
        alloc_right = TOKENS_PER_TRIAL - alloc_left
        rt_ms = request.form.get("rt_ms", type=int)

        crossing_share = alloc_left if step["crossing_side"] == "left" else alloc_right

        db = get_db()
        db.execute(
            """INSERT INTO trials
               (pid, trial_index, pair_id, round_number, crossing_side,
                alloc_left, alloc_right, crossing_share, rt_ms, answered_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (session["pid"], n, pair["pair_id"], pair["round_number"],
             step["crossing_side"], alloc_left, alloc_right,
             crossing_share, rt_ms, datetime.now(timezone.utc).isoformat()),
        )
        db.commit()
        return redirect(url_for("trial", n=n + 1))

    return render_template(
        "trial.html",
        n=n, total=len(plan), tokens=TOKENS_PER_TRIAL,
        mom_min=MOMENTUM_MIN, mom_max=MOMENTUM_MAX,
        left_prices=left, right_prices=right, decimals=pair["decimals"],
    )

@app.route("/finish")
def finish():
    if "pid" not in session:
        abort(403)
    pid = session["pid"]
    db = get_db()
    db.execute("UPDATE participants SET finished_at=? WHERE pid=?",
               (datetime.now(timezone.utc).isoformat(), pid))
    db.commit()

    # Compact results to hand back to Qualtrics: crossing share per pair_id.
    rows = db.execute(
        "SELECT pair_id, crossing_share FROM trials WHERE pid=?", (pid,)
    ).fetchall()
    params = {"PROLIFIC_PID": pid, "task_complete": 1}
    for r in rows:
        params[f"cross_p{r['pair_id']}"] = r["crossing_share"]

    session.clear()
    return redirect(f"{QUALTRICS_RETURN_URL}?{urlencode(params)}")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
