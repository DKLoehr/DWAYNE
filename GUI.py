from tkinter import *
from tkinter import ttk
from functools import partial
from Game import Game

COL_OFFSET = 0
ROW_OFFSET = 1

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

def main():

    root = Tk()
    root.title("DWAYNE")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    game = Game()

    def onPress(move1, move2, newVal):
        if newVal == "+":
            game.addRelation(move1, move2)
        elif newVal == "-":
            game.addRelation(move2, move1)
        else:
            game.removeRelation(move1, move2)
        print(game)

    b = ButtonGrid(mainframe, onPress, game.addMove, game.deleteMove)

    activeMove = StringVar()

    def callAddMove():
        move = activeMove.get()
        if move == "": return
        b.addMove(move)
        activeMove.set("")

    def callDelMove():
        move = activeMove.get()
        if move == "": return
        b.deleteMove(move)
        activeMove.set("")

    moveEntry = ttk.Entry(mainframe, width=10, textvariable=activeMove)
    addMoveButton = ttk.Button(mainframe, text="Add Move", command=callAddMove)
    delMoveButton = ttk.Button(mainframe, text="Delete Move", command=callDelMove)

    moveEntry.grid(row=0, column=0, sticky=(N,W))
    addMoveButton.grid(row=0, column=1, sticky=(N))
    delMoveButton.grid(row=0, column=2, sticky=(N))

    #moveEntry.focus()
    root.bind('<Return>', callAddMove())

    root.mainloop()



if __name__ == "__main__":
    main()
