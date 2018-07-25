from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacts_page, name='contacts_page'),
    path('apply_form/', views.apply_contact_form, name='apply_contact_form'),

]
