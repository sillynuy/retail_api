from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=40)

    def __str__(self):
        return self.product_name


class Store(models.Model):
    store_name = models.CharField(max_length=40)
    product = models.ManyToManyField(Product, through='Remain')

    def __str__(self):
        return self.store_name


class Remain(models.Model):
    store = models.ForeignKey(Store, related_name='remains', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='remain2p', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        unique_together = (('store', 'product'),)

    def __str__(self):
        return f'{self.product}: {self.amount}'


class Purchase(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField()


class Supply(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField()
