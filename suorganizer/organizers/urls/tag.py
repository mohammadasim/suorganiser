from django.urls import path

from ..views import (
    TagDetail,
    TagCreate,
    TagUpdate,
    TagDelete,
    TagList,
)

urlpatterns = [
    path('', TagList.as_view(), name='organizers_tag_list'),
    path('create/', TagCreate.as_view(), name='organizers_tag_create'),
    path('<slug:slug>/', TagDetail.as_view(), name='organizers_tag_detail'),
    path('<slug:slug>/update/', TagUpdate.as_view(), name='organizers_tag_update'),
    path('<slug:slug>/delete/', TagDelete.as_view(), name='organizers_tag_delete'),
]
