from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from accounts.models import Guest, Employee
from phonenumber_field.modelfields import PhoneNumberField
from room.models import Room


# Create your models here.
class Announcement(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.sender)


class Event(models.Model):
    EVENT_TYPES = (
        ('Movie', 'Movie'),
        ('Theater', 'Theater'),
        ('Conference', 'Conference'),
        ('Concert', 'Concert'),
        ('Entertainment', 'Entertainment'),
        ('Live Music', 'Live Music'),
    )

    eventType = models.CharField(max_length=20, choices=EVENT_TYPES)
    location = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    explanation = models.TextField()

    def __str__(self):
        return str(self.eventType)


class EventAttendees(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    numberOfDependees = models.IntegerField(default=0)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + " " + str(self.guest)


class Bills(models.Model):
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)
    totalAmount = models.FloatField()
    summary = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.guest) + " " + str(self.summary) + " " + str(self.totalAmount)

    class Meta:
        verbose_name_plural = 'Bills'


class FoodMenu(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    menuItems = models.TextField()

    def __str__(self):
        return str(self.menuItems) + " " + str(self.startDate)


class Report(models.Model):
    date = models.DateField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return str(self.content) + " " + str(self.date)


class Storage(models.Model):
    ITEM_TYPES = (
        ('Kitchen', 'kitchen'),
        ('Cleaning', 'cleaning'),
        ('Electronic', 'Electronic'),
        ('Linen', 'linen'),
        ('Drinks', 'drinks'),
        ('Other', 'other'),
    )
    itemName = models.CharField(max_length=100)
    itemType = models.CharField(max_length=20, choices=ITEM_TYPES)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.itemName)


class Drink(models.Model):
    DRINK_TYPES = (
        ('wine', 'Wine'),
        ('beer', 'Beer'),
        ('bitters', 'Bitters'),
        ('soft', 'Soft Drinks'),
        ('spirit', 'Spirit'),
        ('water', 'Water'),
        ('other', 'Other'),
    )
    brand = models.CharField(max_length=50)
    drinkType = models.CharField(max_length=20, choices=DRINK_TYPES)
    price = models.FloatField()
    initial_stock = models.IntegerField()
    topup_stock = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    total_sales = models.FloatField(default=0)

    def __str__(self):
        return str(self.brand)

    @property
    def get_total_stock(self):
        initial = int(self.initial_stock)
        topup = int(self.topup_stock)
        total = initial + topup
        return total

    def save(self, *args, **kwargs):
        try:
            self.total_stock = self.get_total_stock
            if self.quantity == 0:
                self.quantity = self.initial_stock
        except Exception as e:
            print(e)
        super().save(*args, **kwargs)


class Sales(models.Model):
    item = models.ForeignKey(Drink, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    quantity = models.IntegerField()
    sales_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item)

    def save(self, *args, **kwargs):
        try:
            stock = Drink.objects.get(brand=self.item.brand)
            if stock.quantity > 0:
                stock.quantity -= self.quantity
            else:
                stock.quantity = stock.total_stock - self.quantity
            stock.total_sales += stock.price * self.quantity
            stock.save()
        except Exception as e:
            print(e)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Sales"
