from django.conf.urls import url
from django.urls import path

from . import views
urlpatterns = [
    path('', views.ListArt.as_view(), name='get_list_art'),
    path('<int:pk>/', views.DetailArt.as_view(), name='get_detail_art'),
    path('<int:pk>/image', views.image_view, name='get_image'),
    path('add_art/', views.get_art, name='add_art'),
    path('sandbox/', views.load_sandbox, name='load_sandbox'),
    path('gallery/<int:pk>', views.LoadGallery.as_view(), name='load_gallery'),
    path('detail_art/<int:pk>', views.art_detailed, name='detail_art'),
    url(r'^detail_art/add_comment/$', views.add_art_comment_to_post, name='add_art_comment_to_post'),
    url(r'^art_comment/approve/$', views.art_comment_approve, name='art_comment_approve'),
    url(r'^art_comment/remove/$', views.art_comment_remove, name='art_comment_remove'),
    url(r'^art_comment/(?P<pk>\d+)/edit/$', views.art_comment_edit, name='art_comment_edit'),
    path('about/', views.about_page, name='about_page'),
    path(r'delete_art/<int:pk>/', views.ArtDelete.as_view(), name='delete_art'),
]

