import re
import random

def get_winner(board, empty = 0):
    """
    Returns the symbol of the winner, or value of 'empty' (def = 0) if there is no winner

      board: an iterable of iterables which contain the pieces at each position
      empty: the value in 'board' that corresponds to no player
    """
    players = set([i for j in board for i in j]) # Get all unique players
    players.discard(empty) # 0 is no player

    for p in players:

        for row in board: # Check row win
            for col in row: 
                if col is not p:
                    break # Break if one element not player p
            else:
                return p

        for i in range(len(board)): # Check col win
            for row in board: 
                if row[i] is not p:
                    break # Break if one element not player p
            else:
                return p

        for i in range(len(board)): # Check main diag win
            if board[i][i] is not p:
                break
        else:
            return p

        for i in range(len(board)): # Check main diag win
            if board[len(board)-1-i][i] is not p:
                break
        else:
            return p

    return empty

def print_board(board, symbol_dict = {0: ' ', 1: 'x', 2: 'o'}, square_names = True):
    """
    Prints the board with a given symbol key.

      board: an iterable of iterables which contain the pieces at each position
      symbol_dict: a dictionary with keys corresponding to all values in board and values as the characters to print
      square_names: if True displays the name of each row (numerical, starting at 1) 
                    and of each column (alphabetical, starting at A)
    """
    if square_names:
        print("  " + ' '.join( [str(chr(i)) for i in range(ord('A'), ord('A') + len(board))]))
        print(''.join(['--']*(len(board[0]) -1) + ['---']))

    for i, row in enumerate(board):
        if square_names:
            print(str(i+1) + "|", end = "")

        for j, col in enumerate(row):
            print(symbol_dict.get(col, str(col)), end="\n" if j is len(row)-1 else "|")
        
        if i is not len(board)-1:
            if square_names:
                print(" |", end = "")

            print(''.join(['-+']*(len(row) -1) + ['-']))

def parse_input(input_str, board, player, empty = 0):
    """
    Changes the board according to the player input.
    
      input_str: raw user input
      board: an iterable of iterables which contain the pieces at each position
      player: the identifier for the player who input this
      empty: the value in 'board' that corresponds to no player

    Returns 0 if the board could be changed
    Returns 1 if the input could not be parsed
    Returns 2 if the input could be parsed, but the row identifier is invalid
    Returns 3 if the input could be parsed, but the column identifier is invalid
    Returns 4 if the input could be parsed and is valid, but spot is occupied
    """
    rowID = re.search(r'\d+', input_str) # Finds first character sequence that is number
    colID = re.search(r'[a-zA-Z]', input_str) # Finds first character

    if rowID is None or colID is None: # Check there is a character and a number in input
        return 1

    row = int(rowID.group()) - 1 # Check row is a valid index for board
    if row < 0 or row >= len(board):
        return 2

    col = ord( colID.group()[0] )
    for start, end in zip(('a', 'A'), ('z', 'Z')): # Get distance from either 'a' or 'A'
        if col >= ord(start) and col <= ord(end):
            col = col - ord(start)
            break

    if col < 0 or col >= len(board[row]): # Check col is a valid index for board[row]
        return 3

    if board[row][col] is not empty:
        return 4

    board[row][col] = player
    return 0

def ai_play(board, computer, human, empty = 0):
    """
    Computer tries to fill board. Will attempt to win or block wins.

      board: an iterable of iterables which contain the pieces at each position
      computer: the value in 'board' that corresponds to the computer
      human: the value in 'board' that corresponds to the human
      empty: the value in 'board' that corresponds to no player

    Returns the play the computer makes
    """
    freeSpots = []

    for i in range(len(board)): # Find empty spots
        for j in range(len(board[i])):
            if board[i][j] is empty:
                freeSpots.append((i, j))

    for who_to_look_for in (computer, human): # Try to win first, then to block human
        for i, j in freeSpots:
            board[i][j] = who_to_look_for # Try this play

            if get_winner(board) == who_to_look_for: 
                board[i][j] = computer
                return get_cell_name(i,j) # AI won or player blocked! This is the play to do
            else:
                board[i][j] = empty # No immediate advantage, reset board

    randomSpot = random.choice(freeSpots) # Play a random empty cell
    board[randomSpot[0]][randomSpot[1]] = computer
    return get_cell_name(randomSpot[0],randomSpot[1])

def get_cell_name(row, col):
    return '' + str(chr(col + ord('A'))) + str(row+1)
    
def is_board_full(board, empty = 0):
    """
    Returns False if value of 'empty' found in board, True otherwise

      board: an iterable of iterables which contain the pieces at each position
      empty: the value in 'board' that corresponds to no player
    """
    for row in board:
        for col in row:
            if col is empty:
                return False

    return True

def play_match(lang, board_rows, board_cols, computer_starts):
    """
    Handles a single match of tic-tac-toe and returns the winner

      lang: language from where to draw the output messages
      board_rows: number of rows of the tic-tac-toe board
      board_cols: number of columns of the tic-tac-toe board
      computer: computer identifier
      human: human indentifier
      starter: identifier of whomever starts
      empty: identifier of unoccupied cells
    """
    computer = 1
    human = 2
    empty = 0
    symbol_dict = {0: ' ', computer if computer_starts else human: 'x', human if computer_starts else computer: 'o'}

    winner = empty
    board = [[0 for i in range(board_cols)] for j in range(board_rows)] # New board
    
    computer_turn = computer_starts

    while True:

        if computer_turn: # Plays computer
            played = ai_play(board, computer, human, empty)
            print(messages[lang][6].format(played))
        else: # Plays human
            error_mess_id = 1
            while error_mess_id is not 0:
                inp = input(messages[lang][7])
                error_mess_id = parse_input(inp, board, human, empty)
                if error_mess_id is not 0:
                    print(messages[lang][error_mess_id])

        
        computer_turn = not computer_turn

        print_board(board, symbol_dict, True)
        winner = get_winner(board, empty)

        if winner is not empty:
            return winner

        if is_board_full(board, empty):
            return empty
    
def play_game(games_to_win, lang, board_rows, board_cols):
    """
    Plays one game of tic-tac-toe. Plays matches until one player gets games_to_win

      lang: language from where to draw the output messages
      board_rows: number of rows of the tic-tac-toe board
      board_cols: number of columns of the tic-tac-toe board
      computer: computer identifier
      human: human indentifier
      starter: identifier of whomever starts
      empty: identifier of unoccupied cells
      symbolDict: a dictionary with keys corresponding to all values in board and values as the characters to print

    Returns name of winner of game
    """
    winner = -1
    score = [0, 0, 0] #Ties, Computer vs Human
    computer_starts = True # Who plays first next
    player_lang = [messages[lang][i] for i in (10,11,12)]
    
    while winner is -1:
        print(messages[lang][5].format(player_lang[1 + (not computer_starts)], 'x') ) # Who plays first

        winner_match = play_match(lang, 3, 3, computer_starts)
        
        score[winner_match] = score[winner_match]+1

        print(messages[lang][8].format( player_lang[winner_match], *score, games_to_win ))

        if winner_match is not 0 and score[winner_match] >= games_to_win:
            winner = winner_match                

        computer_starts = not computer_starts
    
    return player_lang[winner]
    
def test():
    # Check get_winner catches all wins
    assert get_winner([[1,2,1],[1,1,1],[2,1,2]]) == 1
    assert get_winner([[1,2,1],[0,2,1],[2,1,1]]) == 1
    assert get_winner([[1,2,1],[0,1,2],[2,1,1]]) == 1
    assert get_winner([[1,2,1],[0,1,1],[1,1,2]]) == 1

    # Check parse_input parses inputs correcly
    assert parse_input("  Czf  3 99 ", [[1,2,1],[1,1,1],[1,1,0]], 1) == 0
    assert parse_input("  azf  1 99 ", [[0,2,1],[1,1,1],[1,1,2]], 1) == 0
    assert parse_input("  1 ", [[1,2,1],[0,1,1],[1,1,2]], 1) == 1
    assert parse_input("  a ", [[1,2,1],[0,1,1],[1,1,2]], 1) == 1
    assert parse_input("  0a ", [[1,2,1],[0,1,1],[1,1,2]], 1) == 2
    assert parse_input("  4a ", [[1,2,1],[0,1,1],[1,1,2]], 1) == 2
    assert parse_input("  1D ", [[1,2,1],[0,1,1],[1,1,2]], 1) == 3
    assert parse_input("  1d ", [[1,2,1],[0,1,1],[1,1,2]], 1) == 3
    assert parse_input("  1b ", [[1,2,1],[3,1,1],[1,1,2]], 1) == 4
    board = [[0]]
    parse_input("1a", board, 1)
    assert board[0][0] is 1

    # Check ai_play wins and blocks when able
    # Computer wins
    board = [[2,0,1],[2,0,1],[0,0,0]]
    ai_play(board, 1, 2) 
    assert board[2][2] is 1
    # Computer blocks
    board = [[0,0,1],[0,0,1],[0,0,0]]
    ai_play(board, 2, 1) 
    assert board[2][2] is 2

    # Check is_board_full works
    assert is_board_full([[1,2], [4,1]])
    assert not is_board_full([[1,0], [4,1]])

messages = {
    "en_US":
        {
            1: "Sorry, input is not valid. It must contain a digit and a character. Please, try again.",
            2: "Sorry, input is not valid. Row specified is out of bounds of this board. Please, try again.",
            3: "Sorry, input is not valid. Column specified is out of bounds of this board. Please, try again.",
            4: "Sorry, input is not valid. That spot is already occupied. Please, try again.",
            5: "{} goes first and will use the '{}' pieces.",
            6: "Computer plays the {} cell.",
            7: "It's your turn! Please, write what cell you want to play (for example: 'A1'): ",
            8: "{} wins this match! Total score: Ties: {}.  Computer: {}.  Human: {}. The game continues until one of the players achieves {} wins.",
            9: "{} wins the game! Do you want to play again? ('y' for yes): ",
            10: "Nobody",
            11: "Computer",
            12: "Human",
        }
}

def main():
    lang = "en_US"
    games_to_win = 3
    board_size = 3
    cont = True

    while cont: # Repeat as many games as desired
        winner = play_game(games_to_win, lang, board_size, board_size)
        cont = input(messages[lang][9].format(winner)) == 'y'

if __name__ == "__main__":
    test() # Uncomment to unit-test most functions
    main()
