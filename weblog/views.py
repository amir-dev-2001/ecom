from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny, IsAdminUser

class PostList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class PostDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
        