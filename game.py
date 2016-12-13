from player import *
from board import Board

class Game(object):

        def __init__(self):
            player1 = HumanPlayer(0,'w',-1)
            # player2 = HumanPlayer(1, 'b', 1)
            player2 = ComputerPlayer(1,'b',1)
            self.players = [player1, player2]
            self.board = Board(self.players)

        def play(self):
            gameOver = False
            playerTurn = 0
            winner = None
            while(not gameOver):
                player = self.players[playerTurn]
                playerTurn = (playerTurn + 1) % len(self.players)
                opponent = self.players[playerTurn]

                self.board.printBoard()

                player.takeTurn(self.board)

                for peice,row,col in self.board.getPromotions(player):
                    player.promote(peice,row,col,self.board)

                if(self.board.isInCheck(opponent.number)):
                    if(self.board.isCheckmated(opponent.number)):
                        print("Check Mate!")
                        gameOver = True
                        winner = player
                        continue
                    else:
                        print("Check!")
            self.board.printBoard()
            if winner:
                print(winner.name + " Wins!")
            else:
                print("Its a draw!")
