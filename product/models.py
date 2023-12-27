from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, default='usd')

    def display_price(self):
        return "{0:.2f}".format(self.price / 100.0)


class Discount(models.Model):
    percentage = models.FloatField(default=0)
    duration = models.CharField(max_length=255, default='once')


class Tax(models.Model):
    tax_name = models.CharField(max_length=255, default='VAT')
    inclusive = models.BooleanField(default=True)
    percentage = models.FloatField(default=13.0)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True
    )
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
    total_amount = models.IntegerField(default=0)
