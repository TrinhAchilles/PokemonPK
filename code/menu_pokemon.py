"""
Pokemon-PK Main Menu System
Custom main menu with save/load functionality and outlined text
"""
import pygame
import cv2
from pathlib import Path
from settings import *
from save_system import SaveSystem

class VideoBackground:
	"""Handles video playback for menu background"""
	def __init__(self, video_path):
		self.video_path = video_path
		self.cap = None
		self.current_frame = None
		self.fps = 30
		self.frame_count = 0
		self.total_frames = 0
		
		# Frame timing for correct playback speed
		self.frame_time = 0.0
		self.time_per_frame = 1.0 / 30.0  # Default to 30 FPS
		
		# Try to load video
		if Path(video_path).exists():
			self.cap = cv2.VideoCapture(str(video_path))
			self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
			self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
			self.time_per_frame = 1.0 / self.fps  # Calculate time per frame
			print(f"Video loaded: {self.fps} FPS, {self.total_frames} frames")
		else:
			print(f"Warning: Video file not found at {video_path}")
			# Create a fallback gradient background
			self.current_frame = self.create_fallback_background()
	
	def create_fallback_background(self):
		"""Create a gradient background as fallback"""
		surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		for y in range(WINDOW_HEIGHT):
			# Create a dark blue to black gradient
			color_value = int(50 * (1 - y / WINDOW_HEIGHT))
			pygame.draw.line(surf, (color_value, color_value // 2, color_value + 30), 
							(0, y), (WINDOW_WIDTH, y))
		return surf
	
	def update(self, dt):
		"""Read next frame from video at correct speed"""
		if self.cap and self.cap.isOpened():
			# Accumulate time
			self.frame_time += dt
			
			# Only read next frame when enough time has passed
			if self.frame_time >= self.time_per_frame:
				self.frame_time -= self.time_per_frame
				
				ret, frame = self.cap.read()
				
				if not ret:
					# Loop video
					self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
					ret, frame = self.cap.read()
				
				if ret:
					# Convert from OpenCV BGR to Pygame RGB
					frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					# Resize to window size
					frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
					# Convert to pygame surface
					self.current_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
		
		return self.current_frame
	
	def draw(self, surface):
		"""Draw current frame to surface"""
		if self.current_frame:
			surface.blit(self.current_frame, (0, 0))
	
	def cleanup(self):
		"""Release video capture"""
		if self.cap:
			self.cap.release()


def render_text_with_outline(text, font, text_color, outline_color, outline_width=2):
	"""
	Render text with outline effect
	
	Args:
		text (str): Text to render
		font (pygame.Font): Font to use
		text_color (tuple): RGB color for text
		outline_color (tuple): RGB color for outline
		outline_width (int): Width of outline in pixels
	
	Returns:
		pygame.Surface: Rendered text with outline
	"""
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


class MenuButton:
	"""Interactive menu button with outline text"""
	def __init__(self, pos, text, font, callback=None, text_color=(255, 255, 255), 
				 outline_color=(0, 0, 0), outline_width=2):
		self.pos = vector(pos)
		self.text = text
		self.font = font
		self.callback = callback
		self.hovered = False
		self.scale = 1.0
		self.target_scale = 1.0
		self.text_color = text_color
		self.outline_color = outline_color
		self.outline_width = outline_width
		
		# Create text surface with outline
		self.text_surf = render_text_with_outline(
			text, font, text_color, outline_color, outline_width
		)
		self.text_rect = self.text_surf.get_rect(center=pos)
		
		# Hitbox for interaction
		padding = 20
		self.hitbox = self.text_rect.inflate(padding * 2, padding)
		
		# Cooldown to prevent multiple clicks
		self.click_cooldown = 0
	
	def update(self, dt):
		"""Update button animation"""
		# Update cooldown
		if self.click_cooldown > 0:
			self.click_cooldown -= dt
		
		mouse_pos = pygame.mouse.get_pos()
		self.hovered = self.hitbox.collidepoint(mouse_pos)
		
		# Scale animation
		self.target_scale = 1.15 if self.hovered else 1.0
		self.scale += (self.target_scale - self.scale) * 10 * dt
		
		# Check for click
		if self.hovered and pygame.mouse.get_pressed()[0] and self.click_cooldown <= 0:
			if self.callback:
				self.callback()
				self.click_cooldown = 0.3  # 300ms cooldown
	
	def draw(self, surface):
		"""Draw button with hover effect"""
		# Draw background highlight when hovered
		if self.hovered:
			highlight_surf = pygame.Surface(self.hitbox.size, pygame.SRCALPHA)
			highlight_surf.fill((255, 255, 255, 30))
			surface.blit(highlight_surf, self.hitbox)
		
		# Draw text with scale
		scaled_surf = pygame.transform.scale_by(self.text_surf, self.scale)
		scaled_rect = scaled_surf.get_rect(center=self.text_rect.center)
		surface.blit(scaled_surf, scaled_rect)
		
		# Draw selection arrow when hovered
		if self.hovered:
			arrow_pos = (self.text_rect.left - 30, self.text_rect.centery)
			pygame.draw.polygon(surface, self.text_color, [
				(arrow_pos[0] - 15, arrow_pos[1]),
				(arrow_pos[0], arrow_pos[1] - 10),
				(arrow_pos[0], arrow_pos[1] + 10)
			])


class PokemonMainMenu:
	"""Main menu for Pokemon-PK with save/load functionality"""
	def __init__(self, start_new_game_callback, continue_game_callback, 
				 exit_game_callback, fonts):
		self.fonts = fonts
		self.start_new_game_callback = start_new_game_callback
		self.continue_game_callback = continue_game_callback
		self.exit_game_callback = exit_game_callback
		self.active = True
		
		# Save system
		self.save_system = SaveSystem()
		
		# Video background
		video_path = Path(__file__).parent.parent / 'videos' / 'menu_background.mp4'
		self.video_bg = VideoBackground(str(video_path))
		
		# Overlay surface for darkening
		self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.overlay.set_alpha(120)
		self.overlay.fill((0, 0, 0))
		
		# Load custom font or fallback
		self.title_font = self.load_custom_font('SVN-Determination Sans', 80)
		self.button_font = self.load_custom_font('SVN-Determination Sans', 32)
		
		# Load custom logo image or fallback to text
		self.load_title_logo()
		
		# Create menu buttons
		self.menu_buttons = []
		menu_center_x = WINDOW_WIDTH // 2
		menu_y_start = 360  # Moved down from 320 to 360
		menu_spacing = 70
		
		# Check if save exists to enable/disable Continue
		save_exists = self.save_system.save_exists()
		
		button_data = [
			('New Game', self.start_new_game),
			('Continue', self.continue_game if save_exists else None),
			('Settings', self.open_settings),
			('Exit', self.exit_game),
		]
		
		for i, (text, callback) in enumerate(button_data):
			# Gray out Continue if no save exists
			text_color = (255, 255, 255) if callback else (128, 128, 128)
			button = MenuButton(
				(menu_center_x, menu_y_start + i * menu_spacing),
				text,
				self.button_font,
				callback,
				text_color=text_color,
				outline_color=(0, 0, 0),
				outline_width=2
			)
			self.menu_buttons.append(button)
		
		# Show save info if available
		self.save_metadata = self.save_system.get_save_metadata() if save_exists else None
	
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
			# Fallback to existing fonts
			if size > 50:
				return pygame.font.Font(None, size)
			else:
				return self.fonts.get('bold', pygame.font.Font(None, size))
		
		except Exception as e:
			print(f"Error loading font: {e}")
			return pygame.font.Font(None, size)
	
	def load_title_logo(self):
		"""Load custom logo image or fallback to text"""
		logo_path = Path(__file__).parent.parent / 'graphics' / 'logo.png'
		
		try:
			if logo_path.exists():
				# Load custom logo image
				self.title_surf = pygame.image.load(str(logo_path)).convert_alpha()
				
				# Scale the logo to make it smaller
				max_width = 300  # Maximum width for logo (adjust this to make bigger/smaller)
				if self.title_surf.get_width() > max_width:
					scale_factor = max_width / self.title_surf.get_width()
					new_size = (int(self.title_surf.get_width() * scale_factor), 
								int(self.title_surf.get_height() * scale_factor))
					self.title_surf = pygame.transform.smoothscale(self.title_surf, new_size)
				
				self.title_rect = self.title_surf.get_rect(center=(WINDOW_WIDTH // 2, 180))
				print("Custom logo loaded successfully!")
			else:
				# Fallback to text if logo not found
				print("Logo file not found at graphics/logo.png, using text")
				self.title_surf = render_text_with_outline(
					'Pokemon-PK',
					self.title_font,
					(255, 215, 0),  # Yellow/Gold
					(0, 100, 255),  # Blue
					outline_width=4
				)
				self.title_rect = self.title_surf.get_rect(center=(WINDOW_WIDTH // 2, 180))
		
		except Exception as e:
			print(f"Error loading logo: {e}, using text fallback")
			# Fallback to text on error
			self.title_surf = render_text_with_outline(
				'Pokemon-PK',
				self.title_font,
				(255, 215, 0),  # Yellow/Gold
				(0, 100, 255),  # Blue
				outline_width=4
			)
			self.title_rect = self.title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
	
	def start_new_game(self):
		"""Start a new game"""
		self.active = False
		if self.start_new_game_callback:
			self.start_new_game_callback()
	
	def continue_game(self):
		"""Continue from saved game"""
		if self.save_system.save_exists():
			self.active = False
			if self.continue_game_callback:
				self.continue_game_callback()
	
	def open_settings(self):
		"""Open settings menu (placeholder)"""
		print("Settings - Coming soon!")
	
	def exit_game(self):
		"""Exit the game"""
		if self.exit_game_callback:
			self.exit_game_callback()
	
	def update(self, dt):
		"""Update menu"""
		# Update video background with delta time
		self.video_bg.update(dt)
		
		# Update buttons
		for button in self.menu_buttons:
			button.update(dt)
	
	def draw(self, surface):
		"""Draw menu"""
		# Draw video background
		self.video_bg.draw(surface)
		
		# Draw overlay
		surface.blit(self.overlay, (0, 0))
		
		# Draw game title with outline
		surface.blit(self.title_surf, self.title_rect)
		
		# Draw save info if available
		if self.save_metadata:
			info_font = self.fonts.get('small', pygame.font.Font(None, 16))
			save_time = self.save_metadata.get('save_date', '')
			if save_time:
				# Format the datetime
				from datetime import datetime
				try:
					dt = datetime.fromisoformat(save_time)
					save_text = f"Last Save: {dt.strftime('%Y-%m-%d %H:%M')}"
				except:
					save_text = "Save file available"
				
				save_surf = info_font.render(save_text, True, (200, 200, 200))
				save_rect = save_surf.get_rect(center=(WINDOW_WIDTH // 2, 250))
				surface.blit(save_surf, save_rect)
		
		# Draw menu buttons
		for button in self.menu_buttons:
			button.draw(surface)
		
		# Draw version info
		version_font = self.fonts.get('small', pygame.font.Font(None, 14))
		version_surf = version_font.render('v1.0', True, (128, 128, 128))
		version_rect = version_surf.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
		surface.blit(version_surf, version_rect)
	
	def cleanup(self):
		"""Cleanup resources"""
		self.video_bg.cleanup()
