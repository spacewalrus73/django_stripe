from .models import Item, Tax, Order, Discount
from django.contrib import admin

# Register your models here.
admin.site.register([Item, Tax, Order, Discount])
