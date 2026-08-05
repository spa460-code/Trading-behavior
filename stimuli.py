"""
Stimulus set: 8 matched head-to-head pairs + 3 fillers (Adam's handwritten set).

Counterbalanced 4/4 on price level:
  Pairs 1-4: twin ABOVE  -> crossing LOWER-priced
  Pairs 5-8: twin BELOW  -> crossing HIGHER-priced

In every real pair:
  - CROSSING stock lands exactly on the round number at T2.
  - Twin never touches or crosses a salient round number.
  - Both rising, linear, identical absolute step within pair.
Step sizes vary across pairs at the same round ($50: steps 2 & 3; $100:
steps 3 & 1), giving slope variation within price level.
"""

PAIRS = [
    # ---- twin ABOVE: crossing is the LOWER-priced stock -------------------
    {   "pair_id": 1, "round_number": 10.00, "decimals": 2,
        "crossing":    [9.70, 10.00, 10.30],
        "noncrossing": [10.30, 10.60, 10.90],
    },
    {   "pair_id": 2, "round_number": 50, "decimals": 0,
        "crossing":    [48, 50, 52],
        "noncrossing": [54, 56, 58],
    },
    {   "pair_id": 3, "round_number": 100, "decimals": 0,
        "crossing":    [97, 100, 103],
        "noncrossing": [101, 104, 107],
    },
    {   "pair_id": 4, "round_number": 150, "decimals": 0,
        "crossing":    [149, 150, 151],
        "noncrossing": [151, 152, 153],
    },

    # ---- twin BELOW: crossing is the HIGHER-priced stock ------------------
    {   "pair_id": 5, "round_number": 9.00, "decimals": 2,
        "crossing":    [8.70, 9.00, 9.30],
        "noncrossing": [8.30, 8.60, 8.90],
    },
    {   "pair_id": 6, "round_number": 50, "decimals": 0,
        "crossing":    [47, 50, 53],
        "noncrossing": [43, 46, 49],
    },
    {   "pair_id": 7, "round_number": 100, "decimals": 0,
        "crossing":    [99, 100, 101],
        "noncrossing": [97, 98, 99],
    },
    {   "pair_id": 8, "round_number": 200, "decimals": 0,
        "crossing":    [197, 200, 203],
        "noncrossing": [193, 196, 199],
    },

    # ---- FILLER pairs: both non-round, attention check only ---------------
    {   "pair_id": 9, "round_number": None, "decimals": 0,
        "crossing":    [134, 136, 138],
        "noncrossing": [262, 264, 266], "filler": True,
    },
    {   "pair_id": 10, "round_number": None, "decimals": 0,
        "crossing":    [43, 44, 46],
        "noncrossing": [326, 327, 329], "filler": True,
    },
    {   "pair_id": 11, "round_number": None, "decimals": 0,
        "crossing":    [71, 73, 74],
        "noncrossing": [182, 184, 186], "filler": True,
    },
]

TOKENS_PER_TRIAL = 10
MOMENTUM_MIN = 1
MOMENTUM_MAX = 7
