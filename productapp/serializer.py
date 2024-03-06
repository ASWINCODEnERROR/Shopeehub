from rest_framework import serializers
from productapp.models import Product ,Category,Product, ProductImage,ProductVariant,Review,Rating
from orders.models import Order
from django.contrib.auth.models import User
from django.db.models import Avg


   
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =["category_id","title","slug"]
         
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["date_created", "name", "description"]
        

class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    uploaded_images = ProductImageSerializer(source='images', many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=True),
        write_only=True
    )
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    sku = serializers.CharField(max_length=50)
    availability = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "slug", "inventory", "size","price", "product_image", "uploaded_images", "upload_images", "reviews","rating","sku","availability"]

    def get_product_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def create(self, validated_data):
        upload_images = validated_data.pop("upload_images")
        sku = validated_data.pop("sku")
        availability = validated_data.pop("availability")
        product = Product.objects.create(**validated_data)
        for image in upload_images:
            new_product_image = ProductImage.objects.create(product=product, image=image)
        return product
    
    def get_rating(self,obj):
        ratings = Rating.objects.filter(product_id=obj.id)
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        return average_rating

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['size', "price", 'inventory']
    
    
# =================================================================================================

class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Review
        fields = ["id", "date_created", "name", "description", "product_id"]

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")

        review = Review.objects.create(product=product, **validated_data)
        return review



class RatingSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Rating
        fields = ['product_id', 'rating']
        
    def validate_product_id(self, value):
        request = self.context.get("request")
        if not Order.objects.filter(user=request.user, ordered_products__product__id=value, status="completed").exists():
            raise serializers.ValidationError("You must complete an order for this product to rate it")
        return value