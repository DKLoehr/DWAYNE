from tkinter import *
from tkinter import ttk
from functools import partial

class ButtonGrid(object):
    def __init__(self, frame, onPressExternal):
        self.buttons = {}
        self.moves = []
        self.frame = frame
        self.onPressExternal = onPressExternal

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

    def regridAllButtons(self):
        for move1 in self.moves:
            for move2 in self.moves:
                btn = self.buttons[move1, move2]
                btn.grid_forget()
                btn.grid(row=self.moves.index(move1), column=self.moves.index(move2), sticky=N+S+E+W)
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

        mainframe.rowconfigure(len(self.moves), weight=1)
        mainframe.columnconfigure(len(self.moves), weight=1)

        for move2 in self.moves:
            self.addButton(move, move2)
            self.addButton(move2, move)

        self.moves.append(move)
        self.addButton(move, move)
        self.regridAllButtons()

    def deleteMove(self, move):
        if move not in self.moves: return

        self.moves.remove(move)
        self.deleteButton(move, move)
        for move2 in self.moves:
            self.deleteButton(move, move2)
            self.deleteButton(move2, move)

        self.regridAllButtons()

root = Tk()
root.title("DWAYNE")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

def onPress(move1, move2, newVal):
    print("{},{}:{}".format(move1, move2, newVal))

b = ButtonGrid(mainframe, onPress)
b.addMove("rock")
b.addMove("paper")
b.addMove("scissors")

root.mainloop()
