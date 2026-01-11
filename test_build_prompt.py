import sys, types
m = types.ModuleType('llm')
mc = types.ModuleType('llm.client')
mc.generate_response = lambda x: 'OK'
sys.modules['llm'] = m
sys.modules['llm.client'] = mc
from main import build_prompt
from events.event_schema import GameEvent
mood = {'stress': 0.3, 'confidence': 0.7}
e = GameEvent(type='death', cause='creeper', severity=0.9)
print(build_prompt(e, mood).splitlines()[0])
