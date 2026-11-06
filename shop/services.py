from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Product,Order,OrderItem
@transaction.atomic
def create_order(*,customer,items):
 ids=sorted({x["product"] for x in items})
 products={x.id:x for x in Product.objects.select_for_update().filter(id__in=ids,is_active=True)}
 if len(products)!=len(ids): raise ValidationError({"items":"One or more products do not exist or are inactive."})
 order=Order.objects.create(customer=customer); total=Decimal("0.00")
 for item in items:
  product=products[item["product"]]; qty=item["quantity"]
  if product.stock_quantity<qty: raise ValidationError({"items":f"Insufficient stock for {product.sku}."})
  product.stock_quantity-=qty; product.save(update_fields=["stock_quantity"])
  OrderItem.objects.create(order=order,product=product,quantity=qty,unit_price=product.price)
  total+=product.price*qty
 order.total=total; order.save(update_fields=["total"])
 return order
