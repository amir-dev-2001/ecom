from .models import Product, User, Order, OrderItem
from rest_framework.serializers  import ModelSerializer, HyperlinkedModelSerializer, ReadOnlyField, PrimaryKeyRelatedField


class ProductSerializer(ModelSerializer):
#     extra_kwargs = {
#             'user': {'read_only': True}
# }

    user = ReadOnlyField(source='product.user')
    
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'is_avaliable', 
            'price',
            'discount',
            'user',
            
        ]
        optional_fields = [
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
        ]    

        def create(self, validated_data):
            user = validated_data[user]
            if user:
                instance.save()
                
                
                
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
                
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):        
        password = validated_data.pop('password', None)
        instance =  self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save() 
        return instance      
    
    
class UserProfileSerializer(ModelSerializer):
    
    extra_kwargs = {
            'username': {'read_only': True},
            'password': {'read_only': True}

}
    
    
    class Meta: 
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code']
        optional_fields = ['password', 'username' ]

       
    def update(self, instance, validated_data):
        instance.name = validated_data.get('id', instance.username)
        instance.save()
        return instance  

    
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
                

class OrderAddSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'       
        
class OrderItemAddSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'                
                

# class OrderItemSerializer(ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ('order','product', 'count')
        
# class OrderDetailAPIView(ModelSerializer):
    
#     order = PrimaryKeyRelatedField(queryset=Order.objects.all())
    
#     class Meta:
#         model = OrderItem
#         fields = ('product', 'order')
#         depth = 1
