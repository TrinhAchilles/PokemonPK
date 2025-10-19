"""
Loading Screen with GIF Animation
Shows animated loading screen with click-to-continue prompt
"""
import pygame
from pathlib import Path
from settings import *

# Try to import PIL for GIF support, but don't fail if not available
try:
	from PIL import Image
	PIL_AVAILABLE = True
except ImportError:
	PIL_AVAILABLE = False
	print("PIL (Pillow) not available. Loading screen will use placeholder animation.")

class LoadingScreen:
	"""Loading screen with animated GIF and click-to-continue prompt"""
	def __init__(self, display_surface, fonts):
		self.display_surface = display_surface
		self.fonts = fonts
		self.active = True
		self.clicked = False
		
		# Timing
		self.elapsed_time = 0.0
		self.show_prompt_after = 3.0  # Show prompt after 3 seconds
		
		# GIF animation
		self.gif_frames = []
		self.current_frame_index = 0
		self.frame_duration = 0.1  # 100ms per frame (10 FPS)
		self.frame_timer = 0.0
		self.load_gif()
		
		# Load custom font for prompt
		self.prompt_font = self.load_custom_font('SVN-Determination Sans', 32)
		
		# Background
		self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.background.fill((0, 0, 0))
	
	def load_gif(self):
		"""Load GIF animation frames"""
		try:
			# Look for loading GIF in graphics folder
			gif_path = Path(__file__).parent.parent / 'graphics' / 'loading.gif'
			
			if not PIL_AVAILABLE:
				print("PIL not available. Using placeholder animation.")
				print("To use GIF animations, install Pillow: pip install Pillow")
				self.create_placeholder_animation()
				return
			
			if gif_path.exists():
				print(f"Loading GIF: {gif_path}")
				
				# Open GIF with PIL
				gif = Image.open(str(gif_path))
				
				# Extract all frames
				frame_count = 0
				try:
					while True:
						# Convert PIL image to pygame surface
						frame = gif.convert('RGBA')
						
						# Scale to reasonable size if needed
						max_size = 400
						if frame.width > max_size or frame.height > max_size:
							# Calculate scaling
							scale = min(max_size / frame.width, max_size / frame.height)
							new_size = (int(frame.width * scale), int(frame.height * scale))
							frame = frame.resize(new_size, Image.Resampling.LANCZOS)
						
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
				
				print(f"Loaded {frame_count} frames from GIF")
				
				# Set frame duration based on GIF info
				if hasattr(gif, 'info') and 'duration' in gif.info:
					self.frame_duration = gif.info['duration'] / 1000.0  # Convert ms to seconds
				
			else:
				print(f"Loading GIF not found at {gif_path}, using placeholder")
				self.create_placeholder_animation()
				
		except Exception as e:
			print(f"Error loading GIF: {e}")
			self.create_placeholder_animation()
	
	def create_placeholder_animation(self):
		"""Create a simple placeholder animation if GIF not found"""
		# Create simple rotating circle animation
		for i in range(12):
			surf = pygame.Surface((200, 200), pygame.SRCALPHA)
			angle = i * 30
			
			# Draw rotating arc
			for j in range(3):
				start_angle = (angle + j * 120) * 3.14159 / 180
				end_angle = (angle + j * 120 + 30) * 3.14159 / 180
				pygame.draw.arc(surf, (255, 255, 255, 200), 
							   (50, 50, 100, 100), start_angle, end_angle, 10)
			
			self.gif_frames.append(surf)
		
		self.frame_duration = 0.08  # Faster for placeholder
	
	def load_custom_font(self, font_name, size):
		"""Load custom font or fallback to default"""
		try:
			# Try to load custom font from fonts directory
			font_path = Path(__file__).parent.parent / 'graphics' / 'fonts' / f'{font_name}.ttf'
			if font_path.exists():
				return pygame.font.Font(str(font_path), size)
			
			# Try alternate name
			font_path = Path(__file__).parent.parent / 'graphics' / 'fonts' / f'{font_name.replace(" ", "")}.ttf'
			if font_path.exists():
				return pygame.font.Font(str(font_path), size)
			
			print(f"Custom font '{font_name}' not found, using default")
			return pygame.font.Font(None, size)
			
		except Exception as e:
			print(f"Error loading font: {e}")
			return pygame.font.Font(None, size)
	
	def render_text_with_outline(self, text, font, text_color, outline_color, outline_width=3):
		"""Render text with outline effect"""
		# Render the main text
		text_surf = font.render(text, True, text_color)
		w, h = text_surf.get_size()
		
		# Create a larger surface to hold text + outline
		outline_surf = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)
		
		# Render outline by drawing text in all directions
		for dx in range(-outline_width, outline_width + 1):
			for dy in range(-outline_width, outline_width + 1):
				if dx != 0 or dy != 0:
					outline_text = font.render(text, True, outline_color)
					outline_surf.blit(outline_text, (dx + outline_width, dy + outline_width))
		
		# Draw the main text on top
		outline_surf.blit(text_surf, (outline_width, outline_width))
		
		return outline_surf
	
	def update(self, dt):
		"""Update loading screen state"""
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
		
		# Check for mouse click after prompt is shown
		if self.elapsed_time >= self.show_prompt_after:
			# Check for any mouse button click
			if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[2]:
				if not self.clicked:  # Only register once
					self.clicked = True
					self.active = False
					return False  # Signal that loading is complete
		
		return True  # Still loading
	
	def draw(self):
		"""Draw loading screen"""
		# Draw black background
		self.display_surface.blit(self.background, (0, 0))
		
		# Draw GIF animation in center
		if self.gif_frames:
			current_frame = self.gif_frames[self.current_frame_index]
			frame_rect = current_frame.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
			self.display_surface.blit(current_frame, frame_rect)
		
		# Draw "Click anywhere to continue" after delay
		if self.elapsed_time >= self.show_prompt_after:
			prompt_text = "Click anywhere to continue"
			prompt_surf = self.render_text_with_outline(
				prompt_text,
				self.prompt_font,
				(255, 255, 255),  # White
				(0, 0, 0),        # Black outline
				outline_width=3
			)
			prompt_rect = prompt_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
			
			# Add subtle pulse effect
			pulse = abs((self.elapsed_time * 2) % 2 - 1)  # 0 to 1 to 0
			alpha = int(150 + 105 * pulse)  # Pulse between 150 and 255
			prompt_surf.set_alpha(alpha)
			
			self.display_surface.blit(prompt_surf, prompt_rect)
	
	def is_complete(self):
		"""Check if loading is complete"""
		return not self.active
