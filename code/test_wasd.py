"""
Simple WASD key test
Run this to verify your keyboard is detected
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('WASD Test')
clock = pygame.Clock()
font = pygame.font.Font(None, 36)

running = True
message = "Press W, A, S, or D"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    keys = pygame.key.get_pressed()
    
    # Check WASD
    if keys[pygame.K_w]:
        message = "W pressed - UP!"
    elif keys[pygame.K_s]:
        message = "S pressed - DOWN!"
    elif keys[pygame.K_a]:
        message = "A pressed - LEFT!"
    elif keys[pygame.K_d]:
        message = "D pressed - RIGHT!"
    elif keys[pygame.K_UP]:
        message = "Arrow UP works!"
    elif keys[pygame.K_DOWN]:
        message = "Arrow DOWN works!"
    else:
        message = "Press W, A, S, or D"
    
    screen.fill((50, 50, 50))
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 150))
    screen.blit(text, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Test complete!")
