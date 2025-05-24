import pygame
import sys
import random

# Αρχικοποίηση Pygame
pygame.init()

# Ρυθμίσεις παραθύρου
WIDTH, HEIGHT = 300, 400 
LINE_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 50)

board = [[" " for _ in range(3)] for _ in range(3)]

def draw_text(text, x, y, font_obj=font, color=TEXT_COLOR):
    img = font_obj.render(text, True, color)
    rect = img.get_rect(center=(x,y))
    screen.blit(img, rect)

# Κουμπιά
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = BUTTON_COLOR

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        draw_text(self.text, self.rect.centerx, self.rect.centery)

    def is_hover(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)

    def update(self):
        self.color = BUTTON_HOVER_COLOR if self.is_hover() else BUTTON_COLOR

# Οθόνη μενού για επιλογή δυσκολίας και γύρων
def show_menu():
    beginner_btn = Button(50, 50, 200, 40, "Beginner")
    intermediate_btn = Button(50, 110, 200, 40, "Intermediate")

    player_first_btn = Button(50, 200, 200, 40, "Παίξε πρώτος")
    ai_first_btn = Button(50, 260, 200, 40, "Παίξε δεύτερος")

    difficulty = None
    player_starts = None

    while True:
        screen.fill(BG_COLOR)
        draw_text("Επέλεξε δυσκολία:", WIDTH//2, 20)
        draw_text("Ποιος θα ξεκινήσει;", WIDTH//2, 180)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if beginner_btn.rect.collidepoint(event.pos):
                    difficulty = "beginner"
                elif intermediate_btn.rect.collidepoint(event.pos):
                    difficulty = "intermediate"
                elif player_first_btn.rect.collidepoint(event.pos):
                    player_starts = True
                elif ai_first_btn.rect.collidepoint(event.pos):
                    player_starts = False
                if difficulty is not None and player_starts is not None:
                    return difficulty, player_starts

        for btn in [beginner_btn, intermediate_btn, player_first_btn, ai_first_btn]:
            btn.update()
            btn.draw()

        pygame.display.update()

def check_winner(board, symbol):
    for row in board:
        if all(cell == symbol for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)


def beginner_enemy_move(board):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty_cells:
        move = random.choice(empty_cells)
        board[move[0]][move[1]] = 'O'


def intermediate_enemy_move(board):
    win_pos = enemy_can_win(board, 'O')
    if win_pos:
        board[win_pos[0]][win_pos[1]] = 'O'
        return
    block_pos = enemy_can_win(board, 'X')
    if block_pos:
        board[block_pos[0]][block_pos[1]] = 'O'
        return
    beginner_enemy_move(board)

def enemy_can_win(board, symbol):
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = symbol
                if check_winner(board, symbol):
                    board[r][c] = " "
                    return (r, c)
                board[r][c] = " "
    return None

# Σχεδίαση ταμπλό
def draw_board():
    screen.fill(BG_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (100, 0), (100, 300), 3)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 300), 3)
    pygame.draw.line(screen, LINE_COLOR, (0, 100), (300, 100), 3)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (300, 200), 3)

    for r in range(3):
        for c in range(3):
            pos_x = c * 100 + 50
            pos_y = r * 100 + 50
            if board[r][c] == 'X':
                draw_text('X', pos_x, pos_y, large_font, (200, 30, 30))
            elif board[r][c] == 'O':
                draw_text('O', pos_x, pos_y, large_font, (30, 30, 200))


def get_cell_from_pos(pos):
    x, y = pos
    if x > 300 or y > 300:
        return None
    col = x // 100
    row = y // 100
    return (row, col)


def player_move_pygame(pos):
    cell = get_cell_from_pos(pos)
    if cell:
        r, c = cell
        if board[r][c] == " ":
            board[r][c] = 'X'
            return True
    return False


def game_over_screen(winner=None):
    screen.fill(BG_COLOR)
    if winner == 'X':
        draw_text("Κέρδισες!", WIDTH//2, HEIGHT//2, large_font, (0, 150, 0))
    elif winner == 'O':
        draw_text("Έχασες!", WIDTH//2, HEIGHT//2, large_font, (150, 0, 0))
    else:
        draw_text("Ισοπαλία!", WIDTH//2, HEIGHT//2, large_font, (100, 100, 100))
    draw_text("Πατήστε για έξοδο", WIDTH//2, HEIGHT//2 + 50, font)
    pygame.display.update()

    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

difficulty, player_turn = show_menu()

# Ρύθμιση μεγέθους παραθύρου για το παιχνίδι
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
running = True
game_over = False
winner = None

while running:
    draw_board()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            if player_move_pygame(event.pos):
                if check_winner(board, 'X'):
                    winner = 'X'
                    game_over = True
                elif board_full(board):
                    winner = None
                    game_over = True
                else:
                    player_turn = False

    if not player_turn and not game_over:
        pygame.time.wait(300)
        if difficulty == "beginner":
            beginner_enemy_move(board)
        else:
            intermediate_enemy_move(board)
        if check_winner(board, 'O'):
            winner = 'O'
            game_over = True
        elif board_full(board):
            winner = None
            game_over = True
        else:
            player_turn = True

    if game_over:
        game_over_screen(winner)
        running = False

pygame.quit()
sys.exit()
