import pygame
import os
import random
import tinytag
from colorama import Fore
import time
import sys
import select


def get_audio_files(folder_path):
    audio_extensions = (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".wma", ".aac")
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(audio_extensions) and os.path.isfile(os.path.join(folder_path, f))
    ]

current_song = 0
library_path = "library"
playlist = get_audio_files(library_path)
playing = False
paused = False

# Got lazy, thanks chat gpt...
def non_blocking_input(timeout=0.1):
    """Returns user input if available, else None"""
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip().lower().split()
    return None

def list_to_str(list):
    result = ""
    for i in list:
        result = result + i + " "
    return result.strip()

def clear():
    if os.name == "nt":
        os.system("clr")
    if os.name == "posix":
        os.system("clear")

def initialize():
    global MUSIC_END

    clear()
    
    os.environ["SDL_VIDEODRIVER"] = "dummy"  # 👈 no window

    pygame.init()  # initializes everything
    pygame.display.init()  # init display system
    pygame.display.set_mode((1, 1))  # required for events, but won't show

    pygame.mixer.init()
    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)


def play_song(song_path):
    global playing
    playing = True
    print(Fore.GREEN + "Currently playing: " + Fore.RESET + song_path)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()   

def main():
    global current_song, playlist, playing
    while True:
        
        
        pygame.event.pump()

        command = non_blocking_input()

        if playing:
            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    current_song += 1
                    play_song(playlist[current_song])

        if command == None:
            continue
        
        print()

        match command:
            case ["play"]:
                play_song(playlist[current_song])
            case ["pause"]:
                pygame.mixer.music.pause()
            case ["unpause"]:
                pygame.mixer.music.unpause()
            case ["stop"]:
                playing = False
                pygame.mixer.music.stop()
                pygame.event.clear()
            case ["quit"]:
                pygame.mixer.quit()
                print("Goodbye")
                time.sleep(0.2)
                clear()
                quit()
            case ["next"]:
                current_song = (current_song + 1) % len(playlist)
                play_song(playlist[current_song])
            case ["play", num] if num.isdigit():
                index = int(num) - 1
                if 0 <= index < len(playlist):
                    current_song = index
                    play_song(playlist[current_song])
                else:
                    print(Fore.RED + f"Track number {num} out of range." + Fore.RESET)
            case ["prev"]:
                current_song = (current_song - 1) % len(playlist)
                play_song(playlist[current_song])
            case ["help"]:
                pass
            case ["credits"]:
                pass
            case ["license"]:
                pass
            case ["clear"]:
                clear()
            case ["info"]:
                tag = tinytag.TinyTag.get(playlist[current_song])
                print("Currently playing: " + playlist[current_song])
                print("Title:", tag.title)
                print("Artist:", tag.artist)
                print("Album:", tag.album)
                print("Length: ", tag.duration)
            case ["playlist"]:
                n = 0
                for i in playlist:
                    n += 1
                    print(str(n) + " " + i)
            case _:
                print(Fore.RED + list_to_str(command) + Fore.RESET + " is not a valid command")

        print()

initialize()
main()