from tkinter import *
from View import view

class Controller():
    def __init__(self, model, view, root=''):
        self.root = root
        self.model = model
        self.view = view

    def initialize(self):
        self.view.create_widgets()

    def list_products(self):
        return self.model.search_products()
    
    def product_by_name(self, name):
        return self.model.search_product_by_name(name)
