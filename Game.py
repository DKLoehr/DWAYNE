import json # For saving and loading games
import re # Ensure that moves only use alphanumeric characters
import bisect # Lets us insert into a sorted list

class Game(object):
    def __init__(self):
        self.moves = []
        self.beats = {} # Antisymmetric square matrix with elements in {-1, 0, 1}

    def getMoves(self):
        return self.moves

    # Return 1 if move1 beats move2, -1 if move2 beats move1, 0 otherwise
    def testMoves (self, move1, move2):
        if move1 not in self.moves: return
        if move2 not in self.moves: return
        return self.beats[(move1, move2)]

    def addMove(self, move):
        if move in self.moves: return
        if not re.match("^[a-zA-z0-9]+$", move):
            print ("Moves can only use alphanumeric characters")
            return

        bisect.insort(self.moves, move)
        for move2 in self.moves:
            self.beats[(move, move2)] = 0
            self.beats[(move2, move)] = 0

    def deleteMove(self, move):
        if move not in self.moves: return
        self.moves.remove(move)
        del self.beats[move, move]
        for move2 in self.moves:
            del self.beats[move, move2]
            del self.beats[move2, move]

    # Tell the game that move1 beats move2
    def addRelation(self, move1, move2):
        if move1 not in self.moves:
            print ("Unknown move: " + move1)
            return
        if move2 not in self.moves:
            print ("Unknown move: " + move2)
            return
        if move1 == move2:
            print ("A move ({}) cannot beat itself! Ignoring.".format(move1))
            return
        self.beats[(move1, move2)] = 1
        self.beats[(move2, move1)] = -1

    # Tell the game that move1 ties with move2
    def removeRelation(self, move1, move2):
        if move1 not in self.moves:
            print ("Unknown move: " + move1)
            return
        if move2 not in self.moves:
            print ("Unknown move: " + move2)
            return
        self.beats[(move1, move2)] = 0
        self.beats[(move2, move1)] = 0

    def __repr__(self):
        return "Moves: " + self.moves.__repr__() + "\nBeats: " + self.beats.__repr__()

    def __str__(self):
        if len(self.moves) == 0: return "Empty Game"
        maxlen = max([len(move) for move in self.moves])
        if maxlen % 2 == 0: maxlen += 1
        pad_to_maxlen = lambda str : '{s: ^{n}}'.format(s=str,n=maxlen)
        beatsstr = pad_to_maxlen("") + " | ".join([pad_to_maxlen(move) for move in self.moves]) + "\n"
        for move1 in self.moves:
            move1_beats = [self.beats[move1, move2] for move2 in self.moves]
            move1_beats_strs = ['{d: ^ {n}}'.format(d=beat,n=maxlen) for beat in move1_beats]
            beatsstr += pad_to_maxlen(move1) + " | ".join([s for s in move1_beats_strs]) + "\n"
        return beatsstr

    def saveToJson(self, filename):
        jsonBeats = {move1 + "," + move2 : self.beats[(move1, move2)] for move1 in self.moves for move2 in self.moves}
        with open(filename, 'w') as f:
            json.dump(jsonBeats, f)

    def loadFromJson(self, filename):
        self.moves = []
        self.beats = {}
        with open(filename, 'r') as f:
            jsonBeats = json.load(f)
        for moves, beats in jsonBeats.items():
            [move1, move2] = moves.split(",")
            self.addMove(move1)
            self.addMove(move2)
            self.beats[(move1, move2)] = beats
            self.beats[(move2, move1)] = -beats

def main():
    G = Game()

    print(G)

    G.addMove("rock")
    G.addMove("paper")
    G.addMove("scissors")
    G.addRelation("rock", "scissors")
    G.addRelation("paper", "rock")
    G.addRelation("scissors", "paper")

    print (G)
    G.saveToJson("rps.json")

    G.addMove("lizard")
    G.addMove("spock")

    G.addRelation("spock", "rock")
    G.addRelation("spock", "scissors")
    G.addRelation("paper", "spock")
    G.addRelation("lizard", "spock")
    G.addRelation("lizard", "paper")
    G.addRelation("scissors", "lizard")
    G.addRelation("rock", "lizard")

    print(G)
    G.saveToJson("rpsls.json")
    G.loadFromJson("rps.json")

    G.addMove("dragon")
    G.addMove("knight")

    G.addRelation("rock", "knight")
    G.addRelation("paper", "knight")
    G.addRelation("scissors", "knight")
    G.addRelation("dragon", "rock")
    G.addRelation("dragon", "paper")
    G.addRelation("dragon", "scissors")
    G.addRelation("knight", "dragon")

    print (G)

    G.saveToJson("rpsdk.json")
    G.loadFromJson("rps.json")

    print (G)

    G.deleteMove("paper")

    print (G)

if __name__ == "__main__":
    main()
