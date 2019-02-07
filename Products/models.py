from django.db import models
from Home.models import Profile
import os
import random
from django.urls import reverse
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, SmartResize

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 1000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Products/{final_filename}".format(final_filename=final_filename)


class Product(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female'),
    )
    CONDITION_CHOICES = (
        ('used', 'Uerd',),
        ('new', 'New',),
    )
    CATEGORY_CHOICES = (
        ('traditional', 'Traditional',),
        ('formal', 'Formal',),
        ('casual', 'Casual',),
        ('ethnic', 'Ethnic',),
        ('sports', 'Sports',),
        ('western', 'Western',),
        ('t-shirts', 'T-shirts',),
        ('kids', 'Kids',),
        ('jumpsuits', 'Jumpsuits',),
        ('denim', 'Denim',),
        ('winter', 'Winter war',),
    )
    OCCASION_CHOICES = (
        ('wedding', 'Wedding',),
        ('sangeet', 'Sangeet',),
        ('party', 'Party',),
        ('everyday', 'Everyday',),
        ('interview', 'Interview',),
        ('gym', 'Gym',),
        ('outings', 'Outings',),
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES)
    category = models.CharField(max_length=11, choices=CATEGORY_CHOICES)
    occasion = models.CharField(max_length=9, choices=OCCASION_CHOICES)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to=upload_image_path)
    image2 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image4 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    smart1 = ImageSpecField(source='image1', processors=[ResizeToFill(250,250)], format="JPEG", options={'quality': 99})
    smart2 = ImageSpecField(source='image2', processors=[SmartResize(250, 250)], format="JPEG", options={'quality': 99})
    smart3 = ImageSpecField(source='image3', processors=[SmartResize(250, 250)], format="JPEG", options={'quality': 99})
    smart4 = ImageSpecField(source='image4', processors=[SmartResize(250, 250)], format="JPEG", options={'quality': 99})

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Product'

    # on submit click on the product entry page, it redirects to the url below.

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
