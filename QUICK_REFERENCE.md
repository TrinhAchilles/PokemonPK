# Pokemon-PK Quick Reference Card

## 🎮 Launch Game
```bash
cd code
python main_pokemon.py
```

## 📝 Menu Options
- **New Game** - Fresh start
- **Continue** - Load save
- **Settings** - Coming soon
- **Exit** - Quit game

## ⌨️ Controls
- **Mouse** - Click menu buttons
- **ESC** - Return to menu (auto-saves)
- **ENTER** - Monster index
- **Arrow Keys** - Move
- **SPACE** - Interact

## 💾 Auto-Save
- Every 60 seconds automatically
- On ESC (return to menu)
- On game exit
- Shows "Auto-saved" indicator

## 🎨 Visual Style
- **Title**: Yellow text + Blue outline
- **Buttons**: White text + Black outline
- **Font**: SVN Determination Sans

## 📁 Key Files
```
code/main_pokemon.py     - Game launcher
code/menu_pokemon.py     - Menu system
code/save_system.py      - Save/load
saves/save_data.pkl      - Your save
graphics/fonts/          - Add font here
videos/menu_background.mp4 - Add video here
```

## 🔧 Quick Customization

### Change Game Name
**File**: `code/menu_pokemon.py` line 234
```python
'Pokemon-PK'  →  'Your Name'
```

### Change Title Colors
**File**: `code/menu_pokemon.py` line 234-237
```python
(255, 215, 0)  # Yellow text
(0, 100, 255)  # Blue outline
```

### Change Auto-Save Time
**File**: `code/main_pokemon.py` line 26
```python
self.auto_save_interval = 60.0  # seconds
```

## 🐛 Troubleshooting

**Font not found?**
→ Game uses fallback, works fine

**Video not playing?**
→ Gradient displays automatically

**Continue grayed out?**
→ No save exists yet, play first

**Save not working?**
→ Check console for errors

## 📦 Installation
```bash
pip install opencv-python
```

## 📖 Full Docs
- **Setup Guide**: `POKEMON_MENU_SETUP.md`
- **Save System**: `code/save_system.py`
- **Menu Code**: `code/menu_pokemon.py`

---

**Quick Test:**
1. Run: `python code/main_pokemon.py`
2. Click "New Game"
3. Play for 60+ seconds
4. See "Auto-saved" appear
5. Press ESC to return to menu
6. Click "Continue" - you're back!

✨ Ready to play! ✨
