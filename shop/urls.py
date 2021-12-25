from django.urls import path
from .views import home, category, detail
app_name = "shopping"

urlpatterns = [
    path("home/", home,name="home"),
    path("category/<slug:slug>/", category,name="category"),
    path("detail/<slug:slug>", detail,name="detail"),
]