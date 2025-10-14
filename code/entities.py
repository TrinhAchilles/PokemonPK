"""
Entity Classes for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Handles player and NPC character behavior
"""

from settings import * 
from support import check_connections
from timer import Timer
from random import choice
from monster import Monster

class Entity(pygame.sprite.Sprite):
	"""Base entity class for player and NPCs"""
	
	def __init__(self, pos, frames, groups, facing_direction):
		super().__init__(groups)
		self.z = WORLD_LAYERS['main']

		# graphics 
		self.frame_index, self.frames = 0, frames
		self.facing_direction = facing_direction

		# movement 
		self.direction = vector(0, 0)
		self.speed = 250
		self.blocked = False

		# sprite setup
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center=pos)
		self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)

		self.y_sort = self.rect.centery

	def animate(self, dt):
		"""Animate the entity sprite"""
		self.frame_index += ANIMATION_SPEED * dt
		state = self.get_state()
		frame_count = len(self.frames[state])
		self.image = self.frames[state][int(self.frame_index % frame_count)]

	def get_state(self):
		"""Determine current animation state based on movement and direction"""
		moving = bool(self.direction.x != 0 or self.direction.y != 0)
		
		if moving:
			if self.direction.x != 0:
				self.facing_direction = 'right' if self.direction.x > 0 else 'left'
			if self.direction.y != 0:
				self.facing_direction = 'down' if self.direction.y > 0 else 'up'
		
		return f"{self.facing_direction}{'' if moving else '_idle'}"

	def change_facing_direction(self, target_pos):
		"""Change facing direction to look at target position"""
		relation = vector(target_pos) - vector(self.rect.center)
		
		if abs(relation.y) < 30:
			self.facing_direction = 'right' if relation.x > 0 else 'left'
		else:
			self.facing_direction = 'down' if relation.y > 0 else 'up'

	def block(self):
		"""Stop entity movement"""
		self.blocked = True
		self.direction = vector(0, 0)

	def unblock(self):
		"""Allow entity movement"""
		self.blocked = False

class Character(Entity):
	"""NPC character with dialog and battle capabilities"""
	
	def __init__(self, pos, frames, groups, facing_direction, character_data, player, 
				 create_dialog, collision_sprites, radius, nurse, notice_sound):
		super().__init__(pos, frames, groups, facing_direction)
		
		self.character_data = character_data
		self.player = player
		self.create_dialog = create_dialog
		self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
		self.nurse = nurse
		
		# Create monsters for trainers
		self.monsters = None
		if 'monsters' in character_data and character_data['monsters']:
			self.monsters = {i: Monster(name, lvl) for i, (name, lvl) in character_data['monsters'].items()}

		# movement 
		self.has_moved = False
		self.can_rotate = True
		self.has_noticed = False
		self.radius = int(radius)
		self.view_directions = character_data['directions']

		# timers
		self.timers = {
			'look around': Timer(1500, autostart=True, repeat=True, func=self.random_view_direction),
			'notice': Timer(500, func=self.start_move)
		}
		self.notice_sound = notice_sound

	def random_view_direction(self):
		"""Randomly change view direction if character can rotate"""
		if self.can_rotate:
			self.facing_direction = choice(self.view_directions)

	def get_dialog(self):
		"""Get appropriate dialog based on character state"""
		dialog_key = 'defeated' if self.character_data.get('defeated', False) else 'default'
		return self.character_data['dialog'][dialog_key]

	def raycast(self):
		"""Check if player is in line of sight and trigger notice"""
		if check_connections(self.radius, self, self.player) and self.has_los() and not self.has_moved and not self.has_noticed:
			self.player.block()
			self.player.change_facing_direction(self.rect.center)
			self.timers['notice'].activate()
			self.can_rotate = False
			self.has_noticed = True
			self.player.noticed = True
			
			if self.notice_sound:
				self.notice_sound.play()

	def has_los(self):
		"""Check if character has line of sight to player"""
		distance = vector(self.rect.center).distance_to(vector(self.player.rect.center))
		
		if distance < self.radius:
			# Check if any collision rects block the line of sight
			collisions = [bool(rect.clipline(self.rect.center, self.player.rect.center)) 
						  for rect in self.collision_rects]
			return not any(collisions)
		
		return False

	def start_move(self):
		"""Start moving towards player"""
		relation = vector(self.player.rect.center) - vector(self.rect.center)
		if relation.length() > 0:  # Prevent division by zero
			normalized = relation.normalize()
			self.direction = vector(round(normalized.x), round(normalized.y))

	def move(self, dt):
		"""Move character towards player until collision"""
		if not self.has_moved and (self.direction.x != 0 or self.direction.y != 0):
			if not self.hitbox.inflate(10, 10).colliderect(self.player.hitbox):
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center
			else:
				self.direction = vector(0, 0)
				self.has_moved = True
				self.create_dialog(self)
				self.player.noticed = False

	def update(self, dt):
		"""Update character state"""
		for timer in self.timers.values():
			timer.update()

		self.animate(dt)
		
		if self.character_data.get('look_around', False):
			self.raycast()
			self.move(dt)

class Player(Entity):
	"""Player-controlled character"""
	
	def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
		super().__init__(pos, frames, groups, facing_direction)
		self.collision_sprites = collision_sprites
		self.noticed = False

	def input(self):
		"""Handle player keyboard input - Arrow keys and WASD"""
		keys = pygame.key.get_pressed()
		input_vector = vector(0, 0)
		
		# Arrow keys
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1
		
		# WASD keys
		if keys[pygame.K_w]:
			input_vector.y -= 1
		if keys[pygame.K_s]:
			input_vector.y += 1
		if keys[pygame.K_a]:
			input_vector.x -= 1
		if keys[pygame.K_d]:
			input_vector.x += 1
		
		# Normalize diagonal movement
		if input_vector.length() > 0:
			self.direction = input_vector.normalize()
		else:
			self.direction = input_vector

	def move(self, dt):
		"""Move player with collision detection"""
		# Horizontal movement
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('horizontal')

		# Vertical movement
		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('vertical')

	def collisions(self, axis):
		"""Handle collisions with sprites"""
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if axis == 'horizontal':
					if self.direction.x > 0: 
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def update(self, dt):
		"""Update player state"""
		self.y_sort = self.rect.centery
		
		if not self.blocked:
			self.input()
			self.move(dt)
		
		self.animate(dt)
