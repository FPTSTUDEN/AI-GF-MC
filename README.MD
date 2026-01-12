# AI GF MC
- minecraft python script extracts game data -> local llm (maybe -> tts in the future)
- BOOM
# Credits
<!-- [![aigf](https://github.com/FPTSTUDEN/AI-GF-MC/blob/78e6beb2dfb16c07e8d1db7fc97faa9ffa485453/misc/ai_catsdontlikecoffee.png){:width=200px}](https://www.instagram.com/catsdontlikecoffee/) -->
### catsdontlikecoffee
<a href="https://www.instagram.com/catsdontlikecoffee/">
    <img src="misc\ai_catsdontlikecoffee.png" alt="catsdontlikecofee" width="150"/>
</a>

project idea partially inspired by this channel

also the videos are insane and i like it

<a href="https://www.instagram.com/catsdontlikecoffee/">Check them out</a>

### sam-ple
their repo helped me a lot with:
- latest version's syntax
- biolog (a modified version of their biomerecorder)
### Other AIs
- chatgpt, gemini, github copilot... for refining my code and saving my time

<a href="https://github.com/sam-ple">Check them out</a>

# Stable files
- **remote_minescript/elog.py** - event logger to /.minecraft/events.txt
- **remote_minescript/biolog.py** - biome & time on biome logger 
- **main.py** - THE AI: one-time parses events.log for now

# Prerequisites
- **Minecraft** with **Minescript** mod
- **Ollama**: dolphin3:latest
- Any mod with **chat hiding** functionality (to not expose your spammy logging chat)

# TODO
## Logging
(...: in progress, V: Done, X: Failed attempt)
- **under_attack aggregator** not working ...
- **damaged** (cause: lava,monster...) V
- **attacked entity** V
- death ... (0 HP detection possible)
- **low_health**  V
- **monster_near** V
- achievement
- enter_dimension (X) / **biome** V
- ~~lava_near~~ (no need)

- Player action (long duration): mining, farming,...
- Inventory: collective, should be new items only

## Log parser -> comment
- Danger situation (cheer up/feel pity...)
- above logs...

## Memory
- death count (+ reason for death)
