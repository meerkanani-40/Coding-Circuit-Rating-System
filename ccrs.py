import pandas as pd
import random
from collections import defaultdict

# Constants
INITIAL_RATING = 1000
MIN_RATING = 1000
EARLY_K = 40
REGULAR_K = 20

# Rmid based on difficulty
RMID_MAP = {1: 1400,2: 1500,3: 1600}

# Actual problem solved
def actual_problems_solved(rating):
    if rating < 1300:
        return random.choices(range(1, 7), weights=[5,5,2,1,1,1])[0]
    elif rating < 1500:
        return random.choices(range(1, 7), weights=[1,2,8,2,1,1])[0]
    elif rating < 1800:
        return random.choices(range(1, 7), weights=[1,1,2,6,6,1])[0]
    else:
        return random.choices(range(1, 7), weights=[1,1,1,2,4,10])[0]
    
# Expected problem solved
def expected_problems_solved(rating, rmid):
    return 6/(1 + 10**((rmid - rating)/400))

# Decay function
def decay_rating(rating):
    decay = min(50, 0.05*(rating - MIN_RATING))
    return max(MIN_RATING, rating - decay)

# Load participant and event data
df = pd.read_csv("Participant_details.csv")
event_df = pd.read_csv("event_weights.csv")

# Parse list-like strings to actual lists
df['Events Participated'] = df['Events Participated'].apply(eval)

# Initialize storage
participants = {}
ratings_history = defaultdict(dict)

# Quick lookup for event info
event_info = {
    row['Event Number']: (row['Event Weightage'], row['Event Difficulty'])
    for _, row in event_df.iterrows()
}

# Initialize all participants
for _, row in df.iterrows():
    pid = row['Participant Number']
    participants[pid] = {
        "rating": INITIAL_RATING,
        "events": row["Events Participated"],
        "history": [],
        "last_event": -2,
        "event_count": 0
    }

# Simulate all events in sorted order
all_event_numbers = sorted(event_info.keys())

for event_num in all_event_numbers:
    weight, difficulty = event_info[event_num]
    rmid = RMID_MAP[difficulty]

    for pid, pdata in participants.items():
        # Decay if missed 2+ consecutive events
        if event_num - pdata["last_event"] >= 3:
            pdata["rating"] = decay_rating(pdata["rating"])

        if event_num in pdata["events"]:
            pdata["event_count"] += 1
            pdata["last_event"] = event_num
            rating = pdata["rating"]

            mu = expected_problems_solved(rating, rmid)
            S = actual_problems_solved(rating)

            K = EARLY_K if pdata["event_count"] < 3 else REGULAR_K
            delta = K * (S - mu) * weight
            new_rating = max(MIN_RATING, rating + delta)
            pdata["rating"] = new_rating
        else:
            new_rating = pdata["rating"]  # No change if not participated (except possible decay)

        pdata["history"].append((event_num, round(new_rating)))
        ratings_history[pid][event_num] = round(new_rating)

# Create final leaderboard
leaderboard = [(pid, round(data["rating"])) for pid, data in participants.items()]
leaderboard.sort(key=lambda x: x[1], reverse=True)

# Create and export history DataFrame
history_df = pd.DataFrame.from_dict(ratings_history, orient='index').sort_index()
history_df.index.name = "Participant Number"

leaderboard_df = pd.DataFrame(leaderboard, columns=["Participant Number", "Final Rating"])

# Export CSVs
history_df.to_csv("rating_history.csv")
leaderboard_df.to_csv("final_leaderboard.csv", index=False)

print("Files saved: rating_history.csv, final_leaderboard.csv")