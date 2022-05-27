from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('simgUpload', views.simgUpload, name="simgUpload"),
    path('mulimgUpload', views.mulimgUpload, name="mulimgUpload"),
    path('deletePics', views.deletePics, name="deletePics"),
    path('gback', views.gback, name="gback"),
    path('home', views.home, name="home")
]
