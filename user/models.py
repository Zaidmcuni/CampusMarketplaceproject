from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    RESIDENCE_CHOICES = [
        ('carrefour_sherbrooke', 'Carrefour Sherbrooke'),
        ('new_residence', 'New Residence'),
        ('la_citadelle', 'La Citadelle'),
        ('royal_victoria', 'Royal Victoria College'),
        ('molson', 'Molson'),
        ('mcconnell', 'McConnell'),
        ('university_hall', 'University Hall'),
        ('douglas_hall', 'Douglas Hall'),
        ('solin_hall', 'Solin Hall'),
        ('laird_hall', 'Laird Hall'),
        ('off_campus', 'Off Campus'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    residence = models.CharField(max_length=255, choices=RESIDENCE_CHOICES, null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

# user/models.py

@receiver(post_save, sender=User)
def created_or_updated_user_profile(sender, instance, created, **kwargs):
    if created:
        # Use get_or_create to be extra safe
        Profile.objects.get_or_create(user=instance)
    else:
        # Only attempt to save if the profile already exists
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # If it's an existing user without a profile (like your superuser), create it now
            Profile.objects.create(user=instance)



