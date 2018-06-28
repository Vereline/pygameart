from django.urls import path
# from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.ListArt.as_view(), name='get_list_art'),
    path('<int:pk>/', views.DetailArt.as_view(), name='get_detail_art'),
    path('<int:pk>/image', views.image_view, name='get_image'),
    path('add_art/', views.get_art, name='add_art'),
    path(r'delete_art/<int:pk>/', views.ArtDelete.as_view(), name='delete_art'),
]
