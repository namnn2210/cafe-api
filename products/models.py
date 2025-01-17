from django.db import models
from django.core.validators import MinValueValidator
from categories.models import Category


class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='product_images/')  # Store image path
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


class OptionGroup(models.Model):
    """Represents a group of options, e.g., Sugar Levels, Ice Levels."""
    name = models.CharField(max_length=100)  # e.g., "Sugar Levels", "Ice Levels"
    products = models.ManyToManyField(Product, related_name='option_groups')  # Many-to-many relationship

    def __str__(self):
        return self.name


class Option(models.Model):
    """Represents an individual option within an OptionGroup."""
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)  # e.g., "100", "70", "50", "30"

    def __str__(self):
        return f"{self.name} in {self.group.name}"
