import numpy as np


class TicTacToe:
    def __init__(self):
        """Basic Tic Tac Toe

        Parameters
        ----------
        0 : int
            Blank Space
        1 : int
            Player One or X player
        2 : int
            Player Two or O Player

        Examples
        --------
        >>> func((0,0), 'X')
        TO DO XP
        """
        self.board = np.zeros((3, 3), dtype=int)
        self.Map = ['None', 'Player One', 'Player Two']

    def setMark(self, pos=(0, 0), mark='X'):
        try:
            if self.board[pos] == 0:
                if mark == 'X' or mark == '1' or mark == 'x':
                    self.board[pos] = 1
                    print "Position Valid"
                elif mark == 'O' or mark == '2' or mark == 'o':
                    self.board[pos] = 2
                    print "Position Valid"
                else:
                    print "Invalid Mark"

        except IndexError:
            print "Invalid position"

    def check(self):
        for i in [1, 2]:
            for ax in [0, 1]:
                hEv = np.any(np.apply_along_axis(lambda x: np.all(
                    np.equal(x, [i, i, i])), ax, self.board))
                if hEv:
                    return self.Map[i]
            diag = np.all(np.equal(self.board.diagonal(0), [i, i, i]))
            diag2 = np.all(np.equal(np.rot90(self.board).diagonal(0), [i, i, i]))

            if diag == True or diag2 == True:
                return self.Map[i]

        return self.Map[0]

    def getBoard(self):
        return self.board


if __name__ == "__main__":
    tic = TicTacToe()
    tic.setMark((0, 0))
    tic.setMark((1, 1))
    tic.setMark((2, 0))
    tic.setMark((1, 0),'O')
    print tic.getBoard()
    print tic.check()
