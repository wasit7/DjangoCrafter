from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Bike(models.Model):
    # For example, a bike name and its status
    name = models.CharField(max_length=200, unique=True)
    is_available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)

    def __str__(self):
        return self.name

class Rental(models.Model):
    # Rental references user, bike, start & end times, total fee
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
    total_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Rental: {self.user.username} - {self.bike.name}"

    def save(self, *args, **kwargs):
        # If end_time is set, we can automatically calculate total fee
        # based on difference in hours and the bike's hourly_rate
        if self.end_time and not self.total_fee:
            duration = self.end_time - self.start_time
            hours = Decimal(duration.total_seconds() / 3600)
            self.total_fee = round(hours * self.bike.hourly_rate, 2)

            # Mark bike as available again
            self.bike.is_available = True
            self.bike.save()

        else:
            # Mark the bike as not available when rental is created
            self.bike.is_available = False
            self.bike.save()

        super().save(*args, **kwargs)
