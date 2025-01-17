from rest_framework import serializers
from .models import Product, OptionGroup, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['name']


class OptionGroupSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # Include options in the group

    class Meta:
        model = OptionGroup
        fields = ['name', 'options']


class ProductSerializer(serializers.ModelSerializer):
    option_groups = serializers.SerializerMethodField()  # Custom field for options

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'category', 'status', 'option_groups']

    def get_option_groups(self, obj):
        """
        Transform the option groups into the desired structure for the product.
        """
        option_groups = obj.option_groups.prefetch_related('options').all()
        result = {}
        for group in option_groups:
            # Format group name as a key and include its options
            result[group.name] = [option.name for option in group.options.all()]
        return result

