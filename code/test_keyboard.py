"""
Advanced keyboard test - shows ALL keys pressed
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Keyboard Debug - Press ANY key')
clock = pygame.Clock()
font = pygame.font.Font(None, 24)

running = True
pressed_keys = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            key_name = pygame.key.name(event.key)
            print(f"Key pressed: {key_name} (code: {event.key})")
    
    keys = pygame.key.get_pressed()
    
    # Get all currently pressed keys
    pressed_keys = []
    if keys[pygame.K_w]:
        pressed_keys.append("W (K_w)")
    if keys[pygame.K_a]:
        pressed_keys.append("A (K_a)")
    if keys[pygame.K_s]:
        pressed_keys.append("S (K_s)")
    if keys[pygame.K_d]:
        pressed_keys.append("D (K_d)")
    if keys[pygame.K_UP]:
        pressed_keys.append("UP Arrow")
    if keys[pygame.K_DOWN]:
        pressed_keys.append("DOWN Arrow")
    if keys[pygame.K_LEFT]:
        pressed_keys.append("LEFT Arrow")
    if keys[pygame.K_RIGHT]:
        pressed_keys.append("RIGHT Arrow")
    
    # Draw
    screen.fill((30, 30, 40))
    
    title = font.render("Press W, A, S, D or Arrow Keys", True, (255, 255, 100))
    screen.blit(title, (150, 50))
    
    instruction = font.render("(Also check console output)", True, (150, 150, 150))
    screen.blit(instruction, (180, 80))
    
    if pressed_keys:
        y_offset = 150
        for key in pressed_keys:
            text = font.render(f"DETECTED: {key}", True, (100, 255, 100))
            screen.blit(text, (50, y_offset))
            y_offset += 30
    else:
        text = font.render("No keys detected...", True, (200, 200, 200))
        screen.blit(text, (200, 200))
    
    info = font.render("Press ESC to quit", True, (100, 100, 100))
    screen.blit(info, (220, 350))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("\nTest complete!")
print("Check the console output above to see which keys were detected.")
