import sqlite3
import csv
import os
import re

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.import_from_csv()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Склад (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                наименование_товара TEXT UNIQUE,
                цена REAL,
                количество_товара INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Покупатели (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                фамилия_имя TEXT UNIQUE,
                электронная_почта TEXT,
                телефон TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Заказы (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                фамилия_имя TEXT,
                наименование_товара TEXT,
                количество_покупок INTEGER,
                дата_покупки TEXT,
                FOREIGN KEY (фамилия_имя) REFERENCES Покупатели(фамилия_имя),
                FOREIGN KEY (наименование_товара) REFERENCES Склад(наименование_товара)
            )
        ''')
        self.conn.commit()

    def import_from_csv(self):
        # Импорт склада
        if os.path.exists('Sklad.csv'):
            with open('Sklad.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.cursor.execute(
                        'INSERT OR IGNORE INTO Склад (наименование_товара, цена, количество_товара) VALUES (?, ?, ?)',
                        (row['Наименование товара'], float(row['Цена']), int(row['Количество товара']))
                    )
            self.conn.commit()

    def export_to_csv(self):
        # Экспорт склада
        with open('Sklad.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Наименование товара', 'Цена', 'Количество товара'])
            self.cursor.execute('SELECT * FROM Склад')
            for row in self.cursor.fetchall():
                writer.writerow(row[1:])
        
        # Экспорт покупателей
        with open('Clients.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Фамилия Имя', 'Электронная почта', 'Телефон'])
            self.cursor.execute('SELECT * FROM Покупатели')
            for row in self.cursor.fetchall():
                writer.writerow(row[1:])
        
        # Экспорт заказов
        with open('Orders.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Фамилия Имя', 'Наименование товара', 'Количество покупок', 'Дата покупки'])
            self.cursor.execute('SELECT * FROM Заказы')
            for row in self.cursor.fetchall():
                writer.writerow(row[1:])

    def get_customers(self):
        self.cursor.execute("SELECT фамилия_имя FROM Покупатели")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_products(self):
        self.cursor.execute("SELECT наименование_товара FROM Склад")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_warehouse_data(self):
        self.cursor.execute("SELECT * FROM Склад")
        return self.cursor.fetchall()
    
    def get_customers_data(self):
        self.cursor.execute("SELECT * FROM Покупатели")
        return self.cursor.fetchall()
    
    def get_orders_data(self):
        self.cursor.execute("SELECT * FROM Заказы")
        return self.cursor.fetchall()
    
    def add_product(self, name, price, quantity):
        self.cursor.execute(
            'INSERT OR REPLACE INTO Склад (наименование_товара, цена, количество_товара) VALUES (?, ?, ?)',
            (name, price, quantity)
        )
        self.conn.commit()
    
    def add_customer(self, full_name, email, phone):
        self.cursor.execute(
            'INSERT OR IGNORE INTO Покупатели (фамилия_имя, электронная_почта, телефон) VALUES (?, ?, ?)',
            (full_name, email, phone)
        )
        self.conn.commit()
    
    def add_order(self, customer_name, product_name, quantity, order_date):
        # Обновление склада
        self.cursor.execute(
            "UPDATE Склад SET количество_товара = количество_товара - ? WHERE наименование_товара = ?",
            (quantity, product_name)
        )
        
        # Добавление заказа
        self.cursor.execute(
            'INSERT INTO Заказы (фамилия_имя, наименование_товара, количество_покупок, дата_покупки) VALUES (?, ?, ?, ?)',
            (customer_name, product_name, quantity, order_date)
        )
        self.conn.commit()
    
    def check_product_quantity(self, product_name):
        self.cursor.execute(
            "SELECT количество_товара FROM Склад WHERE наименование_товара = ?",
            (product_name,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def delete_product(self, product_name):
        self.cursor.execute(
            "DELETE FROM Склад WHERE наименование_товара = ?",
            (product_name,)
        )
        self.conn.commit()
    
    def delete_customer(self, customer_name):
        self.cursor.execute(
            "DELETE FROM Покупатели WHERE фамилия_имя = ?",
            (customer_name,)
        )
        self.conn.commit()
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        pattern = r'^(\+7|8)[0-9]{10}$'
        return re.match(pattern, phone) is not None