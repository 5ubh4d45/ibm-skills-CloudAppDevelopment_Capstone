from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=400)

    def __str__(self) -> str :
        return f"Name: {self.name}\
            \nDescription: {self.description}\
            \nCar Models: {self.carModels}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.PositiveIntegerField(null=False)
    year = models.DateField(null=False)
    carMake = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="carModels",
        null=False)
    
    SEDAN = "SEDAN"
    SUV = "SUV"
    WAGON = "WAGON"
    HATCHBACK = "HATCHBACK"
    UNKNOWN = "UNDEFINED"
    Car_Type_Choices = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (HATCHBACK, "Hatchback"),
        (UNKNOWN, "UNKNOWN")
    ]
    car_type = models.CharField(null=False, max_length=20, choices=Car_Type_Choices, default=UNKNOWN)

    def __str__(self) -> str:
        return f"Name: {self.name}\
            \nDealer ID: {self.dealer_id}\
            \nYear: {self.year}\
            \nCar Make: {self.carMake}\
            \nCar Type: {self.car_type}"



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id=None):
        # Dealer id
        self.id = id
        # Dealership id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Reviewer purchase
        self.purchase = purchase
        # Reviewer review
        self.review = review
        # Reviewer purchase date
        self.purchase_date = purchase_date
        # Reviewer car make
        self.car_make = car_make
        # Reviewer car model
        self.car_model = car_model
        # Reviewer car year
        self.car_year = car_year
        # Reviewer sentiment
        self.sentiment = sentiment
    def __str__(self):
        return f"Dealer: {self.dealership}\
            \nName: {self.name}\
            \nPurchase: {self.purchase}\
            \nReview: {self.review}\
            \nPurchase Date: {self.purchase_date}\
            \nCar Make: {self.car_make}\
            \nCar Model: {self.car_model}\
            \nCar Year: {self.car_year}\
            \nSentiment: {self.sentiment}"