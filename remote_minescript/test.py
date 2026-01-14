# from curses import echo
from minescript import *
# from remote_minescript.system.lib.minescript import EventQueue, EventType
chat("Hello World")
# from minescript import *
import time

LOG_FILE = "events2.log"

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    line = f"[{now()}] {msg}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    echo(msg)

# import subprocess
import sys
import threading

# subprocess.run([sys.executable, "birec.py"], check=True)
# t1=threading.Thread(target=subprocess.run([sys.executable, "birec.py"], check=True))
# t1.start()
# chat("birec.py executing")
print(next((i for i in get_entities() if i.name=="123"),"ERROR"))
for e in get_entities():
    if e.type=="entity.minecraft.armor_stand" and e.name=="123":
        euuid=e.uuid
        # print(e)
print(next((i for i in get_entities() if i.uuid==euuid),"ERROR").nbt)
# ---------------- event callbacks ----------------

def on_chat(event):
    # event.message : str
    # event.sender  : str | None
    log(f"Chat: {event.sender}: {event.message}")

def on_damage(event):
    # event.amount : float
    # event.source : str | None
    log(f"Damage taken: compare_heath() (source={event.source})")

def on_explosion(event):
    # event.position : (x, y, z)
    log(f"Explosion at {event.position}")
player=get_player()
def retrack_player():
    for entity in get_entities():
        if entity.uuid==player.uuid:
            chat(entity.uuid)
retrack_player()
# ---------------- register listeners ----------------

# add_event_listener("chat", on_chat)
# add_event_listener("damage", on_damage)
# add_event_listener("explosion", on_explosion)
'''
DamageEvent(
    type='damage',
    time='',
    entity_uuid='', # damaged target
    cause_uuid='', #(e.g. skeleton shot -> skeleton_uuid, None)
    source='' # (player, skeleton shot -> arrow)
)
'''
with EventQueue() as eq:
    eq.register_damage_listener()
    eq.register_chat_listener()
    global event
    event = eq.get()
    while True:
        event = eq.get()
        if event.type == EventType.DAMAGE:
            on_damage(event)
            echo(event)
        if event.type == EventType.CHAT:
            if event.message == "--get":
                pass
        # if event.type == EventType.CHAT:
        #     msg = event.message
        #     if msg =="Damage event detected":
        #         echo(msg+" from chat")
echo("Event listeners registered")


# ------------------ biome ------------------
# BIOMES = [
#     "the_void", "plains", "sunflower_plains", "snowy_plains", "ice_spikes",
#     "desert", "swamp", "mangrove_swamp", "forest", "flower_forest",
#     "birch_forest", "dark_forest", "old_growth_birch_forest", "old_growth_pine_taiga",
#     "old_growth_spruce_taiga", "taiga", "snowy_taiga", "savanna", "savanna_plateau",
#     "windswept_hills", "windswept_gravelly_hills", "windswept_forest",
#     "windswept_savanna", "jungle", "sparse_jungle", "bamboo_jungle",
#     "badlands", "eroded_badlands", "wooded_badlands", "meadow", "cherry_grove",
#     "grove", "snowy_slopes", "frozen_peaks", "jagged_peaks", "stony_peaks",
#     "river", "frozen_river", "beach", "snowy_beach", "stony_shore",
#     "warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean", "ocean", "deep_ocean",
#     "cold_ocean", "deep_cold_ocean", "frozen_ocean", "deep_frozen_ocean",
#     "mushroom_fields", "dripstone_caves", "lush_caves", "deep_dark"
# ]
# x, y, z = map(int, player_position())
# SCORE_OBJ = "visited_biomes"
# TEMP_COUNTER = "biome_counter"
# player = player_name()
# birec.init_scoreboard()
# birec.periodic_check()

            # debug: print last_seen_dangers name, id and position
            # debug_msg="DEBUG: "
            # for d in last_seen_dangers:
            #     debug_msg += f"{d.name} (ID: {d.id}) at {format_position(d.position)}, "
            # if debug_msg:
            #     chat(debug_msg)

# def track_player_movement():
    # ---- footsteps (movement) ----
    # if distance(player.position, last_pos) > 2.5:
    #     log(f"Player ran {direction_vector(last_pos, player.position)[3]}to {format_position(player.position)}")
    # elif distance(player.position, last_pos) > 1.3:
    #     log(f"Player moved {direction_vector(last_pos, player.position)[3]}to {format_position(player.position)}")
    # elif distance(player.position, last_pos) > 0.2:
    #     log(f"Player is shifting {direction_vector(last_pos, player.position)[3]}to {format_position(player.position)}")
  