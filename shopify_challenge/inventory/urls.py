from django.urls import path
from .views import (
    CreateProductView, 
    EditProductView, 
    DeleteProductView, 
    GetProductView, 
    GetAllProductsView,
    CreateWarehouseView,
    AssignProductWarehouseView
)

urlpatterns = [
    path('create_product/', CreateProductView.as_view() ),
    path('edit_product/', EditProductView.as_view() ),
    path('delete_product/', DeleteProductView.as_view() ),
    path('list_products/', GetAllProductsView.as_view() ),
    path('get_product/', GetProductView.as_view() ),
    path('create_warehouse/', CreateWarehouseView.as_view() ),
    path('add_to_warehouse/', AssignProductWarehouseView.as_view() ),
]