import pandas as pd
import requests
import io
from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Product
from .serializers import ProductSerializer
from .utils import check_if_product_is_on_sale

FILE_URL = "https://storage.googleapis.com/appreal_test_bucket/products.csv"


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def upload_products(self, request):
        chunksize = 1000
        try:
            file = self.get_remote_file(FILE_URL)
        except:
            return JsonResponse({'message': 'Error fetching file'}, status=400)

        for chunk in pd.read_csv(io.StringIO(file.decode('utf-8')), chunksize=chunksize):
            product_list = chunk.to_dict(orient='records')
            instances = []
            for product in product_list:
                instance = {
                    'client_id': int(float(product['id'])),
                    'title': product['title'],
                    'description': product['description'],
                    'price': product['price'],
                    'in_stock': True,
                    'sale': check_if_product_is_on_sale(product)
                }
                instances.append(instance)

            try:
                with transaction.atomic():
                    Product.objects.bulk_create([Product(**p) for p in instances],
                                                update_conflicts=True,
                                                unique_fields=['client_id'],
                                                update_fields=['title', 'description', 'price', 'sale', 'in_stock']
                                                )
                return JsonResponse({'message': 'Products uploaded successfully'}, status=200)
            except Exception as e:
                print("Error:", e)

    @action(detail=False, methods=['put'], url_path='(?P<id>[0-9]+)/sold')
    def sold(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.in_stock = False
            product.save()
            return JsonResponse({'message': 'Product sold successfully'}, status=200)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'message': 'Product not found'}, status=404)

    def get_remote_file(self, url):
        response = requests.get(url)
        return response.content