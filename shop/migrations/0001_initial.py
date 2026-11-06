from django.conf import settings
from django.db import migrations,models
import django.core.validators
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
 operations=[
 migrations.CreateModel(name="Product",fields=[
 ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
 ("sku",models.CharField(max_length=40,unique=True)),("name",models.CharField(max_length=180)),
 ("description",models.TextField(blank=True)),("price",models.DecimalField(decimal_places=2,max_digits=10,validators=[django.core.validators.MinValueValidator(0)])),
 ("stock_quantity",models.PositiveIntegerField(default=0)),("is_active",models.BooleanField(default=True)),("created_at",models.DateTimeField(auto_now_add=True))]),
 migrations.CreateModel(name="Order",fields=[
 ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
 ("status",models.CharField(choices=[("pending","Pending"),("paid","Paid"),("shipped","Shipped"),("delivered","Delivered"),("cancelled","Cancelled")],default="pending",max_length=20)),
 ("total",models.DecimalField(decimal_places=2,default=0,max_digits=12)),("created_at",models.DateTimeField(auto_now_add=True)),
 ("updated_at",models.DateTimeField(auto_now=True)),("customer",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="orders",to=settings.AUTH_USER_MODEL))],
 options={"ordering":["-created_at"]}),
 migrations.CreateModel(name="OrderItem",fields=[
 ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
 ("quantity",models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
 ("unit_price",models.DecimalField(decimal_places=2,max_digits=10)),
 ("order",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="items",to="shop.order")),
 ("product",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="order_items",to="shop.product"))])]
