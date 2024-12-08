import json
import os

# Load all users from userDB.json
with open('api/userDB.json', 'r', encoding='utf-8') as f:
    all_users = json.load(f)

# Define solo rank priority for sorting
solo_rank_priority = [
    "challenger", "grandmaster", "master", "diamond", "emerald", 
    "platinum", "gold", "silver", "iron", "unranked"
]

def parse_solo_rank(solo: str) -> tuple:
    """
    Parse the solo rank string and return a tuple for sorting.
    Args:
        solo (str): The solo rank string (e.g., "emerald 1 - 75LP").
    Returns:
        tuple: (rank_priority, division, LP), where rank_priority is an index,
               division is an integer (lower is better), and LP is an integer.
    """
    try:
        # Extract rank, division, and LP
        rank, details = solo.split(" ", 1)
        division, lp = details.split(" - ")
        rank_priority = solo_rank_priority.index(rank.lower())
        division = int(division)  # Convert division to integer
        lp = int(lp.replace("LP", ""))  # Convert LP to integer
        return rank_priority, division, lp
    except Exception:
        # Handle unknown or invalid rank formats
        return len(solo_rank_priority), 5, 0  # Default to lowest priority

def ranking(major: str):
    """
    Rank users of the same major based on their solo rank.
    Args:
        major (str): The major to filter users by.
    Returns:
        List[Dict]: A list of ranked users with their solo rank.
    """
    same_major = []

    # Filter users by major
    for email, user_data in all_users.items():
        if user_data['major'] == major:
            nickname = user_data['nickname']
            file_path = f"api/user/{nickname}.json"
            
            # Check if the user's JSON file exists
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as user_file:
                    user_details = json.load(user_file)
                    # Extract solo rank from the user's JSON file
                    solo_rank = user_details[0].get('solo', 'unknown')
                    same_major.append({
                        "email": email,
                        "nickname": nickname,
                        "solo_rank": solo_rank
                    })
    
    # Sort users by solo rank using parsed rank details
    sorted_users = sorted(
        same_major,
        key=lambda user: parse_solo_rank(user['solo_rank'])
    )
    
    return sorted_users


ranked_users = ranking("소프트")

for idx, user in enumerate(ranked_users, start=1):
    print(f"Rank {idx}: {user['nickname']} ({user['solo_rank']})")