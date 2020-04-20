from django.urls import path
from .views import (
    PostList,
    PostDetail,
    PostCreate,
    PostUpdate,
    PostDelete
)

urlpatterns = [
    path('', PostList.as_view(), name='blogs_posts_list'),
    path('<int:year>/<int:month>/<slug:slug>/', PostDetail.as_view(), name='blogs_post_detail'),
    path('create/', PostCreate.as_view(), 'blog_post_create'),
    path('<int:year>/<int:month>/<slug:slug>/update/', PostUpdate.as_view(), name='blogs_post_update'),
    path('<int:year>/<int:month>/<slug:slug>/delete/', PostDelete.as_view(), name='blogs_post_delete'),
]
