from Game import Game
from Player import Player

class DeterministicPlayer(Player):
    def __init__(self, game, beta, historySize, experts):
        assert(historySize >= 0)
        assert(0 < beta < 1)
        Player.__init__(self, game)
        self.beta = beta
        self.historySize = historySize
        self.weightedExperts = [(expert, 1) for expert in experts]
        self.history = []

    def makeMove(self):
        predictweights = {move : 0 for move in self.game.getMoves()}
        moveweights = {move : 0 for move in self.game.getMoves()}
        for (expert, weight) in self.weightedExperts:
            predictweights[expert(self.history)] += weight
        for move1 in self.game.getMoves():
            for move2 in self.game.getMoves():
                moveweights[move1] += predictweights[move2] * self.game.testMoves(move1, move2)
        return max(moveweights, key = lambda key : moveweights[key])

    def observeMove(self, move):
        # Multiply weight by beta if the expert's prediction was wrong
        self.weightedExperts = [(expert, weight * (self.beta ** (expert(self.history) != move)))
                                for (expert, weight) in self.weightedExperts]
        self.history.append(move)
        if len(self.history) > self.historySize: self.history = self.history[1:]
        print (self.history, self.weightedExperts)

def main():
    RPSGame = Game()
    RPSGame.loadFromJson("Games/rps.json")
    print(RPSGame)
    print("rock beats scissors:" + str(RPSGame.testMoves("rock", "scissors")))
    player = DeterministicPlayer(RPSGame, .5, 5, [lambda x : "rock", lambda x : "paper", lambda x : "scissors"])
    while True:
        playerMove = raw_input("Make your move: ")
        if playerMove == "exit": return
        print(playerMove)
        pythonMove = player.makeMove()
        successStr = "I win!" if RPSGame.testMoves(pythonMove, playerMove) == 1 \
                    else "You win!" if RPSGame.testMoves(pythonMove, playerMove) == -1 \
                    else "We tied!"
        print("I made the move: " + pythonMove + ". " + successStr)
        player.observeMove(playerMove)

if __name__ == "__main__":
    main()