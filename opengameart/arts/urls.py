from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListArt.as_view(), name='get_list_art'),
    path('<int:pk>/', views.DetailArt.as_view(), name='get_detail_art'),
    path('<int:pk>/image', views.image_view, name='get_image'),
]