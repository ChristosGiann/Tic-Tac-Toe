import random

board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

def first_turn ():
    while True:
        answer = input("Θέλεις να ξεκινήσεις πρώτος; (ναι/όχι): ").strip().lower()
        if answer == "ναι":
            return True
        elif answer == "όχι":
            return False
        else:
            print("Παρακαλώ απάντησε με 'ναι' ή 'όχι'.")

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

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


def player_move(board):
    while True:
        try:
            move = input("Δώσε τη θέση σου ως 'γραμμή στήλη' (π.χ. 1 2): ")
            row, col = map(int, move.split())
            if row in [1,2,3] and col in [1,2,3]:
                if board[row-1][col-1] == " ":
                    board[row-1][col-1] = 'X'
                    break
                else:
                    print("Η θέση είναι ήδη κατειλημμένη.")
            else:
                print("Οι συντεταγμένες πρέπει να είναι από 1 έως 3.")
        except ValueError:
            print("Λανθασμένη μορφή εισόδου. Πρέπει να δώσεις δύο αριθμούς, π.χ. 1 3.")


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


def beginner_enemy_move(board):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty_cells:
        move = random.choice(empty_cells)
        board[move[0]][move[1]] = 'O'


def intermediate_move(board):
    win_pos = enemy_can_win(board, 'O')
    if win_pos:
        board[win_pos[0]][win_pos[1]] = 'O'
        return

    block_pos = enemy_can_win(board, 'X')
    if block_pos:
        board[block_pos[0]][block_pos[1]] = 'O'
        return

    beginner_enemy_move(board)


# --- Αρχή παιχνιδιού ---

difficulty = input("Επίλεξε δυσκολία: 1 για beginner, 2 για intermediate: ").strip()
while difficulty not in ("1", "2"):
    difficulty = input("Παρακαλώ δώσε 1 ή 2: ").strip()
if difficulty == "1":
    difficulty = "beginner"
else:
    difficulty = "intermediate"

player_turn = first_turn()

while True:
    print_board(board)
    if player_turn:
        player_move(board)
        if check_winner(board, 'X'):
            print_board(board)
            print("Ο παίκτης κέρδισε!")
            break
    else:
        print("Η σειρά του AI...")
        if difficulty == "beginner":
            beginner_enemy_move(board)
        elif difficulty == "intermediate":
            intermediate_move(board)

        if check_winner(board, 'O'):
            print_board(board)
            print("Το AI κέρδισε!")
            break

    if all(cell != " " for row in board for cell in row):
        print_board(board)
        print("Ισοπαλία!")
        break

    player_turn = not player_turn