from core.models import Product, Manufacturer, ProductType, Role, Client, Purchase
from rest_framework import serializers


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ['id_manufacturer', 'manufacturer_name', 'manufacturer_nit']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        mode = ProductType
        exclude = ('created_at', 'updated_at', )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    product_type = serializers.SerializerMethodField('type_of_product')
    manufacturer = serializers.SerializerMethodField('made_by')

    class Meta:
        model = Product
        fields = '__all__'

    def type_of_product(self, obj):
        return obj.product_type.name_product_type

    def made_by(self, obj):
        return obj.manufacturer.manufacturer_name


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class MakePurchaseSerializer(serializers.Serializer):
    id_client = serializers.IntegerField(required=True)
    id_product = serializers.IntegerField(required=True)
    meta_data = serializers.CharField(required=True)

    def validate(self, attrs):
        client = Client.objects.filter(id_client=attrs['id_client'])
        if not client:
            raise ValueError(f"client id {attrs['id_client']} does not exists")
        product = Product.objects.filter(id_product=attrs['id_product'])
        if not product:
            raise ValueError(f"product id {attrs['id_product']} does not exists")

        return attrs






