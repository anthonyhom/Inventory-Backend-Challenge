from itertools import product
from django.shortcuts import get_object_or_404
from .models import Product, City, Warehouse, Stock
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json
from rest_framework import status

# Check if the inventory item exists. If not, create it.
class CreateProductView(APIView):
    def post(self, request, format=None):
        title = request.data['name']
        desc = request.data['description']
        retail_price = request.data['price']
        code = request.data['upc']
        if not (Product.objects.filter(product_code = code).exists()):
            Product.objects.create(product_name = title, product_description = desc, product_msrp = retail_price, product_code = code)
            content = {"detail":"Created new item."}
            return Response(content,status=status.HTTP_201_CREATED)
        else:
            content = {"detail":"Item already exists."}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

# If the inventory item exists, then update the items price. Otherwise throw an error.
# I made the assumption that price can be changed more often than the other fields (name, code, description).
class EditProductView(APIView):
    def post(self, request, format=None):
        new_price = request.data['price']
        code = request.data['upc']
        if Product.objects.filter(product_code = code).exists():
            obj = Product.objects.filter(product_code = code)
            obj.update(product_msrp = new_price)
            content = {"detail":"Updated item."}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {"detail":"Not found."}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
        

# If the inventory item exists, then delete inventory items. Otherwise throw an error.
class DeleteProductView(APIView):
    def post(self, request, format=None):
        code = request.data['upc']
        if Product.objects.filter(product_code = code).exists():
            obj = Product.objects.filter(product_code = code)
            obj.delete()
            content = {"detail":"Deleted item."}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {"detail":"Not found."}
            return Response(content,status=status.HTTP_404_NOT_FOUND)

# Return a list of all inventory items.
class GetAllProductsView(APIView):
    def get(self, request, format=None):
        objs = Product.objects.all()
        serializer = ProductSerializer(objs, many=True)
        d = JSONRenderer().render(serializer.data)
        items = json.loads(d)
        return Response({"item_list":items})

# I made the assumption that a user might also want to search for a specific item.
# Return a searched inventory item.
class GetProductView(APIView):
    def get(self, request, format=None):
        code = request.query_params.get('upc')
        item = get_object_or_404(Product, product_code = code)
        return Response({
            "name": item.product_name,
            "description": item.product_description,
            "msrp": item.product_msrp,
            "upc": item.product_code
        })

# Check if the warehouse exists. If not, create a new warehouse.
class CreateWarehouseView(APIView):
    def post(self, request, format=None):
        building = request.data['building_name']
        street = request.data['street_add']
        city_loc = request.data['city']
        state_loc = request.data['state']
        zip = request.data['zipcode']

        if not (City.objects.filter(city_name = city_loc, state = state_loc, zipcode = zip).exists()):
            City.objects.create(city_name = city_loc, state = state_loc, zipcode = zip)

        city_obj = get_object_or_404(City, city_name = city_loc, state = state_loc, zipcode = zip)

        if not (Warehouse.objects.filter(warehouse_name = building, address = street).exists()):
            Warehouse.objects.create(warehouse_name = building, address = street, city_id = city_obj)
            content = {"detail":"Created new warehouse."}
            return Response(content,status=status.HTTP_201_CREATED)
        else:
            content = {"detail":"Warehouse already exists."}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

# I made the assumption that the user knows what the item and warehouse is. If either of them do not exist in the database, throw an error.
# Check if the inventory item exists in the warehouse. If not, assign the item to the warehouse.
class AssignProductWarehouseView(APIView):
    def post(self, request, format=None):
        code = request.data['upc']
        building = request.data['building_name']
        street = request.data['street_add']
        city_loc = request.data['city']
        state_loc = request.data['state']
        zip = request.data['zipcode']
        stock_amount = request.data['quant']
        item_obj = get_object_or_404(Product, product_code = code)
        city_obj = get_object_or_404(City, city_name = city_loc, state = state_loc, zipcode = zip)
        warehouse_obj = get_object_or_404(Warehouse, warehouse_name = building, address = street, city_id = city_obj)

        if not (Stock.objects.filter(product_id = item_obj, warehouse_id = warehouse_obj).exists()):
            Stock.objects.create(product_id = item_obj, warehouse_id = warehouse_obj, quantity = stock_amount)
            content = {"detail":"Assigned items to warehouse."}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {"detail":"Item is already in warehouse."}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)
        
        