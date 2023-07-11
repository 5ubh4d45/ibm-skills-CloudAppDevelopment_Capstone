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


# <HINT> Create a plain Python class `DealerReview` to hold review data
