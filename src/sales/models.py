from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.shortcuts import reverse, resolve_url

from .utils import generate_code

from products.models import Product
from customers.models import Customer
from profiles.models import Profile




class Position(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  price = models.FloatField(blank=True)
  created = models.DateTimeField(blank=True)

  def save(self, *args, **kwargs):
    self.price = self.product.price * self.quantity
    return super().save(*args, **kwargs)

  def get_sale_id(self):
    # reverse rel between child and parent
    # Sale -> Posistion
    sale = self.sale_set.first()
    return sale.id
  
  def __str__(self):
    return f'id: {self.id}, product: {self.product.name}'



class Sale(models.Model):
  transaction_id = models.CharField(max_length=12, blank=True)
  positions = models.ManyToManyField(Position)
  total_price = models.FloatField(blank=True, null=True)
  customer = models.ForeignKey(Customer, on_delete=CASCADE)
  salesman = models.ForeignKey(Profile, on_delete=CASCADE)
  created = models.DateTimeField(blank=True)
  updated = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    if self.transaction_id == '':
      self.transaction_id = generate_code().upper()
    if self.created is None:
      self.created = timezone.now()
    return super().save(*args, **kwargs)

  def get_positions(self):
    return self.positions.all()

  def get_absolute_url(self) -> str:
    return resolve_url('sales:detail', self.pk)

  def __str__(self):
    return f'Sales for the amount of {self.total_price} rub.'



class CSV(models.Model):
  file_name = models.CharField(max_length=120)
  csv_file = models.FileField(upload_to='csv', null=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.file_name)
