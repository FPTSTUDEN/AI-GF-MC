import time

COOLDOWN_SECONDS = 3
hostile_mob_types = {"Zombie", "Skeleton", "Creeper", "Spider", "Enderman"}

def update_state(state: dict, event) -> None:
    mood = state["mood"]

    if event.type == "player_death":
        mood["stress"] = min(1.0, mood["stress"] + 0.25)
        mood["confidence"] = max(0.0, mood["confidence"] - 0.2)
        state["stats"]["recent_deaths"] += 1
    elif event.type == "under_attack":
        mood["stress"] = min(1.0, mood["stress"] + 0.5)
        mood["confidence"] = max(0.0, mood["confidence"] - 0.5)
    elif event.type == "player_damage":
        mood["stress"] = min(1.0, mood["stress"] + 0.1)
        mood["confidence"] = max(0.0, mood["confidence"] - 0.1)
    elif event.type == "victim_damage" and event.mob in hostile_mob_types:
        mood["confidence"] = min(1.0, mood["confidence"] + 1)
        mood["stress"] = max(0.0, mood["stress"] - 1)

def should_comment(state: dict, event) -> bool:
    now = time.time()
    last = state["stats"]["last_comment_time"]
    last_topic = state["stats"]["last_comment_topic"]
    if event.type in ("achievement", "death", "player_death"):
        return True
    if now - last < COOLDOWN_SECONDS:
        return False
    if event.type == last_topic:
        last_topic = ""
        return False

    state["stats"]["last_comment_time"] = now
    return True

def decide_intent(state: dict, event) -> str:
    mood = state["mood"]

    if event.type in ("death", "player_death"):
        if mood["stress"] > 0.6:
            return "comfort"
        return "tease"

    if event.type == "achievement":
        return "celebrate"

    return "comment"
