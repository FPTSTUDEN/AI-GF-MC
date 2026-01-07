from minescript import *
import time

LOG_FILE = "sound_captions.log"

def log_caption(text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

    # Optional: show in chat
    chat(f"7[Caption] f{text}")

def main():
    chat("aSound caption logger started")

    while True:
        # Get all current subtitles on screen
        subtitles = get_subtitles()

        for subtitle in subtitles:
            # subtitle.text is the caption string
            log_caption(subtitle.text)

        # Prevent duplicate spam (adjust if needed)
        time.sleep(0.25)

main()
