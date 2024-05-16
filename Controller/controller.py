from tkinter import *
from View import view

class Controller():
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view

    def initialize(self):
        self.view.create_widgets()
