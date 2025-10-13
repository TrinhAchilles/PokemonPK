"""
Evolution Animation for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Displays evolution transformation animation
"""

from settings import * 
from timer import Timer

class Evolution:
	"""Handles the evolution animation sequence"""
	
	def __init__(self, frames, start_monster, end_monster, font, end_evolution, star_frames):
		"""
		Initialize evolution animation
		
		Args:
			frames: Dictionary of monster sprite frames
			start_monster: Name of the pre-evolution monster
			end_monster: Name of the evolved monster
			font: Font for rendering text
			end_evolution: Callback when animation completes
			star_frames: List of star animation frames
		"""
		self.display_surface = pygame.display.get_surface()
		
		# Monster sprites
		self.start_monster_surf = pygame.transform.scale2x(frames[start_monster]['idle'][0])
		self.end_monster_surf = pygame.transform.scale2x(frames[end_monster]['idle'][0])
		
		# Timers
		self.timers = {
			'start': Timer(800, autostart=True),
			'end': Timer(1800, func=end_evolution)
		}

		# Star animation
		self.star_frames = [pygame.transform.scale2x(frame) for frame in star_frames]
		self.frame_index = 0.0

		# Screen tint
		self.tint_surf = pygame.Surface(self.display_surface.get_size())
		self.tint_surf.set_alpha(200)

		# White tint for flash effect
		self.start_monster_surf_white = pygame.mask.from_surface(self.start_monster_surf).to_surface()
		self.start_monster_surf_white.set_colorkey('black')
		self.tint_amount = 0.0
		self.tint_speed = 80
		self.start_monster_surf_white.set_alpha(int(self.tint_amount))

		# Text 
		self.start_text_surf = font.render(f'{start_monster} is evolving', False, COLORS['black'])
		self.end_text_surf = font.render(f'{start_monster} evolved into {end_monster}', False, COLORS['black'])

	def display_stars(self, dt):
		"""
		Display star animation effect
		
		Args:
			dt: Delta time in seconds
		"""
		self.frame_index += 20 * dt
		if self.frame_index < len(self.star_frames):
			frame = self.star_frames[int(self.frame_index)]
			rect = frame.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
			self.display_surface.blit(frame, rect)

	def update(self, dt):
		"""
		Update evolution animation state
		
		Args:
			dt: Delta time in seconds
		"""
		# Update timers
		for timer in self.timers.values():
			timer.update()

		# Show animation after start timer completes
		if not self.timers['start'].active:
			self.display_surface.blit(self.tint_surf, (0, 0))
			
			# First phase: Show starting monster with white flash
			if self.tint_amount < 255:
				rect = self.start_monster_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
				self.display_surface.blit(self.start_monster_surf, rect)

				# Fade in white overlay
				self.tint_amount += self.tint_speed * dt
				self.tint_amount = min(self.tint_amount, 255.0)
				self.start_monster_surf_white.set_alpha(int(self.tint_amount))
				self.display_surface.blit(self.start_monster_surf_white, rect)

				# Display "is evolving" text
				text_rect = self.start_text_surf.get_frect(midtop=rect.midbottom + vector(0, 20))
				pygame.draw.rect(
					self.display_surface, COLORS['white'], 
					text_rect.inflate(20, 20), 0, 5
				)
				self.display_surface.blit(self.start_text_surf, text_rect)

			# Second phase: Show evolved monster with stars
			else:
				rect = self.end_monster_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
				self.display_surface.blit(self.end_monster_surf, rect)
				
				# Display "evolved into" text
				text_rect = self.end_text_surf.get_frect(midtop=rect.midbottom + vector(0, 20))
				pygame.draw.rect(
					self.display_surface, COLORS['white'], 
					text_rect.inflate(20, 20), 0, 5
				)
				self.display_surface.blit(self.end_text_surf, text_rect)
				
				# Show star animation
				self.display_stars(dt)

				# Start end timer on first frame of evolved form
				if not self.timers['end'].active:
					self.timers['end'].activate()