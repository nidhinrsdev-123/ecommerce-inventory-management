from django.db import transaction
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product,Order
from .permissions import StaffWriteOrReadOnly,IsOrderOwnerOrStaff
from .serializers import ProductSerializer,OrderSerializer,CheckoutSerializer
from .services import create_order
class ProductViewSet(viewsets.ModelViewSet):
 serializer_class=ProductSerializer; permission_classes=[StaffWriteOrReadOnly]
 filterset_fields=["is_active"]; search_fields=["name","sku","description"]; ordering_fields=["price","name","created_at"]
 def get_queryset(self):
  qs=Product.objects.all()
  return qs if self.request.user.is_staff else qs.filter(is_active=True)
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
 serializer_class=OrderSerializer; permission_classes=[IsAuthenticated,IsOrderOwnerOrStaff]
 def get_queryset(self):
  qs=Order.objects.prefetch_related("items__product").select_related("customer")
  return qs if self.request.user.is_staff else qs.filter(customer=self.request.user)
 def create(self,request,*args,**kwargs):
  s=CheckoutSerializer(data=request.data); s.is_valid(raise_exception=True)
  order=create_order(customer=request.user,items=s.validated_data["items"])
  return Response(self.get_serializer(order).data,status=status.HTTP_201_CREATED)
 @action(detail=True,methods=["post"])
 def transition(self,request,pk=None):
  order=self.get_object(); target=request.data.get("status")
  allowed={"pending":{"cancelled"},"paid":{"shipped"},"shipped":{"delivered"}}
  if target not in allowed.get(order.status,set()): return Response({"detail":"Invalid order status transition."},status=400)
  if target!="cancelled" and not request.user.is_staff: return Response({"detail":"Only staff can advance fulfillment."},status=403)
  if target=="cancelled":
   with transaction.atomic():
    for item in order.items.select_related("product"):
     item.product.stock_quantity+=item.quantity; item.product.save(update_fields=["stock_quantity"])
    order.status=target; order.save(update_fields=["status","updated_at"])
  else: order.status=target; order.save(update_fields=["status","updated_at"])
  return Response(self.get_serializer(order).data)
