from minescript import *
import time
global BIOMES
global b_count
global b_current
from event_writer import write_event
t_begin=time.time()
BIOMES = [
    "the_void", "plains", "sunflower_plains", "snowy_plains", "ice_spikes",
    "desert", "swamp", "mangrove_swamp", "forest", "flower_forest",
    "birch_forest", "dark_forest", "old_growth_birch_forest", "old_growth_pine_taiga",
    "old_growth_spruce_taiga", "taiga", "snowy_taiga", "savanna", "savanna_plateau",
    "windswept_hills", "windswept_gravelly_hills", "windswept_forest",
    "windswept_savanna", "jungle", "sparse_jungle", "bamboo_jungle",
    "badlands", "eroded_badlands", "wooded_badlands", "meadow", "cherry_grove",
    "grove", "snowy_slopes", "frozen_peaks", "jagged_peaks", "stony_peaks",
    "river", "frozen_river", "beach", "snowy_beach", "stony_shore",
    "warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean", "ocean", "deep_ocean",
    "cold_ocean", "deep_cold_ocean", "frozen_ocean", "deep_frozen_ocean",
    "mushroom_fields", "dripstone_caves", "lush_caves", "deep_dark"
]
BIOMES_NETHER = [
    "nether_wastes", "soul_sand_valley", "crimson_forest", "warped_forest",
    "basalt_deltas"
]
BIOMES_END = ["the_end", "end_highlands", "end_midlands", "small_end_islands", "end_barrens" ]
BIOMES.extend(BIOMES_NETHER)
BIOMES.extend(BIOMES_END)
b_count={}
for b in BIOMES: b_count[b]={"duration":0,"count":0}

execute('execute unless entity @e[tag=biome,limit=1] run summon minecraft:armor_stand ~ ~ ~ {Invisible:true,Invulnerable:true,NoBasePlate:true,NoGravity:true,Small:true,Marker:true,Tags:["biome"]}')

def check_biomes(b_current=""):
    execute('execute at @p run tp @e[tag=biome] ~ ~ ~')
    x, y, z = map(int, player_position())
    for b in BIOMES:
        full_biome = f"minecraft:{b}"
        execute(
            f"/execute "
            f"if biome {x} {y} {z} {full_biome} "
            f"run data merge entity @e[type=armor_stand,limit=1,tag=biome] "+"{Invisible:0b,Tags:[\"biome\",\"1\"],"
            f"CustomName:'\"{b}\"'"+"}"
        )
    for b in BIOMES:
        if get_entities(name=str(b))!=[]:
            echo(f"now {b} prev {b_current}")
            if (b!=b_current):
                if (b_current==""):
                    echo(f"entered {b}")
                    write_event({"type":"biome_enter", "biome":b})
                    b_count[b]['count']+=1
                else:
                    echo(f"leaving {b_current}, stayed for {b_count[b_current]['duration']}")
                    echo(f"entering {b} for the {b_count[b]['count']+1} time")
                    write_event({"type":"biome_exit", "biome":b_current, "stay_time":b_count[b_current]['duration'], "entered_biome":b, "entered_biome_count":b_count[b]['count']+1})
                    # write_event({"type":"biome_enter", "biome":b})
                    b_count[b_current]['duration']=0
                    b_count[b]['count']+=1
            echo(f"staying for {b_count[b]['duration']} total {b_count[b]['count']}")

            b_count[b]['duration']+=1
            echo(b)
            time.sleep(1)
            return b
echo("hello")
while True:
    try: bb=check_biomes(bb)
    except: bb=check_biomes()