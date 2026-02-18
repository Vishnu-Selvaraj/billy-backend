from rest_framework import serializers
from .models import User,Item,Invoice,InvoiceItem
from decimal import Decimal
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_name','price']

class ResponseItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class InvoiceItemInputSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class InvoiceCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    date = serializers.DateField()
    discount = serializers.DecimalField(max_digits=5, decimal_places=1)
    items = InvoiceItemInputSerializer(many=True)

    def validate_customer_id(self, value):
        # check customer exists
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Customer not found.")
        return value

    def validate_items(self, value):
        # check items array is not empty
        if len(value) == 0:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():

            item_ids = [i['item_id'] for i in items_data]
            items_map = Item.objects.in_bulk(item_ids)

            for item_id in item_ids:
                if item_id not in items_map:
                    raise serializers.ValidationError(f"Item {item_id} not found.")

            subtotal = Decimal('0')
            invoice_items = []

            for line in items_data:
                item = items_map[line['item_id']]
                line_total = item.price * line['quantity']
                subtotal += line_total

                invoice_items.append(InvoiceItem(
                    item=item,
                    quantity=line['quantity'],
                    unit_price=item.price,      
                    line_total=line_total,      
                ))

            # calculate grand total
            discount = validated_data['discount']
            grand_total = subtotal - (subtotal * discount / 100)

            # save invoice
            invoice = Invoice.objects.create(
                **validated_data,
                grand_total=grand_total,
            )

            for inv_item in invoice_items:
                inv_item.invoice = invoice

            # save all invoice items in one query
            InvoiceItem.objects.bulk_create(invoice_items)

        return invoice