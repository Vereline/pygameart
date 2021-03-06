from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news_list, name='news_list'),
    url(r'^post/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
    url(r'^post/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
]
