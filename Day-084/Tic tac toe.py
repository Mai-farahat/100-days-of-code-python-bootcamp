import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    print("\n")
    print(f"  {board[0]} | {board[1]} | {board[2]} ")
    print(" ---|---|---")
    print(f"  {board[3]} | {board[4]} | {board[5]} ")
    print(" ---|---|---")
    print(f"  {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def print_position_guide():
    print("  Position guide:")
    print("  1 | 2 | 3")
    print(" ---|---|---")
    print("  4 | 5 | 6")
    print(" ---|---|---")
    print("  7 | 8 | 9\n")

def check_winner(board, player):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]             # diags
    ]
    return any(board[a] == board[b] == board[c] == player for a,b,c in wins)

def check_draw(board):
    return all(cell in ['X', 'O'] for cell in board)

def get_player_move(board, player):
    while True:
        try:
            move = int(input(f"  Player {player}, choose a position (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] not in ['X', 'O']:
                return move
            else:
                print("  ❌ Invalid move. Try again.")
        except ValueError:
            print("  ❌ Please enter a number between 1 and 9.")

def get_ai_move(board, ai_mark, human_mark):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    empty = [i for i, cell in enumerate(board) if cell not in ['X', 'O']]

    # Try to win
    for combo in wins:
        ai_cells = [i for i in combo if board[i] == ai_mark]
        empty_cells = [i for i in combo if i in empty]
        if len(ai_cells) == 2 and len(empty_cells) == 1:
            return empty_cells[0]

    # Block human
    for combo in wins:
        human_cells = [i for i in combo if board[i] == human_mark]
        empty_cells = [i for i in combo if i in empty]
        if len(human_cells) == 2 and len(empty_cells) == 1:
            return empty_cells[0]

    # Take center
    if 4 in empty:
        return 4

    # Take a corner
    corners = [i for i in [0, 2, 6, 8] if i in empty]
    if corners:
        return random.choice(corners)

    # Take any edge
    return random.choice(empty)

def play_game(mode):
    board = [str(i+1) for i in range(9)]
    current = 'X'

    if mode == '2':
        ai_mark = 'O'
        human_mark = 'X'

    while True:
        clear()
        print("=" * 30)
        print("        🎮 TIC TAC TOE")
        print("=" * 30)
        print_board(board)

        if mode == '2' and current == ai_mark:
            print(f"  🤖 AI ({ai_mark}) is thinking...\n")
            import time
            time.sleep(0.8)
            move = get_ai_move(board, ai_mark, human_mark)
        else:
            if mode == '2':
                print(f"  👤 Your turn ({human_mark})\n")
            print_position_guide()
            move = get_player_move(board, current)

        board[move] = current

        if check_winner(board, current):
            clear()
            print("=" * 30)
            print("        🎮 TIC TAC TOE")
            print("=" * 30)
            print_board(board)
            if mode == '2' and current == ai_mark:
                print("  🤖 The AI wins! Better luck next time.\n")
            elif mode == '2':
                print("  🏆 You win! Congratulations!\n")
            else:
                print(f"  🏆 Player {current} wins! Congratulations!\n")
            break

        if check_draw(board):
            clear()
            print("=" * 30)
            print("        🎮 TIC TAC TOE")
            print("=" * 30)
            print_board(board)
            print("  🤝 It's a draw! Well played both!\n")
            break

        current = 'O' if current == 'X' else 'X'

def main():
    while True:
        clear()
        print("=" * 30)
        print("        🎮 TIC TAC TOE")
        print("=" * 30)
        print("\n  Welcome! Choose game mode:\n")
        print("  1. Two Players (Human vs Human)")
        print("  2. Single Player (Human vs AI)")
        print("  Q. Quit\n")

        choice = input("  Enter your choice: ").strip().upper()

        if choice == '1':
            play_game('1')
        elif choice == '2':
            play_game('2')
        elif choice == 'Q':
            print("\n  Thanks for playing! Goodbye! 👋\n")
            break
        else:
            print("  Invalid choice. Try again.")
            continue

        again = input("  Play again? (Y/N): ").strip().upper()
        if again != 'Y':
            print("\n  Thanks for playing! Goodbye! 👋\n")
            break

if __name__ == "__main__":
    main()