from player import *
from board import Board
import collections

player_options = {
    'HumanPlayer': HumanPlayer,
    'ComputerPlayer': ComputerPlayer,
    'MinimaxPlayer': MinimaxPlayer,
    'RandomPlayer': RandomPlayer,
}

class Game(object):
    def __init__(self,options):
        if options.white in player_options:
            player1 = player_options[options.white](0,'w',-1,depth=options.depth)
        else:
            print('White Player Agent not recognized (user control is default)')
            exit()
        if options.black in player_options:
            player2 = player_options[options.black](1,'b',1,depth=options.depth)
        else:
            print('Black Player Agent not recognized (computer control is default)')
            exit()
        self.players = [player1, player2]
        self.board = Board(self.players)

    def play(self):
        playerTurn = 0
        gameOver = False
        while(not gameOver):
            self.board.printBoard()
            player = self.players[playerTurn]
            print(player.name + "'s Turn")
            player.takeTurn(self.board)
            gameOver, winner = self.checkGameOver(playerTurn)
            playerTurn = (playerTurn + 1) % len(self.players)
        self.board.printBoard()
        if(winner == 'Ties'):
            print("Its a draw!")
        else:
            print(self.players[winner].name + ' Wins!')
        return winner

class Chess(Game):
        def __init__(self,options):
            super(Chess, self).__init__(options)
            self.positionCounter = collections.Counter()
            self.positionCounter[self.board.toTuple()] += 1

        def checkGameOver(self, playerNumber):
                player = self.players[playerNumber]
                opponentTurn = (player.number + 1) % len(self.players)
                opponent = self.players[opponentTurn]

                for peice,row,col in self.board.getPromotions(player):
                    player.promote(peice,row,col,self.board)
                    self.board.printBoard()

                boardTuple = self.board.toTuple()
                self.positionCounter[boardTuple] += 1
                if(self.positionCounter[boardTuple] > 3):
                    print("Threefold repitition, (this should eventually be a choice...)")
                    return True, 'Ties'

                if(self.board.isInCheck(opponent.number)):
                    if(self.board.isCheckmated(opponent.number)):
                        print("Check Mate!")
                        return True, playerNumber
                    else:
                        print("Check!")
                        return False, None
                elif(self.board.isDraw() or self.board.isStalemated(opponent.number)):
                    print(opponent.name + " has been stalemated")
                    return True, 'Ties'
                return False, None
