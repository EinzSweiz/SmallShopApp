from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recommend.models import Review
from shop.models import Product, Category

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    detail_link = serializers.HyperlinkedIdentityField(
        view_name='product_detail',
        lookup_field='id'
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all(),
    )
    class Meta:
        model = Product
        fields = ['id', 'detail_link', 'title', 'brand', 'image', 'category', 'price', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'content', 'created_by', 'created_at', 'product_id']
        read_only_fields = ['id', 'created_by', 'created_at']

class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all(),
    )
    discount_price = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    review_create = serializers.HyperlinkedIdentityField(
        view_name='review_create',
        lookup_field='id'
    )
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'brand', 'category',
            'price', 'image', 'available', 'discount',
            'created_at', 'updated_at', 'discount_price', 'reviews', 'review_create'
        ]
        
    def get_discount_price(self, obj):
        return obj.get_discount_price()
    
    def get_reviews(self, obj):
        reviews = Review.objects.all()
        return ReviewSerializer(reviews, many=True).data
    
class CustomerUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        # Generate a unique username from email
        username = email.split('@')[0]

        # Ensure the username is unique
        while User.objects.filter(username=username).exists():
            username = f"{username}_{User.objects.count()}"

        user = User(
            email=email,
            username=username  # Assign the unique username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
