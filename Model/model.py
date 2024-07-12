import mysql.connector

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

    def create_database(self):
        self.temp_cursor.execute('create database if not exists Sininho_Baby')


    def create_table(self):
        sql = """
        create table if not exists products(
            id_product int auto_increment not null primary key,
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
        
    
    def add_product(self, product_data):
        sql = 'insert into products(name, price, image, stock) values (%(name)s, %(price)s, %(image)s, %(stock)s)'

        with self.mydb.cursor() as cursor:
            cursor.execute(sql, product_data)

        self.mydb.commit()


    def delete_product(self, id):
        sql = 'delete from products where id_product = %(id)s'
        data = {
            'id': id
        }

        self.cursor.execute(sql, data)
        self.mydb.commit()


    def update_product(self, nome, preco, imagem, estoque):
        sql = 'update loja set name = %(nome)s, price = %(preco)s, image = %(imagem)s, stock = %(estoque)s'

        data = {
            'nome': nome,
            'preco': preco,
            'imagem': imagem,
            'estoque': estoque
        }

        with self.mydb.cursor() as cursor:
            cursor.execute(sql, data)

        self.mydb.commit()

    
    def search_product_by_name(self, name):
        product_by_name = []
        sql = 'select * from products where name = %(name)s'
        data = {
            'name': name
        }

        self.cursor.execute(sql, data)
        row = self.cursor.fetchall()
        for product in row:
            product_by_name.append(product)


        return product_by_name
