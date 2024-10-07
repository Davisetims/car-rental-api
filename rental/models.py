from django.db import models
from car.models import Car
from users.models import User

class Rental(models.Model):
    class RentalStatus(models.TextChoices):
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    rental_status = models.CharField(max_length=10, choices=RentalStatus.choices, default=RentalStatus.ONGOING)
    total_cost = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.return_date:
            rental_duration = (self.return_date - self.rental_date).days
            if rental_duration <= 0:
                rental_duration = 1

            self.total_cost = rental_duration * self.car.daily_rental_rate
        else:
    
            self.total_cost = 0.0

        super().save(*args, **kwargs) 

    def __str__(self):
        return f"Rental {self.id} by {self.customer.username}"
    
    


