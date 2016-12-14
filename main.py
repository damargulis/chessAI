from game import Game

from optparse import OptionParser
import sys

usageStr = """
USAGE:      python main.py <options>
EXAMPLES:   (1) python main.py -w=player -b=computer
            (2) python main.py --white=player --black=computer
"""
def default(str):
    return str + ' [Default: %default]'

parser = OptionParser(usageStr)
parser.add_option('-w', '--white', help=default('White'), default='HumanPlayer')
parser.add_option('-b', '--black', help=default('Black'), default='ComputerPlayer')

options, otherjunk = parser.parse_args(sys.argv)
g = Game(options)
g.play()
