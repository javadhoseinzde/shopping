# Generated by Django 3.0 on 2021-11-28 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_entry',
            name='title',
            field=models.CharField(default=1, max_length=100, verbose_name='اسم محصول'),
            preserve_default=False,
        ),
    ]
