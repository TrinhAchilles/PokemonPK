"""
Battle System for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Handles turn-based combat between player and opponent monsters
"""

from settings import * 
from sprites import MonsterSprite, MonsterNameSprite, MonsterLevelSprite, MonsterStatsSprite, MonsterOutlineSprite, AttackSprite, TimedSprite
from groups import BattleSprites
from game_data import ATTACK_DATA
from support import draw_bar
from timer import Timer
from random import choice

class Battle:
	"""Main battle system class"""
	
	def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts, end_battle, character, sounds):
		"""
		Initialize battle
		
		Args:
			player_monsters: Dictionary of player's monsters
			opponent_monsters: Dictionary of opponent's monsters
			monster_frames: Dictionary of monster sprite frames
			bg_surf: Background surface for battle
			fonts: Dictionary of fonts
			end_battle: Callback when battle ends
			character: Opponent character (None for wild battles)
			sounds: Dictionary of sound effects
		"""
		# general
		self.display_surface = pygame.display.get_surface()
		self.bg_surf = bg_surf
		self.monster_frames = monster_frames
		self.fonts = fonts
		self.monster_data = {'player': player_monsters, 'opponent': opponent_monsters}
		self.battle_over = False
		self.end_battle = end_battle
		self.character = character
		self.sounds = sounds

		# timers 
		self.timers = {
			'opponent delay': Timer(600, func=self.opponent_attack)
		}

		# groups
		self.battle_sprites = BattleSprites()
		self.player_sprites = pygame.sprite.Group()
		self.opponent_sprites = pygame.sprite.Group()

		# control
		self.current_monster = None
		self.selection_mode = None
		self.selected_attack = None
		self.selection_side = 'player'
		self.indexes = {
			'general': 0,
			'monster': 0,
			'attacks': 0,
			'switch': 0,
			'target': 0,
		}
		
		# Available monsters for switching
		self.available_monsters = {}

		self.setup()

	def setup(self):
		"""Set up initial battle state with monsters"""
		for entity, monsters in self.monster_data.items():
			# Only spawn first 3 monsters
			for index, monster in {k: v for k, v in monsters.items() if k <= 2}.items():
				self.create_monster(monster, index, index, entity)

		# Remove opponent monster data that was spawned
		for i in range(len(self.opponent_sprites)):
			if i in self.monster_data['opponent']:
				del self.monster_data['opponent'][i]

	def create_monster(self, monster, index, pos_index, entity):
		"""
		Create a monster sprite in battle
		
		Args:
			monster: Monster instance
			index: Monster index in party
			pos_index: Position index on battlefield
			entity: 'player' or 'opponent'
		"""
		monster.paused = False
		frames = self.monster_frames['monsters'][monster.name]
		outline_frames = self.monster_frames['outlines'][monster.name]
		
		if entity == 'player':
			pos = list(BATTLE_POSITIONS['left'].values())[pos_index]
			groups = (self.battle_sprites, self.player_sprites)
			# Flip frames for player side
			frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames_list] 
					  for state, frames_list in frames.items()}
			outline_frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames_list] 
							  for state, frames_list in outline_frames.items()}
		else:
			pos = list(BATTLE_POSITIONS['right'].values())[pos_index]
			groups = (self.battle_sprites, self.opponent_sprites)

		monster_sprite = MonsterSprite(
			pos, frames, groups, monster, index, pos_index, 
			entity, self.apply_attack, self.create_monster
		)
		MonsterOutlineSprite(monster_sprite, self.battle_sprites, outline_frames)

		# UI elements
		name_pos = (monster_sprite.rect.midleft + vector(16, -70) if entity == 'player' 
					else monster_sprite.rect.midright + vector(-40, -70))
		name_sprite = MonsterNameSprite(name_pos, monster_sprite, self.battle_sprites, self.fonts['regular'])
		level_pos = name_sprite.rect.bottomleft if entity == 'player' else name_sprite.rect.bottomright 
		MonsterLevelSprite(entity, level_pos, monster_sprite, self.battle_sprites, self.fonts['small'])
		MonsterStatsSprite(
			monster_sprite.rect.midbottom + vector(0, 20), 
			monster_sprite, (150, 48), 
			self.battle_sprites, self.fonts['small']
		)

	def input(self):
		"""Handle player input during battle"""
		if self.selection_mode and self.current_monster:
			keys = pygame.key.get_just_pressed()

			# Determine limiter for current selection mode
			match self.selection_mode:
				case 'general':
					limiter = len(BATTLE_CHOICES['full'])
				case 'attacks':
					limiter = len(self.current_monster.monster.get_abilities(all=False))
				case 'switch':
					limiter = len(self.available_monsters)
				case 'target':
					limiter = (len(self.opponent_sprites) if self.selection_side == 'opponent' 
							   else len(self.player_sprites))
				case _:
					limiter = 1

			# Navigation
			if keys[pygame.K_DOWN]:
				self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] + 1) % limiter
			if keys[pygame.K_UP]:
				self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] - 1) % limiter
			
			# Selection
			if keys[pygame.K_SPACE]:
				if self.selection_mode == 'switch':
					index, new_monster = list(self.available_monsters.items())[self.indexes['switch']]
					self.current_monster.kill()
					self.create_monster(new_monster, index, self.current_monster.pos_index, 'player')
					self.selection_mode = None
					self.update_all_monsters('resume')

				elif self.selection_mode == 'target':
					sprite_group = (self.opponent_sprites if self.selection_side == 'opponent' 
									else self.player_sprites)
					sprites = {sprite.pos_index: sprite for sprite in sprite_group}
					if sprites:
						monster_sprite = sprites[list(sprites.keys())[self.indexes['target']]]

						if self.selected_attack:
							self.current_monster.activate_attack(monster_sprite, self.selected_attack)
							self.selected_attack, self.current_monster, self.selection_mode = None, None, None
						else:
							# Catching monster
							if monster_sprite.monster.health < monster_sprite.monster.get_stat('max_health') * 0.9:
								self.monster_data['player'][len(self.monster_data['player'])] = monster_sprite.monster
								monster_sprite.delayed_kill(None)
								self.update_all_monsters('resume')
							else:
								TimedSprite(
									monster_sprite.rect.center, 
									self.monster_frames['ui']['cross'], 
									self.battle_sprites, 1000
								)

				elif self.selection_mode == 'attacks':
					abilities = self.current_monster.monster.get_abilities(all=False)
					# Ensure index is within bounds (abilities list can change as energy is used)
					if abilities and self.indexes['attacks'] < len(abilities):
						self.selection_mode = 'target'
						self.selected_attack = abilities[self.indexes['attacks']]
						self.selection_side = ATTACK_DATA[self.selected_attack]['target']

				elif self.selection_mode == 'general':
					if self.indexes['general'] == 0:  # Fight
						self.selection_mode = 'attacks'
						# Reset attack index when entering attack mode to prevent out-of-bounds errors
						self.indexes['attacks'] = 0
					
					elif self.indexes['general'] == 1:  # Defend
						self.current_monster.monster.defending = True
						self.update_all_monsters('resume')
						self.current_monster, self.selection_mode = None, None
						self.indexes['general'] = 0
					
					elif self.indexes['general'] == 2:  # Switch
						self.selection_mode = 'switch'

					elif self.indexes['general'] == 3:  # Catch
						self.selection_mode = 'target'
						self.selection_side = 'opponent'
				
				self.indexes = {k: 0 for k in self.indexes}

			# Cancel
			if keys[pygame.K_ESCAPE]:
				if self.selection_mode in ('attacks', 'switch', 'target'):
					self.selection_mode = 'general'

	def update_timers(self):
		"""Update all battle timers"""
		for timer in self.timers.values():
			timer.update()

	# Battle system
	def check_active(self):
		"""Check if any monster has full initiative and can act"""
		for monster_sprite in list(self.player_sprites.sprites() + self.opponent_sprites.sprites()):
			# Skip if monster is dead or being removed
			if not monster_sprite.alive() or monster_sprite.monster.health <= 0:
				continue
				
			if monster_sprite.monster.initiative >= 100:
				monster_sprite.monster.defending = False
				self.update_all_monsters('pause')
				monster_sprite.monster.initiative = 0
				monster_sprite.set_highlight(True)
				self.current_monster = monster_sprite
				
				if self.player_sprites in monster_sprite.groups():
					self.selection_mode = 'general'
				else:
					self.timers['opponent delay'].activate()
				break  # Only activate one monster at a time

	def update_all_monsters(self, option):
		"""Pause or resume all monsters' initiative gain"""
		for monster_sprite in self.player_sprites.sprites() + self.opponent_sprites.sprites():
			monster_sprite.monster.paused = (option == 'pause')

	def apply_attack(self, target_sprite, attack, amount):
		"""
		Apply attack damage to target
		
		Args:
			target_sprite: Target monster sprite
			attack: Attack name
			amount: Base damage amount
		"""
		# Play attack animation
		AttackSprite(
			target_sprite.rect.center, 
			self.monster_frames['attacks'][ATTACK_DATA[attack]['animation']], 
			self.battle_sprites
		)
		self.sounds[ATTACK_DATA[attack]['animation']].play()

		# Calculate type effectiveness
		attack_element = ATTACK_DATA[attack]['element']
		target_element = target_sprite.monster.element

		# Double damage (super effective)
		if (attack_element == 'fire' and target_element == 'plant' or
			attack_element == 'water' and target_element == 'fire' or
			attack_element == 'plant' and target_element == 'water'):
			amount *= 2

		# Half damage (not very effective)
		if (attack_element == 'fire' and target_element == 'water' or
			attack_element == 'water' and target_element == 'plant' or
			attack_element == 'plant' and target_element == 'fire'):
			amount *= 0.5

		# Apply defense
		target_defense = 1 - target_sprite.monster.get_stat('defense') / 2000
		if target_sprite.monster.defending:
			target_defense -= 0.2
		target_defense = max(0.0, min(1.0, target_defense))

		# Apply damage
		target_sprite.monster.health -= amount * target_defense
		self.check_death()

		# Resume battle
		self.update_all_monsters('resume')

	def check_death(self):
		"""Check for defeated monsters and handle replacements"""
		for monster_sprite in list(self.opponent_sprites.sprites() + self.player_sprites.sprites()):
			if monster_sprite.monster.health <= 0:
				if self.player_sprites in monster_sprite.groups():  # Player monster defeated
					active_monsters = [(ms.index, ms.monster) 
									   for ms in self.player_sprites.sprites()]
					available_monsters = [(index, monster) for index, monster in self.monster_data['player'].items() 
										  if monster.health > 0 and (index, monster) not in active_monsters]
					
					if available_monsters:
						new_monster_data = (available_monsters[0][1], available_monsters[0][0], 
											monster_sprite.pos_index, 'player')
					else:
						new_monster_data = None
						
				else:  # Opponent monster defeated
					if self.monster_data['opponent']:
						new_monster = list(self.monster_data['opponent'].values())[0]
						new_monster_data = (new_monster, monster_sprite.index, 
											monster_sprite.pos_index, 'opponent')
						# Remove the spawned monster from reserve
						min_key = min(self.monster_data['opponent'].keys())
						del self.monster_data['opponent'][min_key]
					else:
						new_monster_data = None
					
					# Award XP to player monsters
					if len(self.player_sprites) > 0:
						xp_amount = monster_sprite.monster.level * 100 / len(self.player_sprites)
						for player_sprite in self.player_sprites:
							player_sprite.monster.update_xp(xp_amount)

				monster_sprite.delayed_kill(new_monster_data)
				break  # Only process one death at a time

	def opponent_attack(self):
		"""AI-controlled opponent attack"""
		ability = choice(self.current_monster.monster.get_abilities())
		
		# Choose target based on attack type
		if ATTACK_DATA[ability]['target'] == 'player':
			random_target = choice(self.opponent_sprites.sprites())
		else:
			random_target = choice(self.player_sprites.sprites())
		
		self.current_monster.activate_attack(random_target, ability)

	def check_end_battle(self):
		"""Check if battle should end"""
		# Opponents defeated - player wins
		if len(self.opponent_sprites) == 0 and not self.battle_over:
			self.battle_over = True
			self.end_battle(self.character)
			for monster in self.monster_data['player'].values():
				monster.initiative = 0

		# Player defeated - game over
		if len(self.player_sprites) == 0:
			pygame.quit()
			exit()

	# UI drawing
	def draw_ui(self):
		"""Draw battle UI based on current selection mode"""
		if self.current_monster:
			if self.selection_mode == 'general':
				self.draw_general()
			if self.selection_mode == 'attacks':
				self.draw_attacks()
			if self.selection_mode == 'switch':
				self.draw_switch()

	def draw_general(self):
		"""Draw general action menu"""
		for index, (option, data_dict) in enumerate(BATTLE_CHOICES['full'].items()):
			if index == self.indexes['general']:
				surf = self.monster_frames['ui'][f"{data_dict['icon']}_highlight"]
			else:
				surf = pygame.transform.grayscale(self.monster_frames['ui'][data_dict['icon']])
			rect = surf.get_frect(center=self.current_monster.rect.midright + data_dict['pos'])
			self.display_surface.blit(surf, rect)

	def draw_attacks(self):
		"""Draw attack selection menu"""
		# data
		abilities = self.current_monster.monster.get_abilities(all=False)
		width, height = 150, 200
		visible_attacks = 4
		item_height = height / visible_attacks
		v_offset = (0 if self.indexes['attacks'] < visible_attacks 
					else -(self.indexes['attacks'] - visible_attacks + 1) * item_height)

		# bg
		bg_rect = pygame.FRect((0, 0), (width, height)).move_to(
			midleft=self.current_monster.rect.midright + vector(20, 0)
		)
		pygame.draw.rect(self.display_surface, COLORS['white'], bg_rect, 0, 5)

		for index, ability in enumerate(abilities):
			selected = index == self.indexes['attacks']

			# text 
			if selected:
				element = ATTACK_DATA[ability]['element']
				text_color = COLORS[element] if element != 'normal' else COLORS['black']
			else:
				text_color = COLORS['light']
			text_surf = self.fonts['regular'].render(ability, False, text_color)

			# rect 
			text_rect = text_surf.get_frect(
				center=bg_rect.midtop + vector(0, item_height / 2 + index * item_height + v_offset)
			)
			text_bg_rect = pygame.FRect((0, 0), (width, item_height)).move_to(center=text_rect.center)

			# draw
			if bg_rect.collidepoint(text_rect.center):
				if selected:
					if text_bg_rect.collidepoint(bg_rect.topleft):
						pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect, 0, 0, 5, 5)
					elif text_bg_rect.collidepoint(bg_rect.midbottom + vector(0, -1)):
						pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect, 0, 0, 0, 0, 5, 5)
					else:
						pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect)

				self.display_surface.blit(text_surf, text_rect)

	def draw_switch(self):
		"""Draw monster switch menu"""
		# data 
		width, height = 300, 320
		visible_monsters = 4
		item_height = height / visible_monsters
		v_offset = (0 if self.indexes['switch'] < visible_monsters 
					else -(self.indexes['switch'] - visible_monsters + 1) * item_height)
		bg_rect = pygame.FRect((0, 0), (width, height)).move_to(
			midleft=self.current_monster.rect.midright + vector(20, 0)
		)
		pygame.draw.rect(self.display_surface, COLORS['white'], bg_rect, 0, 5)

		# Get available monsters
		active_monsters = [(monster_sprite.index, monster_sprite.monster) 
						   for monster_sprite in self.player_sprites]
		self.available_monsters = {
			index: monster for index, monster in self.monster_data['player'].items() 
			if (index, monster) not in active_monsters and monster.health > 0
		}

		for index, monster in enumerate(self.available_monsters.values()):
			selected = index == self.indexes['switch']
			item_bg_rect = pygame.FRect((0, 0), (width, item_height)).move_to(
				midleft=(bg_rect.left, bg_rect.top + item_height / 2 + index * item_height + v_offset)
			)

			icon_surf = self.monster_frames['icons'][monster.name]
			icon_rect = icon_surf.get_frect(
				midleft=bg_rect.topleft + vector(10, item_height / 2 + index * item_height + v_offset)
			)
			text_surf = self.fonts['regular'].render(
				f'{monster.name} ({monster.level})', 
				False, COLORS['red'] if selected else COLORS['black']
			)
			text_rect = text_surf.get_frect(topleft=(bg_rect.left + 90, icon_rect.top))

			# selection bg
			if selected:
				if item_bg_rect.collidepoint(bg_rect.topleft):
					pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect, 0, 0, 5, 5)
				elif item_bg_rect.collidepoint(bg_rect.midbottom + vector(0, -1)):
					pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect, 0, 0, 0, 0, 5, 5)
				else:
					pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect)

			if bg_rect.collidepoint(item_bg_rect.center):
				for surf, rect in ((icon_surf, icon_rect), (text_surf, text_rect)):
					self.display_surface.blit(surf, rect)
				health_rect = pygame.FRect((text_rect.bottomleft + vector(0, 4)), (100, 4))
				energy_rect = pygame.FRect((health_rect.bottomleft + vector(0, 2)), (80, 4))
				draw_bar(self.display_surface, health_rect, monster.health, 
						 monster.get_stat('max_health'), COLORS['red'], COLORS['black'])
				draw_bar(self.display_surface, energy_rect, monster.energy, 
						 monster.get_stat('max_energy'), COLORS['blue'], COLORS['black'])

	def update(self, dt):
		"""Update battle state"""
		self.check_end_battle()
		
		# updates
		self.input()
		self.update_timers()
		self.battle_sprites.update(dt)
		self.check_active()

		# drawing
		self.display_surface.blit(self.bg_surf, (0, 0))
		self.battle_sprites.draw(
			self.current_monster, self.selection_side, self.selection_mode, 
			self.indexes['target'], self.player_sprites, self.opponent_sprites
		)
		self.draw_ui()
