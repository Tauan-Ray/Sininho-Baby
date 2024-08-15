import mysql.connector
from View import view

class ProductModel:
    def __init__(self):
        self.temp_db = mysql.connector.connect(
            host='localhost',
            user='tauan',
            password='tauan2143'
        )
        self.temp_cursor = self.temp_db.cursor()
        
        self.create_database()

        self.temp_cursor.close()
        self.temp_db.close()


        self.mydb = mysql.connector.connect(
            host='localhost',
            user='tauan',
            password='tauan2143',
            database='Sininho_Baby'
        )
        self.cursor = self.mydb.cursor()

        self.create_table()

        self.view = view


    def create_database(self):
        self.temp_cursor.execute('create database if not exists Sininho_Baby')


    def create_table(self):
        sql = """
        create table if not exists products(
            product_code varchar(8) not null primary key,
            name varchar(200) not null,
            price double not null,
            image tinytext,
            stock int not null
        )
        """

        self.cursor.execute(sql)
        self.mydb.commit()

    def search_products(self):
        products = []
        sql = 'select * from products'
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        for product in row:
            products.append(product)

        return products
    

    def product_data(self, product_code, product_name, price_product, stock_product, image_product = None):
        try:
            price_product_temp = str(price_product)
            if ',' in price_product_temp:
                price_product_temp = price_product_temp.replace(',', '.')

            
            price_product = float(price_product_temp)
            stock_product = int(stock_product)


        except ValueError:
            raise ValueError('Campo preço ou estoque com valores inválidos!')


        return {
            'product_code': product_code,
            'name': product_name,
            'price': price_product,
            'image': image_product,
            'stock': stock_product
        }
        
    
    def add_product(self, product_data):
        sql = 'insert into products(product_code, name, price, image, stock) values (%(product_code)s, %(name)s, %(price)s, %(image)s, %(stock)s)'

        with self.mydb.cursor() as cursor:
            try:
                cursor.execute(sql, product_data)

            except mysql.connector.errors.IntegrityError:
                raise ValueError("Produto com código inserido ja existente.")
                

        self.mydb.commit()


    def delete_product(self, code):
        sql = 'delete from products where product_code = %(product_code)s'
        data = {
            'product_code': code
        }

        self.cursor.execute(sql, data)
        self.mydb.commit()


    def update_product(self, product_data):
        sql = 'update products set product_code = %(product_code)s, name = %(name)s, price = %(price)s, image = %(image)s, stock = %(stock)s WHERE product_code = %(old_code)s'

        with self.mydb.cursor() as cursor:
            try:
                cursor.execute(sql, product_data)

            except mysql.connector.errors.IntegrityError:
                raise ValueError("Produto com código inserido ja existente.")

        self.mydb.commit()

    
    def search_product_by_code(self, code):
        product_by_code = []
        sql = 'select * from products where product_code = %(product_code)s'
        data = {
            'product_code': code
        }

        self.cursor.execute(sql, data)
        row = self.cursor.fetchall()
        for product in row:
            product_by_code.append(product)


        return product_by_code
    

    def update_stock(self, new_stock, product_code):
        sql = 'update products set stock = %(new_stock)s WHERE product_code = %(product_code)s'

        data = {
            "new_stock": new_stock,
            "product_code": product_code
        }

        with self.mydb.cursor() as cursor:
            cursor.execute(sql, data)
            self.mydb.commit()


