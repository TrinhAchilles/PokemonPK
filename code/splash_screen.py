"""
Splash Screen - Shows GIF background for 5 seconds then fades to menu
"""
import pygame
from pathlib import Path
from settings import *

# Try to import PIL for GIF support
try:
	from PIL import Image
	PIL_AVAILABLE = True
except ImportError:
	PIL_AVAILABLE = False
	print("PIL (Pillow) not available for splash screen.")

class SplashScreen:
	"""Splash screen with full-screen GIF that fades to menu"""
	def __init__(self, display_surface):
		self.display_surface = display_surface
		self.active = True
		
		# Timing
		self.elapsed_time = 0.0
		self.display_duration = 5.0  # Show for 5 seconds
		self.fade_duration = 1.0  # Fade out over 1 second
		self.fade_alpha = 0  # Start fully visible
		
		# GIF animation
		self.gif_frames = []
		self.current_frame_index = 0
		self.frame_duration = 0.1
		self.frame_timer = 0.0
		self.load_splash_gif()
		
		# Fade overlay
		self.fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.fade_surface.fill((0, 0, 0))
	
	def load_splash_gif(self):
		"""Load splash GIF animation"""
		try:
			# Look for splash GIF in graphics folder
			gif_path = Path(__file__).parent.parent / 'graphics' / 'splash.gif'
			
			if not PIL_AVAILABLE:
				print("PIL not available. Using solid color splash screen.")
				self.create_fallback_splash()
				return
			
			if gif_path.exists():
				print(f"Loading splash GIF: {gif_path}")
				
				# Open GIF with PIL
				gif = Image.open(str(gif_path))
				
				# Extract all frames
				frame_count = 0
				try:
					while True:
						# Convert PIL image to pygame surface
						frame = gif.convert('RGBA')
						
						# Scale to full screen
						frame = frame.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
						
						# Convert to pygame surface
						mode = frame.mode
						size = frame.size
						data = frame.tobytes()
						
						py_image = pygame.image.fromstring(data, size, mode)
						self.gif_frames.append(py_image)
						
						frame_count += 1
						gif.seek(gif.tell() + 1)
				except EOFError:
					pass  # End of GIF frames
				
				print(f"Loaded {frame_count} frames from splash GIF")
				
				# Set frame duration based on GIF info
				if hasattr(gif, 'info') and 'duration' in gif.info:
					self.frame_duration = gif.info['duration'] / 1000.0
				
			else:
				print(f"Splash GIF not found at {gif_path}, using fallback")
				self.create_fallback_splash()
				
		except Exception as e:
			print(f"Error loading splash GIF: {e}")
			self.create_fallback_splash()
	
	def create_fallback_splash(self):
		"""Create a fallback splash screen if GIF not found"""
		print("Creating fallback splash screen...")
		# Create a dark blue gradient
		surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		for y in range(WINDOW_HEIGHT):
			color_value = int(50 * (1 - y / WINDOW_HEIGHT))
			pygame.draw.line(surf, (color_value, color_value // 2, color_value + 80), 
							(0, y), (WINDOW_WIDTH, y))
		self.gif_frames.append(surf)
		print("Created fallback splash screen")
	
	def update(self, dt):
		"""Update splash screen state"""
		if not self.active:
			return False
		
		# Update elapsed time
		self.elapsed_time += dt
		
		# Update GIF animation
		if self.gif_frames:
			self.frame_timer += dt
			if self.frame_timer >= self.frame_duration:
				self.frame_timer -= self.frame_duration
				self.current_frame_index = (self.current_frame_index + 1) % len(self.gif_frames)
		
		# Calculate fade after display duration
		if self.elapsed_time >= self.display_duration:
			# Start fading
			fade_progress = (self.elapsed_time - self.display_duration) / self.fade_duration
			self.fade_alpha = min(255, int(fade_progress * 255))
			
			# Check if fade is complete
			if self.fade_alpha >= 255:
				self.active = False
				return False
		
		return True  # Still showing
	
	def draw(self):
		"""Draw splash screen"""
		# Draw GIF as full-screen background
		if self.gif_frames:
			current_frame = self.gif_frames[self.current_frame_index]
			self.display_surface.blit(current_frame, (0, 0))
		
		# Draw fade overlay if fading
		if self.fade_alpha > 0:
			self.fade_surface.set_alpha(self.fade_alpha)
			self.display_surface.blit(self.fade_surface, (0, 0))
	
	def is_complete(self):
		"""Check if splash screen is complete"""
		return not self.active
