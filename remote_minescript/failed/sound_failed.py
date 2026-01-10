import minescript
import os

# Path where the text file will be saved
OUTPUT_PATH = os.path.join("C:", "minecraft_live_sounds.txt")

def main():
    print(f"Sound Logger Started! Saving to: {OUTPUT_PATH}")
    
    # Clear the file or create it
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("--- Minecraft Live Sound Log ---\n")

    # Listen for sound events
    # 'sound_played' is the built-in event in Minescript
    for event in minescript.events():
        if event[0] == "sound_played":
            # event[1] contains: sound_name, category, x, y, z, volume, pitch
            sound_name = event[1][0]
            
            # Log to file
            with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
                f.write(f"{sound_name}\n")
            
            # Optional: Notify you in-game (uncomment to see it in chat)
            # minescript.execute(f"/echo Logged: {sound_name}")

if __name__ == "__main__":
    main()