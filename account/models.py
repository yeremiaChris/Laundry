from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Anak(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    CATEGORY = (
            ('Masih Cuci','Masih Cuci'),
            ('Selesai','Selesai'),
            ('Kosong','Kosong'),
            )
    nama = models.CharField(max_length=30)
    jumlah = models.IntegerField(default=0)
    tanggal_antar = models.DateTimeField(default=timezone.now)
    status =  models.CharField(max_length=20,choices=CATEGORY,default='Kosong')
    image_profile = models.ImageField(default='default.png',upload_to='profile_pics')

    def __str__(self):
        return self.nama
