from django.urls import path
from ..views import (CreateNewMegaSession, MegaSessionDetail, DeleteMegaSession,
                     GroupCalculateView, MegaSessionStats)

views_to_add = [
    CreateNewMegaSession,
    MegaSessionDetail,
    DeleteMegaSession,
    GroupCalculateView,
    MegaSessionStats
]
urlpatterns = [path(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]
