from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"Name: {self.name}. Description: {self.description}"


class CarModel(models.Model):

    TYPE_CHOICES = [
        ("sedan", 'Sedan'),
        ("suv", 'SUV'),
        ("wagon", 'Wagon')
    ]
    carmake =  models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    dealer_id = models.IntegerField()
    type_of_car = models.CharField(
        max_length=20,
        choices = TYPE_CHOICES,
        default = "sedan"
    )
    year = models.DateField(default=now)

    def __str__(self):
        return f"Model: {self.name}, Description: {self.description}, Type: {self.type_of_car}, Year: {self.year}"



class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):

        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, car_model, car_year, car_make, dealership, id, name, purchase, purchase_date, review):
        
        self.car_model = car_model
        self.car_year = car_year
        self.dealer_id = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.car_make = car_make
        self.sentiment = ""

    def __str__(self):
        return "Dealer name: " + self.name
