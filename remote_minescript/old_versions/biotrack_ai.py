import minescript as m
import threading
from minescript import EventQueue, EventType

#\eval 'get_entities()[[a.type for a in get_entities()].index("entity.minecraft.armor_stand")]'

# =====================
# CONFIG
# =====================

ARMOR_TAG = "biome_store"
SCORE_OBJ = "visited_biomes"
VISIT_OBJ = "biome_visits"
TEMP_COUNTER = "biome_counter"

player = m.player_name()
def cmd(s):
    m.execute(s)


BIOMES = [
    "the_void", "plains", "sunflower_plains", "snowy_plains", "ice_spikes",
    "desert", "swamp", "mangrove_swamp", "forest", "flower_forest",
    "birch_forest", "dark_forest", "old_growth_birch_forest",
    "old_growth_pine_taiga", "old_growth_spruce_taiga",
    "taiga", "snowy_taiga", "savanna", "savanna_plateau",
    "windswept_hills", "windswept_gravelly_hills",
    "windswept_forest", "windswept_savanna",
    "jungle", "sparse_jungle", "bamboo_jungle",
    "badlands", "eroded_badlands", "wooded_badlands",
    "meadow", "cherry_grove", "grove",
    "snowy_slopes", "frozen_peaks", "jagged_peaks", "stony_peaks",
    "river", "frozen_river", "beach", "snowy_beach", "stony_shore",
    "warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean",
    "ocean", "deep_ocean", "cold_ocean", "deep_cold_ocean",
    "frozen_ocean", "deep_frozen_ocean",
    "mushroom_fields", "dripstone_caves", "lush_caves", "deep_dark"
]
biome_count={}
for b in BIOMES: biome_count[b]=0
# =====================
# INITIALIZATION
# =====================

m.execute("gamerule sendCommandFeedback false")

def init_scoreboards():
    try: m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy")
    except: pass
    try: m.execute(f"scoreboard objectives add {VISIT_OBJ} dummy")
    except: pass
    try: m.execute(f"scoreboard objectives add {TEMP_COUNTER} dummy")
    except: pass

    m.execute("scoreboard objectives setdisplay sidebar")

    for b in BIOMES:
        try:
            m.execute(f"scoreboard players set {b} {SCORE_OBJ} 0")
            m.execute(f"scoreboard players set {b} {VISIT_OBJ} 0")
        except:
            pass

def init_biome_storage():
    # Create marker armor stand if missing
    cmd(
    "/execute unless entity @e[tag=" + ARMOR_TAG + ",limit=1] "
    + "run summon minecraft:armor_stand ~ ~ ~ "
    + "{Tags:[\"" + ARMOR_TAG + "\"],Invisible:1b,Marker:1b,NoGravity:1b}"
)


# =====================
# BIOME FIRST-VISIT LOGIC (UNCHANGED)
# =====================

def check_biomes():
    try:
        x, y, z = map(int, m.player_position())
        for b in BIOMES:
            biome_id = f"minecraft:{b}"

            m.execute(
                f"/execute if score {b} {SCORE_OBJ} matches 0 "
                f"if biome {x} {y} {z} {biome_id} "
                f"run scoreboard players set {b} {SCORE_OBJ} 1"
            )

            m.execute(
                f"/execute if score {b} {SCORE_OBJ} matches 1 "
                f"if biome {x} {y} {z} {biome_id} "
                f"run tellraw {player} "
                f'[{{"text":" First visit: {b}","color":"aqua","bold":true}}]'
            )

            m.execute(
                f"/execute if score {b} {SCORE_OBJ} matches 1 "
                f"if biome {x} {y} {z} {biome_id} "
                f"run scoreboard players set {b} {SCORE_OBJ} 2"
            )
    except Exception as e:
        m.echo(f"check_biomes error: {e}")

# =====================
# BIOME TRANSITION TRACKING (NEW)
# =====================

def update_biome_visit():
    try:
        x, y, z = map(int, m.player_position())

        for b in BIOMES:
            biome_id = f"minecraft:{b}"

            # If biome differs from stored biome AND player is in this biome
            # cmd(
            # "execute unless data entity @e[tag=" + ARMOR_TAG + ",limit=1] "
            # + "{data:{\"minecraft:custom_data\":{biome:\"" + biome_id + "\"}}} "
            # + "if biome " + str(x) + " " + str(y) + " " + str(z) + " " + biome_id + " "
            # + "run scoreboard players add " + b + " " + VISIT_OBJ + " 1"
            # )

            # # Overwrite stored biome
            # cmd(
            # "execute unless data entity @e[tag=" + ARMOR_TAG + ",limit=1] "
            # + "{data:{\"minecraft:custom_data\":{biome:\"" + biome_id + "\"}}} "
            # + "if biome " + str(x) + " " + str(y) + " " + str(z) + " " + biome_id + " "
            # + "run data modify entity @e[tag=" + ARMOR_TAG + ",limit=1] "
            # + "\"minecraft:custom_data\".biome "
            # + "set value \"" + biome_id + "\""
            # )
            # cmd( #version 2
            #     "execute if biome " + str(x) + " " + str(y) + " " + str(z) + " " + biome_id + " "
            #     "unless data entity @e[tag=" + ARMOR_TAG + ",limit=1] "
            #     "{data:{\"minecraft:custom_data\":{biome:\"" + biome_id + "\"}}} "
            #     "run scoreboard players add " + b + " " + VISIT_OBJ + " 1"
            # )
            cmd(
                "execute if biome " + str(x) + " " + str(y) + " " + str(z) + " " + biome_id + " "
                "unless data entity @e[tag=" + ARMOR_TAG + ",limit=1] "
                "{data:{\"minecraft:custom_data\":{biome:\"" + biome_id + "\"}}} "
                "run tellraw @s "
                # "{\"text\":\"[BIOME_NBT]\",\"extra\":[{\"nbt\":\"minecraft:custom_data.biome\",\"entity\":\"@e[tag=" + ARMOR_TAG + ",limit=1]\"}]}"
                 "{\"text\":\"[BIOME_NBT] "+ b +"\"}"
            )
        # update stored biome immediately
            cmd(
                "execute if biome " + str(x) + " " + str(y) + " " + str(z) + " " + biome_id + " "
                "run data modify entity @e[tag=" + ARMOR_TAG + ",limit=1] "
                "\"minecraft:custom_data\".biome "
                "set value \"" + biome_id + "\""
            )
            # break


    except Exception as e:
        m.echo(f" biome transition error: {e}")

# =====================
# DISPLAY / COMMANDS
# =====================

def show_status():
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")

    for b in BIOMES:
        m.execute(
            f"/execute if score {b} {SCORE_OBJ} matches 2.. run "
            f"scoreboard players add {TEMP_COUNTER} {SCORE_OBJ} 1"
        )
#potential
    m.execute(
        f'tellraw {player} ["",'
        f'{{"text":"Biomes visited: ","color":"gold"}},'
        f'{{"score":{{"name":"{TEMP_COUNTER}","objective":"{SCORE_OBJ}"}}}},'
        f'{{"text":"/{len(BIOMES)}","color":"white"}}]'
    )

def reset_all():
    for b in BIOMES:
        m.execute(f"scoreboard players set {b} {SCORE_OBJ} 0")
        m.execute(f"scoreboard players set {b} {VISIT_OBJ} 0")
        biome_count[b]=0

    cmd(
        "data remove entity @e[tag=" + ARMOR_TAG + ",limit=1] "
        + "data.minecraft:custom_data"
    )
    init_biome_storage()


    m.echo("♻️ All biome data reset")

# =====================
# TIMER
# =====================

def periodic_check():
    check_biomes()
    update_biome_visit()
    threading.Timer(2.0, periodic_check).start()

# =====================
# STARTUP
# =====================

init_scoreboards()
init_biome_storage()
periodic_check()

with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo(" BiomeTracker v0.3.0 running")

    while True:
        event = eq.get()
        if event.type == EventType.CHAT:
            msg = event.message.strip()
            if "[BIOME_NBT]" in msg:
                current_biome_nbt = msg.split()[-1].strip()
                m.echo("Current biome from NBT: " + current_biome_nbt + str(biome_count[current_biome_nbt])) #debug
                biome_count[current_biome_nbt]+=2
            if msg.startswith("<") and ">" in msg:
                msg = msg.split(">", 1)[1].strip()

            if msg == "--status":
                show_status()
            elif msg == "--reset":
                reset_all()
