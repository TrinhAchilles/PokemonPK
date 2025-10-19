# Audio Setup Guide

This directory contains audio files for Pokemon-PK.

## Menu Music

To add background music to the main menu, place one of the following files in this directory:

- `menu.mp3` (recommended)
- `menu.wav`
- `menu.ogg`
- `menu_music.mp3`
- `menu_music.wav`
- `menu_music.ogg`

The game will automatically detect and play the first available file from the list above.

## Audio Format Support

The game supports the following audio formats:
- **MP3** (.mp3) - Most common, good compression
- **WAV** (.wav) - Uncompressed, larger file size but best quality
- **OGG** (.ogg) - Good compression with high quality

## Volume Settings

The menu music is set to 50% volume by default to ensure it doesn't overpower the game.

## Where to Find Music

You can use royalty-free music from sources like:
- OpenGameArt.org
- FreeSFX.co.uk
- YouTube Audio Library
- Incompetech.com (Kevin MacLeod)

Make sure any music you use is properly licensed for your project!

## Example Directory Structure

```
audio/
  ├── README.md           (this file)
  ├── menu.mp3           (menu background music)
  ├── overworld.mp3      (overworld music - if needed)
  ├── battle.mp3         (battle music - if needed)
  └── ...                (other sound effects)
```

## Testing

Run the game with `python code/main_pokemon.py` and the menu music should automatically play when you see the main menu.

Press ESC while in-game to return to the menu, and the menu music will resume.
