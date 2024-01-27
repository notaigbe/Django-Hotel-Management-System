# imports
import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import *
from hotel.models import *
from website.models import Reservation
from .forms import *


# The role corresponds to a folder containing the templates for a particular type of user. The role determines the
# permissions a user may have. The various roles are admin, staff, guest, manager, receptionist
@login_required(login_url='login')
def rooms(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    rooms = Room.objects.all()
    firstDayStr = None
    lastDateStr = None

    def chech_availability(fd, ed):
        availableRooms = []
        for room in rooms:
            availList = []
            bookingList = Booking.objects.filter(roomNumber=room)
            if room.statusStartDate is None:
                for booking in bookingList:
                    if booking.startDate > ed.date() or booking.endDate < fd.date():
                        availList.append(True)
                    else:
                        availList.append(False)
                if all(availList):
                    availableRooms.append(room)
            else:
                if room.statusStartDate > ed.date() or room.statusEndDate < fd.date():
                    for booking in bookingList:
                        if booking.startDate > ed.date() or booking.endDate < fd.date():
                            availList.append(True)
                        else:
                            availList.append(False)
                        if all(availList):
                            availableRooms.append(room)

        return availableRooms

    if request.method == "POST":
        if "dateFilter" in request.POST:
            firstDayStr = request.POST.get("fd", "")
            lastDateStr = request.POST.get("ld", "")

            firstDay = datetime.strptime(firstDayStr, '%Y-%m-%d')
            lastDate = datetime.strptime(lastDateStr, '%Y-%m-%d')

            rooms = chech_availability(firstDay, lastDate)

        if "filter" in request.POST:
            if request.POST.get("number") != "":
                rooms = rooms.filter(
                    number__contains=request.POST.get("number"))

            if request.POST.get("capacity") != "":
                rooms = rooms.filter(
                    capacity__gte=request.POST.get("capacity"))

            if request.POST.get("nob") != "":
                rooms = rooms.filter(
                    numberOfBeds__gte=request.POST.get("nob"))

            if request.POST.get("type") != "":
                rooms = rooms.filter(
                    roomType__contains=request.POST.get("type"))

            if request.POST.get("price") != "":
                rooms = rooms.filter(
                    price__lte=request.POST.get("price"))

            context = {
                "role": role,
                "rooms": rooms,
                "number": request.POST.get("number"),
                "capacity": request.POST.get("capacity"),
                "nob": request.POST.get("nob"),
                "price": request.POST.get("price"),
                "type": request.POST.get("type"),
                'segment': 'apartment'
            }
            return render(request, path + "apartments.html", context)

    context = {
        "role": role,
        'rooms': rooms,
        'fd': firstDayStr,
        'ld': lastDateStr,
        'segment': 'apartment'
    }
    return render(request, path + "apartments.html", context)


@login_required(login_url='login')
def add_room(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    rooms = Room.objects.all()

    if request.method == "POST":
        guest = None
        if role == 'guest':
            guest = request.user.guest
        elif role == 'manager' or role == 'admin' or role == 'receptionist':
            guest = request.user.employee

        # announcement = Announcement(sender = sender, content = request.POST.get('textid'))
        number = request.POST.get('number')
        capacity = request.POST.get('capacity')
        numberOfBeds = request.POST.get('beds')
        roomType = request.POST.get('type')
        price = request.POST.get('price')
        name = request.POST.get('name')
        caution_fee = request.POST.get('caution_fee')
        print(capacity)
        room = Room(number=number, capacity=capacity,
                    numberOfBeds=numberOfBeds, roomType=roomType, price=price, name=name, caution_fee=caution_fee)

        room.save()
        return redirect('rooms')

    context = {
        "role": role,
        'rooms': rooms,
        'segment': 'apartment'
    }
    return render(request, path + "add-room.html", context)


@login_required(login_url='login')
def room_profile(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    tempRoom = Room.objects.get(number=pk)
    bookings = Booking.objects.filter(roomNumber=tempRoom)
    guests = Guest.objects.all()
    bookings2 = Booking.objects.all()
    rooms = Room.objects.all()
    context = {
        "role": role,
        "bookings": bookings,
        "room": tempRoom,
        "guests": guests,
        "bookings2": bookings2,
        "rooms": rooms,
        'segment': 'apartment'
    }

    if request.method == "POST":
        if "lockRoom" in request.POST:
            fd = request.POST.get("bsd")
            ed = request.POST.get("bed")
            fd = datetime.strptime(fd, '%Y-%m-%d')
            ed = datetime.strptime(ed, '%Y-%m-%d')
            check = True
            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ed.date():
                    check = False
                    break
            if check:
                tempRoom.statusStartDate = fd
                tempRoom.statusEndDate = ed
                tempRoom.save()
            else:
                messages.error(request, "There is a booking in the interval!")
        if "unlockRoom" in request.POST:
            tempRoom.statusStartDate = None
            tempRoom.statusEndDate = None
            tempRoom.save()
        if "deleteRoom" in request.POST:
            check = True
            for b in bookings:
                if b.startDate <= datetime.now().date() or b.endDate >= datetime.now().date():
                    check = False
            if check:
                tempRoom.delete()
                return redirect("rooms")
            else:
                messages.error(request, "There is a booking in the interval!")

    return render(request, path + "room-profile.html", context)


@login_required(login_url='login')
def room_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    room = Room.objects.get(number=pk)
    form1 = editRoom(instance=room)
    rooms = Room.objects.all()

    context = {
        "role": role,
        "room": room,
        "form1": form1,
        "rooms": rooms,
        'segment': 'apartment'
    }

    if request.method == 'POST':
        form1 = editRoom(request.POST, instance=room)
        print(room.number)
        if form1.is_valid():
            form1.save()
            return redirect("room-profile", pk=room.number)
    return render(request, path + "room-edit.html", context)


@login_required(login_url='login')
def room_services(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    room_services = RoomServices.objects.all()
    context = {
        "role": role,
        "room_services": room_services
    }
    return render(request, path + "room-services.html", context)


@login_required(login_url='login')
def current_room_services(request):
    import datetime

    role = str(request.user.groups.all()[0])
    path = role + "/"

    curGuest = Guest.objects.get(user=request.user)
    curBooking = Booking.objects.filter(guest=curGuest).last()
    if curBooking is not None:
        curRoom = Room.objects.get(number=curBooking.roomNumber.number)
    else:
        context = {
            "role": role,
            "error": "You Don't Have Booking Right Now"
        }
        return render(request, path + "current-room-services.html", context)
    curRoomServices = RoomServices.objects.filter(curBooking=curBooking)

    room_services = RoomServices.objects.all()

    group = Group.objects.get(name='staff')
    users = User.objects.filter(groups=group)
    allEmployees = Employee.objects.filter(user__in=users)
    availableEmployee = list()
    maxTaskNum = 10

    for e in allEmployees:
        counter = 0
        empTasks = Task.objects.filter(employee=e)
        for t in empTasks:
            counter += 1
        if counter < maxTaskNum:
            availableEmployee.append(e)

    context = {
        "role": role,
        "room_services": room_services,
        "curGuest": curGuest,
        "curBooking": curBooking,
        "curRoom": curRoom,
        "curRoomServices": curRoomServices
    }

    if request.method == "POST":
        if "foodReq" in request.POST:
            newServiceReq = RoomServices(
                curBooking=curBooking, price=50.0, room=curRoom, servicesType='Food')
            newServiceReq.save()

            chosenEmp = random.choice(availableEmployee)
            lastTask = Task.objects.filter(employee=chosenEmp).last()
            if lastTask is not None:
                newTask = Task(employee=chosenEmp, startTime=lastTask.endTime,
                               endTime=lastTask.endTime + datetime.timedelta(minutes=30), description="Food Request")
            else:
                newTask = Task(employee=chosenEmp, startTime=datetime.datetime.now(),
                               endTime=datetime.datetime.now() + datetime.timedelta(minutes=30),
                               description="Food Request")
            newTask.save()
            return redirect("current-room-services")

        if "cleaningReq" in request.POST:
            newServiceReq = RoomServices(
                curBooking=curBooking, price=0.0, room=curRoom, servicesType='Cleaning')
            newServiceReq.save()
            chosenEmp = random.choice(availableEmployee)
            lastTask = Task.objects.filter(employee=chosenEmp).last()

            if lastTask is not None:
                newTask = Task(employee=chosenEmp, startTime=lastTask.endTime,
                               endTime=lastTask.endTime + datetime.timedelta(minutes=30),
                               description="Cleaning Request")
            else:
                newTask = Task(employee=chosenEmp, startTime=datetime.datetime.now(),
                               endTime=datetime.datetime.now() + datetime.timedelta(minutes=30),
                               description="Cleaning Request")
            newTask.save()
            return redirect("current-room-services")

        if "techReq" in request.POST:
            newServiceReq = RoomServices(
                curBooking=curBooking, price=0.0, room=curRoom, servicesType='Technical')
            newServiceReq.save()
            chosenEmp = random.choice(availableEmployee)
            lastTask = Task.objects.filter(employee=chosenEmp).last()
            if lastTask is not None:
                newTask = Task(employee=chosenEmp, startTime=lastTask.endTime,
                               endTime=lastTask.endTime + datetime.timedelta(minutes=30), description="Tech Request")
            else:
                newTask = Task(employee=chosenEmp, startTime=datetime.datetime.now(),
                               endTime=datetime.datetime.now() + datetime.timedelta(minutes=30),
                               description="Tech Request")
            newTask.save()
            return redirect("current-room-services")

    return render(request, path + "current-room-services.html", context)


@login_required(login_url='login')
def bookings(request):
    import datetime
    role = str(request.user.groups.all()[0])
    path = role + "/"

    bookings = Booking.objects.all()
    reservations = Reservation.objects.all()
    # calculating total for every booking and reservation:
    booking_cost = {}  # <booking : total>
    reservation_cost = {}  # <reservation : total>

    for booking in bookings:
        start_date = datetime.datetime.strptime(
            str(booking.startDate), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(booking.endDate), "%Y-%m-%d")
        numberOfDays = abs((end_date - start_date).days)
        # get room peice:
        price = Room.objects.get(number=booking.roomNumber.number).price
        total = price * numberOfDays
        booking_cost[booking] = total

    for reservation in reservations:
        start_date = datetime.datetime.strptime(
            str(reservation.startDate), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(reservation.endDate), "%Y-%m-%d")
        numberOfDays = abs((end_date - start_date).days)
        print(numberOfDays)
        # get room price:
        price = Room.objects.get(number=reservation.room.number).price
        print(price)
        total = price * numberOfDays
        reservation_cost[reservation] = total

    if request.method == "POST":
        if "filter" in request.POST:
            if request.POST.get("number") != "":
                rooms = Room.objects.filter(
                    number__contains=request.POST.get("number"))
                bookings = bookings.filter(
                    roomNumber__in=rooms)

            if request.POST.get("name") != "":
                users = User.objects.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = Guest.objects.filter(user__in=users)
                bookings = bookings.filter(
                    guest__in=guests)

            if request.POST.get("rez") != "":
                bookings = bookings.filter(
                    dateOfReservation=request.POST.get("rez"))

            if request.POST.get("fd") != "":
                bookings = bookings.filter(
                    startDate__gte=request.POST.get("fd"))

            if request.POST.get("ed") != "":
                bookings = bookings.filter(
                    endDate__lte=request.POST.get("ed"))

            context = {
                "role": role,
                'bookings': bookings,
                'booking_cost': booking_cost,
                'reservation_cost': reservation_cost,
                'reservations': reservations,
                "name": request.POST.get("name"),
                "number": request.POST.get("number"),
                "rez": request.POST.get("rez"),
                "fd": request.POST.get("fd"),
                "ed": request.POST.get("ed"),
                'segment': 'bookings'
            }

            return render(request, path + "bookings.html", context)

    context = {
        "role": role,
        'bookings': bookings,
        'reservations': reservations,
        'booking_cost': booking_cost,
        'reservation_cost': reservation_cost,
        'segment': 'bookings'
    }
    return render(request, path + "bookings.html", context)


@login_required(login_url='login')
def printReceipt(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    # tempRoom = Room.objects.get(number=pk)
    booking = Booking.objects.get(id=pk)
    start_date = booking.startDate
    end_date = booking.endDate
    numberOfDays = abs((end_date - start_date).days)
    # get room price:
    price = booking.roomNumber.price
    total = price * numberOfDays
    context = {
        "booking": booking,
        'total': total
    }

    return render(request, path + "receipt.html", context)


@login_required(login_url='login')
def booking_make(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    # tempRoom = Room.objects.get(number=pk)

    room = Room.objects.get(number=request.POST.get("roomid"))
    bookings = Booking.objects.filter(roomNumber=room)
    guests = Guest.objects.all()  # we pass this to context
    names = []
    if request.method == 'POST':
        print(f'date={request.POST.get("fd")}')
        if request.POST.get("fd") == "" or request.POST.get("ld") == "":
            print('empty date range')
            return redirect("rooms")

        start_date = datetime.strptime(
            str(request.POST.get("fd")), "%Y-%m-%d")
        end_date = datetime.strptime(
            str(request.POST.get("ld")), "%Y-%m-%d")
        numberOfDays = abs((end_date - start_date).days)
        # get room price:
        price = room.price
        total = price * numberOfDays

        for b in bookings:
            if b.endDate >= start_date.date() and b.startDate <= end_date.date():
                messages.warning(request, "This apartment has been booked for the selected period!")
                return redirect("rooms")

        if 'add' in request.POST:  # add dependee
            name = request.POST.get("depName")
            names.append(name)
            for i in range(room.capacity - 2):
                nameid = "name" + str(i + 1)
                if request.POST.get(nameid) != "":
                    names.append(request.POST.get(nameid))

        if 'bookGuestButton' in request.POST:
            if "guest" in request.POST:
                curguest = Guest.objects.get(id=request.POST.get("guest"))
            else:
                curguest = request.user.guest
            curbooking = Booking(guest=curguest, roomNumber=room, startDate=request.POST.get(
                "fd"), endDate=request.POST.get("ld"))
            curbooking.save()

            for i in range(room.capacity - 1):
                nameid = "name" + str(i + 1)
                if request.POST.get(nameid) != "":
                    if request.POST.get(nameid) is not None:
                        d = Dependants(booking=curbooking,
                                       name=request.POST.get(nameid))
                        d.save()

            messages.success(request, "Successful Booking")
            return redirect("rooms")

    context = {
        "fd": request.POST.get("fd"),
        "ld": request.POST.get("ld"),
        "role": role,
        "guests": guests,
        "room": room,
        "total": total,
        "names": names,
        'segment': 'bookings'
    }

    return render(request, path + "booking-make.html", context)


@login_required(login_url='login')
def deleteBooking(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    booking = Booking.objects.get(id=pk)
    if request.method == "POST":
        booking.delete()
        return redirect('bookings')

    context = {
        "role": role,
        'booking': booking,
        'segment': 'bookings'

    }
    return render(request, path + "deleteBooking.html", context)


@login_required(login_url='login')
def refunds(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    refunds = Refund.objects.all()
    context = {
        "role": role,
        'refunds': refunds
    }

    if request.method == "POST":
        if "decline" in request.POST or "approve" in request.POST:
            refundId = request.POST.get("refund", "")
            guestUserId = request.POST.get("guestUserId", "")

            tempUser = User.objects.get(id=guestUserId)
            receiver = Guest.objects.get(user=tempUser)

            def send(request, receiver, text, subject):

                message_email = 'hms@support.com'
                message = text
                receiver_name = receiver.user.first_name + " " + receiver.user.last_name

                # send email
                send_mail(
                    receiver_name + " " + subject,  # subject
                    message,  # message
                    message_email,  # from email
                    [receiver.user.email],  # to email
                    fail_silently=False,  # for user in users :
                    # user.email
                )

                messages.success(
                    request, 'Feedback E-Mail Was Successfully Sent')

                Refund.objects.filter(id=refundId).delete()
                return render(request, path + "refunds.html", context)

            def send_mail_refund_approved(request, receiver):
                subject = "Refund"
                text = """
                    Dear {guestName},
                    We are pleased to confirm that your refund request has been accepted.
                    The amount of refund will be on your account in 24 hours.
                    This time interval can change up to 48 hours according to your bank.
                    We are very sorry for this inconvenience. We hope to see you soon.
                """
                email_text = text.format(
                    guestName=receiver.user.first_name + " " + receiver.user.last_name)

                send(request, receiver, email_text, subject)

            def send_mail_refund_declined(request, receiver):
                subject = "Refund"
                text = """
                    Dear {guestName},
                    We are sorry to inform you that your refund request has been declined.
                    After our examinations, we see that your request can not be done according to our Hotel Policy.
                    We are very sorry for this inconvenience. We hope to see you soon.
                """
                email_text = text.format(
                    guestName=receiver.user.first_name + " " + receiver.user.last_name)

                send(request, receiver, email_text, subject)

            if "decline" in request.POST:
                send_mail_refund_declined(request, receiver)
            if "approve" in request.POST:
                send_mail_refund_approved(request, receiver)

            refundId = None
            statu = None

        if "filter" in request.POST:
            users = User.objects.all()
            if request.POST.get("gid") != "":
                users = users.filter(
                    id__contains=request.POST.get("gid"))
                guests = Guest.objects.filter(user__in=users)
                refunds = refunds.filter(guest__in=guests)

            if request.POST.get("name") != "":
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = Guest.objects.filter(user__in=users)
                refunds = refunds.filter(guest__in=guests)

            if request.POST.get("booking") != "":
                booking = Booking.objects.get(id=request.POST.get("booking"))
                refunds = refunds.filter(reservation=booking)

            if request.POST.get("reason") != "":
                refunds = refunds.filter(
                    reason__contains=request.POST.get("reason"))

            context = {
                "role": role,
                "refunds": refunds,
                "gid": request.POST.get("gid"),
                "name": request.POST.get("name"),
                "booking": request.POST.get("booking"),
                "reason": request.POST.get("reason")
            }
            return render(request, path + "refunds.html", context)

    return render(request, path + "refunds.html", context)


@login_required(login_url='login')
def request_refund(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    curGuest = Guest.objects.get(user=request.user)

    if request.method == "POST":
        if "sendReq" in request.POST:
            reason = request.POST.get("reqExp")
            curBookingId = request.POST.get("bid")
            currentBooking = Booking.objects.get(id=curBookingId)
            temp = Refund.objects.filter(reservation=currentBooking)
            if not temp:
                currentReq = Refund(
                    guest=curGuest, reservation=currentBooking, reason=reason)
                currentReq.save()
                messages.success(
                    request, "Your request was successfully sent.")
            else:
                messages.error(
                    request, "We already have your refund request for this reservation!")

    context = {
        "role": role,
        "curGuest": curGuest,
        "id": request.POST.get("bookingId")
    }

    return render(request, path + "request-refund.html", context)
