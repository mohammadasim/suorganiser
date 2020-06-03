from django.urls import path

from ..views import (
    StartupDetail, StartupUpdate, StartupDelete, StartupList,
    NewsLinkCreate, NewsLinkDelete, NewsLinkUpdate
)

urlpatterns = [
    path('', StartupList.as_view(), name='organizers_startup_list'),
    path('<slug:slug>/', StartupDetail.as_view(), name='organizers_startup_detail'),
    path('<slug:slug>/update/', StartupUpdate.as_view(), name='organizers_startup_update'),
    path('<slug:slug>/delete/', StartupDelete.as_view(), name='organizers_startup_delete'),
    path('<slug:startup_slug>/add_article_link/', NewsLinkCreate.as_view(), name='organizers_newslink_create'),
    path('<slug:startup_slug>/<slug:newslink_slug>/delete/',
         NewsLinkDelete.as_view(), name='organizers_newslink_delete'),
    path('<slug:startup_slug>/<slug:newslink_slug>/update/',
         NewsLinkUpdate.as_view(), name='organizers_newslink_update')
]
