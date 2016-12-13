class Peice(object):

    def __init__(self,player,name=""):
        self.player_number = player.number
        self.team_color = player.team_color
        self.direction = player.direction
        self.has_moved = False
        self.name = name
        self.can_passant = False

    def getName(self):
        return self.name

    def getFullName(self):
        return 'Peice'

    def getScore(self):
        return 0

    def getAttacks(self,board,row,col):
        moves = self.getPeiceMoves(board,row,col)
        return [move for move in moves if board.getPeice(move[0],move[1])]

    def getPossibleMoves(self,board,row,col):
        possible_moves = self.getPeiceMoves(board,row,col)
        possible_boards = [board.generateSuccessor((row,col),move) for move in possible_moves]
        legal_moves = []
        for i in range(len(possible_boards)):
            if not possible_boards[i].isInCheck(self.player_number):
                legal_moves.append(possible_moves[i])
        return legal_moves

    def canMove(self,board,row,col):
        if row < 0:
            return False
        if col < 0:
            return False
        if row > board.height - 1:
            return False
        if col > board.width - 1:
            return False
        if board.getPeice(row,col):
            return False
        return True

    def canAttack(self,board,row,col):
        if row < 0:
            return False
        if col < 0:
            return False
        if row > board.height - 1:
            return False
        if col > board.width - 1:
            return False
        peice = board.getPeice(row,col)
        if peice:
            return peice.player_number != self.player_number
        return False

class Pawn(Peice):
    def getName(self):
        return 'P'

    def getFullName(self):
        return 'Pawn'

    def getScore(self):
        return 1

    def getPeiceMoves(self,board,row,col):
        possible_moves = []
        if self.canMove(board,row + self.direction, col):
            possible_moves.append((row + self.direction, col))
            if not self.has_moved:
                if self.canMove(board,row + self.direction * 2, col):
                    possible_moves.append((row + self.direction * 2, col))
        if self.canAttack(board,row + self.direction, col + 1):
            possible_moves.append((row + self.direction, col + 1))
        if self.canAttack(board, row + self.direction, col - 1):
            possible_moves.append((row + self.direction, col - 1))
        if self.canAttack(board, row, col -1):
            if board.getPeice(row,col-1).can_passant:
                possible_moves.append(('PL','PL'))
        if self.canAttack(board,row, col +1):
            if board.getPeice(row,col+1).can_passant:
                possible_moves.append(('PR','PR'))
        return possible_moves

class Rook(Peice):
    def getName(self):
        return 'R'

    def getFullName(self):
        return 'Rook'

    def getScore(self):
        return 5

    def getPeiceMoves(self,board,row,col):
        possible_moves = []
        move_row = row - 1
        move_col = col
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row = move_row - 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row + 1
        move_col = col
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row = move_row + 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row
        move_col = col + 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_col = move_col + 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row
        move_col = col - 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_col = move_col - 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        return possible_moves

class Knight(Peice):
    def getName(self):
        return 'N'

    def getFullName(self):
        return 'Knight'

    def getScore(self):
        return 3

    def getPeiceMoves(self,board,row,col):
        possible_spots = [
            (row+2,col+1),
            (row+2,col-1),
            (row+1,col+2),
            (row+1,col-2),
            (row-1,col+2),
            (row-1,col-2),
            (row-2,col+1),
            (row-2,col-1)
        ]
        moves = [move for move in possible_spots if self.canMove(board,move[0],move[1])]
        attacks = [move for move in possible_spots if self.canAttack(board,move[0],move[1])]
        return moves + attacks

class Bishop(Peice):
    def getName(self):
        return 'B'

    def getFullName(self):
        return 'Bishop'

    def getScore(self):
        return 3

    def getPeiceMoves(self,board,row,col):
        possible_moves = []
        move_row = row + 1
        move_col = col + 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row += 1
            move_col += 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row + 1
        move_col = col - 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row = move_row + 1
            move_col = move_col - 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row - 1
        move_col = col - 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row = move_row - 1
            move_col = move_col - 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row - 1
        move_col = col + 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row -= 1
            move_col += 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        return possible_moves

class Queen(Peice):
    def getName(self):
        return 'Q'

    def getFullName(self):
        return 'Queen'

    def getScore(self):
        return 9

    def getPeiceMoves(self,board,row,col):
        possible_moves = []
        move_row = row + 1
        move_col = col + 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row += 1
            move_col += 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row + 1
        move_col = col
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row += 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row + 1
        move_col = col - 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row += 1
            move_col -= 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row
        move_col = col + 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_col += 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row
        move_col = col - 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_col -= 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row - 1
        move_col = col + 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row -= 1
            move_col += 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row - 1
        move_col = col
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row -= 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        move_row = row - 1
        move_col = col - 1
        while self.canMove(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
            move_row -= 1
            move_col -= 1
        if self.canAttack(board,move_row,move_col):
            possible_moves.append((move_row,move_col))
        return possible_moves


class King(Peice):
    def getName(self):
        return 'K'

    def getFullName(self):
        return 'King'

    def getPeiceMoves(self,board,row,col):
        possible_moves = [
            (row+1,col+1),
            (row+1,col),
            (row+1,col-1),
            (row,col+1),
            (row,col-1),
            (row-1,col+1),
            (row-1,col),
            (row-1,col-1)
        ]
        moves = [move for move in possible_moves if self.canMove(board,move[0],move[1])]
        attacks = [move for move in possible_moves if self.canAttack(board,move[0],move[1])]
        possible_moves = moves + attacks

        return possible_moves
