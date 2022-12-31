from .models import Product, User, Order
from rest_framework.serializers  import ModelSerializer, HyperlinkedModelSerializer, ReadOnlyField


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
            'image',
            'user',
            
        ]
        
        def create(self, validated_data):
            user = validated_data[user]
            if user:
                instance.save()
                
                
                
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'address', 'postal_code']
                
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
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('username', instance.username)
        instance.save()
        return instance  
    
    
class OrderSerializer(ModelSerializer):
    # items = ProductSerializer(read_only=False, many=True)
    extra_kwargs = {
            'user': {'read_only': True}
}


    class Meta:
        model = Order
        fields = ('user','product_id', 'total_amount')
                
        # TODO: add product and quantity    
        
    # def create(self, validated_data):
    #         user = validated_data[user]
    #         print(user)   
    #         if user:
    #             instance.save()
                
        
class UserProfileSerializer(ModelSerializer):
    # user = UserSerializer(required=True, many=False)
    # games = UserGameProfileSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'address',] 
        read_only_fields = ('id', )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('password')
        username = self.data['username']
        user = User.objects.get(username=username)
        # print (user)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)
        instance.save()
        return instance        