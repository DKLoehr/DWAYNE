from Game import Game
from Player import Player
import Experts
import random

class DeterministicPlayer(Player):
    def __init__(self, game, beta, experts):
        assert(0 < beta < 1)
        Player.__init__(self, game)
        self.beta = beta
        self.weightedExperts = [(expert, 1) for expert in experts]

    def makeMove(self):
        predictweights = {move : 0 for move in self.game.getMoves()}
        moveweights = {move : 0 for move in self.game.getMoves()}
        for (expert, weight) in self.weightedExperts:
            predictweights[expert.predict()] += weight
        for move1 in self.game.getMoves():
            for move2 in self.game.getMoves():
                moveweights[move1] += predictweights[move2] * self.game.testMoves(move1, move2)
        return max(moveweights, key = lambda key : moveweights[key])

    def observeMove(self, move):
        # Multiply weight by beta if the expert's prediction was wrong
        self.weightedExperts = [(expert, weight * (self.beta ** (expert.predict() != move)))
                                for (expert, weight) in self.weightedExperts]
        # Normalize weights so max weight is 1, to prevent us from getting
        # extremely small weights (unless an expert is terrible compared to the best)
        (_, maxweight) = max(self.weightedExperts, key = lambda ew : ew[1])
        self.weightedExperts = [(expert, weight/maxweight) for (expert, weight) in self.weightedExperts]

        for (expert, _) in self.weightedExperts: expert.observeMove(move)

class NondeterministicPlayer(Player):
    def __init__(self, game, beta, experts):
        assert(0 < beta < 1)
        Player.__init__(self, game)
        self.beta = beta
        self.weightedExperts = [(expert, 1) for expert in experts]

    def makeMove(self):
        predictweights = {move : 0 for move in self.game.getMoves()}
        moveweights = {move : 0 for move in self.game.getMoves()}
        for (expert, weight) in self.weightedExperts:
            predictweights[expert.predict()] += weight
        for move1 in self.game.getMoves():
            for move2 in self.game.getMoves():
                moveweights[move1] += predictweights[move2] * self.game.testMoves(move1, move2)
        return random.choices(self.game.getMoves(), [moveweights[move] for move in self.game.getMoves], k=1)[0]

    def observeMove(self, move):
        # Multiply weight by beta if the expert's prediction was wrong
        self.weightedExperts = [(expert, weight * (self.beta ** (expert.predict() != move)))
                                for (expert, weight) in self.weightedExperts]
        # Normalize weights so max weight is 1, to prevent us from getting
        # extremely small weights (unless an expert is terrible compared to the best)
        (_, maxweight) = max(self.weightedExperts, key = lambda ew : ew[1])
        self.weightedExperts = [(expert, weight/maxweight) for (expert, weight) in self.weightedExperts]

        for (expert, _) in self.weightedExperts: expert.observeMove(move)


def main():
    RPSGame = Game()
    RPSGame.loadFromJson("Games/rps.json")
    #player = DeterministicPlayer(RPSGame, .5, \
    #    [Experts.KthLastMoveExpert(RPSGame.getMoves(), k) for k in range(10)])
    player = DeterministicPlayer(RPSGame, .5, \
        [Experts.WeightedLastMovesExpert(RPSGame.getMoves(), [1, 1])])
    #player = DeterministicPlayer(RPSGame, .5, \
    #    [Experts.ConstantExpert(RPSGame.getMoves(), move) for move in RPSGame.getMoves()])
    playerWins = 0
    pythonWins = 0
    ties = 0
    while True:
        pythonMove = player.makeMove()
        playerMove = input("Make your move: ")
        if playerMove == "exit": return
        if playerMove not in RPSGame.getMoves():
            print("Invalid move: " + playerMove)
            continue

        if RPSGame.testMoves(pythonMove, playerMove) == 1:
            pythonWins += 1
            successStr = "I win!"
        elif RPSGame.testMoves(pythonMove, playerMove) == -1:
            playerWins += 1
            successStr = "You win!"
        else:
            ties += 1
            successStr = "We tied!"
        print("I made the move: " + pythonMove + ". " + successStr)
        print("Me: {}   You : {}   Ties : {}".format(pythonWins, playerWins, ties))

        player.observeMove(playerMove)

if __name__ == "__main__":
    main()
