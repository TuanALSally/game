import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROBOT_SIZE = 60
COIN_SIZE = 35
ENEMY_SIZE = 50
FPS = 30
INITIAL_TIMER = 60  # Initial timer in seconds
COINS_TO_COLLECT = 5  # Number of coins to collect to advance to the next stage
MAX_STAGES = 80  # Maximum number of stages

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 190)  # Set to black for the text
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)  # Darker green for restart button
DARKER_GREEN = (0, 150, 0)  # Darker green for start button
RED = (255, 0, 0)

# List of colors for each stage
STAGE_COLORS = [
    (200, 0, 0),    # Stage 1: Red
    (0, 200, 0),    # Stage 2: Green
    (0, 0, 200),    # Stage 3: Blue
    (200, 200, 0),  # Stage 4: Yellow
    (200, 0, 200),  # Stage 5: Magenta
    (0, 200, 200),  # Stage 6: Cyan
    (200, 165, 0),  # Stage 7: Orange
    (200, 0, 128),  # Stage 8: Purple
]

# Load images
robot_image = pygame.image.load('src/Robot.png')
robot_image = pygame.transform.scale(robot_image, (ROBOT_SIZE, ROBOT_SIZE))
coin_image = pygame.image.load('src/Coin.png')
coin_image = pygame.transform.scale(coin_image, (COIN_SIZE, COIN_SIZE))
enemy_image = pygame.image.load('src/Enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))

# Load sounds
coin_sound = pygame.mixer.Sound('src/vs.wav')

# Classes
class Robot:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Coin:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.rect = coin_image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH - COIN_SIZE), random.randint(0, SCREEN_HEIGHT - COIN_SIZE)))

class Enemy:
    def __init__(self, speed=2, vertical=False):
        self.rect = enemy_image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)))
        self.direction_x = random.choice([-1, 1])  # Horizontal direction
        self.direction_y = random.choice([-1, 1]) if vertical else 0  # Vertical direction
        self.speed = speed

    def move(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        # Bounce off the left and right edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction_x *= -1
        # Bounce off the top and bottom edges
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction_y *= -1

# Functions
def draw_rounded_button(surface, text, position, font, color, radius=10):
    # Create rounded rectangle surface with smaller size
    button_surface = pygame.Surface((200, 40), pygame.SRCALPHA)  # Smaller button size
    pygame.draw.rect(button_surface, color, (0, 0, 200, 40), border_radius=radius)
    # Render text
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(100, 20))  # Center the text
    button_surface.blit(text_surface, text_rect)
    # Draw button on the main surface
    surface.blit(button_surface, position)

def draw_window(robot, coin, enemies, score, timer, stage, coins_collected):
    # Set background color based on the stage
    background_color = STAGE_COLORS[(stage - 1) % len(STAGE_COLORS)]
    window.fill(background_color)
    window.blit(robot.image, robot.rect.topleft)
    window.blit(coin_image, coin.rect.topleft)
    for enemy in enemies:
        window.blit(enemy_image, enemy.rect.topleft)
    # Display score, timer, stage, and coins collected as plain text
    score_text = font.render(f'Coins: {score} | Time: {timer} | Stage: {stage} | Coins Collected: {coins_collected}/{COINS_TO_COLLECT}', True, WHITE)
    window.blit(score_text, (10, 10))  # Draw the score text directly on the window
    pygame.display.update()

def show_game_over(score):
    window.fill(BLACK)
    game_over_text = font.render('GAME OVER!', True, WHITE)  # Keep color as WHITE
    score_text = font.render(f'Final Score: {score}', True, WHITE)  # Keep color as WHITE
    window.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    window.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    # Draw Restart and Exit buttons with updated colors
    draw_rounded_button(window, 'Restart', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60), font, DARK_GREEN)  # Darker green
    draw_rounded_button(window, 'Exit', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110), font, RED)  # Red
    pygame.display.update()
    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (SCREEN_WIDTH // 2 - 100 < mouse_pos[0] < SCREEN_WIDTH // 2 + 100):
                    if (SCREEN_HEIGHT // 2 + 60 < mouse_pos[1] < SCREEN_HEIGHT // 2 + 100):
                        waiting = False  # Restart the game
                        main()  # Call the main function to restart the game
                    elif (SCREEN_HEIGHT // 2 + 110 < mouse_pos[1] < SCREEN_HEIGHT // 2 + 150):
                        pygame.quit()  # Exit the game
                        exit()

def show_start_menu():
    run = True
    while run:
        window.fill(BLACK)
        title_text = font.render('COIN COLLECTOR', True, WHITE)  # Keep color as WHITE
        start_text = font.render('Start Now', True, WHITE)  # Keep color as WHITE
        window.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        draw_rounded_button(window, 'Start Now', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), font, DARKER_GREEN)  # Changed to DARKER_GREEN
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (SCREEN_WIDTH // 2 - 100 < mouse_pos[0] < SCREEN_WIDTH // 2 + 100 and
                    SCREEN_HEIGHT // 2 < mouse_pos[1] < SCREEN_HEIGHT // 2 + 40):  # Adjusted button size
                    run = False  # Start the game

# Main function
def main():
    global window, font
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Coin Collector")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 30, bold=True)  # Set bold to 

    # Show start menu
    show_start_menu()

    # Initialize game objects
    robot = Robot(robot_image)
    coin = Coin()
    enemies = [Enemy(speed=6, vertical=True), Enemy(speed=6, vertical=False)]  # Start with two enemies
    score = 0
    coins_collected = 0
    stage = 1
    timer = INITIAL_TIMER
    last_stage_time = pygame.time.get_ticks()
    run = True
    while run:
        clock.tick(FPS)
        # Update timer (decrease time per stage)
        current_time = pygame.time.get_ticks()
        timer = INITIAL_TIMER - (current_time // 1000) + stage * 2  # Decrease time per stage (2 seconds less for each stage)
        if timer <= 0:
            show_game_over(score)
            break

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Robot movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            robot.move(-8, 0)  # Increased speed from -5 to -8
        if keys[pygame.K_RIGHT]:
            robot.move(8, 0)   # Increased speed from 5 to 8
        if keys[pygame.K_UP]:
            robot.move(0, -8)  # Increased speed from -5 to -8
        if keys[pygame.K_DOWN]:
            robot.move(0, 8)   # Increased speed from 5 to 8

        # Coin collection
        if robot.rect.colliderect(coin.rect):
            coins_collected += 1
            score += 1
            coin_sound.play()
            coin.respawn()

        # Enemy movement and collision
        for enemy in enemies:
            enemy.move()
            if robot.rect.colliderect(enemy.rect):
                show_game_over(score)
                run = False

        # Stage progression
        if coins_collected >= COINS_TO_COLLECT:
            if stage < MAX_STAGES:
                stage += 1
                coins_collected = 0  # Reset coins collected for the next stage
                # Increase enemy speed and add more enemies
                enemies.append(Enemy(speed=3 + stage, vertical=True))  # Increase speed based on stage
                enemies.append(Enemy(speed=3 + stage, vertical=False))  # Add another enemy for each stage
                coin.respawn()  # Respawn the coin in a new location

        draw_window(robot, coin, enemies, score, timer, stage, coins_collected)

    pygame.quit()

if __name__ == "__main__":
    main()
    
    
 # Name of the game: COIN COLLECTOR
# Mode of the project: Course project
# Programming language used: Python
# Characters: Monster and a Robot
# How many levels: 80


# Description
# The main characters in this game are A monster and a robot: the robot should collect coins without getting touched by the monster. If the robot gets touched by the monster, it has to start the game again.
# There are 20 stages, and when you collect 5 coins in each stage, you move on to the next stage, and each stage gets harder and harder, and every stage has a color, and monsters will keep adding in every stage.
# When you level up near the total coins, there is an option called stages. You can see your current stage from that, and there is a timer. You have to pass many stages before the time runs out, and you can see the total number of coins you have collected.
# In the total coin option.


# How To Play
# Objective
# •	Collect a certain number of coins (5 coins) to advance to the next stage.
# •	Avoid colliding with enemies that move around the screen.
# •	Keep an eye on the timer; if it runs out, the game is over.
# Controls
# •	Arrow Keys: Use the arrow keys on your keyboard to move the robot:
# •	Left Arrow: Move left
# •	Right Arrow: Move right
# •	Up Arrow: Move up
# •	Down Arrow: Move down
# Game Mechanics
# 1.	Start Menu: When the game starts, you will see a title screen with a "Start Now" button. Click this button to begin the game.
# 2.	Collecting Coins: Move the robot to collide with the coin. Each time you collect a coin, your score increases, and the coin will respawn in a new random location.
# 3.	Enemies: Enemies will move around the screen. If you collide with an enemy, the game will end.
# 4.	Timer: You have a limited amount of time to complete each stage. The timer decreases as you progress through the stages.
# 5.	Stages: After collecting 5 coins, you will advance to the next stage. With each new stage, the game becomes more challenging as enemies increase in number and speed.
# Game Over
# •	If you run out of time or collide with an enemy, the game will display a "GAME OVER!" message along with your final score.
# •	You will have the option to restart the game or exit.
# Restart/Exit
# •	After a game over, you can click the "Restart" button to play again or the "Exit" button to close the game.
# Tips
# •	Try to avoid the enemies while maneuvering towards the coins.
# •	Plan your moves to collect coins efficiently while keeping an eye on the enemies' positions.

 

