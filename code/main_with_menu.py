"""
Main game launcher with menu integration
This wraps the original Game class to add a main menu with video background
"""
import pygame
from settings import *
from menu import MainMenu
from main import Game

class GameWithMenu:
	"""Wrapper that adds a main menu to the game"""
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Hunter')
		self.clock = pygame.Clock()
		self.running = True
		
		# Game state
		self.in_menu = True
		self.game = None
		
		# Load fonts early for menu
		from pathlib import Path
		code_dir = Path(__file__).parent
		base_path = code_dir.parent
		font_path = base_path / 'graphics' / 'fonts'
		
		self.fonts = {
			'dialog': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 18),
			'small': pygame.font.Font(str(font_path / 'PixeloidSans.ttf'), 14),
			'bold': pygame.font.Font(str(font_path / 'dogicapixelbold.otf'), 20),
		}
		
		# Initialize main menu
		self.main_menu = MainMenu(self.start_game, self.fonts)
	
	def start_game(self):
		"""Start the actual game"""
		self.in_menu = False
		self.main_menu.cleanup()
		self.main_menu = None
		
		# Create game instance
		self.game = Game()
	
	def run(self):
		"""Main game loop"""
		while self.running:
			dt = self.clock.tick(60) / 1000.0
			self.display_surface.fill('black')
			
			# Event handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if self.in_menu:
							self.running = False
						else:
							# Return to menu
							self.in_menu = True
							if self.game:
								# Stop game music
								if hasattr(self.game, 'audio') and 'overworld' in self.game.audio:
									self.game.audio['overworld'].stop()
								# Recreate menu
								self.main_menu = MainMenu(self.start_game, self.fonts)
			
			# Update and draw
			if self.in_menu and self.main_menu:
				self.main_menu.update(dt)
				self.main_menu.draw(self.display_surface)
			elif self.game:
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
			
			pygame.display.flip()
		
		# Cleanup
		if self.main_menu:
			self.main_menu.cleanup()
		pygame.quit()

if __name__ == '__main__':
	try:
		game = GameWithMenu()
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
