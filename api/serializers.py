from typing import Any, Dict
from api.dataclasses import ProductData
from api.exceptions import OutofStockException, ProductDoesNotExistException
from api.models import Order, Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    products = serializers.JSONField()
    total_price = serializers.FloatField(read_only=True)
    status = serializers.CharField(max_length=7, min_length=9, read_only=True)

    def create(self, validated_data: Dict[str, Any]):
        products = validated_data.get("products", [])
        total_price = 0

        for item in products:
            product_item = ProductData.from_json(data=item)
            try:
                product = Product.objects.get(id=product_item.id)
            except Product.DoesNotExist:
                raise ProductDoesNotExistException(
                    f"Product with id = {product_item.id} does not exist"
                )

            if product.stock < product_item.quantity:
                raise OutofStockException

            total_price += product.price * product_item.quantity

        for product in products:
            product_item = ProductData.from_json(data=product)
            product_obj = Product.objects.get(id=product_item.id)
            product_obj.deduct_product_stock(quantity=product_item.quantity)

        order = Order.objects.create(
            products=products, total_price=total_price, status="pending"
        )

        return order
