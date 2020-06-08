from django.conf.urls import url,include
from django.contrib import admin
from trust.views import AllowInstructions
from django.urls import path

views_to_add = [
    AllowInstructions,


]
