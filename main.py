import json
from llm.client import generate_response
from emotion.engine import update_state, decide_intent, should_comment
from events.event_schema import GameEvent
from events.severity import EVENT_SEVERITY, DEFAULT_SEVERITY
from events.event_reader import replay_events
def get_severity(event_type: str) -> float:
    return EVENT_SEVERITY.get(event_type, DEFAULT_SEVERITY)

STATE_FILE = "state/companion_state.json"
def describe_event(event):
    t = event.type

    if t == "under_attack":
        if getattr(event, "target", "") == "player":
            return f"The player is under sustained attack ({event.intensity} hits)."
        return f"A {event.mob} is under heavy attack."

    if t == "imminent_threat":
        return f"Multiple hostile mobs are closing in: {', '.join(event.mobs)}."

    if t == "death":
        return f"The player just died due to {event.cause}."

    if t == "biome_enter":
        return f"The player entered the {event.biome} biome."

    if t == "biome_exit":
        return f"The player left the {event.biome} biome after a long stay."

    if t == "low_health":
        return "The player's health is critically low."

    return f"Event occurred: {t}."


def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def build_prompt(event: GameEvent, mood: dict):
    urgency = (
        "critical" if event.severity >= 0.85 else
        "high" if event.severity >= 0.5 else #0.6 -> 0.5
        "low"
    )

    situation = []

    if event.type == "under_attack":
        who = "you" if event.target == "player" else event.target
        situation.append(
            f"{who} are taking damage"
            + (f" from {event.cause}" if event.cause else "")
            + (f" ({event.intensity} hits)" if event.count else "")
        )

    elif event.type == "imminent_threat":
        situation.append(
            f"Hostile mobs are closing in ({len(event.mobs)} nearby)"
        )

    elif event.type == "player_low_health":
        situation.append(
            f"Health is critically low ({event.health:.1f} HP)"
        )

    elif event.type == "player_death":
        situation.append(
            f"You just died due to {event.cause}"
        )

    elif event.type == "biome_enter":
        situation.append(
            f"You entered the {event.biome} biome"
        )

    elif event.type == "biome_exit":
        situation.append(
            f"You spent a long time in the {event.biome} biome"
        )
    else: 
        print(f"-----{event.type}-----")
        situation.append(str(event.type))

    return f"""
You are an AI companion observing a Minecraft session.

Situation:
- {'; '.join(situation)}
- Urgency: {urgency}

Player state:
- Stress: {mood['stress']:.2f}
- Confidence: {mood['confidence']:.2f}

Respond in 1 - 2 short, natural sentences.
No game mechanics.
""".strip()
# short sentences modification
# Removed: Stay in character. 

SEVERITY_THRESHOLD = 0.3  # tune this

def handle_event(event: GameEvent):
    state = load_state()

    severity = get_severity(event.type)
    event.severity = severity  # attach for prompt use

    update_state(state, event)

    # --- new gate ---
    if severity < SEVERITY_THRESHOLD:
        save_state(state)
        return
    # ----------------

    if not should_comment(state):
        save_state(state)
        return

    intent = decide_intent(state, event)
    prompt = build_prompt(event, state["mood"])  # pass mood dict, not intent

    response = generate_response(prompt)
    responses.append(response)

    # print("AI:", response)
    print(prompt)

    save_state(state)


# ---- TEST ----
if __name__ == "__main__":
    global responses
    responses=[]
    # test_event = GameEvent(type="death", cause="creeper")
    # handle_event(test_event)
    for event in replay_events("events.log"):
        handle_event(event)
    for res in responses:
        print(res)


'''
1. add debug printing for relevant parameters: should-comment, saved state... after each iteration
2. add minor logic fixes so overall structure is more refined
'''