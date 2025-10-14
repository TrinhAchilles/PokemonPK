# Pokemon-PK Main Menu Setup Guide

## ✨ Features Implemented

Your game now has a custom Pokemon-PK themed main menu with:

### Menu Options
- **New Game** - Start a fresh adventure
- **Continue** - Load your saved game (grayed out if no save exists)
- **Settings** - Placeholder for future settings
- **Exit** - Quit the game

### Visual Design
- **Game Title**: "Pokemon-PK" in yellow text with blue outline
- **Menu Items**: White text with black outline
- **Custom Font**: SVN Determination Sans (with fallback)
- **Video Background**: Looping background video support
- **Hover Effects**: Smooth animations and selection arrows

### Auto-Save System
- ✅ Auto-saves every 60 seconds during gameplay
- ✅ Auto-saves when returning to menu (ESC key)
- ✅ Auto-saves on game exit
- ✅ Saves player monsters, position, and progress
- ✅ Shows "Last Save" timestamp on menu

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install opencv-python
```

### Step 2: Add Custom Font (Recommended)

Download **SVN-Determination Sans** font and place it here:
```
workspace/graphics/fonts/SVN-Determination Sans.ttf
```

**Where to find the font:**
1. Search Google for "SVN Determination Sans font download"
2. Or search "Determination Sans font" (similar style)
3. Alternative: Use any font you like - just rename it or the game will use a fallback

**Font alternatives** (if you can't find SVN Determination Sans):
- Determination Mono
- Press Start 2P
- VT323
- Any pixel/retro gaming font

### Step 3: Run the Game
```bash
cd code
python main_pokemon.py
```

## 🎮 How to Use

### Main Menu
- **Mouse**: Click on menu options
- **New Game**: Start a fresh game (will overwrite existing save when you play)
- **Continue**: Resume from your last save (only available if save exists)
- **Exit**: Quit the game

### During Gameplay
- **ESC Key**: Return to menu (auto-saves first)
- **ENTER Key**: Open monster index
- **SPACE**: Interact with NPCs
- **Arrow Keys**: Move player

### Auto-Save Features
- Game automatically saves every 60 seconds
- Saves when you press ESC to return to menu
- Saves when you close the game
- Shows "Auto-saved" indicator briefly after saving
- Continue button shows last save timestamp

## 📁 File Structure

```
workspace/
├── code/
│   ├── main_pokemon.py        # NEW: Pokemon menu launcher
│   ├── menu_pokemon.py        # NEW: Custom menu system
│   ├── save_system.py         # NEW: Save/load system
│   ├── main.py                # Original game (unchanged)
│   └── [other game files]
├── saves/
│   ├── save_data.pkl          # Your game save (auto-created)
│   └── save_metadata.json     # Save info (auto-created)
├── videos/
│   └── menu_background.mp4    # Optional video background
├── graphics/
│   └── fonts/
│       └── SVN-Determination Sans.ttf  # Custom font (add this)
└── requirements.txt
```

## 🎨 Customization

### Changing Colors

Edit `code/menu_pokemon.py` around line 234:

```python
# Title colors (currently yellow with blue outline)
self.title_surf = render_text_with_outline(
    'Pokemon-PK',
    self.title_font,
    (255, 215, 0),    # Change this for text color (Yellow)
    (0, 100, 255),    # Change this for outline (Blue)
    outline_width=4
)

# Button colors (currently white with black outline)
text_color = (255, 255, 255)      # White text
outline_color = (0, 0, 0)         # Black outline
```

### Changing Game Name

Edit `code/menu_pokemon.py` line 234:
```python
self.title_surf = render_text_with_outline(
    'Your Game Name Here',  # Change this
    self.title_font,
    (255, 215, 0),
    (0, 100, 255),
    outline_width=4
)
```

Also update window title in `code/main_pokemon.py` line 17:
```python
pygame.display.set_caption('Your Game Name Here')
```

### Changing Button Layout

Edit `code/menu_pokemon.py` around line 244:
```python
menu_center_x = WINDOW_WIDTH // 2  # Horizontal position
menu_y_start = 320                 # Starting Y position
menu_spacing = 70                  # Space between buttons
```

### Changing Auto-Save Interval

Edit `code/main_pokemon.py` line 26:
```python
self.auto_save_interval = 60.0  # Change to desired seconds
# Example: 120.0 for 2 minutes, 30.0 for 30 seconds
```

### Adding Video Background

1. Place your video at: `videos/menu_background.mp4`
2. Recommended specs:
   - Format: MP4 (H.264)
   - Resolution: 1280x720
   - Duration: 10-30 seconds
   - Size: Under 50MB

## 🔧 Save System Details

### What Gets Saved
- Player monster team (all stats, levels, health, energy, XP)
- Player position on map
- Current map location
- Total playtime
- Game progress

### Save File Location
- Main save: `saves/save_data.pkl`
- Metadata: `saves/save_metadata.json`

### Managing Saves

**View save info:**
The save metadata is human-readable JSON:
```bash
cat saves/save_metadata.json
```

**Delete save:**
```bash
rm saves/save_data.pkl saves/save_metadata.json
```

**Backup save:**
```bash
cp saves/save_data.pkl saves/backup.pkl
cp saves/save_metadata.json saves/backup_meta.json
```

**Export save to JSON (for debugging):**
Edit `code/save_system.py` and add at the end of `SaveSystem.__init__`:
```python
self.export_to_json()  # Creates save_export.json
```

## 🐛 Troubleshooting

### Font Issues

**"Custom font not found"**
- Download SVN Determination Sans and place in `graphics/fonts/`
- Or game will use fallback fonts automatically
- Check filename matches exactly: `SVN-Determination Sans.ttf`

### Save Issues

**"No save file found"**
- This is normal for first run
- "Continue" will be grayed out
- Play the game and it will auto-save

**"Error loading save"**
- Save file may be corrupted
- Delete `saves/save_data.pkl` and start new game
- Check console for error messages

**Save not working**
- Check `saves/` directory exists
- Verify write permissions
- Look for error messages in console

### Video Issues

**Video not playing**
- Video is optional - gradient background will display
- Install opencv: `pip install opencv-python`
- Place video at `videos/menu_background.mp4`

### Performance Issues

**Menu is slow**
- Disable video background
- Reduce auto-save frequency
- Check video file size (should be < 50MB)

## 🎯 Testing the Save System

1. **Start new game:**
   ```bash
   python code/main_pokemon.py
   ```
   Click "New Game"

2. **Play for a bit:**
   - Walk around
   - Wait for "Auto-saved" message (60 seconds)
   - Or press ESC to save and return to menu

3. **Verify save:**
   ```bash
   ls saves/
   # Should see: save_data.pkl and save_metadata.json
   ```

4. **Test continue:**
   - From menu, click "Continue"
   - You should resume where you left off

5. **Test exit save:**
   - Play the game
   - Close window (or press ESC then Exit)
   - Relaunch and Continue - progress should be saved

## 📊 Save System API

### For Developers

If you want to add more data to saves, edit `code/save_system.py`:

**Add data to save:**
```python
# In create_game_state_snapshot function
state['your_new_data'] = game.your_data
```

**Load data from save:**
```python
# In apply_game_state function
if 'your_new_data' in state:
    game.your_data = state['your_new_data']
```

**Manual save:**
```python
from save_system import SaveSystem, create_game_state_snapshot

save_system = SaveSystem()
state = create_game_state_snapshot(game)
save_system.save_game(state)
```

**Manual load:**
```python
from save_system import SaveSystem, apply_game_state

save_system = SaveSystem()
state = save_system.load_game()
if state:
    apply_game_state(game, state)
```

## 🎨 Menu Design Details

### Text Rendering
- Title uses 4-pixel outline for dramatic effect
- Buttons use 2-pixel outline for readability
- All text uses custom outline rendering function

### Animation System
- Buttons scale up 1.15x on hover
- Smooth easing with 10x interpolation factor
- 300ms click cooldown prevents double-clicks
- Selection arrow appears on hover

### Color Scheme
- **Title**: RGB(255, 215, 0) - Gold/Yellow
- **Title Outline**: RGB(0, 100, 255) - Blue
- **Buttons**: RGB(255, 255, 255) - White
- **Button Outline**: RGB(0, 0, 0) - Black
- **Disabled**: RGB(128, 128, 128) - Gray

## 🚀 Advanced Features

### Multiple Save Slots (Future)
To add multiple save slots, modify `save_system.py`:
```python
class SaveSystem:
    def __init__(self, slot=1):
        self.save_file = self.save_dir / f'save_slot_{slot}.pkl'
        self.metadata_file = self.save_dir / f'save_slot_{slot}_meta.json'
```

### Cloud Saves (Future)
Could integrate with:
- Steam Cloud
- Google Drive API
- Custom server

### Save Encryption (Future)
Add encryption to prevent save editing:
```python
from cryptography.fernet import Fernet
# Encrypt save_data before writing
```

## 📝 Notes

- Original `main.py` is completely unchanged
- Can still run original game: `python code/main.py`
- All new features are in separate files
- Save system is fully automatic
- No manual save needed!

## 🎮 Next Steps

1. ✅ Run the game and test new menu
2. 📝 Add custom font for best look
3. 📹 Add video background (optional)
4. ⚙️ Implement Settings menu (when ready)
5. 🎨 Customize colors to your liking

Enjoy your Pokemon-style main menu with auto-save! 🎮✨

---

**Version**: 2.0  
**Features**: Custom menu, auto-save, outlined text  
**Last Updated**: 2025-10-14
