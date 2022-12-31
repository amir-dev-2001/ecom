from rest_framework.views import APIView
from rest_framework import generics, permissions, exceptions
from django.http import JsonResponse
from .models import Product, User, Order
from .serializers import ProductSerializer, UserSerializer, UserProfileSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.fields import CurrentUserDefault

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

# ----------------------------------------------------------------
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        # Add custom claims
        # token['iat'] = datetime.datetime.now()
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['username'] = user.username
        token['address'] = user.address
        # token['date'] = str(datetime.date.today())

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




# ###
from rest_framework_simplejwt.authentication import JWTAuthentication
def apiList(request):
    JWT_authenticator = JWTAuthentication()
    
    response = JWT_authenticator.authenticate(request)
    if response is not None:
    # unpacking
        user , token = response
        print(response)
        return JsonResponse({'msg' : 'this is decoded token claims', 'data' :token.payload})
    else:
        return JsonResponse({'msg' : 'no token is provided in the header or the header is missing'})

# ----------------------------------------------------------------

class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        
        username = data['username']
        if len(username) != 11 and username[0:2] != '09':
            raise exceptions.APIException('invalid number')

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('passwords do not match')
        
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
class LoginAPIView(APIView):
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
    
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        
        
        if user is None:
            raise exceptions.AuthenticationFailed('invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('invalid credentials')
        if response is not None:
            user , token = response
            print(response)
            print(response[1]['username'])            
            print(username)
            if username != response[1]['username']:
                raise exceptions.AuthenticationFailed('invalid credentials for token')

        serializer = UserSerializer(user)

        # return Response(serializer.data)
        return Response(serializer.data)

class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer()

    def put(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        print(response)
        pk = response[1]['user_id']
        print(pk)
        data = request.data
        print(data)
        username = response[1]['username']
        # data['username'] = username
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        address = data['address']
        postal_code = data['postal_code']   
            
        if first_name and last_name and address and postal_code:
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)        
        else:
            raise exceptions.APIException('complete all fields')

        
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    # def perform_create(self, serializer):
    #     # permission_classes = [IsAuthenticated]
    #     # if self.request.user is 
    #     # print(self.request.user)
    #     serializer.save(user=self.request.user)    
        
        
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if product.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('please edit your own product!')    
        
        
class ProductCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    # queryset = Product.objects.all()
    def post(self, request):
        data = request.data
        user = CurrentUserDefault()
        print(user)
        if user:
            return self.create(request, user=user)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
# class UserProfile(generics.ListAPIView):
#     # queryset = User.objects.get(username=self.username)
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]        
#     def get_queryset(self):
#         queryset = User.objects.all()
#         user = self.request.query_params.get('username')
         
#         if user is not None:
#             queryset = queryset.filter(username=username)
#             return queryset
#         else:
#             msg = {'error': 'invalid user'}            
#             return msg  
#     # def post(self, request, *args, **kwargs):
#     #     return self.create(request, *args, **kwargs)


class UserProfileUpdateView(generics.UpdateAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return User.objects.get(user=self.request.user)        
                    
                    
# --------------  order                    

class OrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer
    # queryset = Product.objects.all()
    # def post(self, request):
    #     data = request.data
    #     print(data) # {'items': [{'product_id': '1', 'total_amount': '24000'}]}
    #     product_id = data['product_id']
    #     total_amount = data['total_amount']
        
    #     user = CurrentUserDefault()
    #     print(user)
    #     print(user)
    #     if user:
    #         return self.create(request, user=user,product_id=product_id, total_amount=total_amount)
        
        
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        print(response)
        print(response[1]['user_id'])
        data = request.data
        print(data)
        user = response[1]['user_id']
        data['user'] = user
        product_id = data['product_id']
        total_amount = data['total_amount']
        
        if product_id and total_amount:
            serializer = OrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)        
        else:
            raise exceptions.APIException('invalid number')
        

    



# def validate_user_session(id, token):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=id)
#         if user.session_token == token:
#             return True
#         return False
#     except UserModel.DoesNotExist:
#         return False


# @csrf_exempt
# def order_add(request, id, token):
#     if not validate_user_session(id, token):
#         return JsonResponse({'error': 'Please re-login', 'code': '1'})

#     if request.method == "POST":
#         user_id = id
#         transaction_id = request.POST['transaction_id']
#         amount = request.POST['amount']
#         products = request.POST['products']

#         total_pro = len(products.split(',')[:-1])

#         UserModel = get_user_model()

#         try:
#             user = UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return JsonResponse({'error': 'User does not exist'})

#         ordr = Order(user=user, product_names=products, total_products=total_pro,
#                      transaction_id=transaction_id, total_amount=amount)
#         ordr.save()
#         return JsonResponse({'success': True, 'error': False, 'msg': 'Order placed Successfully'})


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all().order_by('id')
#     serializer_class = OrderSerializer


