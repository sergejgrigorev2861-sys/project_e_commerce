import json
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def get_info(selfself) -> str:
        pass  # pragma: no cover


class ReprMixin:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.description!r}, {self.price}, {self.quantity})"


class Product(BaseProduct, ReprMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def get_info(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __str__(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return (self.__price * self.quantity) + (other.__price * other.quantity)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
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


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"Название категории: {self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> "CategoryIterator":
        return CategoryIterator(self)

    def add_product(self, product: "Product") -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    def add_product_with_check(self, product: "Product") -> None:
        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                if product.price > existing_product.price:
                    existing_product.price = product.price
                return
        self.add_product(product)

    def get_products(self) -> list:
        return self.__products

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


class CategoryIterator:
    def __init__(self, category: "Category") -> None:
        self.__category = category
        self.__products = category.get_products()
        self.__index = 0

    def __iter__(self) -> "CategoryIterator":
        self.__index = 0
        return self

    def __next__(self) -> "Product":
        if self.__index < len(self.__products):
            product = self.__products[self.__index]
            self.__index += 1
            return product
        raise StopIteration
