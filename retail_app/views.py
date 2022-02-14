from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from retail_app.models import Store, Product, Remain, Supply
from retail_app.serializers import StoreSerializerListed, StoreSerializer


@api_view(['GET'])
def stores_list(request):
    """
    Список магазинов
    """
    if request.method == 'GET':
        queryset = Store.objects.all()
        serializer = StoreSerializerListed(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def stores_detailed(request, store_id):
    """
    Данные по магазину с остатками товаров
    """
    if request.method == 'GET':
        queryset = Store.objects.get(id=store_id)
        serializer = StoreSerializer(queryset)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_store(request, store_id):
    """
    Добавление товаров в магазин
    """
    if request.method == 'POST':
        for row in request.data:
            product_id = row['product_id']
            count = row['count']
            if check_product_in_db(row['product_id']):
                product_instance = Product.objects.get(id=product_id)
                store_instance = Store.objects.get(id=store_id)
                # проверка на наличие строки в таблице remains,
                # чтобы не нарушать условие уникальности сочетания product-store
                # если строка есть, то она изменяется, если нет - создаётся
                try:
                    Remain.objects.get(store=store_instance, product=product_instance)
                except Remain.DoesNotExist:
                    Remain.objects.create(
                        store=store_instance,
                        product=product_instance,
                        amount=count
                    )
                else:
                    remain_instances = Remain.objects.select_for_update().filter(
                        store=store_instance,
                        product=product_instance
                    )
                    with transaction.atomic():
                        remain_instances.update(amount=F('amount') + count)
                finally:
                    # добавление данных в таблицу учёта поставок
                    Supply.objects.create(
                        store=store_instance,
                        product=product_instance,
                        amount=count,
                        date=timezone.now()
                    )
            else:
                return Response({"Error: no product in db"})
        return Response({"Success"})


@api_view(['POST'])
def buy_from_store(request, store_id):
    """
    Покупка товаров из магазина
    """
    if request.method == 'POST':
        for row in request.data:
            product_id = row['product_id']
            count = row['count']
            if check_product_in_db(row['product_id']):
                product_instance = Product.objects.get(id=product_id)
                store_instance = Store.objects.get(id=store_id)
                if check_enough_in_store(store_id, product_id, count):
                    remain_instances = Remain.objects.select_for_update().filter(
                        store=store_instance,
                        product=product_instance
                    )
                    with transaction.atomic():
                        remain_instances.update(amount=F('amount') - count)
                    # если остаток товара равен 0 после операции, то строка больше не имеет смысла и удаляется
                    if Remain.objects.get(store=store_instance, product=product_instance).amount == 0:
                        Remain.objects.get(store=store_instance, product=product_instance).delete()
                    return Response({"Success"})
                else:
                    return Response({"Error: no product in store or not enough"})
            else:
                return Response({"Error: no product in DB"})


def check_product_in_db(product_id):
    """
    Проверка на наличие товара (по id) в БД
    """
    try:
        Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return False
    return True


def check_enough_in_store(store_instance, product_instance, demanded_amount):
    """
    Проверка на достаточное для совершения покупки количество товара в магазине
    """
    try:
        remain_instance = Remain.objects.get(store=store_instance, product=product_instance)
    except Remain.DoesNotExist:
        return False
    amount = remain_instance.amount
    if amount < demanded_amount:
        return False
    else:
        return True
