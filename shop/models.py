from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
class Product(models.Model):
 sku=models.CharField(max_length=40,unique=True); name=models.CharField(max_length=180); description=models.TextField(blank=True)
 price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
 stock_quantity=models.PositiveIntegerField(default=0); is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return f"{self.sku} - {self.name}"
class Order(models.Model):
 class Status(models.TextChoices):
  PENDING="pending","Pending"; PAID="paid","Paid"; SHIPPED="shipped","Shipped"; DELIVERED="delivered","Delivered"; CANCELLED="cancelled","Cancelled"
 customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="orders")
 status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
 total=models.DecimalField(max_digits=12,decimal_places=2,default=0); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=["-created_at"]
class OrderItem(models.Model):
 order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items"); product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name="order_items")
 quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)]); unit_price=models.DecimalField(max_digits=10,decimal_places=2)
