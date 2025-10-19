# Installing Dependencies

## Required Dependencies

The game requires the following Python packages:

- **pygame-ce** (>= 2.5.0) - Game engine
- **pytmx** (>= 3.31.0) - TMX map loading
- **opencv-python** (>= 4.8.0) - Video playback for menu background

## Optional Dependencies

- **Pillow** (>= 10.0.0) - For loading GIF animations in loading screen

## Installation Methods

### Option 1: Install All at Once (Recommended)

```bash
pip install -r requirements.txt
```

### Option 2: Install Individually

```bash
pip install pygame-ce
pip install pytmx
pip install opencv-python
pip install Pillow
```

### Option 3: Minimal Installation (No GIF support)

If you only want the essential packages:

```bash
pip install pygame-ce pytmx opencv-python
```

The loading screen will use a simple animated placeholder instead of GIF files.

## Verify Installation

Run this to check all packages are installed:

```bash
python -c "import pygame; import pytmx; import cv2; print('✓ Core dependencies OK')"
```

For full features (including GIF loading):

```bash
python -c "import pygame; import pytmx; import cv2; from PIL import Image; print('✓ All dependencies OK')"
```

## Troubleshooting

### ModuleNotFoundError: No module named 'PIL'

This means Pillow is not installed. Either:
- Install it: `pip install Pillow`
- Or ignore it - the game will work with a placeholder loading animation

### ModuleNotFoundError: No module named 'pygame'

Make sure you're installing `pygame-ce` (not `pygame`):
```bash
pip install pygame-ce
```

### opencv-python installation fails

Try installing without extra modules:
```bash
pip install opencv-python-headless
```

## Platform-Specific Notes

### Windows
```bash
python -m pip install -r requirements.txt
```

### macOS/Linux
```bash
pip3 install -r requirements.txt
```

Or use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
