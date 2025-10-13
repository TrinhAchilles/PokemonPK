"""
Timer Module for Monster Hunter
Compatible with Pygame CE 2.5.5 and Python 3.13.7
Provides timing utilities for game events
"""

from pygame.time import get_ticks

class Timer:
	"""A timer that can trigger a callback function after a duration"""
	
	def __init__(self, duration, repeat=False, autostart=False, func=None):
		"""
		Initialize timer
		
		Args:
			duration: Time in milliseconds before timer triggers
			repeat: Whether timer should restart after triggering
			autostart: Whether to start timer immediately
			func: Callback function to call when timer completes
		"""
		self.duration = duration
		self.start_time = 0
		self.active = False
		self.repeat = repeat
		self.func = func
		
		if autostart:
			self.activate()

	def activate(self):
		"""Start or restart the timer"""
		self.active = True
		self.start_time = get_ticks()

	def deactivate(self):
		"""Stop the timer and optionally restart if repeat is True"""
		self.active = False
		self.start_time = 0
		
		if self.repeat:
			self.activate()

	def update(self):
		"""Update timer state - call this every frame"""
		if self.active:
			current_time = get_ticks()
			if current_time - self.start_time >= self.duration:
				# Timer completed - call callback if it exists
				if self.func:
					self.func()
				self.deactivate()
	
	@property
	def elapsed(self):
		"""Get elapsed time in milliseconds since timer started"""
		if self.active:
			return get_ticks() - self.start_time
		return 0
	
	@property
	def remaining(self):
		"""Get remaining time in milliseconds until timer triggers"""
		if self.active:
			return max(0, self.duration - (get_ticks() - self.start_time))
		return 0
	
	@property
	def progress(self):
		"""Get progress as a value between 0.0 and 1.0"""
		if self.active and self.duration > 0:
			return min(1.0, (get_ticks() - self.start_time) / self.duration)
		return 0.0