import json
from events.event_schema import GameEvent

def replay_events(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield GameEvent(**json.loads(line))
