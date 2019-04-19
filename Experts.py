import random
import itertools

class Expert(object):
    """
    An expert that takes a list of previous plays
    and formulates a prediction for the next move.
    """
    def __init__(self, moves):
        self.moves = moves
        self.history = []

    def predict(self):
        """
        Return a move prediction based on the history
        received by the expert.
        """
        raise NotImplementedError

    def observeMove(self, move):
        pass

class RandomExpert(Expert):
    """
    An expert that picks moves entirely at random.
    """

    def predict(self):
        """
        Return a random move from the choices.
        """
        return random.choice(self.moves)

class ConstantExpert(Expert):
    """
    An expert who always guesses the same move
    """

    def __init__(self, moves, move):
        Expert.__init__(self, moves)
        self.move = move

    def predict(self):
        """
        Return the predetermined move
        """
        return self.move

class KthLastMoveExpert(Expert):
    """
    An expert who picks the k-th last move.
    If there are fewer than k moves so far,
    pick a random move.
    """

    def __init__(self, moves, k):
        Expert.__init__(self, moves)
        self.k = k

    def predict(self):
        """
        Return the k-th move from the end of the list.
        If the list is less than size k, pick randomly.
        """
        if len(self.history) <= self.k:
            return random.choice(self.moves)
        else:
            return self.history[0]

    def observeMove(self, move):
        self.history.append(move)
        if len(self.history) > self.k + 1:
            self.history = self.history[1:]

class DeterministicSequenceExpert(Expert):
    """
    An expert who looks at the last k moves, and
    picks the move which was most often played
    after that sequence
    """

    def movelistToKey(self, lst):
        ret = ""
        for move in lst:
            ret += move + ","
        return ret

    def __init__(self, moves, k):
        Expert.__init__(self, moves)
        self.occurrences = {self.movelistToKey(moves) : 0 for moves in
                            itertools.product(moves, repeat=k+1)}
        self.k = k
        print(self.occurrences, self.k)

    def predict(self):
        """
        Return the k-th move from the end of the list.
        If the list is less than size k, pick randomly.
        """
        if len(self.history) < self.k:
            return self.moves[0]
        maxMove = self.moves[0]
        maxVal = 0
        for move in self.moves:
            print(len(self.history), self.k)
            newVal = self.occurrences[self.movelistToKey(self.history + [move])]
            if newVal > maxVal:
                maxVal = newVal
                maxMove = move
        return maxMove

    def observeMove(self, move):
        self.history.append(move)
        if len(self.history) == self.k + 1:
            self.occurrences[self.movelistToKey(self.history)] += 1
            self.history = self.history[1:]


class NondeterministicSequenceExpert(Expert):
    """
    An expert who looks at the last k moves, and
    picks the move which was most often played
    after that sequence
    """

    def movelistToKey(self, lst):
        ret = ""
        for move in lst:
            ret += move + ","
        return ret

    def __init__(self, moves, k):
        Expert.__init__(self, moves)
        self.occurrences = {self.movelistToKey(moves) : 0 for moves in
                            itertools.product(moves, repeat=k+1)}
        self.k = k

    def predict(self):
        """
        Return the k-th move from the end of the list.
        If the list is less than size k, pick randomly.
        """
        if len(self.history) < self.k:
            return random.choice(self.moves)
        weights = [self.occurrences[self.movelistToKey(self.history + [move])] for move in self.moves]
        return random.choices(self.moves, weights=weights, k=1)[0]


    def observeMove(self, move):
        self.history.append(move)
        if len(self.history) == self.k + 1:
            self.occurrences[self.movelistToKey(self.history)] += 1
            self.history = self.history[1:]

class WeightedLastMovesExpert(Expert):
    """
    An expert who samples a move from a weighted history.
    The last move has weight alpha,
    """

    def __init__(self, moves, weights):
        Expert.__init__(self, moves)
        self.weights = weights

    def predict(self):
        """
        Return a randomly sampled move from the history
        as the prediction, weighing the last k moves
        using the given weights, where k = len(weights).
        If the list is less than size k, pick randomly.
        """
        if len(self.history) < len(self.weights):
            return random.choice(self.moves)
        else:
            return random.choices(self.history, weights=self.weights, k=1)[0]

    def observeMove(self, move):
        self.history.append(move)
        if len(self.history) > len(self.weights):
            self.history = self.history[1:]
