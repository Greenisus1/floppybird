# Floppy Bird

Original fullscreen retro flyer for Pi/Linux terminals. A floppy disk flaps through pipes made of 1s and 0s, green on black, inspired by the tap-to-fly idea of Flappy Bird and Square Bird with new code, name and art. Not an official port, no copied assets, sounds or branding.

Built with AI assistance from my design. Free, offline, no desktop, accounts, API keys, ads, paid unlocks or pip packages.

## Play

Space, W or Up flaps. Gravity pulls the disk down; thread each gap between the pipes. Every pipe cleared is +1. The floor and the pipes end the run. Pipes speed up and gaps tighten as your score grows. P pauses, R restarts, Q/Esc quits. Letter controls accept either casing.

## Display and setup

ANSI truecolor and Unicode half-block pixel art when the terminal advertises support (COLORTERM=truecolor/24bit or direct-color TERM). V toggles pixel/text manually; `python3 floppybird.py --ascii` starts in text mode (pipes are literal 1s and 0s there too). Minimum 60x20; smaller windows pause simulation.

Pi App Store -> Games -> Floppy Bird. Installer checks Python/curses and adds Python with apt/apk/pacman if needed. Package installation needs root; Arch retains its package manager's normal confirmation.

    bash app-store.sh INSTALL
    bash app-store.sh RUN
    python3 -m unittest -v
    python3 test_terminal.py

Best score saved locally at `~/.local/share/floppybird/best.json` only on game over, not on restart/quit. Saves are private, atomic and reject symlinks. No online leaderboard or synchronized sessions.

## Scope and verification

A compact original arcade game: one endless mode, no levels, sound or skins. Local unit and PTY tests cover flapping, gravity, ceiling/floor rules, pipe spawning, scoring, collisions, difficulty ramps, saves, art shapes, resizing and clean terminal exit. Before publication, all 14 unit tests and pixel/text PTY control/resize/exit checks passed on a real aarch64 Raspberry Pi.

MIT license, copyright 2026 Greenisus1.
