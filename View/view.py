from tkinter import *
from tkinter import filedialog as fd, messagebox
from PIL import Image, ImageTk
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
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2)
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


    def update(self, list, compra=False):
        list.delete(0, END)
        products = self.controller.list_products()
        for item in products:
            list.insert(END, item[1])

        if compra:
            list.delete(0, END)
            for item in products:
                if item[4] != 0:
                    list.insert(END, item[1])

                else:
                    messagebox.showwarning('Aviso!!!',
                                        f'O produto {item[1]} está sem estoque.')


    def screen_products(self):
        self.delete_screen()

        # Criando Frames onde serão mostrados os produtos
        frame_product_left = Frame(
        self.frame_main, width=500, height=502, bg='white')
        frame_product_left.place(x=0, y=0)

        frame_product_right = Frame(self.frame_main, width=500, height=502, bg='white')
        frame_product_right.place(x=500, y=0)
        self.clear_screen(frame_product_right)



        list_products = Listbox(frame_product_left, font=(
            'Courier 13'), width=49, height=28, bg='white', fg='black')
        list_products.place(x=2, y=0)
        self.update(list=list_products)


        button_show_product = Button(frame_product_right, text='Exibir produto', width=15, height=1, pady=10, anchor='center', font=(
        'Ivy 10 bold'), relief='raised', overrelief='sunken', bg='#ff77bb', fg='black', borderwidth=2, command=lambda: self.show_infos(list=list_products, frame=frame_product_right))
        button_show_product.place(x=330, y=139)


    def show_infos(self,list, frame):
        self.clear_screen(frame)

        try:
            selected_product = list.curselection()[0]
            name = list.get(selected_product)
            product = self.controller.product_by_name(name)


        except:
            messagebox.showerror("Error",
                                    "Escolha um produto!!!")
            self.screen_products()

        else:
            back_button = Button(frame, text='Limpar informações', width=15, height=1, pady=10, anchor='center', font=(
                'Ivy 10 bold'), relief='raised', overrelief='sunken', bg='#ff77bb', fg='black', borderwidth=2, command=self.screen_products)
            back_button.place(x=330, y=139)

        
            product_name = Label(frame, text='Nome do produto:',
                                        width=15, height=1, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            product_name.place(x=3, y=4)
            
            entry_product_name = Entry(frame, width=30, font=(
                'Arial 13'), justify='left', relief='flat')
            entry_product_name.place(x=155, y=4)


            product_price = Label(frame, text='Preço do produto:',
                                        width=15, height=1, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            product_price.place(x=3, y=40)

            entry_product_price = Entry(frame, width=30, font=(
                'Arial 13'), justify='left', relief='flat', fg='black')
            entry_product_price.place(x=155, y=40)


            stock_product = Label(frame, text='Estoque:',
                                            width=8, height=1, anchor=CENTER, font=('Arial 13'), bg='white', fg='black')
            stock_product.place(x=0, y=76)

            entry_stock_product = Entry(frame, width=37, font=(
                'Arial 13'), justify='left', relief='flat')
            entry_stock_product.place(x=83, y=76)


            entrys_usadas = [entry_product_name, entry_product_price, entry_stock_product]

            entry_product_name.insert(0, product[0][1])
            entry_product_price.insert(0, product[0][2])
            entry_stock_product.insert(0, product[0][4])

            for entry in entrys_usadas:
                entry['state'] = 'readonly'


            try:
                self.display_image(frame=frame, image_path=product[0][3], x=100, y=250)


            except IsADirectoryError:
                pass

    
    def screen_register_product(self):
        self.delete_screen()

        frame_register_left = Frame(self.frame_main, width=500, height=600, bg='white', relief='raised', borderwidth=1)
        frame_register_left.place(x=0,y=0)

        frame_register_right = Frame(self.frame_main, width=500, height=600, bg='white', relief='raised', borderwidth=1)
        frame_register_right.place(x=500, y=0)


        product_name = Label(frame_register_left, text='Nome do produto:', width=15, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        product_name.place(x=7, y=2)

        self.entry_product_name = Entry(frame_register_left, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_product_name.place(x=10, y=25)


        price_product = Label(frame_register_left, text='Preço:', width=6, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        price_product.place(x=7, y=60)

        self.entry_price_product = Entry(frame_register_left, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_price_product.place(x=10, y=83)


        stock_product = Label(frame_register_left, text='Estoque:', width=8, height=1, anchor=CENTER, font=('Arial 14'), bg='white',fg='black')
        stock_product.place(x=6, y=118)

        self.entry_stock_product = Entry(frame_register_left, width=30, font=('Arial 13'), justify='left', relief='raised', borderwidth=2)
        self.entry_stock_product.place(x=10, y=141)

        
        add_image_button = Button(frame_register_left, text='Adicionar imagem', width=15, height=2, anchor='center', font=('Ivy 11 bold'), relief='raised', overrelief='sunken', bg='#0080c0', fg='black', borderwidth=2, command=lambda: self.controller.choice_image(frame=frame_register_left))
        add_image_button.place(x=117, y=444)

        register_product_button = Button(frame_register_left, text='Cadastrar produto', width=13, height=1, anchor='center', font=('Ivy 11 bold'), relief='raised', overrelief='sunken', bg='#00ff40', fg='black', borderwidth=2, command=self.register_product)
        register_product_button.place(x=330, y=16)


    
    def register_product(self):
        product_name = self.entry_product_name.get()
        price_product = self.entry_price_product.get()
        stock_product = self.entry_stock_product.get()

        if not product_name or not price_product or not stock_product:
            messagebox.showerror('ERROR!!', 'Preencha todos os campos!')
            return
        

        try:
            self.controller.register_product_database(product_name=product_name, price_product=price_product, stock_product=stock_product, image_product=self.image_path)
  

        except AttributeError:
            self.controller.register_product_database(product_name=product_name, price_product=price_product, stock_product=stock_product)


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
        self.entry_product_name.delete(0, END)
        self.entry_price_product.delete(0, END)
        self.entry_stock_product.delete(0, END)
        try:
            self.image_label.destroy()

        except AttributeError:
            pass
        
