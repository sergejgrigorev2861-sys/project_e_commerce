import json


class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value

    @classmethod
    def new_product(cls, product_data: dict):
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self._products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        result = ""
        for product in self._products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result


def load_products_from_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = []
    for cat_data in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                quantity=p["quantity"]
            )
            for p in cat_data["products"]
        ]

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products
        )
        categories.append(category)

    return categories
