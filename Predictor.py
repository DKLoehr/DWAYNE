from Game import Game
from Player import Player
import Experts
import random
import math

class DeterministicPlayer(Player):
    def __init__(self, game, beta, experts):
        print("sadas")
        assert(0 < beta < 1)
        Player.__init__(self, game)
        print("lkk")
        self.beta = beta
        self.weightedExperts = [(expert, 1) for expert in experts]

    def makeMove(self):
        predictWeights = {move : 0 for move in self.game.getMoves()}
        for (expert, weight) in self.weightedExperts:
            predictWeights[expert.predict()] += weight
        expectedValue = {move : 0 for move in self.game.getMoves()}
        for move1 in self.game.getMoves():
            for move2 in self.game.getMoves():
                expectedValue[move1] += predictWeights[move2] * self.game.testMoves(move1, move2)
        return max(expectedValue, key = lambda key : expectedValue[key])

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
        predictWeights = {move : 0 for move in self.game.getMoves()}
        for (expert, weight) in self.weightedExperts:
            predictWeights[expert.predict()] += weight
        expectedValue = {move : 0 for move in self.game.getMoves()}
        for move1 in self.game.getMoves():
            for move2 in self.game.getMoves():
                expectedValue[move1] += predictWeights[move2] * self.game.testMoves(move1, move2)
        moveWeights = [math.exp(expectedValue[move]) for move in self.game.getMoves()]
        return random.choices(self.game.getMoves(), moveWeights, k=1)[0]

    def observeMove(self, move):
        # Multiply weight by beta if the expert's prediction was wrong
        self.weightedExperts = [(expert, weight * (self.beta ** (expert.predict() != move)))
                                for (expert, weight) in self.weightedExperts]
        # Normalize weights so max weight is 1, to prevent us from getting
        # extremely small weights (unless an expert is terrible compared to the best)
        (_, maxweight) = max(self.weightedExperts, key = lambda ew : ew[1])
        self.weightedExperts = [(expert, weight/maxweight) for (expert, weight) in self.weightedExperts]

        for (expert, _) in self.weightedExperts: expert.observeMove(move)

def playAgainstUser(G, player):
    playerWins = 0
    pythonWins = 0
    ties = 0
    while True:
        pythonMove = player.makeMove()
        playerMove = input("Enter your move: ")
        if playerMove == "exit": return
        if playerMove not in G.getMoves():
            print ("Unknown move: " + playerMove)
            continue

        if G.testMoves(pythonMove, playerMove) == 1:
            pythonWins += 1
            successStr = "I win!"
        elif G.testMoves(pythonMove, playerMove) == -1:
            playerWins += 1
            successStr = "You win!"
        else:
            ties += 1
            successStr = "We tied!"

        player.observeMove(playerMove)
        print("I made the move: " + pythonMove + ". " + successStr)
        print("Me: {} ({}, {}) You : {} Ties : {}".format(pythonWins,\
            pythonMove, [weight for (expert, weight) in player.weightedExperts],\
            playerWins,\
            ties))

def playAgainstSelf(G, player1, player2, numRounds):
    playerWins = 0
    pythonWins = 0
    ties = 0
    count1 = {move : 0 for move in G.getMoves()}
    count2 = {move : 0 for move in G.getMoves()}
    for i in range(numRounds):
        pythonMove = player1.makeMove()
        playerMove = player2.makeMove()
        count1[pythonMove] += 1
        count2[playerMove] += 1

        if G.testMoves(pythonMove, playerMove) == 1:
            pythonWins += 1
        elif G.testMoves(pythonMove, playerMove) == -1:
            playerWins += 1
        else:
            ties += 1
        player1.observeMove(playerMove)
        player2.observeMove(pythonMove)
        print("Me: {} ({}, {}) You : {} ({}, {}) Ties : {}".format(pythonWins,\
            pythonMove, [weight for (expert, weight) in player1.weightedExperts],\
            playerWins,\
            playerMove, [weight for (expert, weight) in player2.weightedExperts],\
            ties))
    print (count1)
    print (count2)

def main():
    RPSGame = Game()
    RPSGame.loadFromJson("Games/rpsdk.json")
    #player1 = NondeterministicPlayer(RPSGame, .5, \
    #    [Experts.KthLastMoveExpert(RPSGame.getMoves(), k) for k in range(4)])
    #player2 = NondeterministicPlayer(RPSGame, .5, \
    #    [Experts.KthLastMoveExpert(RPSGame.getMoves(), k) for k in range(4)])
    #player2 = DeterministicPlayer(RPSGame, .5, \
    #    [Experts.WeightedLastMovesExpert(RPSGame.getMoves(), [1, 1])])
    #player = DeterministicPlayer(RPSGame, .5, \
    #    [Experts.ConstantExpert(RPSGame.getMoves(), move) for move in RPSGame.getMoves()])
    player1 = NondeterministicPlayer(RPSGame, .5, \
          [Experts.NondeterministicSequenceExpert(RPSGame.getMoves(), k) for k in range(5)])
    player2 = NondeterministicPlayer(RPSGame, .5, \
          [Experts.NondeterministicSequenceExpert(RPSGame.getMoves(), k) for k in range(5)])
    playAgainstSelf(RPSGame, player1, player2, 1000)
    #playAgainstUser(RPSGame, player1)

if __name__ == "__main__":
    main()
