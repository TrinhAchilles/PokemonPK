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

		# Get character name (defaults to "NPC" if not available)
		character_name = getattr(character, 'name', None)
		if not character_name:
			character_name = "Nurse" if character.nurse else "Trainer"

		# Create first dialog sprite
		self.current_dialog = DialogSprite(
			self.dialog[self.dialog_index], 
			self.character, 
			self.all_sprites, 
			self.font,
			character_name
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
				# Get character name (defaults to "NPC" if not available)
				character_name = getattr(self.character, 'name', None)
				if not character_name:
					character_name = "Nurse" if self.character.nurse else "Trainer"
				
				self.current_dialog = DialogSprite(
					self.dialog[self.dialog_index], 
					self.character, 
					self.all_sprites, 
					self.font,
					character_name
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
	"""Dialog box that appears at the bottom of the screen in classic RPG style"""
	
	def __init__(self, message, character, groups, font, character_name="NPC"):
		"""
		Create a dialog sprite
		
		Args:
			message: Text to display
			character: Character showing the dialog
			groups: Sprite groups to add to
			font: Font for rendering text
			character_name: Name of the character speaking
		"""
		super().__init__(groups)
		self.z = WORLD_LAYERS['top']

		# Dialog box dimensions (classic RPG style at bottom of screen)
		box_width = WINDOW_WIDTH - 80  # Leave 40px margin on each side
		box_height = 140
		padding = 20
		name_height = 35
		
		# Create main surface with transparency
		surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
		surf.fill((0, 0, 0, 0))
		
		# Draw semi-transparent dark background
		background_rect = surf.get_frect(topleft=(0, 0))
		pygame.draw.rect(
			surf, 
			(*pygame.Color(COLORS['dark']).rgb, 230),  # Dark with transparency
			background_rect, 
			0,  # Filled
			8   # Border radius
		)
		
		# Draw border
		pygame.draw.rect(
			surf, 
			COLORS['white'], 
			background_rect, 
			3,  # Border width
			8   # Border radius
		)
		
		# Draw character name box
		name_surf = font.render(character_name, False, COLORS['white'])
		name_box_width = name_surf.get_width() + 30
		name_box_rect = pygame.FRect(15, -name_height // 2, name_box_width, name_height)
		
		pygame.draw.rect(
			surf, 
			COLORS['gray'], 
			name_box_rect, 
			0,  # Filled
			6   # Border radius
		)
		pygame.draw.rect(
			surf, 
			COLORS['white'], 
			name_box_rect, 
			2,  # Border width
			6   # Border radius
		)
		
		# Blit character name
		name_rect = name_surf.get_frect(center=(name_box_rect.centerx, name_box_rect.centery))
		surf.blit(name_surf, name_rect)
		
		# Render and wrap text for the message
		text_surf = font.render(message, False, COLORS['white'])
		
		# Blit message text
		text_rect = text_surf.get_frect(topleft=(padding, padding + 10))
		surf.blit(text_surf, text_rect)
		
		# Draw "Press SPACE" indicator in bottom right
		small_font = pygame.font.Font(None, 24)
		indicator_surf = small_font.render("Press SPACE", False, COLORS['light-gray'])
		indicator_rect = indicator_surf.get_frect(bottomright=(box_width - padding, box_height - padding + 5))
		surf.blit(indicator_surf, indicator_rect)

		# Set sprite image and position at bottom of screen
		self.image = surf
		self.rect = self.image.get_frect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
