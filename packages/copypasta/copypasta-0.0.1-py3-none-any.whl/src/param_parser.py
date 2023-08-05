import json

def parse_json(filepath):
    with open(filepath) as f:
        return json.loads(f.read())
