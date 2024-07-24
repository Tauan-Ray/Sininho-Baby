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
    
    
    def product_by_code(self, code):
        return self.model.search_product_by_code(code)
    
    
    def product_data(self, product_code, product_name, price_product, stock_product, image_product = None):
        try:
            price_product_temp = str(price_product)
            if ',' in price_product_temp:
                price_product_temp = price_product_temp.replace(',', '.')

            
            price_product = float(price_product_temp)
            stock_product = int(stock_product)


        except ValueError:
            messagebox.showerror('ERROR!!!', 
                                'Campo preço ou estoque com valores inválidos!')
            return


        return {
            'product_code': product_code,
            'name': product_name,
            'price': price_product,
            'image': image_product,
            'stock': stock_product
        }
    

    def register_product_database(self, product_code, product_name, price_product, stock_product, image_product=None):
        product_data = self.product_data(product_code, product_name, price_product, stock_product, image_product)
        
        self.model.add_product(product_data=product_data)
        self.view.clear_fields()

    
    def update_product_database(self, code_product, name_product, price_product, stock_product, image_product=None):
        product_data = self.product_data(code_product, name_product, price_product, stock_product, image_product)
        product_data['old_code'] = self.view.old_code
        

        self.model.update_product(product_data=product_data)
        
        self.view.clear_fields()
        self.view.screen_products()


    def delete_product_database(self, response, code):
        if response:
            self.model.delete_product(code = code)
            messagebox.showinfo('Sucesso!!!',
                                'Produto deletado com sucesso!')
            
            self.view.update(self.view.list_products)



    def choice_image(self,frame):
        try:
            self.view.image_label.destroy()

        except AttributeError:    
            pass
        
        image_path = self.view.select_image()

        if image_path:
            self.view.display_image(frame=frame, image_path=image_path, x=70, y=234)

        else:
            messagebox.showwarning('AVISO!!!',
                                   'Escolha uma imagem!')
            
