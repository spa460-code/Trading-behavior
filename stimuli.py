"""
Stimulus set: 6 matched head-to-head pairs + 3 fillers.

COUNTERBALANCED DESIGN (controls for price level):
  - In 3 pairs the crossing stock is the LOWER-priced of the two (twin sits above).
  - In 3 pairs the crossing stock is the HIGHER-priced of the two (twin sits below).
  So across the set, "crossing" is not systematically the cheaper or pricier stock.

In every real pair:
  - The CROSSING stock lands exactly on the round number at T2 (max salience).
  - The twin NEVER touches or crosses a salient round number.
  - Both sequences are rising and linear (equal step within each stock -> no
    deceleration confound).
  - % change is closely matched; the crossing stock rises a hair more on average.

Price levels reuse magnitudes validated in Studies 2a / 2b / 3.
"""

PAIRS = [
    # ---- Pair 1: round 1.00 | crossing LOWER (twin above) ----
    {   "pair_id": 1, "round_number": 1.00, "decimals": 2,
        "crossing":    [0.98, 1.00, 1.02],   # +4.08%
        "noncrossing": [1.04, 1.06, 1.08],   # +3.85%, sits above 1.00
    },
    # ---- Pair 2: round 10.00 | crossing HIGHER (twin below) ----
    {   "pair_id": 2, "round_number": 10.00, "decimals": 2,
        "crossing":    [9.90, 10.00, 10.10], # +2.02%
        "noncrossing": [9.60, 9.70, 9.80],   # +2.08%, stays below 10.00
    },
    # ---- Pair 3: round 100 | crossing LOWER (twin above) ----
    {   "pair_id": 3, "round_number": 100, "decimals": 0,
        "crossing":    [98, 100, 102],       # +4.08%
        "noncrossing": [104, 106, 108],      # +3.85%, sits above 100
    },
    # ---- Pair 4: round 150 | crossing HIGHER (twin below) ----
    {   "pair_id": 4, "round_number": 150, "decimals": 0,
        "crossing":    [149, 150, 151],      # +1.34%
        "noncrossing": [146, 147, 148],      # +1.37%, stays below 150
    },
    # ---- Pair 5: round 500 | crossing LOWER (twin above) ----
    {   "pair_id": 5, "round_number": 500, "decimals": 0,
        "crossing":    [495, 500, 505],      # +2.02%
        "noncrossing": [510, 515, 520],      # +1.96%, sits above 500
    },
    # ---- Pair 6: round 1000 | crossing HIGHER (twin below) ----
    {   "pair_id": 6, "round_number": 1000, "decimals": 0,
        "crossing":    [995, 1000, 1005],    # +1.01%
        "noncrossing": [984, 989, 994],      # +1.02%, stays below 1000
    },

    # ---- FILLER pairs: BOTH stocks non-round, no crossing (attention checks) ----
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
