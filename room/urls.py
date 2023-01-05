from django.urls import path, include

from .views import bookings, rooms, room_services, current_room_services, request_refund, add_room, room_profile, \
    room_edit, booking_make, deleteBooking, refunds

urlpatterns = [
    path('bookings/', bookings, name="bookings"),
    path('rooms/', rooms, name="rooms"),
    path('room-services/', room_services, name="room-services"),

    path('current-room-services/', current_room_services,
         name="current-room-services"),
    path('request-refund/', request_refund, name="request-refund"),

    path('add-room/', add_room, name="add-room"),


    path('room-profile/<str:id>/', room_profile, name="room-profile"),
    path('room-edit/<str:pk>/', room_edit, name="room-edit"),


    path('booking-make/', booking_make, name="booking-make"),
    path('refunds/', refunds, name="refunds"),
    path('deleteBooking/<str:pk>/', deleteBooking, name="deleteBooking"),

    ]