# Generated by Django 3.0 on 2021-12-22 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_item_price_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price_discount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5, verbose_name='تخفیف'),
        ),
    ]