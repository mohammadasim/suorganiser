from django.urls import path
from .views import (
    PostList,
    PostDetail,
    PostCreate
)

urlpatterns = [
    path('', PostList.as_view(), name='blogs_posts_list'),
    path('<int:year>/<int:month>/<slug:slug>/', PostDetail.as_view(), name='blogs_post_detail'),
    path('create/', PostCreate.as_view(), 'blog_post_create'),
]
