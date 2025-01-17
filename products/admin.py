from django.contrib import admin
from .models import Product, OptionGroup, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1  # Number of blank options shown by default


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'status', 'image_path')

    def image_path(self, obj):
        return obj.image.name  # Display the relative path

    image_path.short_description = 'Image Path'


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_products')
    inlines = [OptionInline]

    def get_products(self, obj):
        # Fetch all associated products and display their names
        return ", ".join([product.name for product in obj.products.all()])

    get_products.short_description = 'Associated Products'


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
