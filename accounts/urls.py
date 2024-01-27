from django.urls import path, include

from .views import login_page, logout_user, register_page, guests, employees, completeTask, tasks, employee_details, \
    employee_details_edit, add_employee, guest_edit, guest_profile, delete_employee, change_password, login_view, register_user, dashboard
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('backoffice/', dashboard, name='dashboard'),
    # path('backoffice/login/', login_page, name="login"),
    path('backoffice/logout/', logout_user, name="logout"),
    # path('backoffice/register/', register_page, name="register"),
    path('backoffice/login/', login_view, name="login"),
    path('backoffice/register/', register_user, name="register"),
    # path('backoffice/logout/', LogoutView.as_view(), name="logout"),
    path('guests/', guests, name="guests"),
    path('backoffice/employees/', employees, name="employees"),
    path('backoffice/completeTask/<str:pk>/', completeTask, name="completeTask"),
    path('backoffice/tasks/', tasks, name="tasks"),
    path('backoffice/employee-profile/<str:pk>/', employee_details, name="employee-profile"),
    path('backoffice/deleteEmployee/<str:pk>/', delete_employee, name="deleteEmployee"),
    path('backoffice/employee-edit/<str:pk>/', employee_details_edit, name="employee-edit"),
    path('backoffice/employee-add/', add_employee, name="add-employee"),

    path('guest-edit/<str:pk>', guest_edit, name="guest-edit"),
    path('guest-profile/<str:pk>', guest_profile, name="guest-profile"),
    path('backoffice/password/<pk>', change_password, name='change_password'),

]
