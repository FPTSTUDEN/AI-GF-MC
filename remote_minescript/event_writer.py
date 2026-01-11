import json
import time
from pathlib import Path

LOG_FILE = Path("events.log")

# ---------- config ----------
UNDER_ATTACK_WINDOW = 2.0
UNDER_ATTACK_HITS = 3
IMMINENT_THREAT_WINDOW = 3.0

RATE_LIMITS = {
    "low_health": 5,
    "imminent_threat": 5,
    "under_attack": 5
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
