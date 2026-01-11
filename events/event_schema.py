# from dataclasses import dataclass
# from typing import Optional

# @dataclass
# class GameEvent:
#     type: str
#     cause: Optional[str] = None
#     target: Optional[str] = None
#     #location: Optional[str] = None

EVENT_SCHEMA = {
    "type": str,              # "under_attack", "death", "biome_enter", ...
    "time": float,            # unix or session-relative
    "severity": float,        # 0.0–1.0 (already aggregated)
    
    # common actors
    "target": str | None,     # "player", "mob", None
    "source": str | None,     # mob name, environment, "player"

    # combat
    "damage": float | None,
    "health": float | None,
    "count": int | None,      # hits / mobs / seconds
    
    # spatial / world
    "biome": str | None,
    "position": tuple | None,

    # terminal
    "cause": str | None       # used for death
}
class GameEvent:
    def __init__(self, data: dict | None = None, **kwargs):
        """Initialize from a dict (positional) or keyword args.

        Supports both `GameEvent({'type': 'death'})` and
        `GameEvent(type='death')`, plus the existing `GameEvent(**data)` use.
        """
        if data is not None:
            if not isinstance(data, dict):
                raise TypeError("data must be a dict or None")
            self.__dict__.update(data)
        if kwargs:
            self.__dict__.update(kwargs)

    def is_combat(self):
        return self.type in ("under_attack", "imminent_threat")

    def is_terminal(self):
        return self.type == "death"

