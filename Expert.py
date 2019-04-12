import random

class Expert(object):
    """
    An expert that takes a list of previous plays
    and formulates a prediction for the next move.
    """
    def __init__(self, moves):
        self.moves = moves

    def predict(self, history):
        """
        Return a move prediction based on the history
        received by the expert.
        """
        raise NotImplementedError

class RandomExpert(Expert):
    """
    An expert that picks moves entirely at random.
    """

    def predict(self, history):
        """
        Return a random move from the choices.
        """
        return random.choice(history)

class KthLastMoveExpert(Expert):
    """
    An expert who picks the k-th last move.
    If there are fewer than k moves so far,
    pick a random move.
    """

    def __init__(self, moves, k):
        self.moves = moves
        self.k = k

    def predict(self, history):
        """
        Return the k-th move from the end of the list.
        If the list is less than size k, pick randomly.
        """
        if len(history) > self.k:
            return history[-self.k]
        else:
            return random.choice(self.moves)

class WeightedLastMovesExpert(Expert):
    """
    An expert who samples a move from a weighted history.
    The last move has weight alpha,
    """

    def __init__(self, moves, weights):
        self.moves = moves
        self.weights = weights

    def predict(self, history):
        """
        Return a randomly sampled move from the history
        as the prediction, weighing the last k moves
        using the given weights, where k = len(weights).
        If the list is less than size k, pick randomly.
        """
        k = len(self.weights)
        if len(history) > k:
            return random.choices(history[k:], weights=self.weights, k=1)[0]
        else:
            return random.choice(self.moves)
