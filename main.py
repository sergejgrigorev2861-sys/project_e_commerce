from src.classes import load_products_from_json


if __name__ == "__main__":
    categories = load_products_from_json("data/products.json")

    for cat in categories:
        print(f"Категория: {cat.name}")
        print(f"Описание: {cat.description}")
        print(f"Количество товаров: {len(cat.products)}")
        print("-" * 40)

        for product in cat.products:
            print(f"  - {product.name} | {product.price} руб. | {product.quantity} шт.")
        print()