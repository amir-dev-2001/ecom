from . import payment_view

from rest_framework import routers
from django.urls import path, include


from .views import (
    apiList,
    SignupAPIView, 
    LoginAPIView,
    ProductList,
    ProductRetrieveUpdateDestroyAPIView,
    ProductCreateAPIView,
    UserList,
    UserProfileUpdateView,
    OrderView    ,
    MyTokenObtainPairView,\
    UserProfile
)
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


# router = routers.DefaultRouter()
# router.register(r'', OrderViewSet)


urlpatterns = [
    path('', apiList),
    path('signup', SignupAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user/profile/', UserProfile.as_view()),
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('products/create/', ProductCreateAPIView.as_view()),
    
    path('users/', UserList.as_view()),
    path('users/profile/', UserProfileUpdateView.as_view()),
    
    path('order/add/', OrderView.as_view(), name='order.add'),
    # path('order/', include(router.urls)),

    
    path('payment/request/', payment_view.send_request, name='request'),
    path('payment/verify/', payment_view.verify , name='verify'),

    
]


urlpatterns = format_suffix_patterns(urlpatterns)



