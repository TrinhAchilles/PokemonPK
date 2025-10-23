"""
Sprite Group Classes for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Handles sprite rendering with camera offset and layering
"""

from settings import * 
from support import import_image
from entities import Entity

class AllSprites(pygame.sprite.Group):
	"""Sprite group for overworld rendering with camera offset"""
	
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector(0, 0)
		
		# Load UI elements with correct path
		try:
			from pathlib import Path
			base_path = Path(__file__).parent.parent
			self.shadow_surf = import_image(str(base_path), 'graphics', 'other', 'shadow')
			self.notice_surf = import_image(str(base_path), 'graphics', 'ui', 'notice')
		except Exception as e:
			print(f"Warning: Could not load sprite assets: {e}")
			# Create fallback surfaces
			self.shadow_surf = pygame.Surface((64, 32))
			self.shadow_surf.fill((0, 0, 0))
			self.shadow_surf.set_alpha(128)
			self.notice_surf = pygame.Surface((32, 32))
			self.notice_surf.fill((255, 0, 0))

	def draw(self, player):
		"""
		Draw all sprites with camera offset centered on player
		
		Args:
			player: Player entity to center camera on
		"""
		if player is None:
			# Fallback: no camera offset
			for sprite in self:
				self.display_surface.blit(sprite.image, sprite.rect)
			return
		
		# Calculate camera offset
		self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
		self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)

		# Separate sprites by layer
		bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main']]
		main_sprites = sorted(
			[sprite for sprite in self if sprite.z == WORLD_LAYERS['main']], 
			key=lambda sprite: sprite.y_sort
		)
		fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main']]

		# Draw each layer
		for layer in (bg_sprites, main_sprites, fg_sprites):
			for sprite in layer:
				# Check if this is a UI element (no camera offset)
				is_ui = hasattr(sprite, 'is_ui') and sprite.is_ui
				offset = vector(0, 0) if is_ui else self.offset
				
				# Draw shadow for entities
				if isinstance(sprite, Entity):
					shadow_pos = sprite.rect.topleft + offset + vector(40, 110)
					self.display_surface.blit(self.shadow_surf, shadow_pos)
				
				# Draw sprite
				self.display_surface.blit(sprite.image, sprite.rect.topleft + offset)
				
				# Draw notice indicator for player
				if sprite == player and hasattr(player, 'noticed') and player.noticed:
					rect = self.notice_surf.get_frect(midbottom=sprite.rect.midtop)
					self.display_surface.blit(self.notice_surf, rect.topleft + offset)

class BattleSprites(pygame.sprite.Group):
	"""Sprite group for battle rendering with outline highlighting"""
	
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

	def draw(self, current_monster_sprite, side, mode, target_index, player_sprites, opponent_sprites):
		"""
		Draw battle sprites with outline highlighting for current/target monsters
		
		Args:
			current_monster_sprite: Currently selected monster sprite
			side: Which side is being targeted ('player' or 'opponent')
			mode: Current battle mode ('target' or None)
			target_index: Index of target monster
			player_sprites: Group of player monster sprites
			opponent_sprites: Group of opponent monster sprites
		"""
		# Get available positions for the target side
		sprite_group = opponent_sprites if side == 'opponent' else player_sprites
		sprites = {sprite.pos_index: sprite for sprite in sprite_group}
		
		# Get the target monster sprite
		monster_sprite = None
		if sprites:
			sprite_keys = list(sprites.keys())
			if 0 <= target_index < len(sprite_keys):
				monster_sprite = sprites[sprite_keys[target_index]]

		# Draw all sprites sorted by z-layer
		for sprite in sorted(self, key=lambda sprite: sprite.z):
			# Special handling for outline layer
			if sprite.z == BATTLE_LAYERS['outline']:
				# Show outline if:
				# 1. It's the current monster's outline (and not in target mode for player)
				# 2. It's the target monster's outline (in target mode)
				show_current_outline = (
					sprite.monster_sprite == current_monster_sprite and 
					not (mode == 'target' and side == 'player')
				)
				show_target_outline = (
					monster_sprite and 
					sprite.monster_sprite == monster_sprite and 
					sprite.monster_sprite.entity == side and 
					mode == 'target'
				)
				
				if show_current_outline or show_target_outline:
					self.display_surface.blit(sprite.image, sprite.rect)
			else:
				# Draw all other layers normally
				self.display_surface.blit(sprite.image, sprite.rect)
