from django.urls import path, include, register_converter, converters

from .views import home, events, announcements, storage, payment, verify, deleteStorage, deleteFoodMenu, food_menu, \
    food_menu_edit, createEvent, deleteEvent, deleteAnnouncement, error, event_profile, event_edit, drinks, deleteDrink, \
    sales, order, print_receipt, restock, opening_stock, closing_stock, report, frontdesk_check

# register_converter(converters.StringConverter, "yyyy")


urlpatterns = [
    path('backoffice/', home, name="home"),

    path('events/', events, name="events"),

    path('announcements/', announcements, name="announcements"),
    path('backoffice/check/', frontdesk_check, name="frontdesk-check"),
    path('backoffice/storage/', storage, name="storage"),
    path('backoffice/drinks/', drinks, name="drinks"),
    path('backoffice/sales/', sales, name="sales"),
    path('backoffice/restock/', restock, name="restock"),
    path('backoffice/openingstock/', opening_stock, name="opening_stock"),
    path('backoffice/closingstock/', closing_stock, name="closing_stock"),
    path('backoffice/orders/', order, name="orders"),
    path('backoffice/print_receipt/<orders>/<int:total>/', print_receipt, name="print_receipt"),
    path('backoffice/print_receipt/', print_receipt, kwargs={'orders': '', 'total': ''}),
    path('payment/', payment, name="payment"),
    path('verify/', verify, name="verify"),

    path('backoffice/deleteStorage/<str:pk>/', deleteStorage, name="deleteStorage"),
    path('backoffice/deleteDrink/<str:pk>/', deleteDrink, name="deleteDrink"),
    path('backoffice/deleteFoodMenu/<str:pk>/', deleteFoodMenu, name="deleteFoodMenu"),
    path('backoffice/food-menu/', food_menu, name="food-menu"),
    path('backoffice/food-menu/<str:pk>/', food_menu_edit, name="food-menu-edit"),

    path('backoffice/createEvent/', createEvent, name="createEvent"),
    path('backoffice/deleteEvent/<str:pk>/', deleteEvent, name="deleteEvent"),
    path('backoffice/deleteAnnouncement/<str:pk>/',
         deleteAnnouncement, name="deleteAnnouncement"),
    path('error/', error, name="error"),
    path('backoffice/event-profile/<str:id>/', event_profile, name="event-profile"),
    path('backoffice/event-edit/<str:pk>/', event_edit, name="event-edit"),
    path('backoffice/drink_sales/', report, name="sales_report"),
]
