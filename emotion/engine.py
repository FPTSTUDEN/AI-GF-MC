import time

COOLDOWN_SECONDS = 4

def update_state(state: dict, event) -> None:
    mood = state["mood"]

    if event.type == "death":
        mood["stress"] = min(1.0, mood["stress"] + 0.25)
        mood["confidence"] = max(0.0, mood["confidence"] - 0.2)
        state["stats"]["recent_deaths"] += 1

    # elif event.type == "achievement":
    #     mood["excitement"] = min(1.0, mood["excitement"] + 0.3)
    #     mood["confidence"] = min(1.0, mood["confidence"] + 0.2)

def should_comment(state: dict) -> bool:
    now = time.time()
    last = state["stats"]["last_comment_time"]

    if now - last < COOLDOWN_SECONDS:
        return False

    state["stats"]["last_comment_time"] = now
    return True

def decide_intent(state: dict, event) -> str:
    mood = state["mood"]

    if event.type == "death":
        if mood["stress"] > 0.6:
            return "comfort"
        return "tease"

    if event.type == "achievement":
        return "celebrate"

    return "comment"
