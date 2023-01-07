from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from room.models import Room


# Create your models here.
class Reservation(models.Model):
    # CHECKIN_CHOICES = (('in', 'Checked In'), ('out', 'Checked Out'))
    # PAYMENT_CHOICES = (('unpaid', 'Not Paid'), ('partial', 'Deposit'), ('paid', 'Paid Full'))
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phoneNumber = PhoneNumberField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return str(self.room.get_roomType_display) + " " + str(self.name)

    def length_of_stay(self):
        duration = 0
        # bookings = Booking.objects.filter(guest=self)
        day = self.endDate - self.startDate
        duration += int(day.days)

        return duration