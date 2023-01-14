from rest_framework.views import APIView
from rest_framework import generics, permissions, exceptions
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, User, Order
from .serializers import ProductSerializer, UserSerializer, UserProfileSerializer, OrderAddSerializer, OrderItemAddSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.fields import CurrentUserDefault
from rest_framework import status
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
        # token['address'] = user.address
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
    serializer_class = UserProfileSerializer

    def patch(self, request, *args, **kwargs):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        # print('------------------')
        # print(response)
        pk = response[1]['user_id']
        # print(pk)        
        newData = request.data
        print(newData)
        
        user = get_object_or_404(User, pk=pk)
        print('user is ')
        print(user)
        
        serializer = UserProfileSerializer(user ,data=newData, partial=True)
        print(serializer)   
        if serializer.is_valid():
            user = serializer.update(user, validated_data=newData)
            return Response(UserProfileSerializer(user).data) 
            # return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # # -----

        
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
        
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
    


class UserProfileUpdateView(generics.UpdateAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return User.objects.get(user=self.request.user)        
                    


class OrderAddAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderAddSerializer

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        # data = request.data
        user = response[1]['user_id']
        print(request.data)
        request.data['user'] = user
        print(user)
        # order_id = Order.objects.get('')

        serializer = OrderAddSerializer(request)

        return self.create(request) #and Response(serializer.data)
    
class OrderItemAddAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemAddSerializer   


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class = ord


    # def get(self, request, pk):
    #     order = Order.objects.get(pk=pk)
    #     print(order)
    #     return JsonResponse(order)
    
            
# class OrderItemAPIView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderItemSerializer

#     def post(self, request):
#         JWT_authenticator = JWTAuthentication()
#         response = JWT_authenticator.authenticate(request)
#         user = response[1]['user_id']
#         request.data['user'] = user

#         serializer = OrderItemSerializer(request)
#         return self.create(request) #and Response(serializer.data)
                        
                        
# class OrderDetailAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderDetailAPIView
    # def get(self, request, pk):
    #     queryset = OrderItem.objects.select_related().get(id=pk)
    #     return 
    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     print( pk)
    #     r = Order.objects.get(pk=pk)
    #     return r