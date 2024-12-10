import pygame
import random
import math
 
# Initialize Pygame
pygame.init()
 
# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Traitor's Path")
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_GREEN = (34, 139, 34)
 
# Load assets
robot_img = pygame.image.load("src/Robot.png")
coin_img = pygame.image.load("src/Coin.png")
monster_img = pygame.image.load("src/Enemy.png")
door_img = pygame.image.load("src/door.png")
 
# Scale images
robot_img = pygame.transform.scale(robot_img, (50, 50))
coin_img = pygame.transform.scale(coin_img, (30, 30))
monster_img = pygame.transform.scale(monster_img, (60, 60))
door_img = pygame.transform.scale(door_img, (80, 80))
 
# Fonts
font = pygame.font.Font(None, 36)
 
# Function to display text on screen
def draw_text(text, font, color, x, y, center=False):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        render = font.render(line, True, color)
        if center:
            text_rect = render.get_rect(center=(x, y + i * 30))
            screen.blit(render, text_rect)
        else:
            screen.blit(render, (x, y + i * 30))
 
# Function to display the introduction screen
def show_intro():
    screen.fill(BLACK)
    intro_text = (
        "Welcome to The Traitor's Path.\n"
        "Level 1: Collect all the coins while avoiding the monster.\n"
        "Solve the riddle to unlock the door.\n\n"
        "Dante's Divine Comedy:\n"
        '"The last circle is surrounded by giants\n'
        'forming a human wall that rises to the eighth circle.\n'
        'Here, traitors are punished, submerged in ice.\n'
        'This is where you are headed."'
    )
    draw_text(intro_text, font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True)
    draw_text("Press ENTER to start", font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, center=True)
    pygame.display.flip()
 
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
 
# Function to initialize game objects
def init_game():
    robot = pygame.Rect(100, 100, 50, 50)
    coins = [pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50), 30, 30) for _ in range(8)]
    monster = pygame.Rect(random.randint(200, SCREEN_WIDTH - 200), random.randint(200, SCREEN_HEIGHT - 200), 60, 60)
    door = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT // 2, 80, 80)
    return robot, coins, monster, door, 0, False
 
# Function for the monster to chase the player
def move_monster(monster, player, speed):
    dx = player.x - monster.x
    dy = player.y - monster.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance > 0:
        monster.x += int(speed * dx / distance)
        monster.y += int(speed * dy / distance)
 
# Function to show a puzzle (philosophical question)
def show_puzzle():
    question = "What is the worst sin?\n1) Wrath\n2) Greed\n3) Betrayal\n4) Pride"
    correct_answer = "3"
    draw_text(question, font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True)
    pygame.display.flip()
 
    answer = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in "1234":
                    answer = event.unicode
                    return answer == correct_answer
 
# Function to display loss screen with fractals
def draw_fractal(surface, x, y, length, angle, depth):
    if depth == 0:
        return
    x2 = x + length * math.cos(math.radians(angle))
    y2 = y - length * math.sin(math.radians(angle))
    pygame.draw.line(surface, WHITE, (x, y), (x2, y2), 2)
    draw_fractal(surface, x2, y2, length * 0.7, angle - 30, depth - 1)
    draw_fractal(surface, x2, y2, length * 0.7, angle + 30, depth - 1)
 
def show_loss_screen(message):
    screen.fill(BLACK)
    draw_fractal(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 100, -90, 5)
    draw_text(message, font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    draw_text("Press 'R' to retry", font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, center=True)
    pygame.display.flip()
 
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False
 
# Function to draw devil victory screen
def show_victory_screen():
    screen.fill(BLACK)
 
    # Draw devil-like geometric shapes
    pygame.draw.polygon(screen, RED, [(400, 300), (350, 400), (450, 400)])
    pygame.draw.circle(screen, RED, (400, 250), 50)
    pygame.draw.line(screen, RED, (370, 230), (380, 210), 5)  # Left horn
    pygame.draw.line(screen, RED, (430, 230), (420, 210), 5)  # Right horn
 
    draw_text("Yes continue over here.\nYou little traitor!", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    pygame.display.flip()
    pygame.time.wait(5000)
 
# Function to run the second level
def second_level():
    robot = pygame.Rect(50, SCREEN_HEIGHT // 2 - 25, 50, 50)
    path_y = SCREEN_HEIGHT // 2 - 50
    path_height = 100
    running = True
    clock = pygame.time.Clock()
 
    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, (0, path_y, SCREEN_WIDTH, path_height))
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            robot.x += 5
 
        # Constrain movement to the path
        if robot.y < path_y:
            robot.y = path_y
        if robot.y + robot.height > path_y + path_height:
            robot.y = path_y + path_height - robot.height
 
        if robot.x > SCREEN_WIDTH:
            screen.fill(BLACK)
            draw_text(
                "Lucifer is immersed in ice up to his waist,\n crying and drooling. He flaps his wings as if trying to escape,\n  producing a wind that freezes the entire Cocytus.\n Each mouth has a famous traitor, with Brutus and Cassius\n in the left and right mouths respectively. \n In the center is Judas.\n The worst of tortures is applied to him,\n  his head is gnawed by Lucifer's mouth.\n What is seen here is a perversion of the trinity.\n You are heading there.\n What you have done is profane,\n  your conscience will not go unpunished during \n your eternal punishment.\nIn this game, you cannot win.\nYou lose and go to the last circle of hell,\nwhere you belong.\nEnd!!!!!!!",
                font,
                RED,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 40,
                center=True,
            )
            pygame.display.flip()
            pygame.time.wait(22000)
            pygame.quit()
            exit()
 
        screen.blit(robot_img, robot.topleft)
        pygame.display.flip()
        clock.tick(60)
 
# Main function
def main():
    clock = pygame.time.Clock()
 
    robot, coins, monster, door, score, game_over = init_game()
    puzzle_solved = False
    monster_speed = 2
 
    show_intro()
 
    running = True
    while running:
        screen.fill(DARK_GREEN)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        keys = pygame.key.get_pressed()
 
        if not game_over:
            if not puzzle_solved:
                 if show_puzzle():
                       puzzle_solved = True  # Actualizar el estado del rompecabezas si la respuesta es correcta
                 else:
                     show_loss_screen("You failed the question! Betrayal is the worst sin!")
                     robot, coins, monster, door, score, game_over = init_game()
                     continue
 
 
            # Movement
            if keys[pygame.K_UP]:
                robot.y -= 5
            if keys[pygame.K_DOWN]:
                robot.y += 5
            if keys[pygame.K_LEFT]:
                robot.x -= 5
            if keys[pygame.K_RIGHT]:
                robot.x += 5
 
            # Constrain movement
            robot.x = max(0, min(SCREEN_WIDTH - robot.width, robot.x))
            robot.y = max(0, min(SCREEN_HEIGHT - robot.height, robot.y))
 
            # Monster movement
            move_monster(monster, robot, monster_speed)
 
            # Collision detection
            coins = [coin for coin in coins if not robot.colliderect(coin)]
            score = 8 - len(coins)
 
            if robot.colliderect(monster):
                show_loss_screen("The monster caught you! Game Over.")
                robot, coins, monster, door, score, game_over = init_game()
                puzzle_solved = False
                continue
 
            if score == 8 and robot.colliderect(door) and puzzle_solved:
                show_victory_screen()
                second_level()
                running = False
 
        # Draw elements
        for coin in coins:
            screen.blit(coin_img, coin.topleft)
        screen.blit(robot_img, robot.topleft)
        screen.blit(monster_img, monster.topleft)
        screen.blit(door_img, door.topleft)
 
        # Score and puzzle status
        draw_text(f"Coins: {score}/8", font, WHITE, 10, 10)
        if not puzzle_solved:
            draw_text("Solve the puzzle to unlock the door!", font, RED, 10, 40)
 
        pygame.display.flip()
        clock.tick(60)
 
    pygame.quit()
 
# Run the game
if __name__ == "__main__":
    main()