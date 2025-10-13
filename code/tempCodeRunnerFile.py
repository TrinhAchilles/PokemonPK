from settings import *
from game_data import *
from pytmx.util_pygame import load_pygame
from pathlib import Path
from random import randint

from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite, TransitionSprite
from entities import Player, Character
from groups import AllSprites
from dialog import DialogTree
from monster_index import MonsterIndex
from battle import Battle
from timer import Timer
from evolution import Evolution

from support import *
from monster import Monster

class Game:
	# general 
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Hunter')
		self.clock = pygame.Clock()
		self.running = True
		self.encounter_timer = Timer(2000, func=self.monster_encounter)

		# player monsters 
		self.player_monsters = {
			0: Monster('Ivieron', 32),
			1: Monster('Atrox', 15),
			2: Monster('Cindrill', 16),
			3: Monster('Atrox', 10),
			4: Monster('Sparchu', 11),
			5: Monster('Gulfin', 9),
			6: Monster('Jacana', 10),
		}
		for monster in self.player_monsters.values():
			monster.xp += randint(0, monster.level * 100)
		
		self.test_monsters = {
			0: Monster('Finsta', 15),
			1: Monster('Pouch', 13),
			2: Monster('Larvea', 12),
		}

		# groups 
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()

		# transition / tint
		self.transition_target = None
		self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_mode = 'untint'
		self.tint_progress = 0
		self.tint_direction = -1
		self.tint_speed = 600

		# player reference (initialized in setup)
		self.player = None

		self.import_assets()
		self.setup(self.tmx_maps['world'], 'house')
		
		# Start overworld music if available
		if 'overworld' in self.audio:
			self.audio['overworld'].play(loops=-1)

		# overlays 
		self.dialog_tree = None
		self.monster_index = MonsterIndex(self.player_monsters, self.fonts, self.monster_frames)
		self.index_open = False
		self.battle = None
		self.evolution = None

	def import_assets(self):
		"""Import all game assets with error handling"""
		base_path = Path('..')
		
		try:
			# TMX maps
			self.tmx_maps = tmx_importer(str(base_path), 'data', 'maps')

			# Overworld frames
			self.overworld_frames = {
				'water': import_folder(str(base_path), 'graphics', 'tilesets', 'water'),
				'coast': coast_importer(24, 12, str(base_path), 'graphics', 'tilesets', 'coast'),
				'characters': all_character_import(str(base_path), 'graphics', 'characters')
			}

			# Monster frames
			self.monster_frames = {
				'icons': import_folder_dict(str(base_path), 'graphics', 'icons'),
				'monsters': monster_importer(4, 2, str(base_path), 'graphics', 'monsters'),
				'ui': import_folder_dict(str(base_path), 'graphics', 'ui'),
				'attacks': attack_importer(str(base_path), 'graphics', 'attacks')
			}
			self.monster_frames['outlines'] = outline_creator(self.monster_frames['monsters'], 4)

			# Fonts - using Path for cross-platform compatibility
			font_path = base_path / 'graphics' / 'fonts'
			self.fonts = {
				'dialog': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 30),
				'regular': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 18),
				'small': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 14),
				'bold': pygame.font.Font(str(font_path / 'dogicapixelbold.otf'), 20),
			}
			
			# Backgrounds and animations
			self.bg_frames = import_folder_dict(str(base_path), 'graphics', 'backgrounds')
			self.start_animation_frames = import_folder(str(base_path), 'graphics', 'other', 'star animation')
		
			# Audio
			self.audio = audio_importer(str(base_path), 'audio')
			
		except FileNotFoundError as e:
			print(f"Error: Could not find asset file - {e}")
			raise
		except Exception as e:
			print(f"Error loading assets: {e}")
			import traceback
			traceback.print_exc()
			raise

	def setup(self, tmx_map, player_start_pos):
		"""Setup the game world from TMX map data"""
		# Clear the map
		for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, 
					  self.character_sprites, self.monster_sprites):
			group.empty()

		# Reset player reference
		self.player = None

		try:
			# Terrain layers
			for layer_name in ['Terrain', 'Terrain Top']:
				layer = tmx_map.get_layer_by_name(layer_name)
				if layer is None:
					print(f"Warning: Layer '{layer_name}' not found")
					continue
				
				for x, y, surf in layer.tiles():
					if surf:
						Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

			# Water layer
			water_layer = tmx_map.get_layer_by_name('Water')
			if water_layer and 'water' in self.overworld_frames:
				for obj in water_layer:
					for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
						for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
							AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])

			# Coast layer
			coast_layer = tmx_map.get_layer_by_name('Coast')
			if coast_layer and 'coast' in self.overworld_frames:
				for obj in coast_layer:
					terrain = obj.properties.get('terrain', 'grass')
					side = obj.properties.get('side', 'top')
					
					if terrain in self.overworld_frames['coast'] and side in self.overworld_frames['coast'][terrain]:
						AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], 
									   self.all_sprites, WORLD_LAYERS['bg'])
			
			# Objects layer
			objects_layer = tmx_map.get_layer_by_name('Objects')
			if objects_layer:
				for obj in objects_layer:
					if not hasattr(obj, 'image') or obj.image is None:
						continue
					
					if obj.name == 'top':
						Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
					else:
						CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

			# Transition objects
			transition_layer = tmx_map.get_layer_by_name('Transition')
			if transition_layer:
				for obj in transition_layer:
					target = obj.properties.get('target')
					pos = obj.properties.get('pos')
					if target and pos:
						TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (target, pos), self.transition_sprites)

			# Collision objects 
			collision_layer = tmx_map.get_layer_by_name('Collisions')
			if collision_layer:
				for obj in collision_layer:
					BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

			# Grass patches / Monster spawns
			monsters_layer = tmx_map.get_layer_by_name('Monsters')
			if monsters_layer:
				for obj in monsters_layer:
					if hasattr(obj, 'image') and obj.image:
						biome = obj.properties.get('biome', 'grass')
						monsters = obj.properties.get('monsters', [])
						level = obj.properties.get('level', 10)
						MonsterPatchSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.monster_sprites), 
										   biome, monsters, level)

			# Entities layer - First pass to create player
			entities_layer = tmx_map.get_layer_by_name('Entities')
			if entities_layer:
				for obj in entities_layer:
					if obj.name == 'Player':
						if obj.properties.get('pos') == player_start_pos:
							self.player = Player(
								pos=(obj.x, obj.y), 
								frames=self.overworld_frames['characters']['player'], 
								groups=self.all_sprites,
								facing_direction=obj.properties.get('direction', 'down'), 
								collision_sprites=self.collision_sprites)
							break  # Found player, exit loop

			# Validate player was created
			if self.player is None:
				print(f"Warning: No player found with start position '{player_start_pos}', creating default player")
				# Create default player
				if 'player' in self.overworld_frames.get('characters', {}):
					self.player = Player(
						pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 
						frames=self.overworld_frames['characters']['player'], 
						groups=self.all_sprites,
						facing_direction='down', 
						collision_sprites=self.collision_sprites)

			# Second pass for NPCs (now that player exists)
			if entities_layer and self.player:
				for obj in entities_layer:
					if obj.name != 'Player':
						# Create NPC character
						character_id = obj.properties.get('character_id')
						graphic = obj.properties.get('graphic')
						
						if character_id and character_id in TRAINER_DATA and graphic:
							Character(
								pos=(obj.x, obj.y), 
								frames=self.overworld_frames['characters'].get(graphic, self.overworld_frames['characters']['player']), 
								groups=(self.all_sprites, self.collision_sprites, self.character_sprites),
								facing_direction=obj.properties.get('direction', 'down'),
								character_data=TRAINER_DATA[character_id],
								player=self.player,
								create_dialog=self.create_dialog,
								collision_sprites=self.collision_sprites,
								radius=obj.properties.get('radius', 80),
								nurse=character_id == 'Nurse',
								notice_sound=self.audio.get('notice'))

		except Exception as e:
			print(f"Error during map setup: {e}")
			import traceback
			traceback.print_exc()
			
			# Ensure player exists even if setup fails
			if self.player is None and 'player' in self.overworld_frames.get('characters', {}):
				self.player = Player(
					pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 
					frames=self.overworld_frames['characters']['player'], 
					groups=self.all_sprites,
					facing_direction='down', 
					collision_sprites=self.collision_sprites)

	# dialog system
	def input(self):
		"""Handle player input - Pygame CE 2.5.5 compatible"""
		if not self.dialog_tree and not self.battle and self.player:
			# Pygame CE 2.5.5: get_just_pressed() returns sequence of bools
			keys = pygame.key.get_just_pressed()
			
			if keys[pygame.K_SPACE]:
				for character in self.character_sprites:
					if check_connections(100, self.player, character):
						self.player.block()
						character.change_facing_direction(self.player.rect.center)
						self.create_dialog(character)
						character.can_rotate = False

			if keys[pygame.K_RETURN]:
				self.index_open = not self.index_open
				if self.player:
					self.player.blocked = not self.player.blocked

	def create_dialog(self, character):
		"""Create a dialog tree for character interaction"""
		if not self.dialog_tree and self.player:
			self.dialog_tree = DialogTree(character, self.player, self.all_sprites, 
										  self.fonts['dialog'], self.end_dialog)

	def end_dialog(self, character):
		"""End dialog and handle post-dialog logic"""
		self.dialog_tree = None
		
		if character.nurse:
			# Heal all monsters
			for monster in self.player_monsters.values():
				monster.health = monster.get_stat('max_health')
				monster.energy = monster.get_stat('max_energy')
			
			if self.player:
				self.player.unblock()
				
		elif not character.character_data.get('defeated', False):
			# Start battle
			if 'overworld' in self.audio:
				self.audio['overworld'].stop()
			if 'battle' in self.audio:
				self.audio['battle'].play(loops=-1)
				
			biome = character.character_data.get('biome', 'grass')
			self.transition_target = Battle(
				player_monsters=self.player_monsters, 
				opponent_monsters=character.monsters, 
				monster_frames=self.monster_frames, 
				bg_surf=self.bg_frames.get(biome, list(self.bg_frames.values())[0]), 
				fonts=self.fonts, 
				end_battle=self.end_battle,
				character=character, 
				sounds=self.audio)
			self.tint_mode = 'tint'
		else:
			if self.player:
				self.player.unblock()
			self.check_evolution()

	# transition system
	def transition_check(self):
		"""Check if player is touching a transition zone"""
		if not self.player:
			return
			
		sprites = [sprite for sprite in self.transition_sprites 
				   if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			self.player.block()
			self.transition_target = sprites[0].target
			self.tint_mode = 'tint'

	def tint_screen(self, dt):
		"""Handle screen tinting for transitions"""
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				if isinstance(self.transition_target, Battle):
					self.battle = self.transition_target
				elif self.transition_target == 'level':
					self.battle = None
				else:
					# Map transition
					map_name, spawn_pos = self.transition_target
					if map_name in self.tmx_maps:
						self.setup(self.tmx_maps[map_name], spawn_pos)
					else:
						print(f"Warning: Map '{map_name}' not found")
						
				self.tint_mode = 'untint'
				self.transition_target = None

		self.tint_progress = max(0.0, min(self.tint_progress, 255.0))
		self.tint_surf.set_alpha(int(self.tint_progress))
		self.display_surface.blit(self.tint_surf, (0, 0))
	
	def end_battle(self, character):
		"""End battle and return to overworld"""
		if 'battle' in self.audio:
			self.audio['battle'].stop()
			
		self.transition_target = 'level'
		self.tint_mode = 'tint'
		
		if character:
			character.character_data['defeated'] = True
			self.create_dialog(character)
		elif not self.evolution:
			if self.player:
				self.player.unblock()
			self.check_evolution()

	def check_evolution(self):
		"""Check if any monsters should evolve"""
		evolved = False
		for index, monster in self.player_monsters.items():
			if monster.evolution:
				if monster.level == monster.evolution[1]:
					if not evolved:  # Only play sound once
						if 'evolution' in self.audio:
							self.audio['evolution'].play()
						if self.player:
							self.player.block()
					
					self.evolution = Evolution(
						self.monster_frames['monsters'], 
						monster.name, 
						monster.evolution[0], 
						self.fonts['bold'], 
						self.end_evolution, 
						self.start_animation_frames)
					self.player_monsters[index] = Monster(monster.evolution[0], monster.level)
					evolved = True
					break  # Handle one evolution at a time
					
		if not self.evolution and not evolved:
			if 'overworld' in self.audio:
				self.audio['overworld'].play(loops=-1)

	def end_evolution(self):
		"""End evolution animation"""
		self.evolution = None
		if self.player:
			self.player.unblock()
		if 'evolution' in self.audio:
			self.audio['evolution'].stop()
		if 'overworld' in self.audio:
			self.audio['overworld'].play(loops=-1)

	# monster encounters 
	def check_monster(self):
		"""Check for random monster encounters in grass"""
		if not self.player or self.battle:
			return
			
		colliding_patches = [sprite for sprite in self.monster_sprites 
							 if sprite.rect.colliderect(self.player.hitbox)]
		
		if colliding_patches and self.player.direction:
			if not self.encounter_timer.active:
				self.encounter_timer.activate()

	def monster_encounter(self):
		"""Trigger a random wild monster encounter"""
		if not self.player:
			return
			
		sprites = [sprite for sprite in self.monster_sprites 
				   if sprite.rect.colliderect(self.player.hitbox)]
		
		if sprites and self.player.direction:
			self.encounter_timer.duration = randint(800, 2500)
			self.player.block()
			
			if 'overworld' in self.audio:
				self.audio['overworld'].stop()
			if 'battle' in self.audio:
				self.audio['battle'].play(loops=-1)
			
			patch = sprites[0]
			self.transition_target = Battle(
				player_monsters=self.player_monsters, 
				opponent_monsters={index: Monster(monster, patch.level + randint(-3, 3)) 
								   for index, monster in enumerate(patch.monsters)}, 
				monster_frames=self.monster_frames, 
				bg_surf=self.bg_frames.get(patch.biome, list(self.bg_frames.values())[0]), 
				fonts=self.fonts, 
				end_battle=self.end_battle,
				character=None, 
				sounds=self.audio)
			self.tint_mode = 'tint'

	def run(self):
		"""Main game loop - Pygame CE 2.5.5 optimized"""
		while self.running:
			# Delta time (Pygame CE 2.5.5 - returns milliseconds)
			dt = self.clock.tick(60) / 1000.0  # Convert to seconds, 60 FPS cap
			self.display_surface.fill('black')

			# Event loop 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.running = False

			# Update 
			self.encounter_timer.update()
			self.input()
			self.transition_check()
			self.all_sprites.update(dt)
			self.check_monster()
			
			# Drawing
			if self.player:
				self.all_sprites.draw(self.player)
			else:
				# Fallback if player doesn't exist
				self.all_sprites.draw(None)
			
			# Overlays 
			if self.dialog_tree:
				self.dialog_tree.update()
			if self.index_open:
				self.monster_index.update(dt)
			if self.battle:
				self.battle.update(dt)
			if self.evolution:
				self.evolution.update(dt)

			self.tint_screen(dt)
			pygame.display.flip()  # Pygame CE 2.5.5: flip() is optimized

		# Cleanup
		pygame.quit()

if __name__ == '__main__':
	try:
		game = Game()
		game.run()
	except KeyboardInterrupt:
		print("\nGame interrupted by user")
		pygame.quit()
		exit(0)
	except Exception as e:
		print(f"Fatal error: {e}")
		import traceback
		traceback.print_exc()
		pygame.quit()
		exit(1)