class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range (9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]: 
            print('| ' + ' | '.join(row) + ' |')
    
    def print_board_rows():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3 )]

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        else:
            return False
        
    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count('   ')

def play(game, x_player, y_player, print_game = True):
    if print_game: 
        game.print_baord_nums()

    letter = 'X'

    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_plater.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square} ')
                game.print_board()
                print('')


            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            letter = 'O' if letter == 'X' else  'X'

