from django.urls import path
from ..views import (
    StartupDetail,
    StartupUpdate,
    StartupDelete,
    StartupList,
)

urlpatterns = [
    path('', StartupList.as_view(), name='organizers_startup_list'),
    path('<slug:slug>/', StartupDetail.as_view(), name='organizers_startup_detail'),
    path('<slug:slug>/update/', StartupUpdate.as_view(), name='organizers_startup_update'),
    path('<slug:slug>/delete/', StartupDelete.as_view(), name='organizers_startup_delete'),
]
