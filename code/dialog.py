"""
Dialog System for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Handles NPC dialog trees and speech bubbles
"""

from settings import * 
from timer import Timer

class DialogTree:
	"""Manages dialog sequences with NPCs"""
	
	def __init__(self, character, player, all_sprites, font, end_dialog):
		"""
		Initialize dialog tree
		
		Args:
			character: NPC character showing dialog
			player: Player entity
			all_sprites: Sprite group to add dialog sprites to
			font: Font for rendering text
			end_dialog: Callback function when dialog ends
		"""
		self.player = player
		self.character = character
		self.font = font 
		self.all_sprites = all_sprites
		self.end_dialog = end_dialog
		
		# Get dialog from character
		self.dialog = character.get_dialog()
		self.dialog_num = len(self.dialog)
		self.dialog_index = 0

		# Create first dialog sprite
		self.current_dialog = DialogSprite(
			self.dialog[self.dialog_index], 
			self.character, 
			self.all_sprites, 
			self.font
		)
		self.dialog_timer = Timer(500, autostart=True)

	def input(self):
		"""Handle dialog progression input"""
		keys = pygame.key.get_just_pressed()
		
		if keys[pygame.K_SPACE] and not self.dialog_timer.active:
			# Remove current dialog sprite
			self.current_dialog.kill()
			self.dialog_index += 1
			
			# Create next dialog or end conversation
			if self.dialog_index < self.dialog_num:
				self.current_dialog = DialogSprite(
					self.dialog[self.dialog_index], 
					self.character, 
					self.all_sprites, 
					self.font
				)
				self.dialog_timer.activate()
			else:
				# Dialog finished
				self.end_dialog(self.character)

	def update(self):
		"""Update dialog state"""
		self.dialog_timer.update()
		self.input()

class DialogSprite(pygame.sprite.Sprite):
	"""Speech bubble sprite that appears above characters"""
	
	def __init__(self, message, character, groups, font):
		"""
		Create a dialog sprite
		
		Args:
			message: Text to display
			character: Character showing the dialog
			groups: Sprite groups to add to
			font: Font for rendering text
		"""
		super().__init__(groups)
		self.z = WORLD_LAYERS['top']

		# Render text
		text_surf = font.render(message, False, COLORS['black'])
		padding = 5
		width = max(30, text_surf.get_width() + padding * 2)
		height = text_surf.get_height() + padding * 2

		# Create background surface with transparency
		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		surf.fill((0, 0, 0, 0))
		
		# Draw white rounded rectangle background
		pygame.draw.rect(
			surf, 
			COLORS['pure white'], 
			surf.get_frect(topleft=(0, 0)), 
			0,  # Filled
			4   # Border radius
		)
		
		# Blit text centered on background
		text_rect = text_surf.get_frect(center=(width / 2, height / 2))
		surf.blit(text_surf, text_rect)

		# Set sprite image and position above character
		self.image = surf
		self.rect = self.image.get_frect(midbottom=character.rect.midtop + vector(0, -10))