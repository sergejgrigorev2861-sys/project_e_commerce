from src.classes import Product, Category


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
    assert len(category.products) == 2
    assert category.products[0] == p1
    assert category.products[1] == p2


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
    from src.classes import load_products_from_json
    categories = load_products_from_json("data/products.json")
    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"
    assert len(categories[0].products) == 3
    assert categories[0].products[0].name == "Samsung Galaxy C23 Ultra"
