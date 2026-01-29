from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
print("listings loaded")

class Listings(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    CATEGORY_CHOICES = [           
        ("item", "Item"),
        ("service", "Service"),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="listings/", null=True, blank=True)

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    createdat = models.DateTimeField(default=timezone.now)


    RESIDENCE_CHOICES = [          
        ("carrefour_sherbrooke", "Carrefour Sherbrooke"),
        ("new_residence", "New Residence"),
        ("la_citadelle", "La Citadelle"),
        ("royal_victoria", "Royal Victoria College"),
        ("molson", "Molson"),
        ("mcconnell", "McConnell"),
        ("university_hall", "University Hall"),
        ("douglas_hall", "Douglas Hall"),
        ("solin_hall", "Solin Hall"),
        ("laird_hall", "Laird Hall"),
        ("off_campus", "Off Campus"),
    ]
    residence = models.CharField(max_length=50, choices=RESIDENCE_CHOICES)
    is_sold = models.BooleanField(default=False)
    def __str__(self):
        return self.title
