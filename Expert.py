import random

class Expert(object):
    """
    An expert that takes a list of previous plays
    and formulates a prediction for the next move.
    The expert forms its prediction based on a
    Strategy, which describes how it selects a move.
    """
    def __init__(self, moves, strategy):
        self.moves = moves
        self.strategy = strategy

    def predict(self, history):
        """
        Return a move prediction based on the history
        received by the expert.
        """
        return self.strategy.choose(history)

class Strategy(object):
    def choose(self, choices):
        raise NotImplementedError

class RandomStrategy(Strategy):
    """
    A strategy that picks moves entirely at random.
    """

    def choose(self, choices):
        """
        Return a random move from the choices.
        """
        return random.choice(choices)

class KthLastMoveStrategy(Strategy):
    """
    A strategy which picks the k-th last move.
    If there are fewer than k moves so far,
    pick a random move.
    """

    def __init__(self, k):
        self.k = k

    def choose(self, choices):
        """
        Return the k-th move from the end of the list.
        If the list is less than size k, pick randomly.
        """
        if len(choices) > self.k:
            return choices[-self.k]
        else:
            return random.choice(self.moves)
