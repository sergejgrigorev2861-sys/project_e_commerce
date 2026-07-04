import pytest

from src.classes import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def sample_product():
    return Product("Test Product", "Description", 100.0, 10)


@pytest.fixture
def sample_smartphone():
    return Smartphone("S23", "desc", 100, 5, 95.5, "S23", 128, "black")


@pytest.fixture
def sample_grass():
    return LawnGrass("Grass", "desc", 50, 10, "RU", "7 days", "green")


@pytest.fixture
def sample_category():
    return Category("Test Category", "Description", [])
