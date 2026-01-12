# Severity scale:
# 0.0 = ignore
# 0.3 = mild comment
# 0.6 = noticeable
# 0.8 = urgent
# 1.0 = critical

EVENT_SEVERITY = {
    # ----- session -----
    "session_start": 0.4,
    "session_end": 0.4,

    # ----- survival -----
    "player_damage": 0.25,
    "low_health": 0.8,
    "under_attack": 0.9,
    "death": 1.0,
    "player_death": 1.0,

    # ----- mobs -----
    "mob_near": 0.2,
    "mob_incoming": 0.2,
    "imminent_threat": 0.85,
    "mob_retreat": 0.2,

    # ----- combat (offense) -----
    "victim_damage": 0.1,

    # ----- exploration -----
    "biome_enter": 0.4,
    "biome_exit": 0.3,
}

DEFAULT_SEVERITY = 0.2
