import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import Database
from models import Product, Customer, Order

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Система учета заказов")
        self.db = Database()
        
        self.create_widgets()
        self.load_data()
        
        # Добавление начальных данных если база пуста
        if len(self.db.get_warehouse_data()) == 0:
            self.add_initial_data()
        
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')
        
        # Вкладка склада
        self.warehouse_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.warehouse_frame, text='Склад')
        self.create_warehouse_tab()
        
        # Вкладка покупателей
        self.customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.customers_frame, text='Покупатели')
        self.create_customers_tab()
        
        # Вкладка заказов
        self.orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_frame, text='Заказы')
        self.create_orders_tab()
        
        # Кнопка сохранения
        self.save_button = tk.Button(self.root, text="Сохранить данные", command=self.save_data)
        self.save_button.pack(pady=10)

    def create_warehouse_tab(self):
        columns = ('name', 'price', 'quantity')
        self.warehouse_tree = ttk.Treeview(self.warehouse_frame, columns=columns, show='headings')
        self.warehouse_tree.heading('name', text='Наименование товара')
        self.warehouse_tree.heading('price', text='Цена (руб)')
        self.warehouse_tree.heading('quantity', text='Количество')
        
        self.warehouse_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Фрейм для кнопок управления
        manage_frame = ttk.Frame(self.warehouse_frame)
        manage_frame.pack(pady=5)
        
        # Кнопка удаления выбранного товара
        self.delete_product_btn = tk.Button(manage_frame, text="Удалить выбранный товар", command=self.delete_selected_product)
        self.delete_product_btn.pack(side=tk.LEFT, padx=5)
        
        add_frame = ttk.Frame(self.warehouse_frame)
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="Наименование:").grid(row=0, column=0)
        self.product_name = tk.Entry(add_frame)
        self.product_name.grid(row=0, column=1)
        
        tk.Label(add_frame, text="Цена:").grid(row=0, column=2)
        self.product_price = tk.Entry(add_frame)
        self.product_price.grid(row=0, column=3)
        
        tk.Label(add_frame, text="Количество:").grid(row=0, column=4)
        self.product_quantity = tk.Entry(add_frame)
        self.product_quantity.grid(row=0, column=5)
        
        tk.Button(add_frame, text="Добавить товар", command=self.add_product).grid(row=0, column=6, padx=10)

    def create_customers_tab(self):
        columns = ('name', 'email', 'phone')
        self.customers_tree = ttk.Treeview(self.customers_frame, columns=columns, show='headings')
        self.customers_tree.heading('name', text='Фамилия Имя')
        self.customers_tree.heading('email', text='Электронная почта')
        self.customers_tree.heading('phone', text='Телефон')
        
        self.customers_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Фрейм для кнопок управления
        manage_frame = ttk.Frame(self.customers_frame)
        manage_frame.pack(pady=5)
        
        # Кнопка удаления выбранного покупателя
        self.delete_customer_btn = tk.Button(manage_frame, text="Удалить выбранного покупателя", command=self.delete_selected_customer)
        self.delete_customer_btn.pack(side=tk.LEFT, padx=5)
        
        add_frame = ttk.Frame(self.customers_frame)
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="Фамилия Имя:").grid(row=0, column=0)
        self.customer_name = tk.Entry(add_frame)
        self.customer_name.grid(row=0, column=1)
        
        tk.Label(add_frame, text="Email:").grid(row=0, column=2)
        self.customer_email = tk.Entry(add_frame)
        self.customer_email.grid(row=0, column=3)
        
        tk.Label(add_frame, text="Телефон:").grid(row=0, column=4)
        self.customer_phone = tk.Entry(add_frame)
        self.customer_phone.grid(row=0, column=5)
        
        tk.Button(add_frame, text="Добавить покупателя", command=self.add_customer).grid(row=0, column=6, padx=10)

    def create_orders_tab(self):
        columns = ('customer', 'product', 'quantity', 'date')
        self.orders_tree = ttk.Treeview(self.orders_frame, columns=columns, show='headings')
        self.orders_tree.heading('customer', text='Фамилия Имя')
        self.orders_tree.heading('product', text='Товар')
        self.orders_tree.heading('quantity', text='Количество')
        self.orders_tree.heading('date', text='Дата покупки')
        
        self.orders_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        add_frame = ttk.Frame(self.orders_frame)
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="Покупатель:").grid(row=0, column=0)
        self.order_customer = ttk.Combobox(add_frame)
        self.order_customer.grid(row=0, column=1)
        
        tk.Label(add_frame, text="Товар:").grid(row=0, column=2)
        self.order_product = ttk.Combobox(add_frame)
        self.order_product.grid(row=0, column=3)
        
        tk.Label(add_frame, text="Количество:").grid(row=0, column=4)
        self.order_quantity = tk.Entry(add_frame)
        self.order_quantity.grid(row=0, column=5)
        
        tk.Button(add_frame, text="Оформить заказ", command=self.add_order).grid(row=0, column=6, padx=10)

    def load_data(self):
        # Загрузка данных склада
        self.warehouse_tree.delete(*self.warehouse_tree.get_children())
        for row in self.db.get_warehouse_data():
            self.warehouse_tree.insert('', 'end', values=row[1:])
        
        # Загрузка данных покупателей
        self.customers_tree.delete(*self.customers_tree.get_children())
        for row in self.db.get_customers_data():
            self.customers_tree.insert('', 'end', values=row[1:])
        
        # Загрузка данных заказов
        self.orders_tree.delete(*self.orders_tree.get_children())
        for row in self.db.get_orders_data():
            self.orders_tree.insert('', 'end', values=row[1:])
        
        # Обновление комбобоксов
        self.order_customer['values'] = self.db.get_customers()
        self.order_product['values'] = self.db.get_products()

    def add_product(self):
        try:
            name = self.product_name.get()
            price = float(self.product_price.get())
            quantity = int(self.product_quantity.get())
            
            self.db.add_product(name, price, quantity)
            self.load_data()
            
            self.product_name.delete(0, 'end')
            self.product_price.delete(0, 'end')
            self.product_quantity.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def add_customer(self):
        try:
            full_name = self.customer_name.get()
            email = self.customer_email.get()
            phone = self.customer_phone.get()
            
            # Валидация email
            if not self.db.validate_email(email):
                messagebox.showerror("Ошибка", "Некорректный email адрес. Должен содержать @ и точку после него.")
                return
                
            # Валидация телефона
            if not self.db.validate_phone(phone):
                messagebox.showerror("Ошибка", "Некорректный номер телефона. Должен начинаться с 8 или +7 и содержать 10 цифр после этого.")
                return
            
            self.db.add_customer(full_name, email, phone)
            self.load_data()
            
            self.customer_name.delete(0, 'end')
            self.customer_email.delete(0, 'end')
            self.customer_phone.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_order(self):
        try:
            customer = self.order_customer.get()
            product = self.order_product.get()
            quantity = int(self.order_quantity.get())
            
            # Проверка, что количество больше 0
            if quantity <= 0:
                messagebox.showerror("Ошибка", "Количество товара должно быть больше 0!")
                return
            
            # Проверка наличия товара
            available_quantity = self.db.check_product_quantity(product)
            if quantity > available_quantity:
                messagebox.showerror("Ошибка", f"Недостаточно товара на складе. Доступно: {available_quantity}")
                return
            
            # Добавление заказа
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.add_order(customer, product, quantity, order_date)
            
            self.load_data()
            self.order_quantity.delete(0, 'end')
            messagebox.showinfo("Успех", "Заказ успешно оформлен!")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное количество")

    def delete_selected_product(self):
        selected_item = self.warehouse_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите товар для удаления")
            return
            
        product_name = self.warehouse_tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить товар '{product_name}'?"):
            self.db.delete_product(product_name)
            self.load_data()
            messagebox.showinfo("Успех", "Товар успешно удален")

    def delete_selected_customer(self):
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите покупателя для удаления")
            return
            
        customer_name = self.customers_tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить покупателя '{customer_name}'?"):
            self.db.delete_customer(customer_name)
            self.load_data()
            messagebox.showinfo("Успех", "Покупатель успешно удален")

    def save_data(self):
        self.db.export_to_csv()
        messagebox.showinfo("Успех", "Данные сохранены в CSV файлы")

    def add_initial_data(self):
        initial_products = [
            ('Ноутбук ASUS ROG Strix', 95000, 12)
        ]
        
        for name, price, quantity in initial_products:
            self.db.add_product(name, price, quantity)
        
        self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = App(root)
    root.mainloop()
