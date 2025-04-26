from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

#برای پروفایل
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
