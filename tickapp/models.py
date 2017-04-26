from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Show(models.Model):

    title = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    poster = models.ImageField(upload_to="media/img")
    video = models.FileField(upload_to="media/video")
    Description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=100, default="0")
    tickets_no = models.IntegerField()

    def __str__(self):
        return self.title


class Admin:
    pass


class profile(models.Model):
    seller = models.ForeignKey(User)
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Show, default="0")


''' @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
	'''


class Admin:
    pass


class tickettype(models.Model):
    tike_types = models.CharField(max_length=30)
    event = models.ForeignKey(Show)
    amount = models.IntegerField()
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.tike_type


class Admin:
    pass


class ticket(models.Model):
    event = models.ForeignKey(Show, null=True)
    id = models.AutoField(primary_key=True)
    phone_number = models.IntegerField(null=True)
    email = models.EmailField()
    seller = models.ForeignKey(profile, default="0", null=True)
    Name = models.CharField(max_length=100, default="0")
    ticket_type = models.ForeignKey(tickettype, default="0", null=True)
    status = models.BooleanField(default=False)
    pin = models.CharField(max_length=10)


class Admin:
    pass
