import pytest

from src.classes import (Category, LawnGrass, Order, Product, Smartphone,
                         load_products_from_json)


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


def test_product_add_same_class_with_fixture(sample_product):
    p1 = sample_product
    p2 = Product("B", "desc", 200, 2)
    assert p1 + p2 == 1000.0 + 400.0  # 100*10 + 200*2


def test_smartphone_str_with_fixture(sample_smartphone):
    phone = sample_smartphone
    assert str(phone) == "S23, 100 руб. Остаток: 5 шт."


def test_lawn_grass_str_with_fixture(sample_grass):
    grass = sample_grass
    assert str(grass) == "Grass, 50 руб. Остаток: 10 шт."


def test_add_product_valid_with_fixture(sample_category, sample_product):
    category = sample_category
    product = sample_product
    category.add_product(product)
    assert len(category.get_products()) == 1


def test_product_add_different_classes_raises():
    phone = Smartphone("S23", "desc", 100, 5, 95.5, "S23", 128, "black")
    grass = LawnGrass("Grass", "desc", 50, 10, "RU", "7 days", "green")
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        _ = phone + grass


def test_add_product_invalid_raises():
    category = Category("Test", "desc", [])
    with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
        category.add_product("not a product")  # type: ignore


def test_base_product_abstract():
    """Тест: BaseProduct — абстрактный класс, нельзя создать напрямую."""
    from src.classes import BaseProduct
    with pytest.raises(TypeError):
        BaseProduct()  # нельзя создать абстрактный класс напрямую


def test_product_inherits_base():
    """Тест: Product наследует BaseProduct."""
    from src.classes import BaseProduct, Product
    product = Product("Тест", "Описание", 100, 5)
    assert isinstance(product, BaseProduct)


def test_product_repr():
    """Тест: repr() возвращает правильную строку."""
    from src.classes import Product
    product = Product("Ноутбук", "Игровой", 150000, 3)
    expected = "Product('Ноутбук', 'Игровой', 150000, 3)"
    assert repr(product) == expected


def test_smartphone_repr():
    """Тест: repr() работает для наследников."""
    from src.classes import Smartphone
    phone = Smartphone("S23", "desc", 100, 5, 95.5, "S23", 128, "black")
    expected = "Smartphone('S23', 'desc', 100, 5)"
    assert repr(phone) == expected


def test_lawn_grass_repr():
    """Тест: repr() работает для LawnGrass."""
    from src.classes import LawnGrass
    grass = LawnGrass("Grass", "desc", 50, 10, "RU", "7 days", "green")
    expected = "LawnGrass('Grass', 'desc', 50, 10)"
    assert repr(grass) == expected


def test_product_get_info():
    """Тест: get_info() возвращает строку с информацией о продукте."""
    from src.classes import Product
    product = Product("Телефон", "Смартфон", 10000, 5)
    expected = "Телефон, 10000 руб. Остаток: 5 шт."
    assert product.get_info() == expected


def test_order_init():
    """Тест: создание заказа."""
    product = Product("A", "desc", 100, 10)
    order = Order(product, 3)
    assert order.product == product
    assert order.quantity == 3
    assert order.total_price == 300


def test_order_get_items():
    """Тест: get_items() возвращает список с продуктом."""
    product = Product("A", "desc", 100, 10)
    order = Order(product, 3)
    assert order.get_items() == [product]


def test_order_get_total_quantity():
    """Тест: get_total_quantity() возвращает количество."""
    product = Product("A", "desc", 100, 10)
    order = Order(product, 3)
    assert order.get_total_quantity() == 3


def test_category_get_items():
    """Тест: get_items() возвращает список продуктов в категории."""
    p1 = Product("A", "desc", 100, 10)
    p2 = Product("B", "desc", 200, 5)
    category = Category("Test", "desc", [p1, p2])
    assert category.get_items() == [p1, p2]


def test_category_get_total_quantity():
    """Тест: get_total_quantity() возвращает общее количество продуктов."""
    p1 = Product("A", "desc", 100, 10)
    p2 = Product("B", "desc", 200, 5)
    category = Category("Test", "desc", [p1, p2])
    assert category.get_total_quantity() == 15


def test_product_zero_quantity():
    from src.classes import ZeroQuantityError
    with pytest.raises(ZeroQuantityError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Test", "desc", 100, 0)


def test_category_middle_price():
    p1 = Product("A", "desc", 100, 5)
    p2 = Product("B", "desc", 200, 3)
    category = Category("Test", "desc", [p1, p2])
    assert category.middle_price() == 150.0


def test_category_middle_price_empty():
    category = Category("Empty", "desc", [])
    assert category.middle_price() == 0


def test_order_zero_quantity():
    from src.classes import ZeroQuantityError
    product = Product("A", "desc", 100, 10)
    with pytest.raises(ZeroQuantityError, match="Товар с нулевым количеством не может быть добавлен"):
        Order(product, 0)
