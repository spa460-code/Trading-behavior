"""
Stimulus set: 3 matched head-to-head pairs + 3 fillers — UPWARD, tight steps.

All sequences RISE with identical steps within pair. Crossing stock lands
exactly on the round number at T2; twin never touches a salient round.

Pair 1: crossing HIGHER-priced (twin just below)
Pair 2: crossing HIGHER-priced (twin just below)
Pair 3: crossing LOWER-priced  (twin just above)

Filler pair_ids are 7-9 so existing Qualtrics fields (fill_p7-9) apply.
"""

PAIRS = [
    {   "pair_id": 1, "round_number": 10.00, "decimals": 2,
        "crossing":    [9.99, 10.00, 10.01],
        "noncrossing": [9.97, 9.98, 9.99],
    },
    {   "pair_id": 2, "round_number": 150, "decimals": 0,
        "crossing":    [149, 150, 151],
        "noncrossing": [147, 148, 149],
    },
    {   "pair_id": 3, "round_number": 500, "decimals": 0,
        "crossing":    [499, 500, 501],
        "noncrossing": [501, 502, 503],
    },

    # ---- FILLER pairs: both non-round, rising, attention check only -------
    {   "pair_id": 7, "round_number": None, "decimals": 0,
        "crossing":    [134, 136, 138],
        "noncrossing": [262, 264, 266], "filler": True,
    },
    {   "pair_id": 8, "round_number": None, "decimals": 0,
        "crossing":    [43, 44, 46],
        "noncrossing": [326, 327, 329], "filler": True,
    },
    {   "pair_id": 9, "round_number": None, "decimals": 0,
        "crossing":    [71, 73, 74],
        "noncrossing": [182, 184, 186], "filler": True,
    },
]

TOKENS_PER_TRIAL = 10
MOMENTUM_MIN = 1
MOMENTUM_MAX = 7
