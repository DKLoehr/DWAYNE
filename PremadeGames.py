# This file abuses interfaces and python's lack of typechecking in all sorts of ways.
# I'm not proud of it.
# But it works as well as it needs to.

def loadRPS(b):
    moves = [move for move in b.moves]
    for move in moves:
        b.deleteMove(move)
    b.addMove("rock")
    b.addMove("paper")
    b.addMove("scissors")
    b.onPress("rock", "scissors")
    b.onPress("scissors", "paper")
    b.onPress("paper", "rock")

def loadRPSLS(b):
    loadRPS(b)
    b.addMove("lizard")
    b.addMove("spock")
    b.onPress("rock", "lizard")
    b.onPress("scissors", "lizard")
    b.onPress("lizard", "paper")
    b.onPress("lizard", "spock")
    b.onPress("paper", "spock")
    b.onPress("spock", "rock")
    b.onPress("spock", "scissors")

def loadRPSDK(b):
    loadRPS(b)
    b.addMove("dragon")
    b.addMove("knight")
    b.onPress("dragon", "rock")
    b.onPress("dragon", "paper")
    b.onPress("dragon", "scissors")
    b.onPress("knight", "dragon")
    b.onPress("rock", "knight")
    b.onPress("paper", "knight")
    b.onPress("scissors", "knight")
