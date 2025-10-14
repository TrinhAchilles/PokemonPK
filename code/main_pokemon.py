"""
Pokemon-PK Main Game Launcher
Integrates custom menu with save/load system and auto-save
"""
import pygame
from settings import *
from menu_pokemon import PokemonMainMenu
from main import Game
from save_system import SaveSystem, create_game_state_snapshot, apply_game_state

class PokemonGame:
	"""Main game wrapper with Pokemon-PK menu and save system"""
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Pokemon-PK')
		self.clock = pygame.Clock()
		self.running = True
		
		# Game state
		self.in_menu = True
		self.game = None
		self.save_system = SaveSystem()
		
		# Auto-save settings
		self.auto_save_interval = 60.0  # Auto-save every 60 seconds
		self.time_since_last_save = 0.0
		
		# Track total playtime
		self.total_play_time = 0.0
		
		# Load fonts early for menu
		from pathlib import Path
		code_dir = Path(__file__).parent
		base_path = code_dir.parent
		font_path = base_path / 'graphics' / 'fonts'
		
		try:
			self.fonts = {
				'dialog': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 30),
				'regular': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 18),
				'small': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 14),
				'bold': pygame.font.Font(str(font_path / 'dogicapixelbold.otf'), 20),
			}
		except:
			# Fallback fonts
			print("Warning: Could not load custom fonts, using defaults")
			self.fonts = {
				'dialog': pygame.font.Font(None, 30),
				'regular': pygame.font.Font(None, 18),
				'small': pygame.font.Font(None, 14),
				'bold': pygame.font.Font(None, 20),
			}
		
		# Initialize main menu
		self.main_menu = PokemonMainMenu(
			self.start_new_game,
			self.continue_game,
			self.exit_game,
			self.fonts
		)
	
	def start_new_game(self):
		"""Start a new game"""
		print("Starting new game...")
		self.in_menu = False
		self.main_menu.cleanup()
		self.main_menu = None
		
		# Create new game instance
		self.game = Game()
		
		# Add tracking variables to game
		self.game.total_play_time = 0.0
		self.game.current_map_name = 'world'
		self.game.current_spawn_name = 'house'
		
		# Reset auto-save timer
		self.time_since_last_save = 0.0
		self.total_play_time = 0.0
	
	def continue_game(self):
		"""Continue from saved game"""
		print("Loading saved game...")
		
		# Load save data
		save_data = self.save_system.load_game()
		if not save_data:
			print("Failed to load save, starting new game instead")
			self.start_new_game()
			return
		
		self.in_menu = False
		self.main_menu.cleanup()
		self.main_menu = None
		
		# Create game instance
		self.game = Game()
		
		# Apply saved state
		apply_game_state(self.game, save_data)
		
		# Restore playtime
		self.total_play_time = save_data.get('game_time', 0.0)
		self.game.total_play_time = self.total_play_time
		
		# Reset auto-save timer
		self.time_since_last_save = 0.0
		
		print(f"Game loaded! Playtime: {self.total_play_time:.1f}s")
	
	def exit_game(self):
		"""Exit the game"""
		print("Exiting game...")
		self.running = False
	
	def auto_save(self):
		"""Perform auto-save"""
		if self.game:
			# Update playtime
			if hasattr(self.game, 'total_play_time'):
				self.game.total_play_time = self.total_play_time
			
			# Create save snapshot
			state = create_game_state_snapshot(self.game)
			
			# Save the game
			if self.save_system.save_game(state):
				print("Auto-save complete")
			else:
				print("Auto-save failed")
	
	def return_to_menu(self):
		"""Return to main menu (auto-save first)"""
		if self.game:
			# Auto-save before returning to menu
			print("Saving game before returning to menu...")
			self.auto_save()
			
			# Stop music
			if hasattr(self.game, 'audio'):
				if 'overworld' in self.game.audio:
					self.game.audio['overworld'].stop()
				if 'battle' in self.game.audio:
					self.game.audio['battle'].stop()
		
		# Recreate menu
		self.in_menu = True
		self.main_menu = PokemonMainMenu(
			self.start_new_game,
			self.continue_game,
			self.exit_game,
			self.fonts
		)
		self.game = None
	
	def run(self):
		"""Main game loop"""
		while self.running:
			dt = self.clock.tick(60) / 1000.0
			self.display_surface.fill('black')
			
			# Event handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# Auto-save before quitting
					if self.game and not self.in_menu:
						print("Saving game before exit...")
						self.auto_save()
					self.running = False
					
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if self.in_menu:
							self.running = False
						else:
							# Return to menu (with auto-save)
							self.return_to_menu()
			
			# Update and draw
			if self.in_menu and self.main_menu:
				self.main_menu.update(dt)
				self.main_menu.draw(self.display_surface)
				
			elif self.game:
				# Track playtime
				self.total_play_time += dt
				
				# Auto-save timer
				self.time_since_last_save += dt
				if self.time_since_last_save >= self.auto_save_interval:
					self.auto_save()
					self.time_since_last_save = 0.0
				
				# Run one frame of the game
				self.game.encounter_timer.update()
				self.game.input()
				self.game.transition_check()
				self.game.all_sprites.update(dt)
				self.game.check_monster()
				
				# Drawing
				if self.game.player:
					self.game.all_sprites.draw(self.game.player)
				else:
					self.game.all_sprites.draw(None)
				
				# Overlays
				if self.game.dialog_tree:
					self.game.dialog_tree.update()
				if self.game.index_open:
					self.game.monster_index.update(dt)
				if self.game.battle:
					self.game.battle.update(dt)
				if self.game.evolution:
					self.game.evolution.update(dt)
				
				self.game.tint_screen(dt)
				
				# Draw auto-save indicator
				if self.time_since_last_save < 1.0:  # Show for 1 second after save
					font = self.fonts['small']
					save_text = font.render('Auto-saved', True, (100, 255, 100))
					self.display_surface.blit(save_text, (10, 10))
			
			pygame.display.flip()
		
		# Cleanup
		if self.main_menu:
			self.main_menu.cleanup()
		
		# Final auto-save on exit
		if self.game and not self.in_menu:
			print("Final save before exit...")
			self.auto_save()
		
		pygame.quit()


if __name__ == '__main__':
	try:
		game = PokemonGame()
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
