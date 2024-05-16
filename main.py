from View import view as v
from Model import model as m
from Controller import controller as c
from tkinter import *


def main():
    root = Tk()
    root.title('Sininho Baby')
    root.geometry('1000x600')
    root.resizable(False, False)

    model = m.ProductModel()
    view = v.View(root)
    controller = c.Controller(root, model, view)

    controller.initialize()
    
    root.mainloop()


if __name__ == '__main__':
    main()