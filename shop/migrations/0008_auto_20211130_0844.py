# Generated by Django 3.0 on 2021-11-30 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_entry_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_entry',
            name='categor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Category', verbose_name='انتخاب کتگوری'),
        ),
    ]