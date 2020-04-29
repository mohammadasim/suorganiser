from django.urls import path
from ..views import (
    tag_detail,
    TagCreate,
    TagUpdate,
    TagDelete,
    TagList
)

urlpatterns = [
    path('', TagList.as_view(), name='organizers_tag_list'),
    path('create/', TagCreate.as_view(), name='organizers_tag_create'),
    path('<slug:slug>/', tag_detail, name='organizers_tag_detail'),
    path('<slug:slug>/update/', TagUpdate.as_view(), name='organizers_tag_update'),
    path('<slug:slug>/delete/', TagDelete.as_view(), name='organizers_tag_delete'),
]
