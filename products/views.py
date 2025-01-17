from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, OptionGroup, Option
from categories.models import Category
from .serializers import ProductSerializer, OptionGroupSerializer
from rest_framework.permissions import IsAuthenticated


class ProductListCreateView(APIView):
    """
    Handles listing all products and creating a new product.
    """

    def get(self, request):
        products = Product.objects.filter(status="active")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a single product.
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class OptionGroupListCreateView(APIView):
    """
    Handles listing all option groups and creating a new group for a product.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        option_groups = OptionGroup.objects.filter(product_id=product_id)
        serializer = OptionGroupSerializer(option_groups, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['product'] = product.id  # Add product ID to the data
        serializer = OptionGroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsByCategoryView(APIView):
    """
    Fetch products by category.
    """

    def get(self, request, category_id):
        try:
            # Check if the category exists
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filter products by the given category
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OptionGroupEditView(APIView):
    """
    Add or update an option group and associate it with multiple products.
    """
    def post(self, request):
        # Request data example:
        # {
        #     "name": "Sugar Levels",
        #     "options": [{"name": "100"}, {"name": "70"}],
        #     "products": [1, 2]  # List of product IDs
        # }
        data = request.data
        products = data.pop('products', [])
        serializer = OptionGroupSerializer(data=data)

        if serializer.is_valid():
            option_group = serializer.save()

            # Associate the option group with products
            for product_id in products:
                try:
                    product = Product.objects.get(id=product_id)
                    option_group.products.add(product)
                except Product.DoesNotExist:
                    return Response({"error": f"Product with ID {product_id} not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
