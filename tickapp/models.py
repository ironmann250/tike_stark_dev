from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Show(models.Model):
    idshow = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=100)
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
    iduser = models.CharField(primary_key=True, max_length = 40)
    event = models.ForeignKey(Show, default="0")
    def __str__(self):
        return self.iduser


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
    idticktype = models.CharField(primary_key=True,max_length =30)

    def __str__(self):
        return self.tike_types


class Admin:
    pass


class ticket(models.Model):
    event = models.CharField(max_length=30, null=True)
    phone_number = models.IntegerField(null=True)
    pin = models.CharField(max_length=10)
    email = models.EmailField()
    seller = models.CharField(max_length=20, null=True)
    Name = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=30, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.Name
    


class Admin:
    pass
