import factory
from faker import Faker
from retail_app import models

fake = Faker('ru_RU')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    product_name = "продукт"


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Store

    store_name = fake.street_name()


class RemainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Remain

    store = factory.SubFactory(StoreFactory)
    product = factory.SubFactory(ProductFactory)
    amount = 10
