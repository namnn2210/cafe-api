from django.urls import path
from .views import ProductListCreateView, ProductDetailView, OptionGroupListCreateView,ProductsByCategoryView,OptionGroupEditView

urlpatterns = [
    path('products', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/option-groups', OptionGroupListCreateView.as_view(), name='option-group-list-create'),
    path('option-groups/', OptionGroupEditView.as_view(), name='option-group-edit'),
    path('products/category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products-by-category'),
]
