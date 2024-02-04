import json


def tuple_key_to_str(t):
    return json.dumps(t)


# Your dictionary
candidate_pairs = {(0, 3): 10, (0, 4): 15, (3, 5): 10, (1, 7): 10, (2, 6): 10}

json_string = json.dumps({tuple_key_to_str(k): v for k, v in candidate_pairs.items()})

with open("candidate_pair.json", "w") as f:
    f.write(json_string)
