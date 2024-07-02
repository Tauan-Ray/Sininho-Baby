from View import view as v
from Model import model as m
from Controller import controller as c
from tkinter import *

print('teste')

def main():
    root = Tk()
    root.title('Sininho Baby')
    root.geometry('1000x600')
    root.resizable(False, False)

    model = m.ProductModel()
    view = v.View(root=root)
    controller = c.Controller(root=root, model=model, view=view)

    controller.initialize()
    
    root.mainloop()


if __name__ == '__main__':
    main()
