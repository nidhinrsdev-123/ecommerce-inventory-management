import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from shop.models import Product,Order,OrderItem
@pytest.mark.django_db
def test_checkout_decrements_stock_and_totals_order():
 u=get_user_model().objects.create_user(username="buyer",password="password123")
 p=Product.objects.create(sku="KB-1",name="Keyboard",price=Decimal("25.00"),stock_quantity=5)
 c=APIClient(); c.force_authenticate(user=u); r=c.post("/api/orders/",{"items":[{"product":p.id,"quantity":2}]},format="json")
 assert r.status_code==201 and r.data["total"]=="50.00"
 p.refresh_from_db(); assert p.stock_quantity==3
@pytest.mark.django_db
def test_insufficient_stock_rolls_back_checkout():
 u=get_user_model().objects.create_user(username="buyer2",password="password123")
 p=Product.objects.create(sku="M-1",name="Mouse",price=Decimal("10.00"),stock_quantity=1)
 c=APIClient(); c.force_authenticate(user=u); r=c.post("/api/orders/",{"items":[{"product":p.id,"quantity":3}]},format="json")
 assert r.status_code==400 and Order.objects.count()==0
 p.refresh_from_db(); assert p.stock_quantity==1
@pytest.mark.django_db
def test_customer_cannot_advance_order_to_paid():
 u=get_user_model().objects.create_user(username="buyer3",password="password123")
 p=Product.objects.create(sku="P-1",name="Pen",price=Decimal("2.00"),stock_quantity=2)
 o=Order.objects.create(customer=u); OrderItem.objects.create(order=o,product=p,quantity=1,unit_price=p.price)
 c=APIClient(); c.force_authenticate(user=u)
 assert c.post(f"/api/orders/{o.id}/transition/",{"status":"paid"},format="json").status_code==400
