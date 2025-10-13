import pygame
from sys import exit

# Pygame CE 2.5.5 + Python 3.13.7: Vector2 is available as pygame.Vector2
vector = pygame.Vector2

# Window and Game Settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6
BATTLE_OUTLINE_WIDTH = 4

# Color Palette - Using tuples for better performance in Pygame CE 2.5.5
COLORS = {
	'white': '#f4fefa', 
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire': '#f8a060',
	'water': '#50b0d8',
	'plant': '#64a990', 
	'black': '#000000', 
	'red': '#f03131',
	'blue': '#66d7ee',
	'normal': '#ffffff',
	'dark white': '#f0f0f0'
}

# Rendering Layers for Z-ordering in Overworld
WORLD_LAYERS = {
	'water': 0,
	'bg': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}

# Battle System Positions
BATTLE_POSITIONS = {
	'left': {
		'top': (360, 260), 
		'center': (190, 400), 
		'bottom': (410, 520)
	},
	'right': {
		'top': (900, 260), 
		'center': (1110, 390), 
		'bottom': (900, 550)
	}
}

# Battle Rendering Layers
BATTLE_LAYERS = {
	'outline': 0,
	'name': 1,
	'monster': 2,
	'effects': 3,
	'overlay': 4
}

# Battle UI Choices Configuration
BATTLE_CHOICES = {
	'full': {
		'fight': {'pos': vector(30, -60), 'icon': 'sword'},
		'defend': {'pos': vector(40, -20), 'icon': 'shield'},
		'switch': {'pos': vector(40, 20), 'icon': 'arrows'},
		'catch': {'pos': vector(30, 60), 'icon': 'hand'}
	},
	
	'limited': {
		'fight': {'pos': vector(30, -40), 'icon': 'sword'},
		'defend': {'pos': vector(40, 0), 'icon': 'shield'},
		'switch': {'pos': vector(30, 40), 'icon': 'arrows'}
	}
}

# Type checking helper for Python 3.13.7
def is_valid_color(color_key: str) -> bool:
	"""Check if a color key exists in COLORS dictionary"""
	return color_key in COLORS

# Vector2 helper functions for Pygame CE 2.5.5
def create_vector(x: float, y: float) -> vector:
	"""Create a Vector2 instance with type safety"""
	return vector(float(x), float(y))

def lerp_vector(start: vector, end: vector, t: float) -> vector:
	"""Linear interpolation between two vectors"""
	t = max(0.0, min(1.0, t))  # Clamp t between 0 and 1
	return start + (end - start) * t