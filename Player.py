from Game import Game

class Player(object):
    def __init__(self, game):
        self.game = game

    def makeMove(self):
        raise NotImplementedError

    def observeMove(self, move):
        raise NotImplementedError
