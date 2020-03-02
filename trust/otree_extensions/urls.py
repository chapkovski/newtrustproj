from django.conf.urls import url

from trust.views import AllowInstructions

views_to_add = [
    AllowInstructions

]
urlpatterns = [url(i.url_pattern, i.as_view(), name=i.url_name) for i in views_to_add]