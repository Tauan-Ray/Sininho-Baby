from tkinter import *
from tkinter import filedialog as fd, messagebox
from PIL import Image, ImageTk
from re import match
from Controller.controller import Controller
from Model.model import ProductModel
class View:
    def __init__(self, root):
        self.root = root
        self.model = ProductModel()
        self.controller = Controller(model=self.model, view=self)


    def create_widgets(self):
        # Criando Frames
        header = Frame(self.root, width=1001, height=50, bg='#ff77bb', relief='raised', borderwidth=1)
        header.place(x=0, y=0)

        menu_frame = Frame(self.root, width=1001, height=53, bg='#0080c0', relief='raised', borderwidth=1)
        menu_frame.place(x=0, y=49)

        self.frame_main = Frame(self.root, width=1000, height=498, bg='white')
        self.frame_main.place(x=0, y=102)

        name_store = Label(header,text='Sininho Baby, onde o seu bebê encontra conforto', width=45, height=1, anchor=CENTER, font=('Arial 18 bold'), bg='#ff77bb',fg='black')
        name_store.place(x=240, y=8)


        # Configurando Menu
        button_register_product = Button(menu_frame, text='Cadastrar produto', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2, command=self.screen_register_product)
        button_register_product.place(x=3, y=2)

        button_products = Button(menu_frame, text='Produtos', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2, command=self.screen_products)
        button_products.place(x=160, y=2)
        

        button_purchase = Button(menu_frame, text='Compras', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2, command= self.screen_purchase)
        button_purchase.place(x=317, y=2)

        button_create_pdf_profit = Button(menu_frame, text='Lucro Geral', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2)
        button_create_pdf_profit.place(x=474, y=2)


    def delete_screen(self):
        widgets = self.frame_main.winfo_children()
        for widget in widgets:
            widget.destroy()


    def clear_screen(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def update(self, list, screen_product=False):
        list.delete(0, END)
        products = self.controller.list_products()
        for item in products:
            if item[4] == 0:
                pass
            else:
                list.insert(END, f'{item[1]}/{item[0]}')

        if screen_product:
            list.delete(0, END)
            for item in products:
                if item[4] != 0:
                    list.insert(END, f'{item[1]}/{item[0]}')

                else:
                    messagebox.showwarning('Aviso!!!',
                                        f'O produto {item[1]}/{item[0]} está sem estoque.')
                    
    
    def search_product_code(self, list):
        try:
            selected_product = list.curselection()[0]
            name_and_code = list.get(selected_product)
            code = lambda name_code: name_code[name_code.find('/')+1:]

            product = self.controller.product_by_code(code(name_and_code))

            return product


        except:
            self.show_error("Escolha um produto!!!")


    
    def show_success(self, message):
        messagebox.showinfo("Sucesso", message)

    def show_error(self, message):
        messagebox.showerror("Erro", message)


    def clear_fields(self):
        self.entry_code_product.delete(0, END)
        self.entry_name_product.delete(0, END)
        self.entry_price_product.delete(0, END)
        self.entry_stock_product.delete(0, END)
        try:
            self.image_label.destroy()

        except AttributeError:
            pass


    def screen_products(self):
        self.delete_screen()

        # Criando Frames onde serão mostrados os produtos
        frame_product_left = Frame(
        self.frame_main, width=500, height=502, bg='white')
        frame_product_left.place(x=0, y=0)

        self.frame_product_right = Frame(self.frame_main, width=500, height=502, bg='white')
        self.frame_product_right.place(x=500, y=0)
        self.clear_screen(self.frame_product_right)


        self.list_products = Listbox(frame_product_left, font=(
            'Courier 13'), width=49, height=26, bg='white', fg='black')
        self.list_products.place(x=2, y=0)
        self.update(list=self.list_products, screen_product=True)

        self.search_bar_entry = Entry(self.frame_product_right, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.search_bar_entry.place(x=5, y=5)


        search_bar_button = Button(self.frame_product_right, text='Buscar produto', width=10, height=1, pady=3, anchor='center', font=('Ivy 10'), relief='raised', overrelief='sunken', bg='#D3D3D3', fg='black', borderwidth=2, command=self.search_product)
        search_bar_button.place(x=15, y=35)

        show_product_button = Button(self.frame_product_right, text='Exibir produto', width=15, height=1, pady=5, anchor='center', font=(
        'Ivy 10 '), relief='raised', overrelief='sunken', bg='#007bff', fg='black', borderwidth=2, command=lambda: self.show_infos(list=self.list_products, frame=self.frame_product_right))
        show_product_button.place(x=339, y=139)

        update_product_button = Button(self.frame_product_right, text='Atualizar produto', width=15, height=1, pady=5, anchor='center', font=(
        'Ivy 10 '), relief='raised', overrelief='sunken', bg='#ffc107', fg='black', borderwidth=2, command=self.update_product_screen)
        update_product_button.place(x=339, y= 178)
        
        delete_product_button = Button(self.frame_product_right, text='Deletar produto', width=15, height=1, pady=5, anchor='center', font=(
        'Ivy 10 '), relief='raised', overrelief='sunken', bg='#fa2d4c', fg='black', borderwidth=2, command=self.delete_product)
        delete_product_button.place(x=339, y= 217)
        
        
    def search_product(self):
        code = self.search_bar_entry.get()

        if code == "":
            self.show_error("Insira o código de algum produto.")

        elif bool(match(r"^\d+$", code)):
            product = self.controller.product_by_code(code)

            try:
                self.list_products.delete(0, END)
                self.list_products.insert(END, f'{product[0][1]}/{product[0][0]}')

            except IndexError:
                self.show_error("Produto não encontrado.")
                self.update(list=self.list_products, screen_product=True)


        else:
            self.show_error("Insira apenas números.")
            return

 
    def show_infos(self,list, frame):
        self.clear_screen(frame)

        product = self.search_product_code(list=list)
        if product is None:
            return

        if product is None:
            self.delete_screen()
            self.screen_products()

        else:
            back_button = Button(frame, text='Limpar informações', width=15, height=1, pady=5, anchor='center', font=(
                'Ivy 10'), relief='raised', overrelief='sunken', bg='#007bff', fg='black', borderwidth=2, command=self.screen_products)
            back_button.place(x=330, y=145)


            product_code = Label(frame, text='Código do produto: ',
                                        width=15, height=1, padx=2, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            product_code.place(x=8, y=4)
            
            entry_code_product = Entry(frame, width=30, font=(
                'Arial 13'), justify='left', relief='flat')
            entry_code_product.place(x=162, y=4)

        
            product_name = Label(frame, text='Nome do produto:',
                                        width=15, height=1, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            product_name.place(x=8, y=40)
            
            entry_name_product = Entry(frame, width=30, font=(
                'Arial 13'), justify='left', relief='flat')
            entry_name_product.place(x=162, y=40)


            product_price = Label(frame, text='Preço do produto:',
                                        width=15, height=1, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            product_price.place(x=8, y=76)

            entry_price_product = Entry(frame, width=30, font=(
                'Arial 13'), justify='left', relief='flat', fg='black')
            entry_price_product.place(x=162, y=76)


            stock_product = Label(frame, text='Estoque:',
                                            width=8, height=1, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            stock_product.place(x=7, y=110)

            entry_stock_product = Entry(frame, width=37, font=(
                'Arial 13'), justify='left', relief='flat')
            entry_stock_product.place(x=92, y=110)


            entrys_usadas = [entry_code_product, entry_name_product, entry_price_product, entry_stock_product]

            entry_code_product.insert(0, product[0][0])
            entry_name_product.insert(0, product[0][1])
            entry_price_product.insert(0, product[0][2])
            entry_stock_product.insert(0, product[0][4])

            for entry in entrys_usadas:
                entry['state'] = 'readonly'


            try:
                self.display_image(frame=frame, image_path=product[0][3], x=100, y=250)


            except AttributeError:
                pass

    
    def create_product_components(self, frame):
        product_code = Label(frame, text='Código do produto:', width=15, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        product_code.place(x=7, y=2)

        self.entry_code_product = Entry(frame, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_code_product.place(x=10, y=25)


        product_name = Label(frame, text='Nome do produto:', width=15, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        product_name.place(x=7, y=60)

        self.entry_name_product = Entry(frame, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_name_product.place(x=10, y=83)


        price_product = Label(frame, text='Preço:', width=6, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        price_product.place(x=7, y=118)

        self.entry_price_product = Entry(frame, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_price_product.place(x=10, y=141)


        stock_product = Label(frame, text='Estoque:', width=8, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        stock_product.place(x=6, y=176)

        self.entry_stock_product = Entry(frame, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_stock_product.place(x=10, y=199)

        
        self.add_image_button = Button(frame, text='Adicionar imagem', width=15, height=1, pady=7 ,anchor='center', font=('Ivy 11'), relief='raised', overrelief='sunken', bg='#FF7F50', fg='black', borderwidth=2, command=lambda: self.choice_image(frame=frame))
        self.add_image_button.place(x=108, y=444)

        self.register_product_button = Button(frame, text='Cadastrar produto', width=13, height=1, anchor='center', font=('Ivy 11'), relief='raised', overrelief='sunken', bg='#2ECC71', fg='black', borderwidth=2, command=self.register_product)
        self.register_product_button.place(x=330, y=16)
        

    def update_product_screen(self):
        self.clear_screen(self.frame_product_right)
        
        try:
            selected_product = self.list_products.curselection()[0]
            name_and_code = self.list_products.get(selected_product)
            code = lambda name_code: name_code[name_code.find('/')+1:]

            product = self.controller.product_by_code(code(name_and_code))

            self.old_code = code(name_and_code)


        except:
            self.show_error("Escolha um produto!!!")
            self.screen_products()


        else:
            self.create_product_components(self.frame_product_right)

            self.register_product_button['text'] = 'Atualizar produto'
            self.register_product_button['bg'] = '#ffc107'
            self.register_product_button['command'] = self.update_product
                

            self.entry_code_product.insert(0, product[0][0])
            self.entry_name_product.insert(0, product[0][1])
            self.entry_price_product.insert(0, product[0][2])
            self.entry_stock_product.insert(0, product[0][4])

    
    def update_product(self):
        product_data = self.get_product_data()

        self.controller.update_product_database(
            code_product=product_data['product_code'],
            name_product=product_data['product_name'],
            price_product=product_data['price_product'],
            stock_product=product_data['stock_product'],
            image_product=product_data['image_product']
        )

        self.update(self.list_products)


    def delete_product(self):
        code = self.search_product_code(self.list_products)

        if code is None:
            return
        
        else:
            response = messagebox.askyesno("Confirmar Deleção", "Tem certeza que deseja deletar o produto?")
            self.controller.delete_product_database(response = response, code = code[0][0])


    def screen_register_product(self):
        self.delete_screen()

        frame_register_left = Frame(self.frame_main, width=500, height=600, bg='white', relief='raised', borderwidth=1)
        frame_register_left.place(x=0,y=0)

        frame_register_right = Frame(self.frame_main, width=500, height=600, bg='white', relief='raised', borderwidth=1)
        frame_register_right.place(x=500, y=0)

        self.create_product_components(frame_register_left)

        self.list_products_register = Listbox(frame_register_right, font=('Courier 13'), width=49, height=26, bg='white', fg='black')
        self.list_products_register.place(x=2, y=0)
        self.update(list=self.list_products_register)

    
    def register_product(self):
        product_data = self.get_product_data()
        
        try:
            self.controller.register_product_database(
                product_code=product_data['product_code'],
                product_name=product_data['product_name'],
                price_product=product_data['price_product'],
                stock_product=product_data['stock_product'],
                image_product=product_data['image_product']
            )
        except TypeError:
            pass
        
        else:
            self.update(self.list_products_register)

    
    def get_product_data(self):
        product_code = self.entry_code_product.get()
        product_name = self.entry_name_product.get()
        price_product = self.entry_price_product.get()
        stock_product = self.entry_stock_product.get()

        if not product_code or not product_name or not price_product or not stock_product:
            self.show_error('Preencha todos os campos!')
            return

        image_product = self.image_path if hasattr(self, 'image_path') else None
        

        return {
            'product_code': product_code,
            'product_name': product_name,
            'price_product': price_product,
            'stock_product': stock_product,
            'image_product': image_product
        }
    

    def screen_purchase(self):
        self.delete_screen()
        frame_purchase_left = Frame(self.frame_main, width=500, height=600, bg='white', relief='raised', borderwidth=1)
        frame_purchase_left.place(x=0,y=0)

        frame_purchase_right = Frame(self.frame_main, width=500, height=600, bg='white', relief='raised', borderwidth=1)
        frame_purchase_right.place(x=500, y=0)

        self.list_purchase = Listbox(frame_purchase_left, font=(
            'Courier 13'), width=33, height=26, bg='white', fg='black')
        self.list_purchase.place(x=2, y=0)
        self.update(list=self.list_purchase)


        button_add_to_cart = Button(frame_purchase_left, text='Adicionar ao carrinho', width=14, height=1, pady=6, padx=15 ,anchor='center', font=('Ivy 10'), relief='raised', overrelief='sunken', bg='#FFA500', fg='black', borderwidth=2, command= self.add_to_car)
        button_add_to_cart.place(x=343, y=260)

        button_create_invoice = Button(frame_purchase_right, text='Gerar nota fiscal', width=14, height=1, pady=6, padx=15 ,anchor='center', font=('Ivy 10'), relief='raised', overrelief='sunken', bg='#ADD8E6', fg='black', borderwidth=2, command= self.add_to_car)
        button_create_invoice.place(x=343, y=260)


        self.list_car = Listbox(frame_purchase_right, font=(
            'Courier 13'), width=33, height=26, bg='white', fg='black')
        self.list_car.place(x=0, y=0)


    
    def add_to_car(self):
        products = self.search_product_code(self.list_purchase)
        if products[0][4] > 0:
            self.list_car.insert(END, products[0][1])
            new_stock = products[0][4] - 1
            self.controller.update_stock_database(new_stock=new_stock, product_code=products[0][0])

        else:
            selected_index = self.list_purchase.curselection()
            if selected_index:
                self.list_purchase.delete(selected_index)



    def choice_image(self,frame):
        try:
            self.image_label.destroy()

        except AttributeError:    
            pass
        
        image_path = self.select_image()

        if image_path:
            self.display_image(frame=frame, image_path=image_path, x=70, y=234)

        else:
            self.show_error('Escolha uma imagem!')


    def select_image(self):
        self.image_path = fd.askopenfilename()
        return self.image_path
    

    def display_image(self, frame, image_path, x, y):
        product_image = Image.open(image_path)
        product_image = product_image.resize((250, 250))
        product_image = ImageTk.PhotoImage(product_image)

        self.image_label = Label(frame, image=product_image, width=250, height=200)
        self.image_label.image = product_image # Mantendo referência para evitar a coleta de lixo
        self.image_label.place(x=x, y=y)
    

    def clear_fields(self):
        self.entry_code_product.delete(0, END)
        self.entry_name_product.delete(0, END)
        self.entry_price_product.delete(0, END)
        self.entry_stock_product.delete(0, END)
        try:
            self.image_label.destroy()

        except AttributeError:
            pass
