"""
Stimulus set: 6 matched head-to-head pairs (rising, against-the-effect).

Each pair has:
  - a CROSSING stock: lands exactly on the round number at T2 (max salience),
    and carries a marginally LARGER % rise than its twin (against-the-effect).
  - a NON-CROSSING twin: same neighborhood, stays on one side of the round number.

All sequences are three displayed prices, linear / equal-step (removes the
deceleration confound), rising.

To ADD counterbalancing (twin below vs. above the round number) or filler pairs,
just extend this list — the rest of the app reads it generically.
"""

PAIRS = [
    {
        "pair_id": 1,
        "round_number": 1.00,
        "crossing":     [0.98, 1.00, 1.02],   # +4.08%
        "noncrossing":  [1.04, 1.06, 1.08],   # +3.85%
        "decimals": 2,
    },
    {
        "pair_id": 2,
        "round_number": 10.00,
        "crossing":     [9.90, 10.00, 10.10], # +2.02%
        "noncrossing":  [10.20, 10.30, 10.40],# +1.96%
        "decimals": 2,
    },
    {
        "pair_id": 3,
        "round_number": 100,
        "crossing":     [98, 100, 102],       # +4.08%
        "noncrossing":  [104, 106, 108],      # +3.85%
        "decimals": 0,
    },
    {
        "pair_id": 4,
        "round_number": 500,
        "crossing":     [495, 500, 505],      # +2.02%
        "noncrossing":  [510, 515, 520],      # +1.96%
        "decimals": 0,
    },
    {
        "pair_id": 5,
        "round_number": 900,
        "crossing":     [882, 900, 918],      # +4.08%
        "noncrossing":  [936, 954, 972],      # +3.85%
        "decimals": 0,
    },
    {
        "pair_id": 6,
        "round_number": 1000,
        "crossing":     [985, 1000, 1015],    # +3.05%
        "noncrossing":  [1030, 1045, 1060],   # +2.91%
        "decimals": 0,
    },

    # ---- FILLER pairs: BOTH stocks non-round, no crossing. -------------
    # Shown to participants but NOT part of the DV (never passed to Qualtrics).
    # "crossing"/"noncrossing" here are just left/right labels — neither
    # sequence lands on or crosses a salient round number.
    {
        "pair_id": 7,
        "round_number": None,
        "crossing":     [64.36, 65.46, 66.32],
        "noncrossing":  [71.28, 72.41, 73.55],
        "decimals": 2,
        "filler": True,
    },
    {
        "pair_id": 8,
        "round_number": None,
        "crossing":     [23.17, 23.61, 24.08],
        "noncrossing":  [38.44, 39.02, 39.63],
        "decimals": 2,
        "filler": True,
    },
    {
        "pair_id": 9,
        "round_number": None,
        "crossing":     [142.30, 144.10, 145.80],
        "noncrossing":  [213.40, 215.10, 216.80],
        "decimals": 2,
        "filler": True,
    },
]

TOKENS_PER_TRIAL = 10   # budget to split on each screen
MOMENTUM_MIN = 1
MOMENTUM_MAX = 7
