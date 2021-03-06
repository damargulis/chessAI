Chess game and AI agent

USAGE:
 * python main.py
     * default game (human plays as white, random-computer plays as black)
 * python main.py -w MinimaxPlayer -b HumanPlayer
     * human plays as black, minimax agent plays as white
 * python main.py --help
     * see list of commands


Play chess with humans or computers!  Either color can take any role.

Agents Available:
 * HumanPlayer
     * You control this. Enter moves as 'row,col' (ex: '3,1').  The rows and columns are numbered.
     * Castle with 'KC' for kings castle and 'QC' for queens castle.  Type HELP for additional help.

 * ComputerPlayer
     * Picks the move the maximizes their next position
     * Currently determines 'position' by using peice points

 * MinimaxPlayer
     * Uses a minimax tree with a depth of 3 to pick its move
     * Uses same state evaluation as above


TODO:
 - [x] Playable chess game
 - [x] User controls and AI controls
 - [x] Best current move agent
 - [x] Minimax agent w/ alpha/beta pruning
 - [ ] Create additional evaluation functions
 - [ ] Control for pawn promotion in the AI
