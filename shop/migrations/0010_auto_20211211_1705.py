# Generated by Django 3.0 on 2021-12-11 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_orderitem_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='اسم کالا')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='ادرس کالا')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('material', models.CharField(choices=[('درجه یک', 'درجه یک'), ('متوسط', 'متوسط')], max_length=50, verbose_name='کیفیت')),
                ('price', models.DecimalField(decimal_places=0, max_digits=30, null=True, verbose_name='قیمت')),
                ('pic', models.ImageField(upload_to='images/', verbose_name='عکس اصلی')),
                ('categor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Category', verbose_name='انتخاب کتگوری')),
                ('color_id', models.ManyToManyField(to='shop.color')),
                ('img_id', models.ManyToManyField(related_name='img', to='shop.img')),
            ],
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='Prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Item'),
        ),
        migrations.DeleteModel(
            name='product_entry',
        ),
    ]
