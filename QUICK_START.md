# Quick Start - Main Menu with Video Background

## 🎮 What's New

Your game now has a beautiful main menu with looped video background, inspired by modern game menus like DUELIST!

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install opencv-python
```

### Step 2: Add Your Video (Optional)
Place a video file at: `videos/menu_background.mp4`

**Don't have a video?** No problem! The menu will display a stylish gradient background as a fallback.

### Step 3: Run the Game
```bash
cd code
python main_with_menu.py
```

## 🎨 Features

✅ **Video Background** - Seamless looping background video  
✅ **Animated Buttons** - Hover effects and smooth transitions  
✅ **Main Menu Items**:
- **PLAY** - Start the game
- **SANDBOX** - Coming soon
- **COLLECTION** - Coming soon

✅ **Top Menu Icons**:
- QUESTS
- PROFILE  
- SETTINGS
- FRIENDS

✅ **ESC Key**: Returns to menu from game

## 📁 File Structure

```
workspace/
├── code/
│   ├── main.py              # Original game (unchanged)
│   ├── main_with_menu.py    # NEW: Game with menu
│   └── menu.py              # NEW: Menu system
├── videos/
│   └── menu_background.mp4  # Your video (optional)
└── requirements.txt         # Dependencies
```

## 🎬 Finding a Background Video

**Free Sources:**
- [Pexels Videos](https://www.pexels.com/videos/)
- [Pixabay](https://pixabay.com/videos/)
- [Mixkit](https://mixkit.co/free-stock-video/)

**Search Terms:**
- "abstract particles"
- "fantasy landscape"
- "space background"
- "game background"

**Recommended Format:**
- MP4 (H.264)
- 1280x720 or higher
- 10-30 seconds
- Under 50MB

## 🛠️ Troubleshooting

### "No module named 'cv2'"
```bash
pip install opencv-python
```

### Video not playing?
- Check file exists at `videos/menu_background.mp4`
- Try a different video file
- The gradient fallback will display automatically

### Want to customize?
Edit `code/menu.py` to change:
- Button positions
- Colors
- Text
- Layout

## 📖 Full Documentation

See `MENU_SETUP.md` for complete documentation and customization options.

## 🎯 Next Steps

1. ✅ Run the game with `python main_with_menu.py`
2. 📹 Add your custom background video
3. 🎨 Customize colors and layout
4. 🚀 Implement the placeholder menu functions

Enjoy your new cinematic menu! 🎮✨
