from tkinter import *
from tkinter import filedialog as fd
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
    
    
    def product_by_code(self, code):
        return self.model.search_product_by_code(code)
    
    
    def update_stock_database(self, new_stock, product_code):
        return self.model.update_stock(new_stock, product_code)

    

    def register_product_database(self, product_code, product_name, price_product, stock_product, image_product=None):
        try:
            product_data = self.model.product_data(product_code, product_name, price_product, stock_product, image_product)
        except ValueError as e:
            self.view.show_error(str(e))
            return
        

        try:
            self.model.add_product(product_data=product_data)
            self.view.show_success("Produto cadastrado com sucesso!!!")

            self.view.clear_fields()
        except ValueError as e:
            self.view.show_error(str(e))
            return

    
    def update_product_database(self, code_product, name_product, price_product, stock_product, image_product=None):
        try:
            product_data = self.model.product_data(code_product, name_product, price_product, stock_product, image_product)
            product_data['old_code'] = self.view.old_code

    
            try:
                self.model.update_product(product_data=product_data)
                self.view.show_success("Produto atualizado com sucesso!!!")

                self.view.clear_fields()
                self.view.screen_products()
            except ValueError as e:
                self.view.show_error(str(e))


        except ValueError as e:
            self.view.show_error(str(e))


    def delete_product_database(self, response, code):
        if response:
            self.model.delete_product(code = code)
            self.view.show_success("Produto deletado com sucesso")
            
            self.view.update(self.view.list_products)
