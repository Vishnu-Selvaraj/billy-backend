from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=1, default=0)


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
