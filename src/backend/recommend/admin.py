from django.contrib import admin
from .models import Review



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'created_by', 'created_at', 'content', 'rating']
    search_fields = ['created_by']
    list_filter = ['created_at', 'product']