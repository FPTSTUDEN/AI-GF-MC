from minescript import *
import time
import math

# from minescript.system.lib.minescript import chat # no need 

LOG_FILE = "event_log.txt"

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    line = f"[{now()}] {msg}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    chat(msg)

def distance(now, last):
    dx = now[0] - last[0]
    dy = now[1] - last[1]
    dz = now[2] - last[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def direction_vector(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    dz = to_pos[2] - from_pos[2]
    direction=""
    if dx > 0:
        direction += "East "
    elif dx < 0:
        direction += "West "
    if dz > 0:
        direction += "South "
    elif dz < 0:
        direction += "North "
    if dy > 0:
        direction += "Up "
    elif dy < 0:
        direction += "Down "
    return (dx, dy, dz, direction)

def format_position(pos):
    return f"({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})"

# ------------------ state ------------------

last_pos = None
last_health = None
seen_entity_ids = set()

# ------------------ main ------------------
'''
Sample EntityData():
{
    'id': 12345,
    'type': 'entity.minecraft.zombie',
    'name': 'Zombie',
    'position': (x, y, z),
    'health': 20.0,
    'yaw': 0.0,
    'pitch': 0.0
}
'''
def main():
    global last_pos, last_health

    player = get_player()
    last_pos = player.position  # tuple (x, y, z)
    last_health = player.health # float
    last_seen_dangers=[]

    log("Event logger started")

    while True:
        player = get_player()

        # ---- footsteps (movement) ----
        if distance(player.position, last_pos) > 2.5:
            log(f"Player ran {direction_vector(last_pos, player.position)[3]}to {format_position(player.position)}")
        elif distance(player.position, last_pos) > 1.3:
            log(f"Player moved {direction_vector(last_pos, player.position)[3]}to {format_position(player.position)}")
        elif distance(player.position, last_pos) > 0.2:
            log(f"Player is shifting {direction_vector(last_pos, player.position)[3]}to {format_position(player.position)}")
        

        # ---- damage detection ----
        if player.health < last_health:
            damage = last_health - player.health
            log(f"Player took damage ({damage:.1f} HP)")

        # ---- nearby hostile mobs ----
        # for e in entities(): echo(e['name'])
        for e in get_entities():
            if e.id not in seen_entity_ids:
                    for monster in ["creeper","zombie","skeleton","spider","enderman","witch","drowned","husk","stray","phantom","pillager","ravager","evoker","vindicator"]:
                        if monster in e.type and distance(player.position, e.position) < 5:
                            log(f"Hostile mob nearby: {e.name} at {format_position(e.position)}")
                            seen_entity_ids.add(e.id)
            else:
                if e.id in [a.id for a in last_seen_dangers]:
                    last_danger=last_seen_dangers[[a.id for a in last_seen_dangers].index(e.id)]
                    proxity_before = distance(last_pos, last_danger.position)
                    proxity_now = distance(player.position, e.position)
                    if proxity_now>5:
                        last_seen_dangers.remove(last_seen_dangers[[a.id for a in last_seen_dangers].index(e.id)])
                        continue
                    if int(proxity_now*10) < int(proxity_before*10):
                        log(f"Careful! The #{e.id} {e.name} is getting closer!")
                    elif int(proxity_now*10) > int(proxity_before*10):
                        log(f"Luckily, the #{e.id} {e.name} is moving away.")
                    last_seen_dangers.remove(last_seen_dangers[[a.id for a in last_seen_dangers].index(e.id)])
                last_seen_dangers.append(e) if len(last_seen_dangers)<5 else last_seen_dangers.append(e) and last_seen_dangers.pop(0)
                # debug: print last_seen_dangers name, id and position
                # debug_msg="DEBUG: "
                # for d in last_seen_dangers:
                #     debug_msg += f"{d.name} (ID: {d.id}) at {format_position(d.position)}, "
                # if debug_msg:
                #     chat(debug_msg)
        last_pos = player.position
        last_health = player.health

        time.sleep(0.5)

main()
