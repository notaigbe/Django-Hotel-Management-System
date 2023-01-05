from django.urls import path, include

from .views import home, events, announcements, storage, payment, verify, deleteStorage, deleteFoodMenu, food_menu, \
    food_menu_edit, createEvent, deleteEvent, deleteAnnouncement, error, event_profile, event_edit

urlpatterns = [
    path('backoffice/', home, name="home"),

    path('events/', events, name="events"),

    path('announcements/', announcements, name="announcements"),

    path('storage/', storage, name="storage"),
    path('payment/', payment, name="payment"),
    path('verify/', verify, name="verify"),

    path('deleteStorage/<str:pk>/', deleteStorage, name="deleteStorage"),
    path('deleteFoodMenu/<str:pk>/', deleteFoodMenu, name="deleteFoodMenu"),
    path('food-menu/', food_menu, name="food-menu"),
    path('food-menu/<str:pk>/', food_menu_edit, name="food-menu-edit"),

    path('createEvent/', createEvent, name="createEvent"),
    path('deleteEvent/<str:pk>/', deleteEvent, name="deleteEvent"),
    path('deleteAnnouncement/<str:pk>/',
         deleteAnnouncement, name="deleteAnnouncement"),
    path('error/', error, name="error"),
    path('event-profile/<str:id>/', event_profile, name="event-profile"),
    path('event-edit/<str:pk>/', event_edit, name="event-edit"),
    ]