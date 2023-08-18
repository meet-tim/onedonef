from django.urls import path
from . import views
from django.contrib.auth  import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),

    path('factories/', views.factories, name="factories"),

    path('districts/', views.districts, name="districts"),

    path('factories/details/<factory_id>', views.details, name="details"),

    path('search/', views.search, name='search'),

    path('factories/<str:cat_filter>', views.filter, name="filter"),

]

