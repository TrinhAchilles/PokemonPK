"""
Support Functions for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Handles asset importing and game utilities
"""

from settings import *
from pathlib import Path
from os import walk
from pytmx.util_pygame import load_pygame

# Import functions
def import_image(*path, alpha=True, format='png'):
	"""Import a single image file"""
	full_path = Path(*path).with_suffix(f'.{format}')
	surf = pygame.image.load(str(full_path)).convert_alpha() if alpha else pygame.image.load(str(full_path)).convert()
	return surf

def import_folder(*path):
	"""Import all images from a folder as a list"""
	frames = []
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return frames
	
	for root, sub_folders, image_names in walk(str(folder_path)):
		for image_name in sorted(image_names, key=lambda name: int(name.split('.')[0]) if name.split('.')[0].isdigit() else 0):
			# Skip hidden files (like .DS_Store on macOS)
			if image_name.startswith('.'):
				continue
			
			full_path = Path(root) / image_name
			try:
				surf = pygame.image.load(str(full_path)).convert_alpha()
				frames.append(surf)
			except Exception as e:
				print(f"Error loading {full_path}: {e}")
	return frames

def import_folder_dict(*path):
	"""Import all images from a folder as a dictionary"""
	frames = {}
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return frames
	
	for root, sub_folders, image_names in walk(str(folder_path)):
		for image_name in image_names:
			# Skip hidden files (like .DS_Store on macOS)
			if image_name.startswith('.'):
				continue
			
			full_path = Path(root) / image_name
			try:
				surf = pygame.image.load(str(full_path)).convert_alpha()
				frames[image_name.split('.')[0]] = surf
			except Exception as e:
				print(f"Error loading {full_path}: {e}")
	return frames

def import_sub_folders(*path):
	"""Import all subfolders as separate frame lists"""
	frames = {}
	folder_path = Path(*path)
	
	for root, sub_folders, _ in walk(str(folder_path)):
		if sub_folders:
			for sub_folder in sub_folders:
				frames[sub_folder] = import_folder(*path, sub_folder)
	return frames

def import_tilemap(cols, rows, *path):
	"""Import and split a tilemap into individual tiles"""
	frames = {}
	surf = import_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0, 0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames

def character_importer(cols, rows, *path):
	"""Import character sprite sheet and organize by direction"""
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	
	for row, direction in enumerate(('down', 'left', 'right', 'up')):
		new_dict[direction] = [frame_dict[(col, row)] for col in range(cols)]
		new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
	return new_dict

def all_character_import(*path):
	"""Import all character sprite sheets from a directory"""
	new_dict = {}
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return new_dict
	
	for root, _, image_names in walk(str(folder_path)):
		for image in image_names:
			# Skip hidden files (like .DS_Store on macOS)
			if image.startswith('.'):
				continue
			
			if image.endswith(('.png', '.jpg', '.jpeg')):
				image_name = image.split('.')[0]
				try:
					# Use the actual path where the file was found (root), not the original path
					root_path = Path(root)
					new_dict[image_name] = character_importer(4, 4, str(root_path), image_name)
					print(f"Loaded character sprite: {image_name}")
				except Exception as e:
					print(f"Error importing character {image_name}: {e}")
					import traceback
					traceback.print_exc()
	
	# Print summary of loaded characters for debugging
	if new_dict:
		print(f"Successfully loaded {len(new_dict)} character sprite sheets: {list(new_dict.keys())}")
	else:
		print(f"Warning: No character sprites found in {folder_path}")
	
	return new_dict

def coast_importer(cols, rows, *path):
	"""Import coast tileset and organize by terrain and side"""
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	terrains = ['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i']
	sides = {
		'topleft': (0, 0), 'top': (1, 0), 'topright': (2, 0), 
		'left': (0, 1), 'right': (2, 1), 'bottomleft': (0, 2), 
		'bottom': (1, 2), 'bottomright': (2, 2)
	}
	
	for index, terrain in enumerate(terrains):
		new_dict[terrain] = {}
		for key, pos in sides.items():
			new_dict[terrain][key] = [frame_dict[(pos[0] + index * 3, pos[1] + row)] for row in range(0, rows, 3)]
	return new_dict

def tmx_importer(*path):
	"""Import all TMX map files from a directory"""
	tmx_dict = {}
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return tmx_dict
	
	for root, sub_folders, file_names in walk(str(folder_path)):
		for file in file_names:
			# Skip hidden files (like .DS_Store on macOS)
			if file.startswith('.'):
				continue
			
			if file.endswith('.tmx'):
				try:
					full_path = Path(root) / file
					tmx_dict[file.split('.')[0]] = load_pygame(str(full_path))
				except Exception as e:
					print(f"Error loading TMX {file}: {e}")
	return tmx_dict

def monster_importer(cols, rows, *path):
	"""Import monster sprite sheets and organize by state"""
	monster_dict = {}
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return monster_dict
	
	for root, sub_folders, image_names in walk(str(folder_path)):
		for image in image_names:
			# Skip hidden files (like .DS_Store on macOS)
			if image.startswith('.'):
				continue
			
			if image.endswith(('.png', '.jpg', '.jpeg')):
				image_name = image.split('.')[0]
				try:
					monster_dict[image_name] = {}
					# Use the actual path where the file was found (root), not the original path
					root_path = Path(root)
					frame_dict = import_tilemap(cols, rows, str(root_path), image_name)
					for row, key in enumerate(('idle', 'attack')):
						monster_dict[image_name][key] = [frame_dict[(col, row)] for col in range(cols)]
				except Exception as e:
					print(f"Error importing monster {image_name}: {e}")
					import traceback
					traceback.print_exc()
	
	# Print summary for debugging
	if monster_dict:
		print(f"Successfully loaded {len(monster_dict)} monster sprite sheets")
	
	return monster_dict

def outline_creator(frame_dict, width):
	"""Create outlined versions of monster sprites"""
	outline_frame_dict = {}
	
	for monster, monster_frames in frame_dict.items():
		outline_frame_dict[monster] = {}
		for state, frames in monster_frames.items():
			outline_frame_dict[monster][state] = []
			for frame in frames:
				new_surf = pygame.Surface(vector(frame.get_size()) + vector(width * 2, width * 2), pygame.SRCALPHA)
				new_surf.fill((0, 0, 0, 0))
				white_frame = pygame.mask.from_surface(frame).to_surface()
				white_frame.set_colorkey('black')

				# Draw outline in 8 directions
				new_surf.blit(white_frame, (0, 0))
				new_surf.blit(white_frame, (width, 0))
				new_surf.blit(white_frame, (width * 2, 0))
				new_surf.blit(white_frame, (width * 2, width))
				new_surf.blit(white_frame, (width * 2, width * 2))
				new_surf.blit(white_frame, (width, width * 2))
				new_surf.blit(white_frame, (0, width * 2))
				new_surf.blit(white_frame, (0, width))
				outline_frame_dict[monster][state].append(new_surf)
	return outline_frame_dict

def attack_importer(*path):
	"""Import attack animation sprite sheets"""
	attack_dict = {}
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return attack_dict
	
	for root, _, image_names in walk(str(folder_path)):
		for image in image_names:
			# Skip hidden files (like .DS_Store on macOS)
			if image.startswith('.'):
				continue
			
			if image.endswith(('.png', '.jpg', '.jpeg')):
				image_name = image.split('.')[0]
				try:
					full_path = Path(root) / image_name
					attack_dict[image_name] = list(import_tilemap(4, 1, str(full_path.parent), image_name).values())
				except Exception as e:
					print(f"Error importing attack {image_name}: {e}")
	return attack_dict

def audio_importer(*path):
	"""Import all audio files from a directory"""
	files = {}
	folder_path = Path(*path)
	
	if not folder_path.exists():
		print(f"Warning: Folder not found: {folder_path}")
		return files
	
	for root, _, file_names in walk(str(folder_path)):
		for file_name in file_names:
			# Skip hidden files (like .DS_Store on macOS)
			if file_name.startswith('.'):
				continue
			
			if file_name.endswith(('.wav', '.mp3', '.ogg')):
				try:
					full_path = Path(root) / file_name
					files[file_name.split('.')[0]] = pygame.mixer.Sound(str(full_path))
				except Exception as e:
					print(f"Error loading audio {file_name}: {e}")
	return files

# Game functions
def draw_bar(surface, rect, value, max_value, color, bg_color, radius=1):
	"""Draw a progress bar on a surface"""
	ratio = rect.width / max_value if max_value > 0 else 0
	bg_rect = rect.copy()
	progress = max(0.0, min(rect.width, value * ratio))
	progress_rect = pygame.FRect(rect.topleft, (progress, rect.height))
	pygame.draw.rect(surface, bg_color, bg_rect, 0, radius)
	pygame.draw.rect(surface, color, progress_rect, 0, radius)

def check_connections(radius, entity, target, tolerance=30):
	"""Check if entity is facing target within radius"""
	relation = vector(target.rect.center) - vector(entity.rect.center)
	
	# Check if within radius
	if relation.length() < radius:
		# Check if facing the right direction
		if entity.facing_direction == 'left' and relation.x < 0 and abs(relation.y) < tolerance:
			return True
		elif entity.facing_direction == 'right' and relation.x > 0 and abs(relation.y) < tolerance:
			return True
		elif entity.facing_direction == 'up' and relation.y < 0 and abs(relation.x) < tolerance:
			return True
		elif entity.facing_direction == 'down' and relation.y > 0 and abs(relation.x) < tolerance:
			return True
	
	return False