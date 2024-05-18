import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='tauan',
    password='tauan2143',
    database='sininhobaby'
)

class ProductModel:
    def __init__(self):
        self.cursor = mydb.cursor()
        
    def search_products(self):
        products = []
        sql = 'select * from loja'
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        for product in row:
            products.append(product)

        return products
    
    def add_product(self, nome, preco, imagem, estoque):
        sql = 'insert into loja(nome, preco, imagem, estoque) values (%(nome)s, %(preco)s, %(imagem)s, %(estoque)s)'

        data = {
            'nome': nome,
            'preco': preco,
            'imagem': imagem,
            'estoque': estoque
        }

        with mydb.cursor() as cursor:
            cursor.execute(sql, data)

        mydb.commit()


    def delete_product(self, id):
        sql = 'delete from loja where id_produto = %(id)s'
        data = {
            'id': id
        }

        self.cursor.execute(sql, data)
        mydb.commit()


    def update_product(self, nome, preco, imagem, estoque):
        sql = 'update loja set nome = %(nome)s, preco = %(preco)s, imagem = %(imagem)s, estoque = %(estoque)s'

        data = {
            'nome': nome,
            'preco': preco,
            'imagem': imagem,
            'estoque': estoque
        }

        with mydb.cursor() as cursor:
            cursor.execute(sql, data)

        mydb.commit()

    
    def search_product_by_name(self, name):
        product_by_name = []
        sql = 'select * from loja where nome = %(name)s'
        data = {
            'name': name
        }

        self.cursor.execute(sql, data)
        row = self.cursor.fetchall()
        for product in row:
            product_by_name.append(product)


        return product_by_name