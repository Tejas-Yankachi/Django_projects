# filepath: c:\cms\myenv\cemproj\cemapp\models.py
from django.db import models
from django.contrib.auth.models import User  # Import User for linking profiles
from django.shortcuts import render

class Profile(models.Model):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

def __str__(self):
        return self.user.username


class Fertilizer(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    minimum_stock = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='fertilizers/', null=True, blank=True)

    def __str__(self):
        return self.name

    def is_low_stock(self):
        return self.quantity <= self.minimum_stock


class SoilType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ph_range = models.CharField(max_length=50)  # Changed to CharField for simplicity

    def __str__(self):
        return self.name

class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ideal_soil = models.ForeignKey(SoilType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from django.db import models

class Recommendation(models.Model):
    crop = models.ForeignKey('Crop', on_delete=models.CASCADE)
    soil_type = models.ForeignKey('SoilType', on_delete=models.CASCADE)
    suitable_fertilizers = models.ManyToManyField('Fertilizer', blank=True)

    def __str__(self):
        return f"Recommendation for {self.crop.name} on {self.soil_type.name}"
    


class Sale(models.Model):
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    # Farmer details
    farmer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Only reduce stock on first save
            if self.quantity_sold <= 0:
                raise ValueError("Quantity sold must be greater than 0.")
            if self.quantity_sold > self.fertilizer.quantity:
                raise ValueError("Insufficient stock for the selected fertilizer.")
            self.fertilizer.quantity -= self.quantity_sold
            self.fertilizer.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer_name} - {self.fertilizer.name} on {self.date.date()}"

    @property
    def total_price(self):
        return self.quantity_sold * self.unit_price

    @property
    def amount_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance_due(self):
        return self.total_price - self.amount_paid
    
class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
    )
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - ₹{self.amount} on {self.date.date()}"

