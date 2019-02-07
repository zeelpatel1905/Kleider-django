from django.db import models
import os
import random
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField(default='')

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return self.name


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 1000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/{final_filename}".format(final_filename=final_filename)


class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter valid phone number. Phone number must be enterd in the formate : '+9999999999'.")
    GANDER_CHOICES= {
        ('M','Male',),
        ('F', 'Female',),
        ('O', 'other',),
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(validators=[phone_regex],max_length=15,blank=True)
    gender = models.CharField(max_length=1, choices=GANDER_CHOICES,)
    birth_date = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Help(models.Model):
    write = models.CharField(max_length=200)

    def __str__(self):
        return self.write

class Feedback(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    write = models.CharField(max_length=200)

    def __str__(self):
        return self.write
