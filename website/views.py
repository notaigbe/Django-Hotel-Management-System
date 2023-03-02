from datetime import datetime, timedelta
from email.mime.text import MIMEText

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from psycopg2._range import DateTimeTZRange

from .forms import reservationForm
from .models import Reservation
from room.models import Room, Booking


# Create your views here.
def index(request):
    # role = str(request.user.groups.all()[0])
    # path = role + "/"
    rooms = Room.objects.all()
    return render(request, "website/index.html", {'rooms': rooms})


def inner_page(request, page):
    # role = str(request.user.groups.all()[0])
    # path = role + "/"
    rooms = Room.objects.all()
    title = ""
    if page == 'about':
        title = 'About Us'
    elif page == 'contact':
        title = 'Contact'
    elif page == 'events':
        title = 'Events'
    elif page == 'reservation':
        title = 'Reservation'
        # form = reservationForm()
    elif page == 'apartments':
        title = 'Apartments'
    return render(request, f"website/{page}.html", {'page': page, 'title': title, 'rooms': rooms})


def view_room(request, room):
    room = Room.objects.get(name=room)
    print(room)
    title = room.name
    page = room.name

    return render(request, f"website/room-single.html", {'page': page, 'title': title, 'room': room})


def check_available(request):
    if request.method == 'POST':
        available = check_availability(datetime.strptime(request.POST.get('checkin_date'),
                                                         '%d %B, %Y'),
                                       datetime.strptime(request.POST.get('checkout_date'),
                                                         '%d %B, %Y'))

        print(len(available))
        if len(available) == 1:
            messages.info(
                request, f"There is {len(available)} apartment/room available for the selected dates")
        elif len(available) < 1:
            messages.info(
                request, f"There are no apartments/rooms available for the selected dates")
        else:
            messages.info(
                request, f"There are {len(available)} apartments/rooms available for the selected dates")
    return redirect('index')


def check_availability(fd, ed):
    rooms = Room.objects.all()
    firstDayStr = None
    lastDateStr = None
    availableRooms = []
    for room in rooms:
        availList = []
        bookingList = Reservation.objects.filter(room=room)
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


def reservation(request):
    if request.method == 'POST':
        print(datetime.strptime(request.POST.get('startDate'), '%d %B, %Y'))
        cur_room = Room.objects.get(name=request.POST.get("room"))
        print(cur_room)

        if len(Room.objects.filter(name=request.POST.get("room"))) != 0:
            room = Room.objects.get(name=request.POST.get('room'))
            bookingList = Reservation.objects.filter(room=room)
            ed = datetime.strptime(request.POST.get('startDate'), '%d %B, %Y')
            fd = datetime.strptime(request.POST.get('endDate'),
                                   '%d %B, %Y')
            if len(bookingList) != 0:
                for booking in bookingList:
                    print(booking.startDate)
                    if booking.startDate is not None:
                        if booking.startDate > ed.date() or booking.endDate < fd.date():
                            print('Reservation function not empty')
                            guest = Reservation(
                                name=request.POST.get('name'),
                                email=request.POST.get('email'),
                                phoneNumber=request.POST.get('phoneNumber'),
                                room=room,
                                startDate=datetime.strptime(request.POST.get('startDate'), '%d %B, %Y'),
                                endDate=datetime.strptime(request.POST.get('endDate'), '%d %B, %Y')
                            )
                            guest.save()

                            room.statusStartDate = datetime.strptime(request.POST.get('startDate'), '%d %B, %Y')
                            room.statusEndDate = datetime.strptime(request.POST.get('endDate'), '%d %B, %Y')
                            room.save()
                            messages.info(
                                request,
                                f"The {request.POST.get('room')} apartment/room has been successfully reserved for {request.POST.get('startDate')} - {request.POST.get('endDate')}")
                        else:
                            messages.info(
                                request, f"The {request.POST.get('room')} apartment/room is unavailable for the dates selected")
                    else:
                        print('Reservation function empty')
                        guest = Reservation(
                            name=request.POST.get('name'),
                            email=request.POST.get('email'),
                            phoneNumber=request.POST.get('phoneNumber'),
                            room=room,
                            startDate=datetime.strptime(request.POST.get('startDate'), '%d %B, %Y'),
                            endDate=datetime.strptime(request.POST.get('endDate'), '%d %B, %Y')
                        )
                        guest.save()

                        room.statusStartDate = datetime.strptime(request.POST.get('startDate'), '%d %B, %Y')
                        room.statusEndDate = datetime.strptime(request.POST.get('endDate'), '%d %B, %Y')
                        room.save()
                        messages.info(
                            request,
                            f"The {request.POST.get('room')} apartment/room has been successfully reserved for {request.POST.get('startDate')} - {request.POST.get('endDate')}")

            else:

                guest = Reservation(
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    phoneNumber=request.POST.get('phoneNumber'),
                    room=room,
                    startDate=datetime.strptime(request.POST.get('startDate'), '%d %B, %Y'),
                    endDate=datetime.strptime(request.POST.get('endDate'), '%d %B, %Y')
                )
                guest.save()
                room.statusStartDate = datetime.strptime(request.POST.get('startDate'), '%d %B, %Y')
                room.statusEndDate = datetime.strptime(request.POST.get('endDate'), '%d %B, %Y')
                room.save()
                messages.info(
                    request,
                    f"The {request.POST.get('room')} apartment/room has been successfully reserved for {request.POST.get('startDate')} - {request.POST.get('endDate')}")

        else:
            messages.error(
                request, f"The {request.POST.get('room')} apartment/room doesn't exist in the database")

        return redirect(inner_page, page='reservation')


def contact(request):
    if request.method == 'POST':
        # form = ContactForm(request.POST)
        # if form.is_valid():
        subject = request.POST.get('subject')
        contact_email = request.POST.get('contact_email')
        body = {
            'title': f'You have a new message from a visitor to your website on {timezone.now().strftime("%a %b %d %H:%M:%S %Z %Y")}',
            'name': f"Visitor: {request.POST.get('name')}",
            'email': f"Visitor Email: {request.POST.get('email')}",
            # 'subject': f"Subject: {request.POST.get('subject')}",
            'message': f"Message: {request.POST.get('message')}",
        }
        message = MIMEText("\n".join(body.values()))
        message['Body'] = "\n".join(body.values())
        message['Subject'] = 'Message from Website visitor'
        message['From'] = 'info@gnotable.ng'
        message['To'] = 'info.canleeservices@gmail.com'

        try:
            send_mail(message['Subject'], message['Body'], message['From'], [message['To']], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        # return HttpResponse('OK')

        messages.info(request, "Your message has been sent")
        return redirect("index")
