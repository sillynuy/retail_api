import pytest
from retail_app.views import check_product_in_db, check_enough_in_store
from retail_app import models
from .factories import StoreFactory, ProductFactory, RemainFactory


def test_not_enough(db):
    """
    Тест функции проверки на достаточность товара в магазине.
    Здесь запрашивается больше, чем есть в наличии, поэтому функция должна вернуть False
    """
    store = StoreFactory.create()
    product = ProductFactory.create()
    remain = RemainFactory.create(store=store, product=product, amount=2)
    assert check_enough_in_store(store, product, 5) is False


def test_enough(db):
    """
    Тест функции проверки на достаточность товара в магазине.
    Здесь запрашивается меньше, чем есть в наличии, поэтому функция должна вернуть True
    """
    store = StoreFactory.create()
    product = ProductFactory.create()
    remain = RemainFactory.create(store=store, product=product, amount=2)
    assert check_enough_in_store(store, product, 1) is True


def test_product_in_db(db):
    """
    Тест функции проверки на наличие товара в БД.
    Запрашивается товар, который есть, поэтому функция должна вернуть True
    """
    product = ProductFactory.create()
    assert check_product_in_db(product.id) is True


def test_product_not_in_db(db):
    """
    Тест функции проверки на наличие товара в БД.
    Запрашивается товар, которого нет, поэтому должна вернуть False
    """
    product = ProductFactory.create()
    product_id = product.id
    product.delete()
    assert check_product_in_db(product_id) is False

