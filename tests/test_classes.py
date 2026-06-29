import pytest

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
    assert "Товар1" in category.products
    assert "Товар2" in category.products


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
    assert "Samsung Galaxy C23 Ultra" in categories[0].products
    assert "Iphone 15" in categories[0].products


def test_add_product():
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Тест", "Описание", [])
    product = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(product)
    assert "Телефон" in category.products
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


def test_add_product_with_check_duplicate():
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Тест", "Описание", [])
    p1 = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(p1)

    p2 = Product("Телефон", "Смартфон", 8000, 3)
    category.add_product_with_check(p2)

    # Проверяем, что количество суммировалось (5+3=8)
    assert "Телефон" in category.products
    # Проверяем, что цена осталась максимальной (10000)
    assert "10000" in category.products


def test_add_product_with_check_price_update():
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Тест", "Описание", [])
    p1 = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(p1)

    p2 = Product("Телефон", "Смартфон", 12000, 3)  # цена выше
    category.add_product_with_check(p2)

    # Проверяем, что цена обновилась до 12000
    assert "12000" in category.products


def test_add_product_with_check_new():
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Тест", "Описание", [])
    p1 = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(p1)

    p2 = Product("Планшет", "Планшет", 20000, 2)  # новый продукт
    category.add_product_with_check(p2)

    # Проверяем, что продукт добавлен
    assert "Планшет" in category.products
    assert Category.product_count == 2


def test_price_setter_confirmation(monkeypatch):
    product = Product("Телефон", "Смартфон", 10000, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 8000
    assert product.price == 8000


def test_price_setter_cancel(monkeypatch):
    product = Product("Телефон", "Смартфон", 10000, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 8000
    assert product.price == 10000  # цена не изменилась


def test_product_str():
    product = Product("Телефон", "Смартфон", 10000, 5)
    assert str(product) == "Телефон, 10000 руб. Остаток: 5 шт."


def test_product_add():
    p1 = Product("A", "desc", 100, 10)
    p2 = Product("B", "desc", 200, 2)
    assert p1 + p2 == 1400.0


def test_category_str():
    category = Category("Тест", "Описание", [])
    product = Product("Телефон", "Смартфон", 10000, 5)
    category.add_product(product)
    assert str(category) == "Название категории: Тест, количество продуктов: 5 шт."


def test_category_iterator():
    """Тест: итератор категории перебирает все продукты."""
    category = Category("Тест", "Описание", [])
    p1 = Product("A", "desc A", 100.0, 5)
    p2 = Product("B", "desc B", 200.0, 3)
    category.add_product(p1)
    category.add_product(p2)

    products = [product.name for product in category]
    assert products == ["A", "B"]


def test_category_iterator_iter_method():
    category = Category("Тест", "Описание", [])
    p1 = Product("A", "desc A", 100.0, 5)
    p2 = Product("B", "desc B", 200.0, 3)
    category.add_product(p1)
    category.add_product(p2)

    iterator1 = category.__iter__()   # прямой вызов
    assert next(iterator1) == p1
    assert next(iterator1) == p2

    # Повторный вызов __iter__ должен дать НОВЫЙ итератор
    iterator2 = category.__iter__()
    assert next(iterator2) == p1
    assert next(iterator2) == p2

    # iterator1 и iterator2 — разные объекты
    assert iterator1 is not iterator2


def test_category_iterator_next():
    category = Category("Тест", "Описание", [])
    p1 = Product("A", "desc A", 100.0, 5)
    category.add_product(p1)

    iterator = iter(category)
    assert next(iterator) == p1

    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iterator_iter_on_iterator():
    category = Category("Тест", "Описание", [])
    p1 = Product("A", "desc A", 100.0, 5)
    category.add_product(p1)

    iterator = iter(category)          # создаём итератор
    iterator2 = iter(iterator)         # вызываем __iter__ на итераторе

    assert next(iterator2) == p1       # должен вернуть первый продукт
