from __future__ import print_function
import random

def printHelp():
    print("*********************************")
    print("Command      Meaning")
    print("HELP         Print help menu")
    print("EXIT         QUIT")
    print("PRINT        Print Board")
    print("KC           Castle Kings Side")
    print("QC           Castle Queens Side")
    print("*********************************")


class Player(object):
    def __init__(self,number,color,direction,depth=3,name=""):
        self.depth = int(depth)
        self.number = number
        self.team_color = color
        self.direction = direction
        if name == "":
            name = "Player " + str(number)
        self.name = name

        self.analyzed = 0

    def takeTurn(self,board):
        pass

    def promote(self,peice,row,col):
        pass

class HumanPlayer(Player):

    def takeTurn(self,board):
        print(self.name + "'s Turn")

        all_possible_moves = board.getAllMoves(self.number)
        possible_peice_spots = [move[0] for move in all_possible_moves]

        [peice, row, col] = self.getPeice(board, possible_peice_spots)
        if(peice == 'KC' or peice == 'QC'):
            board.castle(peice,self.direction)
        else:
            print("Move " + peice.getFullName() + " to: ")
            possible_actions = [move[1] for move in all_possible_moves if move[0] == (row,col)]
            [move_row, move_col] = self.getMove(peice,row,col,board,possible_actions)
            if move_row == 'PR' or move_row == 'PL':
                board.en_passant(move_row,move_col,self.direction)
            else:
                board.movePeice(row,col,move_row,move_col)


    def getMove(self,peice,row,col,board,possible):
        if ('PL','PL') in possible:
            possible.append((row+self.direction,col-1))
        if ('PR','PR') in possible:
            possible.append((row+self.direction,col+1))
        while(True):
            [move_row,move_col] = self.readInput(board)
            if ('PL','PL') in possible and move_row == row+self.direction and move_col == col-1:
                return ('PL',(row,col))
            if ('PR','PR') in possible and move_row == row+self.direction and move_col == col+1:
                return ('PR',(row,col))
            if ((move_row,move_col) in possible):
                return [move_row,move_col]
            print("Illegal Move")

    def getPeice(self,board,possible):
        while(True):
            [row,col] = self.readInput(board)
            if((row == 'KC' or row == 'QC')):
                if row in possible:
                    return (row,row,row)
                else:
                    print(row + " not currently possible")
                    continue
            peice = board.getPeice(row,col)
            if not peice:
                print("No peice")
                continue
            if peice.player_number == self.number:
                if (row,col) in possible:
                    return [peice, row, col]
                else:
                    print("No possible moves for " + peice.getFullName())
                    continue
            else:
                print("Not your peice")
                continue


    def readInput(self,board,extra_options=[]):

        options = [
            ("EXIT", lambda : exit()),
            ("HELP", lambda : printHelp()),
            ("PRINT", lambda : board.printBoard())
        ] + extra_options
        while(True):
            spot = raw_input("Enter a spot (row,col): ")
            if spot in [option[0] for option in options]:
                for option in options:
                    if option[0] == spot:
                        option[1]()
                        break
            else:
                if spot == 'KC' or spot == 'QC':
                    return (spot,spot)
                spot = spot.split(',')
                if len(spot) != 2:
                    print("Bad Format")
                    continue
                if not (spot[0].isdigit() and spot[1].isdigit()):
                    print("Bad Format")
                    continue
                [row,col] = [int(x) for x in spot]
                if row > board.height or col > board.width:
                    print("Not a spot on board")
                    continue
                return [row,col]

    def promote(self,peice,row,col,board):
        print("Promote " + peice.getFullName() + " at " + str(row) + "," + str(col))
        done = False
        while(not done):
            promotion = raw_input("Replace with (Q,R,K,B): ")
            done = board.promote(self,row,col,promotion)

import time
import random

class ComputerPlayer(Player):
    def takeTurn(self,board):
        print(self.name + " is thinking...")
        start = time.time()
        move = self.getMove(board)
        peice = board.getPeice(move[0][0],move[0][1])
        end = time.time()
        if peice:
            print("Moving " + peice.getFullName() + " to " + str(move[1]) + " Time: ", (end - start))
        else:
            import pdb; pdb.set_trace()
            print ("!!!!!!!!!!!!!!!!!!!!")
        board.movePeice(move[0][0],move[0][1],move[1][0],move[1][1])

    def getMove(self,board):
        all_possible_moves = board.getAllMoves(self.number)
        all_possible_moves = [move for move in all_possible_moves if str(move[0][0]).isdigit()]
        possible_boards = [board.generateSuccessor(move[0],move[1]) for move in all_possible_moves]
        scores = [board.evaluate(self.number) for board in possible_boards]
        maxValue = max(scores)
        best_actions = [a for a,v in zip(all_possible_moves, scores) if v == maxValue]
        return random.choice(best_actions)


    def promote(self,peice,row,col,board):
        board.promote(self,row,col,'Q')

import sys
class MinimaxPlayer(ComputerPlayer):

    def getMove(self,board):

        self.analyzed = 0
        all_possible_moves = board.getAllMoves(self.number)
        possible_boards = [board.generateSuccessorFromMove(move,self.direction) for move in all_possible_moves]
        inf = float('inf')
        scores = [self.getMin(board,1,-1*inf,inf) for board in possible_boards]

        # print(all_possible_moves)
        # print(scores)
        maxValue = max(scores)

        bestActions = [a for a, v in zip(all_possible_moves, scores) if v == maxValue]
        print('Analyzed: ', self.analyzed)
        # print('best:', bestActions)
        return random.choice(bestActions)

    def getMax(self,board,depth, alpha, beta):

        if depth >= self.depth:
            self.analyzed += 1
            print('Analyzed: ',self.analyzed,end='\r')
            sys.stdout.flush()
            return board.evaluate(self.number)
        else:
            all_possible_moves = board.getAllMoves(self.number)
            if(len(all_possible_moves) == 0):
                return 0
            v = -1 * float('inf')
            for move in all_possible_moves:
                possible_board = board.generateSuccessorFromMove(move,self.direction)
                v = max(v, self.getMin(possible_board,depth+1,alpha,beta))
                alpha = max(alpha,v)
                if beta <= alpha:
                    break
            return v

    def getMin(self,board,depth, alpha, beta):

        player_number = int(not self.number)
        player_direction = self.direction * -1
        if depth >= self.depth:
            self.analyzed += 1
            print('Analyzed: ',self.analyzed,end='\r')
            sys.stdout.flush()

            return board.evaluate(self.number)
        else:
            all_possible_moves = board.getAllMoves(player_number)
            if len(all_possible_moves) == 0:
                return 0
            v = float('inf')
            for move in all_possible_moves:
                possible_board = board.generateSuccessorFromMove(move,self.direction)
                v = min(v, self.getMax(possible_board, depth+1,alpha,beta))
                beta = min(beta,v)
                if beta <= alpha:
                    break
            return v

    def promote(self,peice,row,col,board):
        board.promote(self,row,col,'Q')
