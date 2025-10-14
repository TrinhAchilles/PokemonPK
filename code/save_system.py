"""
Save/Load system for game state persistence
Handles saving and loading player progress, monsters, and game state
"""
import json
import pickle
from pathlib import Path
from datetime import datetime

class SaveSystem:
	"""Manages game save and load operations"""
	
	def __init__(self, save_dir='saves'):
		"""Initialize save system"""
		# Get the correct save directory path
		code_dir = Path(__file__).parent
		base_path = code_dir.parent
		self.save_dir = base_path / save_dir
		self.save_dir.mkdir(exist_ok=True)
		
		self.save_file = self.save_dir / 'save_data.pkl'
		self.metadata_file = self.save_dir / 'save_metadata.json'
	
	def save_exists(self):
		"""Check if a save file exists"""
		return self.save_file.exists()
	
	def save_game(self, game_state):
		"""
		Save the current game state
		
		Args:
			game_state (dict): Dictionary containing game state data
				Expected keys:
				- player_monsters: dict of Monster objects
				- player_position: tuple (x, y)
				- current_map: str (map name)
				- current_spawn: str (spawn position)
				- game_time: float (total play time)
		"""
		try:
			# Save the main game data
			with open(self.save_file, 'wb') as f:
				pickle.dump(game_state, f)
			
			# Save metadata (human-readable)
			metadata = {
				'save_date': datetime.now().isoformat(),
				'game_version': '1.0',
				'player_level': self._calculate_party_level(game_state.get('player_monsters', {})),
				'monster_count': len(game_state.get('player_monsters', {})),
				'current_map': game_state.get('current_map', 'world'),
				'playtime': game_state.get('game_time', 0.0)
			}
			
			with open(self.metadata_file, 'w') as f:
				json.dump(metadata, f, indent=2)
			
			print(f"Game saved successfully at {datetime.now().strftime('%H:%M:%S')}")
			return True
			
		except Exception as e:
			print(f"Error saving game: {e}")
			import traceback
			traceback.print_exc()
			return False
	
	def load_game(self):
		"""
		Load saved game state
		
		Returns:
			dict: Game state dictionary or None if load fails
		"""
		if not self.save_exists():
			print("No save file found")
			return None
		
		try:
			with open(self.save_file, 'rb') as f:
				game_state = pickle.load(f)
			
			print(f"Game loaded successfully")
			return game_state
			
		except Exception as e:
			print(f"Error loading game: {e}")
			import traceback
			traceback.print_exc()
			return None
	
	def get_save_metadata(self):
		"""
		Get save file metadata without loading the full save
		
		Returns:
			dict: Metadata or None if not available
		"""
		if not self.metadata_file.exists():
			return None
		
		try:
			with open(self.metadata_file, 'r') as f:
				return json.load(f)
		except Exception as e:
			print(f"Error reading metadata: {e}")
			return None
	
	def delete_save(self):
		"""Delete the save file"""
		try:
			if self.save_file.exists():
				self.save_file.unlink()
			if self.metadata_file.exists():
				self.metadata_file.unlink()
			print("Save file deleted")
			return True
		except Exception as e:
			print(f"Error deleting save: {e}")
			return False
	
	def _calculate_party_level(self, monsters):
		"""Calculate average party level"""
		if not monsters:
			return 0
		total = sum(monster.level for monster in monsters.values())
		return total // len(monsters)
	
	def export_to_json(self, filename='save_export.json'):
		"""Export save data to JSON format (for debugging/backup)"""
		if not self.save_exists():
			return False
		
		try:
			game_state = self.load_game()
			
			# Convert to JSON-serializable format
			exportable = {
				'current_map': game_state.get('current_map'),
				'current_spawn': game_state.get('current_spawn'),
				'game_time': game_state.get('game_time'),
				'player_position': game_state.get('player_position'),
				'monsters': {}
			}
			
			# Export monster data
			for idx, monster in game_state.get('player_monsters', {}).items():
				exportable['monsters'][idx] = {
					'name': monster.name,
					'level': monster.level,
					'health': monster.health,
					'energy': monster.energy,
					'xp': monster.xp
				}
			
			export_path = self.save_dir / filename
			with open(export_path, 'w') as f:
				json.dump(exportable, f, indent=2)
			
			print(f"Save exported to {export_path}")
			return True
			
		except Exception as e:
			print(f"Error exporting save: {e}")
			return False


def create_game_state_snapshot(game):
	"""
	Create a snapshot of the current game state for saving
	
	Args:
		game: The Game instance
	
	Returns:
		dict: Game state snapshot
	"""
	state = {
		'player_monsters': game.player_monsters,
		'current_map': 'world',  # Will be updated when map tracking is added
		'current_spawn': 'house',  # Will be updated when position tracking is added
		'game_time': 0.0,  # Will track total playtime
		'player_position': (0, 0)  # Will be updated with actual position
	}
	
	# Get player position if available
	if hasattr(game, 'player') and game.player:
		state['player_position'] = (game.player.rect.x, game.player.rect.y)
	
	# Track current map (will need to add this to Game class)
	if hasattr(game, 'current_map_name'):
		state['current_map'] = game.current_map_name
	
	if hasattr(game, 'current_spawn_name'):
		state['current_spawn'] = game.current_spawn_name
	
	if hasattr(game, 'total_play_time'):
		state['game_time'] = game.total_play_time
	
	return state


def apply_game_state(game, state):
	"""
	Apply a loaded game state to the game instance
	
	Args:
		game: The Game instance
		state (dict): Loaded game state
	
	Returns:
		bool: Success status
	"""
	try:
		# Restore player monsters
		if 'player_monsters' in state:
			game.player_monsters = state['player_monsters']
		
		# Restore map and position
		current_map = state.get('current_map', 'world')
		current_spawn = state.get('current_spawn', 'house')
		
		# Setup the game world with saved position
		if hasattr(game, 'tmx_maps') and current_map in game.tmx_maps:
			game.setup(game.tmx_maps[current_map], current_spawn)
		
		# Restore player position if it was saved
		if 'player_position' in state and hasattr(game, 'player') and game.player:
			pos = state['player_position']
			game.player.rect.x = pos[0]
			game.player.rect.y = pos[1]
			game.player.hitbox.center = game.player.rect.center
		
		# Restore playtime
		if 'game_time' in state:
			game.total_play_time = state['game_time']
		
		# Update monster index if it exists
		if hasattr(game, 'monster_index') and game.monster_index:
			game.monster_index.monsters = game.player_monsters
		
		print("Game state applied successfully")
		return True
		
	except Exception as e:
		print(f"Error applying game state: {e}")
		import traceback
		traceback.print_exc()
		return False
