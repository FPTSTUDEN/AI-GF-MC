import minescript as m
# import threading 
# #modified
# from minescript import EventQueue, EventType
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

m.execute("gamerule send_command_feedback false")

SCORE_OBJ = "visited_biomes"
TEMP_COUNTER = "biome_counter"
player = m.player_name()
def reset_scoreboard():
    for b in BIOMES:
        try:
            m.execute(f"scoreboard players set {b} {SCORE_OBJ} 0")
        except: pass
    m.execute(f"scoreboard players set {TEMP_COUNTER} {SCORE_OBJ} 0")
    m.echo("♻️ Biome scores have been reset")
reset_scoreboard()