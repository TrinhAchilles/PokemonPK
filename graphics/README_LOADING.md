# Loading Screen Setup Guide

This guide explains how to add a custom loading screen GIF to Pokemon-PK.

## Overview

When you click "New Game" or "Continue", a loading screen appears with:
1. Animated GIF in the center
2. After 3 seconds, text appears: "Click anywhere to continue"
3. Click anywhere to start the game

## Adding Your Loading GIF

### Step 1: Prepare Your GIF

Place your loading animation GIF file in the `graphics` folder with the name:
```
graphics/loading.gif
```

### Recommended GIF Specifications

- **Format**: GIF (animated)
- **Size**: 400x400 pixels or smaller (will be auto-scaled)
- **Frame Rate**: 10-30 FPS
- **Duration**: Any (loops automatically)
- **Style**: Should fit your game's aesthetic

### Popular Loading Animation Ideas

- Pokéball rotating
- Character walking/running
- Spinning logo
- Progress bar animation
- Pixel art loading animation

## Where to Get Loading GIFs

You can create or find loading animations from:
- **Create your own**: Use tools like Aseprite, Piskel, or GIMP
- **Free resources**: 
  - OpenGameArt.org
  - itch.io (free game assets)
  - Kenney.nl
- **Make sure**: Any asset you use is properly licensed!

## File Structure

```
graphics/
  ├── README_LOADING.md     (this file)
  ├── loading.gif           (your loading animation - ADD THIS)
  ├── fonts/
  │   └── SVN-Determination Sans.ttf  (used for text)
  ├── logo.png
  └── ...
```

## Fallback Behavior

If `loading.gif` is not found, the system will automatically create a simple rotating circle animation as a placeholder.

## Customization

### Timing
To change how long before "Click anywhere to continue" appears, edit `loading_screen.py`:
```python
self.show_prompt_after = 3.0  # Change this value (in seconds)
```

### Text Styling
The text uses:
- **Font**: SVN-Determination Sans (32pt)
- **Color**: White (#FFFFFF)
- **Outline**: Black, 3 pixels wide
- **Effect**: Subtle pulse/fade animation

### GIF Size
The GIF is automatically scaled to a maximum of 400 pixels while maintaining aspect ratio.

## Testing

1. Place your `loading.gif` in the `graphics` folder
2. Run the game: `python code/main_pokemon.py`
3. Click "New Game" or "Continue"
4. You should see your loading animation
5. After 3 seconds, click anywhere to continue

## Troubleshooting

### GIF doesn't appear
- Check that the file is named exactly `loading.gif` (lowercase)
- Verify the file is in the `graphics` folder (not in a subfolder)
- Make sure it's a valid GIF file
- Check console output for error messages

### GIF is too large/small
- The system auto-scales GIFs larger than 400px
- For best results, use 200-400px GIF files
- Maintain square or near-square aspect ratios

### Animation is too fast/slow
- Check your GIF's frame delay settings
- Most GIF editors let you set delay per frame
- Recommended: 60-100ms per frame

## Example GIF Creation (Aseprite)

1. Create sprites in Aseprite (200x200px canvas)
2. Add animation frames
3. Set frame duration to 100ms
4. Export as GIF
5. Save as `loading.gif`
6. Copy to `graphics/` folder

## Technical Details

- The loading screen uses PIL (Pillow) to load GIF files
- All frames are extracted and converted to Pygame surfaces
- Frame timing is preserved from the original GIF
- Supports transparency (RGBA mode)
- Click detection works with any mouse button
