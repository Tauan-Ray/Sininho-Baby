from tkinter import *
from tkinter import filedialog as fd, messagebox
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
    
    def register_product_database(self, product_name, price_product, stock_product, image_product = ''):
        try:
            price_product = float(price_product)
            stock_product = int(stock_product)


        except ValueError:
            messagebox.showerror('ERROR!!!', 
                                'Campo preço ou estoque com valores inválidos!')
            return


        data = {
            'name': product_name,
            'price': price_product,
            'image': image_product,
            'stock': stock_product
        }
        

        self.model.add_product(product_data=data)
        messagebox.showinfo('Sucesso!!!',
                            'Produto cadastrado com sucesso.')

        self.view.clear_fields()


    def choice_image(self,frame):
        image_path = self.view.select_image()

        if image_path:
            self.view.display_image(frame=frame, image_path=image_path, x=70, y=230)

        else:
            messagebox.showwarning('AVISO!!!',
                                   'Escolha uma imagem!')
            
