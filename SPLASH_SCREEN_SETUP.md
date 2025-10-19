# Splash Screen Setup Guide

## What It Does

When you launch the game, a **splash screen** appears for 5 seconds showing your GIF as a full-screen background, then smoothly fades to the main menu.

## How to Add Your Splash GIF

Place your animated GIF here:
```
graphics/splash.gif
```

## GIF Requirements

- **Format**: Animated GIF
- **Size**: Any size (will be scaled to full screen automatically)
- **Duration**: Any (loops during the 5-second display)
- **Recommended**: 1920x1080 or your game's resolution for best quality

## Timing Configuration

To change how long the splash screen displays, edit `code/splash_screen.py`:

```python
self.display_duration = 5.0  # Show for 5 seconds (change this)
self.fade_duration = 1.0     # Fade out over 1 second (change this)
```

## What Happens

1. **Game launches** → Splash screen appears
2. **0-5 seconds** → Your GIF plays as full-screen background
3. **5-6 seconds** → Fades to black smoothly
4. **6 seconds** → Main menu appears with menu music

## If GIF Not Found

If `graphics/splash.gif` doesn't exist, the game will show a blue gradient as fallback.

## File Structure

```
graphics/
  ├── splash.gif        (startup splash screen - ADD THIS)
  ├── loading.gif       (loading screen animation)
  ├── logo.png          (menu logo)
  └── ...
```

## Example Splash GIF Ideas

- Game logo animation
- Studio/developer logo
- "Press Start" animation
- Title reveal animation
- Character showcase

## Technical Details

- Uses PIL (Pillow) to load GIF files
- Scales to full screen maintaining aspect ratio (stretched to fit)
- Smooth alpha fade transition
- Automatically loops GIF during display time
- No user input required (automatic transition)

## Troubleshooting

### Splash screen doesn't show
- Check the file is named exactly `splash.gif` (lowercase)
- Verify it's in the `graphics` folder
- Make sure Pillow is installed: `pip install Pillow`
- Check console for error messages

### GIF looks stretched/distorted
- Use a GIF with the same aspect ratio as your game window
- Recommended: 16:9 aspect ratio (e.g., 1920x1080, 1280x720)

### Want to skip splash screen during development
Edit `code/splash_screen.py`:
```python
self.display_duration = 0.1  # Very short duration for testing
```

Or comment out splash screen initialization in `code/main_pokemon.py`
