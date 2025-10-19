# Loading Screen Implementation - Quick Start

## ✅ What's Been Added

A loading screen now appears when you click "New Game" or "Continue" with these features:

1. **GIF Animation**: Shows an animated loading GIF in the center
2. **Click-to-Continue Prompt**: After 3 seconds, displays "Click anywhere to continue"
3. **Custom Font**: Text uses SVN-Determination Sans with white color and black outline
4. **Smooth Transitions**: Menu → Loading Screen → Game

## 🚀 How to Use

### Step 1: Add Your Loading GIF

Place a GIF file named `loading.gif` in the `graphics` folder:

```
graphics/loading.gif
```

If you don't have a loading GIF yet, the system will automatically create a simple rotating circle animation as a placeholder.

### Step 2: Run the Game

```bash
python code/main_pokemon.py
```

### Step 3: Test It!

1. Click "New Game" or "Continue" from the main menu
2. You'll see the loading screen with your GIF
3. After 3 seconds, "Click anywhere to continue" will appear
4. Click anywhere to start the game

## 📝 Files Modified

- `code/loading_screen.py` - **NEW** - Loading screen class with GIF support
- `code/main_pokemon.py` - Added loading screen integration
- `graphics/README_LOADING.md` - Detailed guide for customization

## 🎨 Customization

### Change the delay before showing text

Edit `code/loading_screen.py`:
```python
self.show_prompt_after = 3.0  # Change to desired seconds
```

### Change the text

Edit `code/loading_screen.py`, find:
```python
prompt_text = "Click anywhere to continue"
```

### Change text styling

The text currently uses:
- Font: SVN-Determination Sans (32pt)
- Color: White (#FFFFFF)  
- Outline: Black, 3px wide
- Effect: Pulsing fade animation

Edit the `render_text_with_outline` call in the `draw()` method to customize.

## 🔧 Technical Details

- Uses PIL (Pillow) to load and parse GIF files
- Extracts all frames and respects original timing
- Auto-scales GIFs larger than 400px
- Supports transparency
- Click detection works with any mouse button
- Falls back to simple animation if GIF not found

## 📁 Recommended GIF Specs

- **Size**: 200-400px (square or near-square)
- **Format**: Animated GIF
- **Frame Rate**: 10-30 FPS  
- **Duration**: Any (loops automatically)
- **Theme**: Match your game's aesthetic!

## 🆘 Troubleshooting

### No GIF shows up
- Check the file is named exactly `loading.gif` (lowercase)
- Verify it's in the `graphics` folder (not a subfolder)
- Look at console output for error messages

### GIF is choppy
- Try a GIF with fewer frames
- Check your GIF's frame delay settings
- Recommended: 60-100ms per frame

### Text doesn't show
- Make sure SVN-Determination Sans font is installed in `graphics/fonts/`
- Check console for font loading errors

## 🎮 Example GIF Ideas

- Rotating Pokéball
- Character running/walking animation
- Spinning logo
- Loading bar
- Pixel art animation
- "Now Loading..." text animation

## ✨ Next Steps

1. Find or create a loading GIF that matches your game's style
2. Place it in `graphics/loading.gif`
3. Test by clicking "New Game"
4. Adjust timing/styling if needed

For more details, see `graphics/README_LOADING.md`
