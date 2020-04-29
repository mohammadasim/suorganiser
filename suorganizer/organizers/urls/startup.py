from django.urls import path
from ..views import (
    startup_detail,
    StartupUpdate,
    StartupDelete,
    StartupList,
)

urlpatterns = [
    path('', StartupList.as_view(), name='organizers_startup_list'),
    path('<slug:slug>/', startup_detail, name='organizers_startup_detail'),
    path('<slug:slug>/update/', StartupUpdate.as_view(), name='organizers_startup_update'),
    path('<slug:slug>/delete/', StartupDelete.as_view(), name='organizers_startup_delete'),
]
