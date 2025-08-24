class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Customer:
    def __init__(self, full_name, email, phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

class Order:
    def __init__(self, customer_name, product_name, quantity, order_date):
        self.customer_name = customer_name
        self.product_name = product_name
        self.quantity = quantity
        self.order_date = order_date