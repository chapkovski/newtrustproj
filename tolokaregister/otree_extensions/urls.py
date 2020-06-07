from django.contrib import admin
from django.urls import path
from ..views import TolokaSessionDetail, GetInfo, AcceptAnswer, PayBonus

views_to_add = [
    GetInfo,
    AcceptAnswer,
    PayBonus,
    TolokaSessionDetail
]
urlpatterns = [path(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]

urlpatterns += [path('admin/', admin.site.urls)]
