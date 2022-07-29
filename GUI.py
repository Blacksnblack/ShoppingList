# -*- coding: utf-8 -*-
from tkinter import PanedWindow, Tk, Entry, Button, Label
from tkinter import CENTER, LEFT, X, TOP, N, BOTTOM, BOTH, END, S
import os.path

dataFileName = 'ShoppingList.dat'


class SaveLoader:
    def __init__(self):
        self.items = []

    def printAllItems(self):
        for item in self.items:
            print(item)

    def setItems(self, allItems):
        self.items = allItems

    def getAllItems(self):
        return self.items

    def OutputToFile(self):
        with open(dataFileName, "w") as f:
            f.write("\n".join(self.items))

    def InputFile(self):
        with open(dataFileName, "r") as f:
            self.items = f.readlines()
            print(self.items)

    def getTitle(self):
        return "Shopping List"


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Shopping List Application")
        self.minsize(640, 400)
        self.configure(background='#4d4d4d')
        self.iconbitmap('icon.ico')
        self.focus()
        self.bind("<KeyRelease>", self.keyup)
        self.itemsPane = PanedWindow(self)
        self.top = PanedWindow(self)
        self.insertElement = PanedWindow(self.itemsPane)
        self.SL = SaveLoader()

    def keyup(self, e):
        if e.keysym == 'Return':  # keycode 13
            self.newItem()
            self.saveData()
        elif 48 <= e.keycode <= 90:  # 0 -> through -> Z (upper)
            self.saveData()
        return

    def newItem(self, string=""):
        itemPane = PanedWindow(self.insertElement)

        entryField = Entry(itemPane, bd=2, justify=CENTER)
        entryField.pack(side=LEFT, fill=X, expand=5)
        entryField.focus()
        entryField.insert(0, string)

        deleteButton = Button(itemPane, text="Remove Item", command=lambda: itemPane.destroy())
        deleteButton.pack(side=LEFT, fill=X)

        itemPane.pack(side=TOP, fill=X)
        return

    def saveButtonCall(self):
        self.saveData()
        self.SL.printAllItems()
        self.SL.OutputToFile()

    def saveData(self):
        allItems = []
        items = [item for item in self.insertElement.winfo_children()]
        for item in items:
            entries = [entry for entry in item.winfo_children() if isinstance(entry, Entry)]
            for entry in entries:
                allItems.append(entry.get().upper())
        self.SL.setItems(allItems)

    def createShoppingListGui(self):
        # top Pane
        self.top.pack(fill=X)

        # Items Pane
        # Insert and Save Element
        self.insertElement = PanedWindow(self.itemsPane, height=300)
        self.insertElement.pack(fill=BOTH, side=TOP)

        bottomPane = PanedWindow(self.itemsPane)

        insertButton = Button(bottomPane, text="Insert New Item", command=lambda: self.newItem())
        insertButton.pack(side=LEFT, fill=X, expand=1)
        saveButton = Button(bottomPane, text="Submit", command=lambda: self.saveButtonCall(), bd=2, justify=CENTER)
        saveButton.pack(side=LEFT, fill=X, anchor=CENTER, expand=1)

        bottomPane.pack(fill=X, side=BOTTOM)

        self.itemsPane.pack(fill=BOTH)
        # End of items pane

        self.checkForInputFile()
        if len(self.insertElement.winfo_children()) == 0:  # gui needs at least one item to look good
            self.newItem()

    def checkForInputFile(self):
        if os.path.exists(dataFileName):
            self.SL.InputFile()
            items = self.SL.getAllItems()
            for item in items:
                self.newItem(item)
