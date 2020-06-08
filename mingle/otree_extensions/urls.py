from django.urls import path
from ..views import CreateNewMegaSession

views_to_add = [
    CreateNewMegaSession
]
urlpatterns = [path(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]
