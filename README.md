# E-commerce проект

## Описание

Проект представляет собой ядро для интернет-магазина. Реализованы основные сущности:

- **Product** — товар (название, описание, цена, количество)
- **Category** — категория товаров (название, описание, список товаров)

## Установка

```
git clone https://github.com/sergejgrigorev2861-sys/project_e_commerce.git
cd project_e_commerce
poetry install
```
## Ссылка на репозиторий
https://github.com/sergejgrigorev2861-sys/project_e_commerce

## Покрытие тестами

100% (6 тестов)

## Отчёт о покрытии

```
poetry run pytest --cov=src --cov-report=html
```

## Лицензия

Проект распространяется под лицензией MIT.