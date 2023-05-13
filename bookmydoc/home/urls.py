from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.dummy),
    path('slot',views.homes),
    path('result',views.slot),
    path('success',views.book),
    path('medigo',views.medigo),
    path('em',views.em)
]