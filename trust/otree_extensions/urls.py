from django.conf.urls import url,include
from django.contrib import admin
from trust.views import AllowInstructions
from django.urls import path

views_to_add = [
    AllowInstructions,


]
urlpatterns = [url(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]
urlpatterns += [path('admin/', admin.site.urls)]
