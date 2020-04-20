from django.urls import path
from .views import (
    tag_list,
    tag_detail,
    TagCreate,
    TagUpdate,
    TagDelete,
    startup_detail,
    startup_list,
    StartupUpdate,
    StartupDelete,
    NewsLinkUpdate,
    NewsLinkCreate,
    NewsLinkDelete
)

urlpatterns = [
    path('tag/', tag_list, name='organizers_tag_list'),
    path('tag/create/', TagCreate.as_view(), 'organizer_tag_create'),
    path('tag/<slug:slug>/', tag_detail, name='organizers_tag_detail'),
    path('tag/<slug:slug>/update/', TagUpdate.as_view(), 'organizers_tag_update'),
    path('tag/<slug:slug>/delete/', TagDelete.as_view(), 'organizers_tag_delete'),
    path('startup/', startup_list, name='organizers_startup_list'),
    path('startup/<slug:slug>/', startup_detail, name='organizers_startup_detail'),
    path('startup/<slug:slug>/update/', StartupUpdate.as_view(), 'organizers_startup_update'),
    path('startup/<slug:slug>/delete/', StartupDelete.as_view(), 'organizers_startup_delete'),
    path('newslink/create/', NewsLinkCreate.as_view(), name='organizers_newslink_create'),
    path('newslink/update/<pk:pk>/', NewsLinkUpdate.as_view(), name='organizers_newslink_update'),
    path('newslink/delete/<pk:pk>/', NewsLinkDelete.as_view(), name='organizers_newslink_delete'),

]
