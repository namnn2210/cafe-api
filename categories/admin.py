from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'status')
    list_filter = ('status',)
    search_fields = ('name',)
