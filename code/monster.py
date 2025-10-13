"""
Monster Class for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Handles monster stats, abilities, and leveling
"""

from game_data import MONSTER_DATA, ATTACK_DATA
from random import randint

class Monster:
	"""Represents a monster with stats, abilities, and experience"""
	
	def __init__(self, name, level):
		"""
		Initialize a monster
		
		Args:
			name: Monster name (must exist in MONSTER_DATA)
			level: Starting level for the monster
		"""
		self.name = name
		self.level = level
		self.paused = False

		# Validate monster exists
		if name not in MONSTER_DATA:
			raise ValueError(f"Monster '{name}' not found in MONSTER_DATA")

		# stats 
		self.element = MONSTER_DATA[name]['stats']['element']
		self.base_stats = MONSTER_DATA[name]['stats']
		self.health = self.base_stats['max_health'] * self.level
		self.energy = self.base_stats['max_energy'] * self.level
		self.initiative = 0
		self.abilities = MONSTER_DATA[name]['abilities']
		self.defending = False

		# experience
		self.xp = 0
		self.level_up = self.level * 150
		self.evolution = MONSTER_DATA[self.name]['evolve']

	def __repr__(self):
		"""String representation of the monster"""
		return f'Monster: {self.name}, Level: {self.level}'

	def get_stat(self, stat):
		"""
		Get a scaled stat value based on level
		
		Args:
			stat: Stat name (max_health, attack, defense, etc.)
		
		Returns:
			Stat value scaled by level
		"""
		return self.base_stats[stat] * self.level

	def get_stats(self):
		"""
		Get all monster stats as a dictionary
		
		Returns:
			Dictionary of all stats scaled by level
		"""
		return {
			'health': self.get_stat('max_health'),
			'energy': self.get_stat('max_energy'),
			'attack': self.get_stat('attack'),
			'defense': self.get_stat('defense'),
			'speed': self.get_stat('speed'),
			'recovery': self.get_stat('recovery'),
		}

	def get_abilities(self, all=True):
		"""
		Get available abilities for this monster
		
		Args:
			all: If True, return all unlocked abilities
				 If False, only return abilities the monster can afford
		
		Returns:
			List of ability names
		"""
		if all:
			return [ability for lvl, ability in self.abilities.items() 
					if self.level >= lvl]
		else:
			return [ability for lvl, ability in self.abilities.items() 
					if self.level >= lvl and ATTACK_DATA[ability]['cost'] < self.energy]

	def get_info(self):
		"""
		Get monster info for UI display
		
		Returns:
			Tuple of (current, max) values for health, energy, and initiative
		"""
		return (
			(self.health, self.get_stat('max_health')),
			(self.energy, self.get_stat('max_energy')),
			(self.initiative, 100)
		)

	def reduce_energy(self, attack):
		"""
		Reduce energy by attack cost
		
		Args:
			attack: Attack name
		"""
		if attack in ATTACK_DATA:
			self.energy -= ATTACK_DATA[attack]['cost']

	def get_base_damage(self, attack):
		"""
		Calculate base damage for an attack
		
		Args:
			attack: Attack name
		
		Returns:
			Base damage amount
		"""
		if attack in ATTACK_DATA:
			return self.get_stat('attack') * ATTACK_DATA[attack]['amount']
		return 0

	def update_xp(self, amount):
		"""
		Add experience and level up if threshold reached
		
		Args:
			amount: XP amount to add
		"""
		if self.level_up - self.xp > amount:
			self.xp += amount
		else:
			# Level up!
			self.level += 1
			self.xp = amount - (self.level_up - self.xp)
			self.level_up = self.level * 150

	def stat_limiter(self):
		"""Ensure health and energy stay within valid ranges"""
		self.health = max(0.0, min(self.health, self.get_stat('max_health')))
		self.energy = max(0.0, min(self.energy, self.get_stat('max_energy')))

	def update(self, dt):
		"""
		Update monster state
		
		Args:
			dt: Delta time in seconds
		"""
		self.stat_limiter()
		
		if not self.paused:
			self.initiative += self.get_stat('speed') * dt