# Generated by Django 3.0.6 on 2020-06-06 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200601_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anak',
            name='status',
            field=models.CharField(choices=[('Masih Cuci', 'Masih Cuci'), ('Selesai', 'Selesai'), ('Kosong', 'Kosong')], default='Kosong', max_length=20),
        ),
    ]