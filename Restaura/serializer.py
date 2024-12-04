from rest_framework import serializers
from . models import Category, MenuItems,  Order, Cart
from decimal import Decimal
from rest_framework.validators import UniqueValidator
#from rest_framework.validators import UniqueTogetherValidator
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'

#ModelSerializer
class MenuSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax =serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    class Meta:
        model = MenuItems
        fields =['id', 'title' ,'price',  'stock', 'price_after_tax', 'category', 'category_id', 'featured']
        extra_kwargs = {
            'Nombre_Menu': {
                'validators': [
                    UniqueValidator(queryset=MenuItems.objects.all())
                    ]} 
            }  
       
        
    def calculate_tax(self, product:MenuItems):
        return product.price * Decimal(1.1)
    
    def validate(self, attrs):
       if(attrs['price']<2):
           raise serializers.ValidationError('Price should not be less than 2.0')
       if(attrs['inventory']<0):
           raise serializers.ValidationError('Stock cannot be negative')
       return super().validate(attrs)
    
    def validate_empty_values(self, data):
        return super().validate_empty_values(data)
    def validate_title(self, value):
        return bleach.clean(value )
    
#class UserSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = userview
   #     fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

        
        
        