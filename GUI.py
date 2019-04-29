from tkinter import *
from tkinter import ttk
from functools import partial
from math import sqrt, ceil
from Game import Game
from PremadeGames import loadRPS, loadRPSLS, loadRPSDK
import Predictor
import Experts

flatten = lambda z: [x for y in z for x in y]

COL_OFFSET = 0
ROW_OFFSET = 2

class ButtonGrid(object):
    def __init__(self, frame, onPressExternal, onAdd, onDelete):
        self.buttons = {}
        self.moves = []
        self.frame = frame
        self.onPressExternal = onPressExternal
        self.onAdd = onAdd
        self.onDelete = onDelete
        self.rowLabels = {}
        self.colLabels = {}

    ''' Internal Functions -- do not call from outside the class '''

    def onPress(self, move1, move2):
        if move1 == move2: return

        oldVal = self.buttons[move1, move2]['text']
        if oldVal == '0':
            newVal = '+'    # New text for this button
            otherVal = '-'  # New text for the button move2,move1
        elif oldVal == '+':
            newVal = '-'
            otherVal = '+'
        else: # oldVal == '-'
            newVal = '0'
            otherVal = '0'
        self.buttons[move1, move2]['text'] = newVal
        self.buttons[move2, move1]['text'] = otherVal
        self.onPressExternal(move1, move2, newVal)

    def regridAll(self):
        for move1 in self.moves:
            self.rowLabels[move1].grid(row=1+ROW_OFFSET+self.moves.index(move1), column=COL_OFFSET)
            self.colLabels[move1].grid(row=ROW_OFFSET, column=1+COL_OFFSET+self.moves.index(move1))
            for move2 in self.moves:
                btn = self.buttons[move1, move2]
                #btn.grid_forget()
                btn.grid(row=ROW_OFFSET+1+self.moves.index(move1), \
                         column=COL_OFFSET+1+self.moves.index(move2), \
                         sticky=N+S+E+W)
                btn['command'] = partial(self.onPress, move1, move2)

    def addButton(self, move1, move2):
        btn = ttk.Button(self.frame, text='0')#text=move1 + "," + move2)
        self.buttons[move1,move2] = btn

    def deleteButton(self, move1, move2):
        self.buttons[move1, move2].grid_forget()
        del self.buttons[move1, move2]

    ''' External functions '''

    def addMove(self, move):
        if move in self.moves: return

        self.frame.rowconfigure(len(self.moves)+ROW_OFFSET+1, weight=1)
        self.frame.columnconfigure(len(self.moves)+COL_OFFSET+1, weight=1)

        for move2 in self.moves:
            self.addButton(move, move2)
            self.addButton(move2, move)

        self.moves.append(move)
        self.addButton(move, move)
        self.rowLabels[move] = ttk.Label(self.frame, text=move)
        self.colLabels[move] = ttk.Label(self.frame, text=move)
        self.regridAll()
        self.onAdd(move)

    def deleteMove(self, move):
        if move not in self.moves: return

        self.moves.remove(move)
        self.rowLabels[move].grid_forget()
        del self.rowLabels[move]
        self.colLabels[move].grid_forget()
        del self.colLabels[move]
        self.deleteButton(move, move)
        for move2 in self.moves:
            self.deleteButton(move, move2)
            self.deleteButton(move2, move)

        self.regridAll()
        self.onDelete(move)

    def activate(self):
        for _, button in self.buttons.items():
            button["state"] = NORMAL

    def deactivate(self):
        for _, button in self.buttons.items():
            button["state"] = DISABLED

class PlayGUI(object):
    def __init__(self, root, moves, game, onFinish, predictorConstructor):
        self.moves = moves
        self.beats = game.testMoves
        self.frame = ttk.Frame(root)
        self.onFinish = onFinish
        self.predictor = predictorConstructor(game)

        self.playerScore = 0
        self.pythonScore = 0
        self.ties = 0

        self.playerScoreStr = StringVar()
        self.pythonScoreStr = StringVar()
        self.tiesStr = StringVar()
        self.playerMoveStr = StringVar()
        self.pythonMoveStr = StringVar()
        self.roundWinStr = StringVar()
        self.roundWinStr.set("asdsa")

        self.playerScoreStr.set(self.playerScore)
        self.pythonScoreStr.set(self.pythonScore)
        self.tiesStr.set(self.ties)

        self.topBar = []
        self.topBar.append(ttk.Label(self.frame, text="You: ", foreground="blue"))
        self.topBar.append(ttk.Label(self.frame, width=3, textvariable=self.playerScoreStr, foreground="blue"))
        self.topBar.append(ttk.Label(self.frame, text="Ties: ", foreground="green"))
        self.topBar.append(ttk.Label(self.frame, width=3, textvariable=self.tiesStr, foreground="green"))
        self.topBar.append(ttk.Label(self.frame, text="DWAYNE: ", foreground="red"))
        self.topBar.append(ttk.Label(self.frame, width=3, textvariable=self.pythonScoreStr, foreground="red"))
        self.topBar.append(ttk.Button(self.frame, text="Forfeit", command=self.onFinish))

        # Dummy label to take up space in row 2
        #ttk.Label(self.frame, text = "").grid(row=2, column=1)
        self.secondBar = []
        self.secondBar.append(ttk.Label(self.frame, text="You played: ", foreground="blue"))
        self.secondBar.append(ttk.Label(self.frame, width=1+max([len(move) for move in moves]), \
                                        textvariable=self.playerMoveStr, foreground="blue"))

        self.roundWinLabel = ttk.Label(self.frame, textvariable = self.roundWinStr)
        self.secondBar.append(self.roundWinLabel)
        self.secondBar.append(ttk.Label(self.frame)) # Dummy label to take up space

        self.secondBar.append(ttk.Label(self.frame, text="DWAYNE played: ", foreground="red"))
        self.secondBar.append(ttk.Label(self.frame, width=1+max([len(move) for move in moves]), \
                                        textvariable=self.pythonMoveStr, foreground="red"))

        self.moveButtons = [ttk.Button(self.frame, text=move, command=partial(self.processMove, move)) for move in self.moves]
        self.movesBar = []

        # Make buttons as close to a square as we can get
        sq = max(3, ceil(sqrt(len(self.moveButtons))))
        #print(sq)
        self.moveBars = [self.moveButtons[sq*i:sq*(i+1)] for i in range(sq)]

        allBars = [self.topBar, self.secondBar] + self.moveBars
        for i, bar in enumerate(allBars):
            for j, elt in enumerate(bar):
                elt.grid(row=i, column=j, stick=N)

    def processMove(self, move1):
        move2 = self.predictor.makeMove()
        self.predictor.observeMove(move1)
        self.playerMoveStr.set(move1)
        self.pythonMoveStr.set(move2)
        beats = self.beats(move1, move2)
        if beats == 1:
            self.playerScore += 1
            self.playerScoreStr.set(self.playerScore)
            self.roundWinStr.set("You won!")
            self.roundWinLabel["foreground"] = "blue"
        elif beats == -1:
            self.pythonScore += 1
            self.pythonScoreStr.set(self.pythonScore)
            self.roundWinStr.set("DWAYNE won!")
            self.roundWinLabel["foreground"] = "red"
        else:
            self.ties += 1
            self.tiesStr.set(self.ties)
            self.roundWinStr.set("You tied!")
            self.roundWinLabel["foreground"] = "green"
        # TODO: End the game at an appropriate score

    def show(self):
        self.frame.grid(column=1, row=0, sticky=(N, W, E, S))

    def hide(self):
        self.frame.grid_forget()

class SetupGUI(object):
    def __init__(self, root, game, predictorConstructor):
        self.root = root
        self.game = game
        self.predictorConstructor = predictorConstructor
        self.frame = ttk.Frame(root)
        self.buttonGrid = ButtonGrid(self.frame, self.onPress, game.addMove, game.deleteMove)
        self.activeMove = StringVar()
        self.topBar = [[], []]
        self.topBar[0].append(ttk.Entry(self.frame, width=10, textvariable=self.activeMove))
        self.topBar[0].append(ttk.Button(self.frame, text="Add Move", command=self.callAddMove))
        self.topBar[0].append(ttk.Button(self.frame, text="Delete Move", command=self.callDelMove))
        self.topBar[0].append(ttk.Button(self.frame, text="Play!", command = self.startGame))
        self.topBar[1].append(ttk.Button(self.frame, text="Load RPS", command=partial(loadRPS, self.buttonGrid)))
        self.topBar[1].append(ttk.Button(self.frame, text="Load RPSLS", command=partial(loadRPSLS, self.buttonGrid)))
        self.topBar[1].append(ttk.Button(self.frame, text="Load RPSDK", command=partial(loadRPSDK, self.buttonGrid)))
        for i, bar in enumerate(self.topBar):
            for j, elt in enumerate(bar):
                elt.grid(row=i, column=j, stick=N)

    def startGame(self):
        self.buttonGrid.deactivate()
        for elt in flatten(self.topBar):
            elt["state"] = DISABLED
        self.playGUI = PlayGUI(self.root, self.buttonGrid.moves, self.game, self.endGame, self.predictorConstructor)
        self.playGUI.show()

    def endGame(self):
        self.buttonGrid.activate()
        for elt in flatten(self.topBar):
            elt["state"] = NORMAL
        self.playGUI.hide()

    def show(self):
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

    def hide(self):
        self.frame.grid_forget()

    def addPlayCommand(self, command):
        self.topBar[3]["command"] = command

    # Interal Functions

    def onPress(self, move1, move2, newVal):
        if newVal == "+":
            self.game.addRelation(move1, move2)
        elif newVal == "-":
            self.game.addRelation(move2, move1)
        else:
            self.game.removeRelation(move1, move2)
        #print(self.game)

    def callAddMove(self):
        move = self.activeMove.get()
        if move == "": return
        self.buttonGrid.addMove(move)
        self.activeMove.set("")

    def callDelMove(self):
        move = self.activeMove.get()
        if move == "": return
        self.buttonGrid.deleteMove(move)
        self.activeMove.set("")

def main():
    root = Tk()
    root.title("DWAYNE")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    game = Game()

    makePredictor = lambda game : Predictor.NondeterministicPlayer(game, .5, \
          [Experts.NondeterministicSequenceExpert(game.getMoves(), k) for k in range(5)])

    GUI = SetupGUI(root, game, makePredictor)
    GUI.show()

    root.mainloop()



if __name__ == "__main__":
    main()
