from django.urls import path
from .views import index, inner_page, reservation, check_available, view_room, contact

urlpatterns = [
    path('', index, name="index"),
    path('navigate/<page>', inner_page, name="inner-page"),
    path('make-reservation', reservation, name="make-reservation"),
    path('check-available', check_available, name="check-available"),
    path('view-room/<room>', view_room, name="view-room"),
    path('contact', contact, name="contact"),

]
