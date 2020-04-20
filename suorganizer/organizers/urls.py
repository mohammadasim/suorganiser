from django.urls import path
from .views import (
    tag_list,
    tag_detail,
    startup_detail,
    startup_list,
    TagCreate,
    NewsLinkUpdate,
    NewsLinkCreate
)

urlpatterns = [
    path('tag/', tag_list, name='organizers_tag_list'),
    path('tag/create/', TagCreate.as_view(), 'organizer_tag_create'),
    path('tag/<slug:slug>/', tag_detail, name='organizers_tag_detail'),
    path('startup/', startup_list, name='organizers_startup_list'),
    path('startup/<slug:slug>/', startup_detail, name='organizers_startup_detail'),
    path('newslink/create/', NewsLinkCreate.as_view(), name='organizers_newslink_create'),
    path('newslink/update/<pk:pk>/', NewsLinkUpdate.as_view(), name='organizers_newslink_update'),

]
