from tkinter import *
class View:
    def __init__(self, root):
        self.root = root

    def create_widgets(self):
        # Criando Frames
        header = Frame(self.root, width=1001, height=50, bg='#ff77bb', relief='raised', borderwidth=1)
        header.place(x=0, y=0)

        menu_frame = Frame(self.root, width=1001, height=53, bg='#0080c0', relief='raised', borderwidth=1)
        menu_frame.place(x=0, y=49)

        frame_main = Frame(self.root, width=1000, height=498, bg='white')
        frame_main.place(x=0, y=102)


        name_store = Label(header,text='Sininho Baby, onde o seu bebê encontra conforto', width=45, height=1, anchor=CENTER, font=('Arial 18 bold'), bg='#ff77bb',fg='black')
        name_store.place(x=240, y=8)


        # Configurando Menu
        button_register_product = Button(menu_frame, text='Cadastrar produto', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2)
        button_register_product.place(x=3, y=2)

        button_products = Button(menu_frame, text='Produtos', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2)
        button_products.place(x=160, y=2)

        button_purchase = Button(menu_frame, text='Compras', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2)
        button_purchase.place(x=317, y=2)

        button_create_pdf_profit = Button(menu_frame, text='Lucro Geral', width=15, height=2, anchor='center', font=(
            'Ivy 9 bold'), relief='raised', overrelief='sunken', bg='white', fg='black', borderwidth=2)
        button_create_pdf_profit.place(x=474, y=2)

        