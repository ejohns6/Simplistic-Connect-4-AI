Program  is an A.I. for connect four that looks ahead x amount of moves for player
 x ahead where x is set when the program is started by a system argument and is
given a current state of the connect four in the format of a txt file where the
txt file looks like
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ x o _
_ _ _ _ x o _
The program decides the best move on a simplestic scoring system where
 it counts the number of x's or o's in 3 in a row.

Program is run with the arguments in the order of "TheCurrentMapState" "HowManyMovesAhead"b