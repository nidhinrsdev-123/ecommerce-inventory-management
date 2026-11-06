from rest_framework import serializers
from .models import Product,Order,OrderItem
class ProductSerializer(serializers.ModelSerializer):
 class Meta:
  model=Product; fields=("id","sku","name","description","price","stock_quantity","is_active","created_at"); read_only_fields=("id","created_at")
class OrderItemSerializer(serializers.ModelSerializer):
 product_name=serializers.CharField(source="product.name",read_only=True)
 class Meta:
  model=OrderItem; fields=("id","product","product_name","quantity","unit_price"); read_only_fields=("id","product_name","unit_price")
class OrderSerializer(serializers.ModelSerializer):
 items=OrderItemSerializer(many=True,read_only=True)
 class Meta:
  model=Order; fields=("id","customer","status","total","items","created_at","updated_at"); read_only_fields=("id","customer","status","total","created_at","updated_at")
class CheckoutSerializer(serializers.Serializer):
 items=serializers.ListField(child=serializers.DictField(),allow_empty=False)
 def validate_items(self,items):
  result=[]
  for item in items:
   if set(item)!={"product","quantity"}: raise serializers.ValidationError("Each item must contain product and quantity only.")
   try: pid=int(item["product"]); qty=int(item["quantity"])
   except (TypeError,ValueError): raise serializers.ValidationError("Product and quantity must be integers.")
   if qty<1: raise serializers.ValidationError("Quantity must be at least 1.")
   result.append({"product":pid,"quantity":qty})
  return result
