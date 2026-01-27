import json
import time
from pathlib import Path

LOG_FILE = Path("events.log")
#./minescript/single_event.log
SINGLE_EVENT_LOG_FILE = Path("minescript/single_event.log")
# ---------- config ----------
UNDER_ATTACK_WINDOW = 4.0
UNDER_ATTACK_HITS = 3
IMMINENT_THREAT_WINDOW = 4.0

RATE_LIMITS = {
    "low_health": 5,
    "imminent_threat": 4,
    "under_attack": 3
}
# ----------------------------

LAST_EMIT = {}

player_damage_times = []
victim_damage_times = {}
recent_threats = []

# ---------- utilities ----------
def now():
    return time.time()

def rate_limited(event_type):
    t = now()
    last = LAST_EMIT.get(event_type, 0)

    if t - last < RATE_LIMITS.get(event_type, 0):
        return True

    LAST_EMIT[event_type] = t
    return False
def write_event(event: dict):
    event["timestamp"] = int(time.time())

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    with SINGLE_EVENT_LOG_FILE.open("w", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
