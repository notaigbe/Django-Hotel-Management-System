from django.contrib.postgres.fields import DateRangeField, DateTimeRangeField
from django.db import models
from django.utils import timezone

from accounts.models import Guest
# Create your models here.


class Room(models.Model):
    ROOM_TYPES = (
        ('1', '3 Bedroom'),
        ('2', '2 Bedroom'),
        ('3', '1 Bedroom'),
        ('4', 'Single Room'),
    )
    ORDER_TYPES = (
        ('order-1', 'ORDER 1'),
        ('order-2', 'ORDER 2'),
    )
    name = models.CharField(max_length=20, unique=True)
    number = models.IntegerField(primary_key=True)
    capacity = models.SmallIntegerField()
    numberOfBeds = models.SmallIntegerField()
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.FloatField()
    caution_fee = models.FloatField(default=0)
    statusStartDate = models.DateField(null=True, blank=True)
    statusEndDate = models.DateField(null=True, blank=True)
    offer = models.FloatField(default=0)
    offerType = models.CharField(max_length=20, choices=ORDER_TYPES, default='order-1')
    image = models.ImageField(upload_to='media/rooms', blank=True,
                                           null=True, default='Normal.jpg')
    description_p1 = models.TextField(max_length=500, null=True, blank=True)
    description_p2 = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def numOfDep(self):
        return Dependants.objects.filter(booking=self).count()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)


class Dependants(models.Model):
    booking = models.ForeignKey(Booking,   null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def str(self):
        return str(self.booking) + " " + str(self.name)


class Refund(models.Model):
    guest = models.ForeignKey(Guest,   null=True, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return str(self.guest)


class RoomServices(models.Model):
    SERVICES_TYPES = (
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning'),
        ('Technical', 'Technical'),
    )

    curBooking = models.ForeignKey(
        Booking,   null=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    createdDate = models.DateField(default=timezone.now)
    servicesType = models.CharField(max_length=20, choices=SERVICES_TYPES)
    price = models.FloatField()

    def str(self):
        return str(self.curBooking) + " " + str(self.room) + " " + str(self.servicesType)
