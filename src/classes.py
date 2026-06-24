import json


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self.__price:
            answer = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {value}? (y/n): ")
            if answer.lower() == 'y':
                self.__price = value
            else:
                print("Понижение цены отменено")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product) -> None:
        self.__products.append(product)
        Category.product_count += 1

    def add_product_with_check(self, product) -> None:
        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                if product.price > existing_product.price:
                    existing_product.price = product.price
                return
        self.add_product(product)

    @property
    def products(self) -> str:
        result = ""
        for product in self.__products:
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
