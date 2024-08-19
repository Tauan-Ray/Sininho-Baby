from tkinter import *
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

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


    
    def add_to_car(self, list_purchase, list_car, label):
        try:
            selected_product = list_purchase.curselection()[0]
            name_and_code = list_purchase.get(selected_product)
            code = lambda name_code: name_code[name_code.find('/')+1:]

            products = self.product_by_code(code(name_and_code))

        except:
            self.show_error("Escolha um produto!!!")

        if products[0][4] > 0:
            list_car.insert(END, f"{products[0][1]}/{products[0][0]}")
            new_stock = products[0][4] - 1
            self.update_stock_database(new_stock, products[0][0])

            self.view.total_price += products[0][2]

            label["text"] = f"R${self.view.total_price}"

        else:
            selected_index = list_purchase.curselection()
            if selected_index:
                list_purchase.delete(selected_index)

    
    def create_invoice(self, list_car):
        size_list_car = list_car.size()
        date_hour = datetime.now()
        formated_date = date_hour.strftime("%d-%m-%Y")
        formated_hour = date_hour.strftime("%H:%M:%S")
        self.date_hour_complete = f'{formated_date} - {formated_hour}'

        if size_list_car == 0:
            self.show_error("Adicione produtos no carrinho primeiro.")

        else:
            self.create_pdf(list_car=list_car, pdf_path=f"invoice/Nota fiscal - {self.date_hour_complete}.pdf")
            self.view.show_success("Nota fiscal gerada com sucesso!")
            self.view.screen_purchase()


    def create_pdf(self, pdf_path, list_car):
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=letter)

        cabecalho_fonte = 'font/GreatVibes-Regular.ttf'
        pdfmetrics.registerFont(TTFont("GreatVibes", cabecalho_fonte))


        def line(y):
            pdf_canvas.setStrokeColorRGB(0,0,0)
            pdf_canvas.setLineWidth(1)
            pdf_canvas.line(0, y, 620, y)


        header = 'Sininho Baby \n'
        subtitle = 'Onde o seu bebê encontra conforto'

        # Criando cabeçalho e subtitulo
        header_pdf = pdf_canvas.beginText(180, 745)
        header_pdf.setFont("GreatVibes", 47)
        header_pdf.textLines(header)
        pdf_canvas.drawText(header_pdf)

        subtitle_pdf = pdf_canvas.beginText(160, 700)
        subtitle_pdf.setFont('GreatVibes', 28)
        subtitle_pdf.textLines(subtitle)
        pdf_canvas.drawText(subtitle_pdf)

        line(680)

        # Inserindo campo de data
        date_pdf  = pdf_canvas.beginText(10, 660)
        date_pdf.setFont('Helvetica', 10)
        date_pdf.textLines(f'Data: {self.date_hour_complete}')
        pdf_canvas.drawText(date_pdf)

        # Inserindo contato e endereço
        address_and_contact = f'''emailteste@gmail.com \n
                            Rua teste endereço, 999 \n
                            (99) 99999-9999
        '''

        address_and_contact_pdf = pdf_canvas.beginText(468, 660)
        address_and_contact_pdf.setFont('Helvetica', 10)
        address_and_contact_pdf.textLines(address_and_contact)
        pdf_canvas.drawText(address_and_contact_pdf)

        line(590)

        product_pdf = pdf_canvas.beginText(20, 570)
        product_pdf.setFont('Helvetica-Bold', 12)
        product_pdf.textLines('Produtos')
        pdf_canvas.drawText(product_pdf)

        price_pdf = pdf_canvas.beginText(280, 570)
        price_pdf.setFont('Helvetica-Bold', 12)
        price_pdf.textLines('Preço')
        pdf_canvas.drawText(price_pdf)

        quantity_pdf = pdf_canvas.beginText(390, 570)
        quantity_pdf.setFont('Helvetica-Bold', 12)
        quantity_pdf.textLines('Qtd')
        pdf_canvas.drawText(quantity_pdf)

        total_pdf = pdf_canvas.beginText(500, 570)
        total_pdf.setFont('Helvetica-Bold', 12)
        total_pdf.textLines('Total')
        pdf_canvas.drawText(total_pdf)

        line(560)

        products = list_car.get(0, END)
        count_identical_products = {}

        for product in products:
            if product in count_identical_products:
                count_identical_products[product] += 1
            else:
                count_identical_products[product] = 1

        
        self.y = 540

        for product_name, count_identical_products in count_identical_products.items():
            code = lambda name_code: name_code[name_code.find('/')+1:]
            product = self.product_by_code(code=code(product_name))
            
            name_product = product[0][1]
            price_product = product[0][2]
            quantity_product = count_identical_products
            total_product = (price_product * quantity_product)

            add_product = pdf_canvas.beginText(20, self.y)
            add_product.setFont('Helvetica', 11)
            add_product.textLines(name_product)
            pdf_canvas.drawText(add_product)

            add_price = pdf_canvas.beginText(280, self.y)
            add_price.setFont('Helvetica', 11)
            add_price.textLines(f'R${price_product}')
            pdf_canvas.drawText(add_price)

            add_quantity = pdf_canvas.beginText(398, self.y)
            add_quantity.setFont('Helvetica', 11)
            add_quantity.textLines(str(quantity_product))
            pdf_canvas.drawText(add_quantity)

            add_total_purchase = pdf_canvas.beginText(500, self.y)
            add_total_purchase.setFont('Helvetica', 11)
            add_total_purchase.textLine(f'R${total_product}')
            pdf_canvas.drawText(add_total_purchase)

            self.y -= 25

        
        line(self.y)
        final_value = f"Total da compra: R${self.view.total_price}"
        total = pdf_canvas.beginText(394, self.y-25)
        total.setFont("Helvetica", 15)
        total.textLines(final_value)
        pdf_canvas.drawText(total)

        pdf_canvas.save()
        self.view.total_price = 0