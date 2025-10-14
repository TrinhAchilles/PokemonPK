import pygame
import cv2
from pathlib import Path
from settings import *

class VideoBackground:
	"""Handles video playback for menu background"""
	def __init__(self, video_path):
		self.video_path = video_path
		self.cap = None
		self.current_frame = None
		self.fps = 30
		self.frame_count = 0
		self.total_frames = 0
		
		# Try to load video
		if Path(video_path).exists():
			self.cap = cv2.VideoCapture(str(video_path))
			self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
			self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
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
	
	def update(self):
		"""Read next frame from video"""
		if self.cap and self.cap.isOpened():
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


class Button:
	"""Interactive button for menu"""
	def __init__(self, pos, text, font, callback=None, icon=None):
		self.pos = vector(pos)
		self.text = text
		self.font = font
		self.callback = callback
		self.icon = icon
		self.hovered = False
		self.scale = 1.0
		self.target_scale = 1.0
		
		# Create text surface
		self.text_surf = self.font.render(text, False, COLORS['white'])
		self.text_rect = self.text_surf.get_rect(midleft=pos)
		
		# Hitbox for interaction
		padding = 20
		self.hitbox = self.text_rect.inflate(padding * 2, padding)
	
	def update(self, dt):
		"""Update button animation"""
		mouse_pos = pygame.mouse.get_pos()
		self.hovered = self.hitbox.collidepoint(mouse_pos)
		
		# Scale animation
		self.target_scale = 1.1 if self.hovered else 1.0
		self.scale += (self.target_scale - self.scale) * 10 * dt
		
		# Check for click
		if self.hovered and pygame.mouse.get_pressed()[0]:
			if self.callback:
				self.callback()
	
	def draw(self, surface):
		"""Draw button with hover effect"""
		# Draw background highlight when hovered
		if self.hovered:
			highlight_surf = pygame.Surface(self.hitbox.size)
			highlight_surf.set_alpha(30)
			highlight_surf.fill(COLORS['white'])
			surface.blit(highlight_surf, self.hitbox)
		
		# Draw text with scale
		scaled_surf = pygame.transform.scale_by(self.text_surf, self.scale)
		scaled_rect = scaled_surf.get_rect(center=self.text_rect.center)
		surface.blit(scaled_surf, scaled_rect)
		
		# Draw decorative arrow when hovered
		if self.hovered:
			arrow_pos = (self.text_rect.left - 20, self.text_rect.centery)
			pygame.draw.polygon(surface, COLORS['white'], [
				(arrow_pos[0] - 10, arrow_pos[1]),
				(arrow_pos[0], arrow_pos[1] - 8),
				(arrow_pos[0], arrow_pos[1] + 8)
			])


class IconButton:
	"""Icon-based button for top menu"""
	def __init__(self, pos, text, icon_surf=None, callback=None):
		self.pos = vector(pos)
		self.text = text
		self.icon_surf = icon_surf
		self.callback = callback
		self.hovered = False
		self.scale = 1.0
		
		# Create icon placeholder if no surface provided
		if not self.icon_surf:
			self.icon_surf = pygame.Surface((60, 60))
			self.icon_surf.fill(COLORS['light-gray'])
			# Draw simple icon placeholder
			pygame.draw.circle(self.icon_surf, COLORS['white'], (30, 30), 20, 3)
		
		self.rect = self.icon_surf.get_rect(center=pos)
		self.hitbox = self.rect.inflate(20, 20)
	
	def update(self, dt):
		"""Update icon button"""
		mouse_pos = pygame.mouse.get_pos()
		self.hovered = self.hitbox.collidepoint(mouse_pos)
		
		# Scale animation
		target_scale = 1.1 if self.hovered else 1.0
		self.scale += (target_scale - self.scale) * 10 * dt
		
		# Check for click
		if self.hovered and pygame.mouse.get_pressed()[0]:
			if self.callback:
				self.callback()
	
	def draw(self, surface, font):
		"""Draw icon button"""
		# Draw icon with scale
		scaled_surf = pygame.transform.scale_by(self.icon_surf, self.scale)
		scaled_rect = scaled_surf.get_rect(center=self.rect.center)
		
		# Draw glow effect when hovered
		if self.hovered:
			glow_surf = pygame.Surface(scaled_rect.inflate(20, 20).size)
			glow_surf.set_alpha(50)
			glow_surf.fill(COLORS['blue'])
			surface.blit(glow_surf, scaled_rect.inflate(20, 20))
		
		surface.blit(scaled_surf, scaled_rect)
		
		# Draw text label below icon
		text_surf = font.render(self.text, False, COLORS['white'])
		text_rect = text_surf.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))
		surface.blit(text_surf, text_rect)


class MainMenu:
	"""Main menu with video background"""
	def __init__(self, start_game_callback, fonts):
		self.fonts = fonts
		self.start_game_callback = start_game_callback
		self.active = True
		
		# Video background
		video_path = Path(__file__).parent.parent / 'videos' / 'menu_background.mp4'
		self.video_bg = VideoBackground(str(video_path))
		
		# Overlay surface for darkening
		self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.overlay.set_alpha(100)
		self.overlay.fill(COLORS['black'])
		
		# Create menu buttons
		self.menu_buttons = []
		menu_x = 250
		menu_y_start = 300
		menu_spacing = 80
		
		button_data = [
			('PLAY', self.start_game),
			('SANDBOX', self.open_sandbox),
			('COLLECTION', self.open_collection),
		]
		
		for i, (text, callback) in enumerate(button_data):
			button = Button(
				(menu_x, menu_y_start + i * menu_spacing),
				text,
				self.fonts.get('bold', self.fonts['regular']),
				callback
			)
			self.menu_buttons.append(button)
		
		# Top icons
		self.icon_buttons = []
		icon_x_start = WINDOW_WIDTH - 250
		icon_spacing = 80
		
		icon_data = [
			('QUESTS', self.open_quests),
			('PROFILE', self.open_profile),
			('SETTINGS', self.open_settings),
			('FRIENDS', self.open_friends),
		]
		
		for i, (text, callback) in enumerate(icon_data):
			icon = IconButton(
				(icon_x_start + i * icon_spacing, 60),
				text,
				None,  # Will use placeholder
				callback
			)
			self.icon_buttons.append(icon)
		
		# Bug report button
		self.bug_button = Button(
			(WINDOW_WIDTH - 150, 20),
			'FOUND A BUG?',
			self.fonts['small'],
			self.report_bug
		)
		
		# Booster packs display
		self.booster_count = 0
	
	def start_game(self):
		"""Start the main game"""
		self.active = False
		if self.start_game_callback:
			self.start_game_callback()
	
	def open_sandbox(self):
		"""Open sandbox mode"""
		print("Sandbox mode - Coming soon!")
	
	def open_collection(self):
		"""Open collection viewer"""
		print("Collection - Coming soon!")
	
	def open_quests(self):
		"""Open quests menu"""
		print("Quests - Coming soon!")
	
	def open_profile(self):
		"""Open player profile"""
		print("Profile - Coming soon!")
	
	def open_settings(self):
		"""Open settings menu"""
		print("Settings - Coming soon!")
	
	def open_friends(self):
		"""Open friends list"""
		print("Friends - Coming soon!")
	
	def report_bug(self):
		"""Open bug report"""
		print("Bug report - Thank you!")
	
	def update(self, dt):
		"""Update menu"""
		# Update video background
		self.video_bg.update()
		
		# Update buttons
		for button in self.menu_buttons:
			button.update(dt)
		
		for icon in self.icon_buttons:
			icon.update(dt)
		
		self.bug_button.update(dt)
	
	def draw(self, surface):
		"""Draw menu"""
		# Draw video background
		self.video_bg.draw(surface)
		
		# Draw overlay
		surface.blit(self.overlay, (0, 0))
		
		# Draw game title
		title_font = pygame.font.Font(None, 120)
		title_surf = title_font.render('DUELIST', False, COLORS['white'])
		title_rect = title_surf.get_rect(topleft=(100, 80))
		surface.blit(title_surf, title_rect)
		
		# Draw booster packs info
		booster_text = f"{self.booster_count} BOOSTER"
		booster_surf = self.fonts['small'].render(booster_text, False, COLORS['white'])
		booster_rect = booster_surf.get_rect(midtop=(350, 150))
		surface.blit(booster_surf, booster_rect)
		
		packs_text = "PACKS"
		packs_surf = self.fonts['small'].render(packs_text, False, COLORS['white'])
		packs_rect = packs_surf.get_rect(midtop=(350, 170))
		surface.blit(packs_surf, packs_rect)
		
		# Draw menu buttons
		for button in self.menu_buttons:
			button.draw(surface)
		
		# Draw top icon buttons
		for icon in self.icon_buttons:
			icon.draw(surface, self.fonts['small'])
		
		# Draw bug button
		self.bug_button.draw(surface)
	
	def cleanup(self):
		"""Cleanup resources"""
		self.video_bg.cleanup()
