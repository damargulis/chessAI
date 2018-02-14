from __future__ import print_function
from board import Board
from player import *
import time
import sys

TEST_LENGTH = 10

def testComputerPlayer(player, depth):
    p1 = player(0, 'w',1, display=False, depth=depth)
    p2 = player(1, 'b',-1, display=False, depth=depth)
    b = Board([p1,p2])
    start = time.time()
    i = 0
    while( i < 25):
        i += 1
        try:
            p1.takeTurn(b)
            p2.takeTurn(b)
        except Exception as e:
            #print('ERROR: ' + str(e))
            break
    t =  time.time() - start
    return t, i

def run_test(name, klass,depth=3):
    print('Test ' + name + " depth = " + str(depth))
    time = 0
    rounds = 0
    for i in range(TEST_LENGTH):
        _time, _rounds = testComputerPlayer(klass,depth=depth)
        time += _time
        rounds += _rounds
        print('.', end='')
        sys.stdout.flush()
    print()
    print('Time: ' + str(time))
    print('Rounds: ' + str(rounds))
    print(str(time / rounds) + ' time/round')

def main():
    run_test('ComputerPlayer', ComputerPlayer)
    run_test('RandomPlayer', RandomPlayer)
    for i in range(3):
        run_test('MinimaxPlayer', MinimaxPlayer, depth=i)




if __name__ == '__main__':
    main()
