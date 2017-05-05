from player import *
from board import Board

class Game(object):
    def __init__(self,options):
        if(options.white == 'HumanPlayer'):
            player1 = HumanPlayer(0,'w',-1)
        elif(options.white == 'ComputerPlayer'):
            player1 = ComputerPlayer(0,'w',-1)
        elif(options.white == 'MinimaxPlayer'):
            player1 = MinimaxPlayer(0,'w',-1,depth=options.depth)
        else:
            print('White Player Agent not recognized (user control is default)')
            exit()
        if(options.black == 'HumanPlayer'):
            player2 = HumanPlayer(1,'b',1)
        elif(options.black == 'ComputerPlayer'):
            player2 = ComputerPlayer(1,'b',1)
        elif(options.black == 'MinimaxPlayer'):
            player2 = MinimaxPlayer(1,'b',1,depth=options.depth)
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
            playerTurn = (playerTurn + 1) % len(self.players)
            player.takeTurn(self.board)
            gameOver = self.checkGameOver(playerTurn)

class Chess(Game):
        def __init__(self,options):
            super(Chess, self).__init__(options)

        def checkGameOver(self, playerNumber):
                player = self.players[playerNumber]
                opponentTurn = (player.number + 1) % len(self.players)
                opponent = self.players[opponentTurn]

                for peice,row,col in self.board.getPromotions(player):
                    player.promote(peice,row,col,self.board)
                    self.board.printBoard()

                if(self.board.isInCheck(opponent.number)):
                    if(self.board.isCheckmated(opponent.number)):
                        print("Check Mate!")
                        print(player.name + " Wins!")
                        return True
                    else:
                        print("Check!")
                        return False
                elif(self.board.isDraw()):
                    print("It's a Draw!")
                    return True
                elif(self.board.isStalemated(opponent.number)):
                    print(opponent.name + " has been stalemated.  Its a Draw!")
                    return True
