# Generated by Django 3.0 on 2021-11-29 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20211129_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Category', verbose_name='انتخاب کتگوری'),
            preserve_default=False,
        ),
    ]