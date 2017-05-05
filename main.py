from game import Game

from optparse import OptionParser
import sys

usageStr = """
USAGE:      python main.py <options>
EXAMPLES:   (1) python main.py -w player -b computer
            (2) python main.py --white=player --black=computer --number=3
            --depth=5
"""
def default(str):
    return str + ' [Default: %default]'

def main():
    parser = OptionParser(usageStr)
    parser.add_option('-w', '--white', help=default('White'), default='HumanPlayer')
    parser.add_option('-b', '--black', help=default('Black'), default='ComputerPlayer')
    parser.add_option('-d', '--depth', help=default('Depth of recursion'), default='3')
    parser.add_option('-n', '--number', help=default('Number of games'), default='1')

    options, otherjunk = parser.parse_args(sys.argv)
    print("Playing " + options.number + " game(s) of chess")
    for i in range(int(options.number)):
        g = Game(options)
        g.play()

if __name__ == '__main__':
    main()
