"""
Stimulus set: 6 matched head-to-head pairs + 3 fillers (updated set).

Pairing (by list position), counterbalanced 3/3 on price level:
  Pair 1: crossing HIGHER   Pair 2: crossing LOWER
  Pair 3: crossing LOWER    Pair 4: crossing HIGHER
  Pair 5: crossing HIGHER   Pair 6: crossing LOWER

In every real pair:
  - CROSSING stock lands exactly on the round number at T2.
  - Twin never touches or crosses a multiple of 10 ($ pairs) / 1.00 (decimal pairs).
  - Both rising, linear, identical absolute step within pair (3 or 0.30).
"""

PAIRS = [
    {   "pair_id": 1, "round_number": 100, "decimals": 0,
        "crossing":    [97, 100, 103],
        "noncrossing": [93, 96, 99],          # below -> crossing HIGHER
    },
    {   "pair_id": 2, "round_number": 90, "decimals": 0,
        "crossing":    [87, 90, 93],
        "noncrossing": [101, 104, 107],       # above -> crossing LOWER
    },
    {   "pair_id": 3, "round_number": 50, "decimals": 0,
        "crossing":    [47, 50, 53],
        "noncrossing": [53, 56, 59],          # above -> crossing LOWER
    },
    {   "pair_id": 4, "round_number": 60, "decimals": 0,
        "crossing":    [57, 60, 63],
        "noncrossing": [41, 44, 47],          # below -> crossing HIGHER
    },
    {   "pair_id": 5, "round_number": 10.00, "decimals": 2,
        "crossing":    [9.70, 10.00, 10.30],
        "noncrossing": [9.30, 9.60, 9.90],    # below -> crossing HIGHER
    },
    {   "pair_id": 6, "round_number": 9.00, "decimals": 2,
        "crossing":    [8.70, 9.00, 9.30],
        "noncrossing": [10.30, 10.60, 10.90], # above -> crossing LOWER
    },

    # ---- FILLER pairs (unchanged): both non-round, attention check only ---
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
