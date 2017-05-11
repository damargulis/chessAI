from __future__ import print_function
from peices import *
import copy

class Board(object):

    white_cell = "  "
    black_cell = "XX"

    def __init__(self,players,height=8,width=8):
        board = []
        for i in range(height):
            board.append([None] * width)
        self.board = board
        self.height = height
        self.width = width
        self.initializePeices(players)

    def initializePeices(self,players):
        [p1,p2] = players
        self.board[7][0] = Rook(p1)
        self.board[7][1] = Knight(p1)
        self.board[7][2] = Bishop(p1)
        self.board[7][3] = Queen(p1)
        self.board[7][4] = King(p1)
        self.board[7][5] = Bishop(p1)
        self.board[7][6] = Knight(p1)
        self.board[7][7] = Rook(p1)
        for i in range(self.width):
            self.board[6][i] = Pawn(p1)
            self.board[1][i] = Pawn(p2)
        self.board[0][0] = Rook(p2)
        self.board[0][1] = Knight(p2)
        self.board[0][2] = Bishop(p2)
        self.board[0][3] = Queen(p2)
        self.board[0][4] = King(p2)
        self.board[0][5] = Bishop(p2)
        self.board[0][6] = Knight(p2)
        self.board[0][7] = Rook(p2)

    def getPeice(self,row,col):
        if row < 0 or row > self.height - 1 or col < 0 or col > self.width:
            return None
        return self.board[row][col]

    def getAllMoves(self, player_number):
        all_possible_moves = []
        for i,row in enumerate(self.board):
            for j,peice in enumerate(row):
                if peice and peice.player_number == player_number:
                    moves = peice.getPossibleMoves(self,i,j)
                    all_possible_moves += [((i,j),move) for move in moves]
                    if isinstance(peice, King) and not peice.has_moved:
                        kingsRook = row[7]
                        queensRook = row[0]
                        if not self.isInCheck(player_number):
                            if kingsRook and isinstance(kingsRook, Rook) and not kingsRook.has_moved:
                                if row[6] == None and row[5] == None:
                                    check1 = self.generateSuccessor((i,j),(i,5))
                                    check2 = self.generateSuccessor((i,j),(i,6))
                                    if not check1.isInCheck(player_number) and not check2.isInCheck(player_number):
                                        all_possible_moves.append(("KC","KC"))
                            if queensRook and isinstance(queensRook, Rook) and not queensRook.has_moved:
                                if row[3] == None and row[2] == None and row[1] == None:
                                    check1 = self.generateSuccessor((i,j),(i,3))
                                    check2 = self.generateSuccessor((i,j),(i,2))
                                    check3 = self.generateSuccessor((i,j),(i,1))
                                    if not check1.isInCheck(player_number) and not check2.isInCheck(player_number) and not check3.isInCheck(player_number):
                                        all_possible_moves.append(("QC","QC"))


        return all_possible_moves

    def getAllAttacks(self, player_number):
        all_possible_attacks = []
        for i,row in enumerate(self.board):
            for j,peice in enumerate(row):
                if peice and peice.player_number == player_number:
                    attacks = peice.getAttacks(self,i,j)
                    all_possible_attacks += [((i,j),move) for move in attacks]
        return all_possible_attacks

    def getPromotions(self,player):

        goal_row = 0 if player.direction == - 1 else self.height - 1
        row = self.board[goal_row]
        promotions = []
        for j,peice in enumerate(row):
            if isinstance(peice, Pawn) and peice.player_number == player.number:
                promotions.append((peice,goal_row,j))
        return promotions

    def promote(self,player,row,col,promotion):
        if promotion == 'Q':
            self.board[row][col] = Queen(player)
            return True
        elif promotion == 'R':
            self.board[row][col] = Rook(player)
            return True
        elif promotion == 'K':
            self.board[row][col] = Knight(player)
            return True
        elif promotion == 'B':
            self.board[row][col] = Bishop(player)
            return True
        else:
            return False

    def clearPassant(self, number):
        for row in self.board:
            for peice in row:
                if peice and peice.player_number == number:
                    peice.can_passant = False

    def makeMove(self,move,player_direction):
        if move[0] == 'QC' or move[0] == 'KC':
            self.castle(move,player_direction)
        else:
            from_spot, to_spot = move[0], move[1]
            if to_spot[0] == 'PR' or to_spot[0] == 'PL':
                self.en_passant(to_spot[0],from_spot,player_direction)
            else:
                self.movePeice(from_spot[0],from_spot[1],to_spot[0],to_spot[1])

    def movePeice(self,from_row,from_col,to_row,to_col):
        peice = self.board[from_row][from_col]
        if peice:
            if to_row == 'PR' or to_row == 'PL':
                return self.en_passant(to_row,(from_row,from_col),peice.direction)
            peice.has_moved = True
            self.board[to_row][to_col] = peice
            self.board[from_row][from_col] = None
            self.clearPassant(peice.player_number)
            if isinstance(peice, Pawn):
                if abs(from_row - to_row) == 2:
                    peice.can_passant = True

    def castle(self,castle_type,direction):
        home_row = 0 if direction == 1 else self.height - 1
        row = self.board[home_row]
        if castle_type == 'KC':
            row[6], row[4] = row[4], None
            row[5], row[7] = row[7], None
        elif castle_type == 'QC':
            row[2], row[4] = row[4], None
            row[3], row[0] = row[0], None

    def en_passant(self,passant_type,spot,player_direction):
        if passant_type == 'PR':
            self.board[spot[0]+player_direction][spot[1]+1] = self.board[spot[0]][spot[1]]
            self.board[spot[0]][spot[1]] = None
            self.board[spot[0]][spot[1]+1] = None
        elif passant_type == 'PL':
            self.board[spot[0]+player_direction][spot[1]-1] = self.board[spot[0]][spot[1]]
            self.board[spot[0]][spot[1]] = None
            self.board[spot[0]][spot[1]-1] = None


    def generateSuccessor(self,from_spot,to_spot):
        new_board = copy.deepcopy(self)
        new_board.movePeice(from_spot[0],from_spot[1],to_spot[0],to_spot[1])
        return new_board

    def generateSuccessorFromMove(self,move,player_direction):
        new_board = copy.deepcopy(self)
        new_board.makeMove(move,player_direction)
        return new_board

    def isInCheck(self,player_number):
        for i,row in enumerate(self.board):
            for j,peice in enumerate(row):
                if peice and not peice.player_number == player_number:
                    attacks = peice.getAttacks(self,i,j)
                    for attack in attacks:
                        attacked_peice = self.board[attack[0]][attack[1]]
                        if isinstance(attacked_peice,King) and attacked_peice.player_number == player_number:
                            return True
        return False

    def isCheckmated(self,player_number):
        for i,row in enumerate(self.board):
            for j,peice in enumerate(row):
                if peice and peice.player_number == player_number:
                    moves = peice.getPossibleMoves(self,i,j)
                    if len(moves) > 0:
                        return False
        return True

    def isDraw(self):
        total_peices = [peice for row in self.board for peice in row if peice != None]
        if len(total_peices) == 2:
            return True
        elif len(total_peices) == 3:
            extra_peice = [peice for peice in total_peices if not isinstance(peice, King)][0]
            if isinstance(extra_peice, Knight):
                return True
            elif isinstance(extra_peice, Bishop):
                return True
            else:
                return False
        else:
            extra_peices = [peice for peice in total_peices if not isinstance(peice, King)]
            not_bishops = [peice for piece in total_peices if not isinstance(peice, Bishop)]
            if len(not_bishops) != 0:
                return False
            else:
                colors = []
                for i,row in enumerate(self.board):
                    for j,peice in enumerate(row):
                        if(isinstance(peice, Bishop)):
                            colors.append((i + j) % 2)
                        elif (isinstance(peice, King)):
                            continue
                        else:
                            return False
                if(len(set(colors)) == 1):
                    return True
                else:
                    return False

    def isStalemated(self,player_number):
        all_moves = self.getAllMoves(player_number)
        return len(all_moves) == 0

    def evaluate(self,player_number):
        player_points = 0
        opponent_points = 0
        if(self.isCheckmated(player_number)):
            return -1 * float('inf')
        elif(self.isCheckmated(int(not player_number))):
            return float('inf')
        for row in self.board:
            for peice in row:
                if peice:
                    if peice.player_number == player_number:
                        player_points+=peice.getScore()
                    else:
                        opponent_points+=peice.getScore()
        return (player_points - opponent_points)

    def printCell(self,x,y):
        cell = self.board[x][y]
        if cell == None:
            if (x + y) % 2 == 0:
                print(Board.white_cell,end="")
            else:
                print(Board.black_cell,end="")
        else:
            print(cell.team_color + cell.getName(), end="")

    def printBoard(self):
        print("  " + '  '.join([" " + str(x) for x in range(len(self.board[0]))]))
        for i in range(self.height):
            print(i,end="")
            for j in range(self.width):
                print(" ",end="")
                self.printCell(i,j)
                print(" ",end="")
            print()
