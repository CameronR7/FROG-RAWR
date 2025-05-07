import pygame
import math
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

bg_img = pygame.image.load("jungle.jpg")  # Background image (e.g., jungle)
bg_img = pygame.transform.scale(bg_img, (800, 600))  # Match window size

# Load and scale frog image
frog_img = pygame.image.load("frog.png")
frog_img = pygame.transform.scale(frog_img, (100, 100))  
frog_rect = frog_img.get_rect(center=(400, 300))

# Load and scale fly image (custom mouse)
fly_img = pygame.image.load("fly.png")
fly_img = pygame.transform.scale(fly_img, (30, 30))
pygame.mouse.set_visible(False)  # Initially hide the system cursor

# Font for text display
font = pygame.font.Font(None, 36)

# Frog movement variables
start_pos = pygame.Vector2(400, 300)
end_pos = pygame.Vector2(400, 300)
position = start_pos.copy()
hop_start_time = pygame.time.get_ticks()
hop_duration = 200  # ms
is_hopping = False
hop_height = 20  # peak arc height
hop_cooldown = 300  # delay between hops
last_hop_end_time = 0

# Game state variables
game_over = False
message = ""
play_again_button = pygame.Rect(300, 450, 200, 50)

# Function to start a new hop
def start_new_hop(target_x, target_y):
    global start_pos, end_pos, hop_start_time, is_hopping
    start_pos = pygame.Vector2(position)
    end_pos = pygame.Vector2(target_x, target_y)
    hop_start_time = pygame.time.get_ticks()
    is_hopping = True

# Reset the game to start over
def reset_game():
    global position, is_hopping, game_over, message
    position = start_pos.copy()
    is_hopping = False
    game_over = False
    message = ""
    pygame.mouse.set_visible(False)  # Hide the cursor again

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # If the game is over, check for button click
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    reset_game()

    # Get target (mouse) position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    fly_pos = (mouse_x - 15, mouse_y - 15)

    # If game over, stop the frog and fly movement
    if game_over:
        # Stop frog movement when game is over
        frog_rect.center = (int(position.x), int(position.y))
        pygame.mouse.set_visible(True)  # Show the mouse cursor after game over
    else:
        # Distance to target (fly)
        target_vec = pygame.Vector2(mouse_x, mouse_y)
        dist = target_vec.distance_to(position)

        # Start new hop if not already hopping and cooldown passed
        current_time = pygame.time.get_ticks()
        if not is_hopping and dist > 10 and current_time - last_hop_end_time > hop_cooldown:
            # Move a fixed step toward the target
            direction = (target_vec - position).normalize()
            step = direction * 50  # hop step distance
            new_target = position + step
            start_new_hop(new_target.x, new_target.y)

        # Smoothly animate hop
        if is_hopping:
            t = (current_time - hop_start_time) / hop_duration
            if t >= 1.0:
                position = end_pos
                is_hopping = False
                last_hop_end_time = current_time
            else:
                # Linear interpolation for x, y + vertical arc
                position = start_pos.lerp(end_pos, t)
                arc = math.sin(t * math.pi) * hop_height
                frog_rect.center = (int(position.x), int(position.y - arc))
        else:
            frog_rect.center = (int(position.x), int(position.y))

    # Detect if frog reached the fly
    target_vec = pygame.Vector2(mouse_x, mouse_y)
    if position.distance_to(target_vec) < 10:  # Close enough to fly
        game_over = True
        message = "You have been eaten!"
        play_again_button = pygame.Rect(300, 450, 200, 50)  # Play Again button

    # Drawing
    screen.blit(bg_img, (0, 0))  # Fill screen with background
    screen.blit(frog_img, frog_rect)  # Draw the frog
    screen.blit(fly_img, fly_pos)  # Draw the fly

    if game_over:
        # Display "You have been eaten!" message
        text_surface = font.render(message, True, (255, 0, 0))
        screen.blit(text_surface, (250, 300))

        # Draw the "Play Again" button
        pygame.draw.rect(screen, (0, 255, 0), play_again_button)
        button_text = font.render("Play Again", True, (0, 0, 0))
        screen.blit(button_text, (play_again_button.centerx - button_text.get_width() // 2, play_again_button.centery - button_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
