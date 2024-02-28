from rest_framework import serializers
from productapp.models import Product ,Category,Product, ProductImage,ProductVariant,Review
from authentication.models import User


   
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

    class Meta:
        model = Product
        fields = ["id", "name", "description", "slug", "inventory", "size","price", "product_image", "uploaded_images", "upload_images", "reviews"]

    def get_product_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def create(self, validated_data):
        upload_images = validated_data.pop("upload_images")
        product = Product.objects.create(**validated_data)
        for image in upload_images:
            new_product_image = ProductImage.objects.create(product=product, image=image)
        return product

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


