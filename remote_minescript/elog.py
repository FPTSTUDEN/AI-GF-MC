from minescript import *
import time
import math

LOG_FILE = "event_log.txt"

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    line = f"[{now()}] {msg}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    chat(msg)

def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

# ------------------ state ------------------

last_pos = None
last_health = None
seen_entity_ids = set()

# ------------------ main ------------------

def main():
    global last_pos, last_health

    player = get_player()
    last_pos = player.position  # tuple (x, y, z)
    last_health = player.health # float

    log("Event logger started")

    while True:
        player = get_player()

        # ---- footsteps (movement) ----
        if distance(player.position, last_pos) > 0.25:
            log("Player moved (footsteps)")

        # ---- damage detection ----
        if player.health < last_health:
            log(f"Player took damage ({last_health - player.health})")

        # ---- nearby hostile mobs ----
        # for e in entities(): echo(e['name'])
        for e in get_entities():
            if e.id not in seen_entity_ids:
                # if e.type in (
                #     "minecraft:creeper",
                #     "minecraft:zombie",
                #     "minecraft:skeleton",
                #     "minecraft:spider"
                # ):
                    for monster in ["creeper","zombie","skeleton"]:
                        if monster in e.type:
                            log(f"Hostile mob nearby: {e.type}")
                            seen_entity_ids.add(e.id)

        last_pos = player.position
        last_health = player.health

        time.sleep(0.3)

main()
