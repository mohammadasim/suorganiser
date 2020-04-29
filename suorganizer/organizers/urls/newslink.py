from django.urls import path
from ..views import (
    NewsLinkUpdate,
    NewsLinkCreate,
    NewsLinkDelete
)

urlpatterns = [
    path('create/', NewsLinkCreate.as_view(), name='organizers_newslink_create'),
    path('update/<int:pk>/', NewsLinkUpdate.as_view(), name='organizers_newslink_update'),
    path('delete/<int:pk>/', NewsLinkDelete.as_view(), name='organizers_newslink_delete'),
]
