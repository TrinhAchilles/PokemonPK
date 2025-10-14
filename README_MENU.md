# Main Menu System - Complete Documentation

## Overview

A professional main menu system with video background support has been added to your game. The design is inspired by modern game menus with smooth animations, hover effects, and a cinematic feel.

![Menu Features](https://via.placeholder.com/800x400/1a1a2e/ffffff?text=Main+Menu+with+Video+Background)

## Features

### Visual Elements
- **Looped Video Background**: Smooth, continuous background video playback
- **Gradient Fallback**: Automatic fallback to stylish gradient if video not found
- **Game Title**: Large "DUELIST" title at the top
- **Booster Packs Display**: Shows player's booster pack count

### Interactive Elements
- **Main Menu Buttons**:
  - PLAY - Starts the game
  - SANDBOX - Placeholder for sandbox mode
  - COLLECTION - Placeholder for collection viewer
  
- **Top Navigation Icons**:
  - QUESTS - Quest system (placeholder)
  - PROFILE - Player profile (placeholder)
  - SETTINGS - Game settings (placeholder)
  - FRIENDS - Friends list (placeholder)

- **Bug Report Button**: "FOUND A BUG?" in top-right corner

### Animations
- Smooth scale animations on hover
- Arrow indicators for active buttons
- Glow effects on icon buttons
- Seamless transitions between menu and game

## Architecture

### Components

#### 1. `menu.py` - Menu System
**VideoBackground Class**
- Handles video playback using OpenCV
- Automatic looping
- Fallback gradient generation
- Frame-by-frame rendering to Pygame surface

**Button Class**
- Interactive text buttons
- Hover detection and animations
- Callback system for actions
- Scale effects and visual feedback

**IconButton Class**
- Icon-based buttons for top menu
- Support for custom icon images
- Text labels below icons
- Glow effects on hover

**MainMenu Class**
- Coordinates all menu elements
- Manages button callbacks
- Handles update/draw cycle
- Resource cleanup

#### 2. `main_with_menu.py` - Game Wrapper
**GameWithMenu Class**
- Wraps original Game class
- Manages menu/game state switching
- Handles font loading for menu
- Coordinates event handling
- Seamless transition between menu and game

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

Dependencies:
- `pygame-ce>=2.5.0` - Game engine
- `pytmx>=3.31` - Tilemap support
- `opencv-python>=4.8.0` - Video playback

### Directory Structure
```
workspace/
├── code/
│   ├── main.py              # Original game (unchanged)
│   ├── main_with_menu.py    # Game with menu integration
│   ├── menu.py              # Menu system
│   ├── settings.py          # Shared settings
│   └── [other game files]
├── videos/
│   └── menu_background.mp4  # Background video (optional)
├── graphics/
│   └── fonts/               # Game fonts
├── requirements.txt         # Python dependencies
└── README_MENU.md          # This file
```

## Usage

### Running the Game

**With Menu:**
```bash
cd code
python main_with_menu.py
```

**Original (No Menu):**
```bash
cd code
python main.py
```

### Controls
- **Mouse**: Click buttons to interact
- **ESC Key**: 
  - In menu: Quit game
  - In game: Return to menu
- **ENTER Key** (in game): Open monster index

## Customization

### Changing Button Layout

Edit `code/menu.py`, line ~190:
```python
menu_x = 250              # X position of main buttons
menu_y_start = 300        # Y position of first button
menu_spacing = 80         # Spacing between buttons
```

### Changing Icon Layout

Edit `code/menu.py`, line ~205:
```python
icon_x_start = WINDOW_WIDTH - 250  # Starting X for icons
icon_spacing = 80                   # Space between icons
```

### Changing Colors

Edit `code/settings.py`:
```python
COLORS = {
    'white': '#f4fefa',
    'blue': '#66d7ee',
    # Add more colors...
}
```

### Adding Custom Icons

Replace placeholder icons in `menu.py`:
```python
# Load custom icon image
from pathlib import Path
icon_path = Path(__file__).parent.parent / 'graphics' / 'icons' / 'quests.png'
icon_surf = pygame.image.load(str(icon_path))

# Use in IconButton
icon = IconButton(pos, "QUESTS", icon_surf, self.open_quests)
```

### Implementing Menu Functions

Edit the callback methods in `MainMenu` class:

```python
def open_quests(self):
    """Open quests menu"""
    # Add your quests system here
    print("Quests - Coming soon!")

def open_collection(self):
    """Open collection viewer"""
    # Add your collection viewer here
    print("Collection - Coming soon!")
```

## Video Background Setup

### Recommended Video Specs
- **Format**: MP4 (H.264 codec)
- **Resolution**: 1280x720 or higher (will be scaled)
- **Duration**: 10-30 seconds for seamless looping
- **File Size**: Under 50MB for good performance
- **Style**: Atmospheric, game-themed, not too distracting

### Finding Free Videos

**Stock Video Sites:**
1. [Pexels Videos](https://www.pexels.com/videos/) - Free, no attribution required
2. [Pixabay Videos](https://pixabay.com/videos/) - Free, no attribution required
3. [Mixkit](https://mixkit.co/free-stock-video/) - Free with simple license
4. [Videvo](https://www.videvo.net/) - Free and premium options

**Search Terms:**
- "abstract background loop"
- "particle effects"
- "fantasy landscape"
- "space animation"
- "nebula loop"
- "sci-fi background"
- "game menu background"

### Adding Your Video

1. Download your chosen video
2. Rename it to `menu_background.mp4`
3. Place it in the `videos` folder
4. Run the game - it should load automatically!

### Creating a Looping Video

If your video doesn't loop seamlessly, use ffmpeg:

```bash
# Reverse and concatenate for seamless loop
ffmpeg -i input.mp4 -filter_complex "[0:v]reverse[r];[0:v][r]concat=n=2:v=1" output.mp4
```

### Fallback Behavior

If no video is found, the menu automatically displays a gradient background:
- Dark blue to black gradient
- Professional appearance
- No performance impact
- Always available

## Troubleshooting

### Video Issues

**Video not playing**
- Check file exists at `videos/menu_background.mp4`
- Verify opencv-python is installed: `pip list | grep opencv`
- Try different video codec (H.264 recommended)
- Check console for error messages

**Video playback is laggy**
- Reduce video resolution to 1280x720
- Compress video file (< 20MB)
- Lower video framerate to 24-30fps
- Use H.264 codec

### Import Errors

**"No module named 'cv2'"**
```bash
pip install opencv-python
```

**"No module named 'menu'"**
Make sure you're running from the `code` directory:
```bash
cd code
python main_with_menu.py
```

### Font Errors

**"Font not found"**
Ensure graphics/fonts directory exists with required fonts:
- PixeloidSans.ttf
- dogicapixelbold.otf

### Performance

**Menu is slow**
- Use smaller video file
- Lower video resolution
- Remove video and use gradient fallback
- Check CPU usage (video decoding can be intensive)

## Integration with Existing Game

The menu system is designed to not interfere with your existing game:

1. **Original game unchanged**: `main.py` remains intact
2. **Wrapper approach**: `main_with_menu.py` wraps the Game class
3. **No dependencies**: Can run original game without menu
4. **Clean separation**: Menu logic isolated in `menu.py`

### Adding Menu to Your Game

If you want to integrate the menu directly into your game:

1. Import menu in your main file:
   ```python
   from menu import MainMenu
   ```

2. Add game state flags:
   ```python
   self.in_menu = True
   self.game_started = False
   ```

3. Create menu before game:
   ```python
   self.main_menu = MainMenu(self.start_game_callback, self.fonts)
   ```

4. Update main loop:
   ```python
   if self.in_menu:
       self.main_menu.update(dt)
       self.main_menu.draw(surface)
   else:
       # Run game logic
   ```

## API Reference

### MainMenu Class

```python
MainMenu(start_game_callback, fonts)
```

**Parameters:**
- `start_game_callback` (callable): Function to call when PLAY is clicked
- `fonts` (dict): Dictionary of pygame fonts

**Methods:**
- `update(dt)`: Update menu animations
- `draw(surface)`: Draw menu to surface
- `cleanup()`: Release video resources

### VideoBackground Class

```python
VideoBackground(video_path)
```

**Parameters:**
- `video_path` (str): Path to MP4 video file

**Methods:**
- `update()`: Read next video frame
- `draw(surface)`: Draw frame to surface
- `cleanup()`: Release video capture

### Button Class

```python
Button(pos, text, font, callback=None, icon=None)
```

**Parameters:**
- `pos` (tuple): (x, y) position
- `text` (str): Button text
- `font` (pygame.Font): Font for text
- `callback` (callable): Function to call on click
- `icon` (Surface): Optional icon image

**Methods:**
- `update(dt)`: Update button state
- `draw(surface)`: Draw button

## Performance Tips

1. **Video Optimization**
   - Use H.264 codec for best compatibility
   - Keep resolution at 1280x720
   - Compress to < 20MB
   - Use 24-30 FPS

2. **Menu Performance**
   - Disable video during development
   - Use gradient fallback for slower systems
   - Reduce icon count if needed

3. **Memory Management**
   - Menu cleans up video when game starts
   - Video resources properly released
   - No memory leaks

## Future Enhancements

Possible additions to the menu system:

- [ ] Settings menu implementation
- [ ] Save/load game system
- [ ] Multiplayer lobby
- [ ] Achievement showcase
- [ ] Statistics dashboard
- [ ] Custom keybinding menu
- [ ] Audio/video settings
- [ ] Profile customization
- [ ] News/updates feed
- [ ] Discord integration

## Credits

**Menu System**
- Video playback: OpenCV
- Graphics: Pygame Community Edition
- Design inspiration: Modern game menus

**Your Game**
- Original game code intact and functional
- Compatible with all existing features

## License

This menu system follows the same license as your game.

## Support

For issues or questions:
1. Check this documentation
2. Review `QUICK_START.md` for basics
3. Check console output for errors
4. Verify all dependencies installed

---

**Version**: 1.0  
**Last Updated**: 2025-10-14  
**Compatible With**: Pygame CE 2.5.5+, Python 3.13+
