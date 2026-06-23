from src.classes import Category, Product, load_products_from_json


def test_product_init():
    """Тест: корректная инициализация Product"""
    product = Product("Ноутбук", "Игровой ноутбук", 150000.0, 3)
    assert product.name == "Ноутбук"
    assert product.description == "Игровой ноутбук"
    assert product.price == 150000.0
    assert product.quantity == 3


def test_product_another():
    """Тест: другой Product"""
    product = Product("Наушники", "Беспроводные", 5000.0, 10)
    assert product.name == "Наушники"
    assert product.price == 5000.0
    assert product.quantity == 10


def test_category_init():
    """Тест: корректная инициализация Category"""
    p1 = Product("Товар1", "Описание1", 100.0, 1)
    p2 = Product("Товар2", "Описание2", 200.0, 2)
    category = Category("Электроника", "Всё для дома", [p1, p2])

    assert category.name == "Электроника"
    assert category.description == "Всё для дома"
    assert len(category._products) == 2


def test_category_counters():
    """Тест: автоматическое обновление счётчиков категорий и продуктов"""
    # Сбрасываем счётчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    p3 = Product("P3", "D3", 30.0, 3)

    Category("Cat1", "Desc1", [p1])
    Category("Cat2", "Desc2", [p2, p3])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_product_count_after_category():
    """Тест: product_count обновляется при создании новой категории"""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("A", "A desc", 10.0, 1)
    p2 = Product("B", "B desc", 20.0, 2)
    Category("Cat", "Desc1", [p1, p2])

    assert Category.product_count == 2


def test_load_from_json():
    categories = load_products_from_json("data/products.json")
    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"
    assert len(categories[0]._products) == 3


def test_add_product():
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Тест", "Описание", [])
    product = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(product)
    assert len(category._products) == 1
    assert Category.product_count == 1


def test_product_property():
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Тест", "Описание", [])
    product = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(product)
    expected = "Телефон, 10000 руб. Остаток: 5 шт.\n"
    assert category.products == expected


def test_new_product():
    data = {"name": "Телефон", "description": "Смартфок", "price": 10000, "quantity": 5}
    product = Product.new_product(data)
    assert product.name == "Телефон"
    assert product.price == 10000
    assert product.quantity == 5


def test_price_setter_positive():
    product = Product("Телефон", "Смартфон", 10000, 5)
    product.price = 15000
    assert product.price == 15000


def test_price_setter_zero():
    product = Product("Телефон", "Смартфон", 10000, 5)
    product.price = 0
    assert product.price == 10000
