import requests

payload = {
    "model": "mistral:7b-instruct",
    "prompt": "React emotionally to a player falling into lava.",
    "stream": False
}

r = requests.post(
    "http://localhost:11434/api/generate",
    json=payload,
    timeout=30
)

print(r.json()["response"])
'''
 Oh no! That poor player just fell into the fiery depths of the lava pit! I feel a sense of empathy and concern for their safety. It's important to remember, however, that this is a virtual environment and, thankfully, they are only pixels on a screen. But still, it's always unfortunate when someone encounters such an unexpected obstacle in their gaming journey. Let's hope they have a backup save or find some helpful items soon to get back on track!
 '''