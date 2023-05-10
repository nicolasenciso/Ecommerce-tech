from .serializers import ProductSerializer, ManufacturerSerializer, \
    ProductTypeSerializer, RoleSerializer, ClientSerializer, MakePurchaseSerializer, \
    PurchaseSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.models import Product, Manufacturer, ProductType, Role, Client, Purchase, ClientProducts
from decimal import Decimal
from django.db import transaction

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)


class ManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()
    permission_classes = (IsAuthenticated,)


class ProductTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()
    permission_classes = (IsAuthenticated,)


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (IsAdminUser,)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (IsAuthenticated,)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def make_purchase(request):
    serialized = MakePurchaseSerializer(data=request.data, many=True)

    if serialized.is_valid():
        total_cost = Decimal(0.0)
        with transaction.atomic():
            for purchase in request.data:
                total_cost += Product.objects.filter(id_product=purchase.get('id_product')) \
                    .values('price_product')[0]['price_product']

            new_purchase = Purchase(client_id=purchase.get('id_client'), total_cost_purchase=total_cost)

            if not new_purchase.save():
                Response(status=status.HTTP_400_BAD_REQUEST)

            for cli_pur in request.data:
                if not ClientProducts(client_id=cli_pur.get('id_client'), product_id=cli_pur.get('id_product'),
                                      purchase_id=new_purchase.id_purchase).save():
                    return Response('Not able to save register', status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response('some required data is missing', status=status.HTTP_400_BAD_REQUEST)

    return Response(new_purchase.id_purchase, status=status.HTTP_201_CREATED)
