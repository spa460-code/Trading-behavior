"""
TB51 stimulus set (Saeed's revision, Oct 26): 12 single-stock price sequences.
2 (round vs non-round) x 2 (down vs up), 3 trials per cell.
end_dist = size of the last step (middle -> last) in %, 1 / 3 / 7, same in every cell.
"""

TRIALS = [
    # ---- Round, down ----
    {"trial_id": 1,  "cond": "round",    "direction": "down", "level": 10,  "end_dist": 1, "decimals": 2, "prices": [10.40, 10.00, 9.90]},
    {"trial_id": 2,  "cond": "round",    "direction": "down", "level": 100, "end_dist": 3, "decimals": 0, "prices": [103, 100, 97]},
    {"trial_id": 3,  "cond": "round",    "direction": "down", "level": 50,  "end_dist": 7, "decimals": 2, "prices": [51.00, 50.00, 46.00]},
    # ---- Round, up ----
    {"trial_id": 4,  "cond": "round",    "direction": "up",   "level": 20,  "end_dist": 7, "decimals": 2, "prices": [19.40, 20.00, 21.40]},
    {"trial_id": 5,  "cond": "round",    "direction": "up",   "level": 5,   "end_dist": 3, "decimals": 2, "prices": [4.85, 5.00, 5.15]},
    {"trial_id": 6,  "cond": "round",    "direction": "up",   "level": 200, "end_dist": 1, "decimals": 0, "prices": [199, 200, 202]},
    # ---- Non-round, down ----
    {"trial_id": 7,  "cond": "nonround", "direction": "down", "level": 10,  "end_dist": 1, "decimals": 2, "prices": [9.62, 9.32, 9.22]},
    {"trial_id": 8,  "cond": "nonround", "direction": "down", "level": 100, "end_dist": 3, "decimals": 0, "prices": [97, 94, 91]},
    {"trial_id": 9,  "cond": "nonround", "direction": "down", "level": 50,  "end_dist": 7, "decimals": 2, "prices": [47.10, 45.90, 42.50]},
    # ---- Non-round, up ----
    {"trial_id": 10, "cond": "nonround", "direction": "up",   "level": 20,  "end_dist": 7, "decimals": 2, "prices": [17.70, 18.20, 19.47]},
    {"trial_id": 11, "cond": "nonround", "direction": "up",   "level": 5,   "end_dist": 3, "decimals": 2, "prices": [5.27, 5.44, 5.60]},
    {"trial_id": 12, "cond": "nonround", "direction": "up",   "level": 200, "end_dist": 1, "decimals": 0, "prices": [206, 207, 209]},
]

