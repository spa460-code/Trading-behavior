"""
Stimulus set: 3 matched head-to-head pairs + 3 fillers — DOWNWARD direction.

All sequences FALL. The crossing stock lands exactly on the round number
at T2 (falling through it); the twin never touches a salient round number.

Pair 1: crossing HIGHER-priced   (twin below)
Pair 2: crossing HIGHER-priced   (twin below)
Pair 3: crossing LOWER-priced    (twin above)

Fillers fall as well (reversed from the upward set), both stocks non-round.
Filler pair_ids are 7-9 so the existing Qualtrics fields (fill_p7-9) apply.
"""

PAIRS = [
    {   "pair_id": 1, "round_number": 10.00, "decimals": 2,
        "crossing":    [10.01, 10.00, 9.99],
        "noncrossing": [9.90, 9.80, 9.70],
    },
    {   "pair_id": 2, "round_number": 150, "decimals": 0,
        "crossing":    [151, 150, 149],
        "noncrossing": [144, 143, 142],
    },
    {   "pair_id": 3, "round_number": 500, "decimals": 0,
        "crossing":    [501, 500, 499],
        "noncrossing": [509, 508, 507],
    },

    # ---- FILLER pairs: both non-round, falling, attention check only ------
    {   "pair_id": 7, "round_number": None, "decimals": 0,
        "crossing":    [138, 136, 134],
        "noncrossing": [266, 264, 262], "filler": True,
    },
    {   "pair_id": 8, "round_number": None, "decimals": 0,
        "crossing":    [46, 44, 43],
        "noncrossing": [329, 327, 326], "filler": True,
    },
    {   "pair_id": 9, "round_number": None, "decimals": 0,
        "crossing":    [74, 73, 71],
        "noncrossing": [186, 184, 182], "filler": True,
    },
]

TOKENS_PER_TRIAL = 10
MOMENTUM_MIN = 1
MOMENTUM_MAX = 7
