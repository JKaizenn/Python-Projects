'Jessen Forbush| Python Projects: #1 TicTacToe'

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
WINDOW_WIDTH = 720
PIXEL_WIDTH = WINDOW_WIDTH // 3
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))

# Set up clock for frame rate control
clock = pygame.time.Clock()

# Define colors
white = (255, 255, 255)

# Define the Tic Tac Toe board
board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

# Function to load icons
def load_icon(path, resolution):
    icon = pygame.image.load(path)
    return pygame.transform.scale(icon, resolution)

# Load icons for grid, X, and O
GRID = load_icon('icons/grid.png', (WINDOW_WIDTH, WINDOW_WIDTH))
ICON_X = load_icon('icons/x.png', [PIXEL_WIDTH // 3, PIXEL_WIDTH // 3])
ICON_O = load_icon('icons/o.png' , [PIXEL_WIDTH // 3, PIXEL_WIDTH // 3])

# Define players
Player_1 = 0
Player_2 = 1
player = Player_1

# Initialize game state variables
game_over = False
winner = None

# Countdown variables
countdown_time = 10  # Countdown time in seconds
countdown_started = False
last_tick_time = pygame.time.get_ticks()

# Function to handle player turns
def play_turn(current_player):
    global game_over
    if game_over:
        return False
    
    curr_coordinate = pygame.mouse.get_pos()
    col, row = curr_coordinate[0] // PIXEL_WIDTH, curr_coordinate[1] // PIXEL_WIDTH
    if pygame.mouse.get_pressed()[0] and board[row][col] is None:
        board[row][col] = current_player
        return True
    return False

# Function to draw icons on the screen
def draw_icons():
    for i, row in enumerate(board):
        for j, col in enumerate(board[i]):
            if board[i][j] == 0:
                screen.blit(ICON_X, [j * PIXEL_WIDTH, i * PIXEL_WIDTH])
            elif board[i][j] == 1:
                screen.blit(ICON_O, [j * PIXEL_WIDTH, i * PIXEL_WIDTH])

# Function to check if a row has equal icons
def has_equal_icons(elements, game_player):
    for element in elements:
        if element != game_player:
            return False
    return True

# Functions to check for winning conditions
def has_winning_row(game_player):
    return any(has_equal_icons(row, game_player) for row in board)

def has_winning_col(game_player):
    return any(has_equal_icons([board[i][j] for i in range(3)], game_player) for j in range(3))

def has_winning_diagonal(game_player):
    return (has_equal_icons([board[i][i] for i in range(3)], game_player) or
            has_equal_icons([board[i][2 - i] for i in range(3)], game_player))

def is_winner(game_player):
    return (has_winning_row(game_player) or
            has_winning_col(game_player) or
            has_winning_diagonal(game_player))

# Function to check for game end conditions
def check_victory():
    global game_over, winner, countdown_started

    if is_winner(Player_1):
        game_over = True
        winner = 'Player 1'
        countdown_started = True
    elif is_winner(Player_2):
        game_over = True
        winner = 'Player 2'
        countdown_started = True
    elif all(all(cell is not None for cell in row) for row in board):
        game_over = True
        winner = 'Draw'
        countdown_started = True

# Function to draw winner message and countdown
def draw_winner_message():
    global countdown_time, countdown_started, last_tick_time

    if winner:
        font = pygame.font.Font(None, 36)
        text = font.render(f'{winner} won!', True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.center = (WINDOW_WIDTH // 2, WINDOW_WIDTH // 2)
        screen.blit(text, textRect)

        if game_over and countdown_started and countdown_time > 0:
            current_tick_time = pygame.time.get_ticks()
            if current_tick_time - last_tick_time >= 1000:  # Decrease countdown every second (1000 milliseconds)
                countdown_time -= 1
                last_tick_time = current_tick_time

            countdown_text = font.render(f'Quitting in {countdown_time} seconds...', True, (255, 0, 0))
            countdownRect = countdown_text.get_rect()
            countdownRect.center = (WINDOW_WIDTH // 2, WINDOW_WIDTH // 2 + 50)
            screen.blit(countdown_text, countdownRect)  # Draw countdown text

        elif countdown_time <= 0:
            quit_game()

# Function to handle quitting the game
def quit_game():
    pygame.quit()
    sys.exit()

# Initialize font
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
            
    pygame.display.flip()
    screen.fill(white)
    screen.blit(GRID, (0, 0))
    
    if player == Player_1:
        pygame.display.set_caption("Player 1's Turn")
    else:
        pygame.display.set_caption("Player 2's Turn")
        
    if play_turn(player):
        player = 1 - player
        
    draw_icons()
    check_victory()
    draw_winner_message()

    if countdown_time <= 0:
        quit_game()
    
    pygame.display.update()
    clock.tick(60)
