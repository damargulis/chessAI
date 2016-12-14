from player import *
from board import Board

class Game(object):

        def __init__(self,options):
            if(options.white == 'HumanPlayer'):
                player1 = HumanPlayer(0,'w',-1)
            elif(options.white == 'ComputerPlayer'):
                player1 = ComputerPlayer(0,'w',-1)
            elif(options.white == 'MinimaxPlayer'):
                player1 = MinimaxPlayer(0,'w',-1)
            else:
                print('White Player Agent not recognized (user control is default)')
                exit()
            if(options.black == 'HumanPlayer'):
                player2 = HumanPlayer(1,'b',1)
            elif(options.black == 'ComputerPlayer'):
                player2 = ComputerPlayer(1,'b',1)
            elif(options.black == 'MinimaxPlayer'):
                player2 = MinimaxPlayer(1,'b',1)
            else:
                print('Black Player Agent not recognized (computer control is default)')
                exit()
            self.players = [player1, player2]
            self.board = Board(self.players)

        def play(self):
            gameOver = False
            playerTurn = 0
            self.board.printBoard()
            while(not gameOver):
                player = self.players[playerTurn]
                playerTurn = (playerTurn + 1) % len(self.players)
                opponent = self.players[playerTurn]

                player.takeTurn(self.board)
                self.board.printBoard()


                for peice,row,col in self.board.getPromotions(player):
                    player.promote(peice,row,col,self.board)
                    self.board.printBoard()

                if(self.board.isInCheck(opponent.number)):
                    if(self.board.isCheckmated(opponent.number)):
                        print("Check Mate!")
                        gameOver = True
                        print(player.name + " Wins!")
                        continue
                    else:
                        print("Check!")
                elif(self.board.isDraw()):
                    gameOver = True
                    print("It's a Draw!")
                    continue
                elif(self.board.isStalemated(opponent.number)):
                    gameOver = True
                    print(opponent.name + " has been stalemated.  Its a Draw!")
                    continue
