from datetime import datetime, date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from django.db.models import Count, F
from django.shortcuts import render, redirect

from hotel.models import *
# Own imports
# from accounts.models import *
from room.models import *
from .forms import *


# Create your views here.


def register_page(request):
    form = CreateUserForm(initial={'password1': 'guest_password', 'password2': 'guest_password'})
    if str(request.user.groups.all()[0]) == 'guest':
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                print('valid')
                return_next = request.POST.get('next', '/')
                if len(User.objects.filter(email=request.POST.get("email"))) != 0:
                    messages.warning(
                        request, f'Email address {request.POST.get("email")} already exists')
                    return redirect('register')
                if len(Guest.objects.filter(phoneNumber=request.POST.get("phoneNumber"))) != 0:
                    messages.warning(
                        request, f'User with phone number {request.POST.get("phoneNumber")} already exists')
                    return redirect('register')

                user = form.save()
                username = form.cleaned_data.get('email')
                password = "guest_pass"

                group = Group.objects.get(name="guest")
                user.groups.add(group)

                curGuest = Guest(
                    user=user, phoneNumber=request.POST.get("phoneNumber"))
                curGuest.save()

                messages.success(
                    request, 'Guest account created successfully for ' + username)
                # user = authenticate(request, username=username, password=password)

                # return redirect("guest-profile", pk=user.id)
                return redirect(return_next)

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def add_employee(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    form = CreateUserForm()
    form2 = ROLES()
    form3 = CreateEmployeeForm()

    if request.method == 'POST':
        post = request.POST.copy()  # to make it mutable
        post['phoneNumber'] = "+234" + post['phoneNumber']
        request.POST = post

        form = CreateUserForm(request.POST)
        form2 = ROLES(request.POST)
        form3 = CreateEmployeeForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save()
            employee = form3.save()
            employee.user = user
            employee.save()

            username = form.cleaned_data.get('username')

            role = form2.cleaned_data.get("ROLES_TYPES")

            group = Group.objects.get(name=role)
            user.groups.add(group)

            messages.success(
                request, role + ' Account created successfully for ' + username)

            return redirect('employees')

    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        "role": role,
        'segment': 'employees'
    }
    return render(request, path + "add-employee.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def guests(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    topRange = Booking.objects.all().values("guest").annotate(
        total=Count("guest")).order_by("-total")
    topLimit = 10
    topList = []
    for t in topRange:
        if len(topList) > 10:
            break
        else:
            topList.append(Guest.objects.get(id=t.get("guest")))

    bookings = Booking.objects.all()
    fd = datetime.combine(date.today() - timedelta(days=30), datetime.min.time())
    ld = datetime.combine(date.today(), datetime.min.time())
    guests = []

    for b in bookings:
        if b.endDate >= fd.date() and b.startDate <= ld.date():
            if b.guest not in guests:
                guests.append(b.guest)

    if request.method == "POST":
        if "filterDate" in request.POST:

            if request.POST.get("f_day") == "" and request.POST.get("l_day") == "":
                guests = Guest.objects.all()

                context = {
                    "role": role,
                    "guests": guests,
                    "fd": "",
                    "ld": "",
                    'segment': 'guests'
                }
                return render(request, path + "guests.html", context)

            if request.POST.get("f_day") == "":
                fd = datetime.strptime("1970-01-01", '%Y-%m-%d')
            else:
                fd = request.POST.get("f_day")
                fd = datetime.strptime(fd, '%Y-%m-%d')

            if request.POST.get("l_day") == "":
                ld = datetime.strptime("2030-01-01", '%Y-%m-%d')
            else:
                ld = request.POST.get("l_day")
                ld = datetime.strptime(ld, '%Y-%m-%d')

            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ld.date():
                    if b.guest not in guests:
                        guests.append(b.guest)

        if "filterGuest" in request.POST:
            guests = Guest.objects.all()
            users = User.objects.all()
            if request.POST.get("id") != "":
                users = users.filter(
                    id__contains=request.POST.get("id"))
                guests = guests.filter(user__in=users)

            if request.POST.get("name") != "":
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = guests.filter(user__in=users)

            if request.POST.get("email") != "":
                users = users.filter(email__contains=request.POST.get("email"))
                guests = guests.filter(user__in=users)

            if request.POST.get("number") != "":
                guests = guests.filter(
                    phoneNumber__contains=request.POST.get("number"))

            context = {
                "role": role,
                "guests": guests,
                "id": request.POST.get("id"),
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "number": request.POST.get("number"),
                'segment': 'guests'
            }
            return render(request, path + "guests.html", context)

        if "top" in request.POST:
            topRange = Booking.objects.all().values("guest").annotate(
                total=Count("guest")).order_by("-total")
            topList = []
            topLimit = request.POST.get("top")
            for t in topRange:
                if len(topList) >= int(topLimit):
                    break
                else:
                    topList.append(Guest.objects.get(id=t.get("guest")))
            context = {
                "role": role,
                "guests": guests,
                "topList": topList,
                "topLimit": topLimit,
                "fd": fd,
                "ld": ld,
                'segment': 'guests'
            }
            return render(request, path + "guests.html", context)
    context = {
        "role": role,
        "guests": guests,
        "topList": topList,
        "topLimit": topLimit,
        "fd": fd,
        "ld": ld,
        'segment': 'guests'
    }
    return render(request, path + "guests.html", context)


@login_required(login_url='login')
def employees(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    if role == 'manager':
        employees = Employee.objects.all().exclude(user__groups=4).exclude(user=request.user)
    else:
        employees = Employee.objects.all().exclude(user=request.user)

    if request.method == "POST":
        if "filter" in request.POST:
            users = User.objects.all()
            if request.POST.get("id") != "":
                users = users.filter(
                    id__contains=request.POST.get("id"))
                employees = employees.filter(user__in=users)

            if request.POST.get("name") != "":
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                employees = employees.filter(user__in=users)

            if request.POST.get("email") != "":
                users = users.filter(email__contains=request.POST.get("email"))
                employees = employees.filter(user__in=users)

            if request.POST.get("number") != "":
                employees = employees.filter(
                    phoneNumber__contains=request.POST.get("number"))

            if request.POST.get("filterRole") != "":
                try:
                    group = Group.objects.get(
                        name__contains=request.POST.get("filterRole"))
                except:
                    group = None
                users = users.filter(groups=group)
                employees = employees.filter(user__in=users)

        context = {
            "role": role,
            "employees": employees,
            "id": request.POST.get("id"),
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "number": request.POST.get("number"),
            "filterRole": request.POST.get("filterRole"),
            'segment': 'employees'
        }
        return render(request, path + "employees.html", context)

    context = {
        "role": role,
        "employees": employees,
        'segment': 'employees'
    }
    return render(request, path + "employees.html", context)


@login_required(login_url='login')
def employee_details(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        employee = Employee.objects.get(user=user)
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        employee.phoneNumber = request.POST.get("phoneNumber")
        user.password = request.POST.get("password")
        user.save()
        employee.save()
        return redirect("home")

    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempUser = User.objects.get(id=pk)
    employee = Employee.objects.get(user=tempUser)
    tasks = Task.objects.filter(employee=employee)
    context = {
        "role": role,
        "employee": employee,
        "tasks": tasks,
        'segment': 'employees'
    }
    return render(request, path + "employee-profile.html", context)


@login_required(login_url='login')
def employee_details_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempuser = User.objects.get(id=pk)
    employee = Employee.objects.get(user=tempuser)

    form1 = editEmployee(instance=employee)
    form2 = editUser(instance=tempuser)

    context = {
        "role": role,
        "employee": employee,
        "user": tempuser,
        "form1": form1,
        "form2": form2,
        'segment': 'employees'
    }

    if request.method == "POST":
        print(request.POST)
        form1 = editEmployee(request.POST, instance=employee)
        form2 = editUser(request.POST, instance=tempuser)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.info(request, "Staff Update Successful")
        else:
            messages.error(request, "Staff Update Failed")

    return render(request, path + "employee-edit.html", context)


@login_required(login_url='login')
def delete_employee(request, pk):
    role = str(request.user.groups.first())
    path = role + "/"

    tempuser = User.objects.get(id=pk)
    print(tempuser)
    employee = Employee.objects.get(user=tempuser)

    # if request.method == "POST":

    # form1 = editEmployee(instance=employee)
    # form2 = editUser(instance=tempuser)

    context = {
        "role": role,
        "employee": employee,
        "user": tempuser,
        # "form1": form1,
        # "form2": form2
        'segment': 'employees'
    }

    if request.method == "POST":
        employee.delete()
        return redirect('employees')

    return render(request, path + "deleteEmployee.html", context)


@login_required(login_url='login')
def guest_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    tempuser = User.objects.get(id=pk)
    guest = Guest.objects.get(user=tempuser)
    form1 = editGuest(instance=guest)
    form2 = editUser(instance=tempuser)

    context = {
        "role": role,
        "guest": guest,
        "form1": form1,
        "form2": form2,
        "user": tempuser,
        'segment': 'guests'
    }

    if request.method == "POST":
        form1 = editGuest(request.POST, instance=guest)
        form2 = editUser(request.POST, instance=tempuser)
        if form1.is_valid and form2.is_valid:
            form1.save()
            form2.save()

    return render(request, path + "guest-edit.html", context)


@login_required(login_url='login')
def guest_profile(request, pk):
    tempUser = User.objects.get(id=pk)
    guest = Guest.objects.get(user=tempUser)

    if request.method == 'POST':
        tempUser.first_name = request.POST.get("first_name")
        tempUser.last_name = request.POST.get("last_name")
        guest.phoneNumber = request.POST.get("phoneNumber")
        tempUser.save()
        guest.save()
        return redirect("home")
    role = str(request.user.groups.all()[0])
    path = role + "/"

    eventAttendees = EventAttendees.objects.filter(guest=guest)
    bookings = Booking.objects.filter(guest=guest)
    context = {
        "role": role,
        "guest": guest,
        "eventAttendees": eventAttendees,
        "bookings": bookings,
        'segment': 'guests'
    }
    return render(request, path + "guest-profile.html", context)


@login_required(login_url='login')
def tasks(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempEmp = Employee.objects.get(user=request.user)
    tasks = Task.objects.filter(employee=tempEmp)

    context = {
        "role": role,
        'tasks': tasks
    }
    if request.method == "POST":
        if "markAsComplete" in request.POST:
            tid = request.POST.get("tid")
            Task.objects.get(id=tid).delete()
            return redirect("tasks")

        if "filter" in request.POST:
            if request.POST.get("id") != "":
                tasks = tasks.filter(id=request.POST.get("id"))

            if request.POST.get("desc") != "":
                tasks = tasks.filter(
                    description__contains=request.POST.get("desc"))

            if request.POST.get("fd") != "":
                tasks = tasks.filter(startTime__gte=request.POST.get("fd"))

            if request.POST.get("ed") != "":
                tasks = tasks.filter(endTime__lte=request.POST.get("ed"))

            context = {
                "role": role,
                "tasks": tasks,
                "id": request.POST.get("id"),
                "desc": request.POST.get("desc"),
                "fd": request.POST.get("fd"),
                "ed": request.POST.get("ed")
            }

    return render(request, path + "tasks.html", context)


@login_required(login_url='login')
def completeTask(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")

    context = {
        "role": role,
        'task': task

    }
    return render(request, path + "completeTask.html", context)


def change_password(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempuser = User.objects.get(id=pk)
    form = SetPasswordForm(tempuser)
    if request.method == 'POST':
        form = SetPasswordForm(tempuser, request.POST)
        context = {
            "role": role,
            "user": tempuser,
            "form": form,
        }
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password updated successfully')
            return redirect('employee-edit', pk)
        else:
            messages.error(request, 'error')
        return render(request, path + 'change-password.html', context)
    return render(request, path + 'change-password.html', {'form': form, 'role': role})


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url="login")
def dashboard(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    if role == 'manager':
        employees = Employee.objects.all().exclude(user__groups=4).exclude(user=request.user)
    else:
        employees = Employee.objects.all().exclude(user=request.user)

    low_stock = Drink.objects.filter(quantity__lt=F('restock_level'))
    low_stock_count = low_stock.count()
    out_of_stock = Drink.objects.filter(quantity=0)
    out_of_stock_count = out_of_stock.count()
    sales = Sales.objects.all()

    sales_total = 0
    for sale in sales:
        sales_total += sale.amount
        print(sale.amount)
    print(low_stock)
        
    context = {'segment': 'dashboard',
               'role': role,
               'low_stock': low_stock,
               'low_stock_count': low_stock_count,
               'out_of_stock': out_of_stock,
               'out_of_stock_count': out_of_stock_count,
               'sales_total': sales_total}

    # html_template = loader.get_template('home/index.html')
    return render(request, 'home/index.html', context)
