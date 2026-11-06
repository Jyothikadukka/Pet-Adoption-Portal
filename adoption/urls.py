from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('pets/', views.pet_list, name='pet_list'),

    path(
    'adopt/<int:pet_id>/',
    views.adopt_pet,
    name='adopt_pet'
),

path(
    'pet/<int:pet_id>/',
    views.pet_details,
    name='pet_details'
),

path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),
path(
    'contact/',
    views.contact,
    name='contact'
),
path(
    "give-pet/",
    views.give_pet,
    name="give_pet"
),

path(
    "submit-pet/",
    views.submit_pet,
    name="submit_pet"
),
path(
    "approve-pet/<int:id>/",
    views.approve_pet,
    name="approve_pet"
),


path(
    "reject-pet/<int:id>/",
    views.reject_pet,
    name="reject_pet"
),
path(
    "my-submitted-pets/",
    views.my_submitted_pets,
    name="my_submitted_pets"
),


]