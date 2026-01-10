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

import subprocess
import sys
import threading

# subprocess.run([sys.executable, "birec.py"], check=True)
t1=threading.Thread(target=subprocess.run([sys.executable, "birec.py"], check=True))
t1.start()
chat("birec.py executing")

# ---------------- event callbacks ----------------

def on_chat(event):
    # event.message : str
    # event.sender  : str | None
    log(f"Chat: {event.sender}: {event.message}")

def on_damage(event):
    # event.amount : float
    # event.source : str | None
    log(f"Damage taken: {event.amount} (source={event.source})")

def on_explosion(event):
    # event.position : (x, y, z)
    log(f"Explosion at {event.position}")

# ---------------- register listeners ----------------

# add_event_listener("chat", on_chat)
# add_event_listener("damage", on_damage)
# add_event_listener("explosion", on_explosion)
with EventQueue() as eq:
    eq.register_damage_listener()
    eq.register_chat_listener()
    while True:
        event = eq.get()
        if event.type == EventType.DAMAGE:
            echo(event)
            echo("Damage event detected")
        if event.type == EventType.CHAT:
            msg = event.message
            if msg =="Damage event detected":
                echo(msg+" from chat")
echo("Event listeners registered")
