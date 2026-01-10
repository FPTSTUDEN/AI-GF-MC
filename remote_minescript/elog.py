from minescript import *
import time
import math
import threading
# import minescript.biotrack as biotrack

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
global seen_entity_ids
seen_entity_ids = set()

# ------------------ main ------------------
'''SAMPLES
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
Sample DamageEvent(
    type='damage',
    time='',
    entity_uuid='', # damaged target
    cause_uuid='', #(e.g. skeleton shot -> skeleton_uuid, None)
    source='' # (player, skeleton shot -> arrow)
)
Sample player(): uuid, health, name, id
'''
player = get_player()
last_pos = player.position  # tuple (x, y, z)
last_health = player.health # float
last_seen_dangers=[]
# eq=EventQueue()
# eq.register_damage_listener()
# eq.register_chat_listener()
# global damage_event
# event = eq.get()
# echo("Event listeners registered")

log("Event logger started!")
def main():
    global last_pos, last_health, last_seen_dangers, player
    global damage_event
    player = get_player()  

    # ---- damage detection ----

    try: 
        if damage_event.entity_uuid==player.uuid:
            damage = last_health - player.health
            source=damage_event.source
            log(f"Player took damage ({damage:.1f} HP) by {source} current health {player.health:.1f}")
        elif damage_event.cause_uuid==player.uuid:
            for entity in get_entities():
                if entity.uuid==damage_event.entity_uuid:
                    victim=entity
                    break
            log(f"#{victim.id} {victim.name} took damage by player current health {victim.health}")
    except:
        log("Warning: No damage listener yet")
        

    # ---- low health warning ----
    if player.health <= 5.0 and last_health > 5.0:
        log(f"Warning: Player health is {player.health:.1f} HP!")


    last_pos = player.position
    last_health = player.health
def periodic_danger_check():
    # ---- nearby hostile mobs ----
    # for e in entities(): echo(e['name'])
    player=get_player()
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
                if proxity_now>15: #view
                    last_seen_dangers.remove(last_seen_dangers[[a.id for a in last_seen_dangers].index(e.id)])
                    continue
                # if abs(proxity_now-proxity_before)>1.5:
                if proxity_now < proxity_before:
                    log(f"Incoming #{e.id} {e.name}!")
                elif proxity_now > proxity_before:
                    log(f"Distancing from #{e.id} {e.name}...")
                last_seen_dangers.remove(last_seen_dangers[[a.id for a in last_seen_dangers].index(e.id)])
            last_seen_dangers.append(e) if len(last_seen_dangers)<5 else last_seen_dangers.append(e) and last_seen_dangers.pop(0)
    threading.Timer(2, periodic_danger_check).start()


def damage_check():
    main()


with EventQueue() as eq:
    eq.register_damage_listener()
    eq.register_chat_listener()
    # event = eq.get()
    echo("Event listeners registered...")
    echo("Please wait... Running checks...")

    damage_check()
    periodic_danger_check()
    echo("Checks ran successfully")
    while True:
        event = eq.get()
        if event.type == EventType.DAMAGE:
            damage_event=event
            damage_check()
        # if event.type == EventType.CHAT:
        #     msg = event.message
        #     if msg =="Damage event detected":
        #         echo(msg+" from chat")




