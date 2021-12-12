from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.db.models.signals import post_save



class Category(models.Model):
    title = models.CharField(unique=True, null=True, max_length=100,verbose_name="اسم دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, null=True, verbose_name="آدرس دسته بندی؟")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")

    def __str__(self):
        return self.title

class color(models.Model):
    id1 = models.IntegerField(verbose_name="ایدی")
    title = models.CharField(max_length=100, null=True, verbose_name="رنگ")

    def __str__(self):
        return self.title


class img(models.Model):
    title = models.CharField(max_length=100,verbose_name="اسم")
    imag = models.ImageField(upload_to = "images/")
    qty = models.IntegerField(verbose_name="تعداد")

    def __str__(self):
        return self.title



class Item(models.Model):
    MATERIAL_CHOICES = (
		('درجه یک', 'درجه یک'),		 
		('متوسط', "متوسط"),	
	)
    title = models.CharField(max_length=100, null=True,verbose_name="اسم کالا")
    slug = models.SlugField(max_length=100, unique=True,verbose_name="ادرس کالا")
    description = models.TextField(verbose_name="توضیحات")
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, verbose_name="کیفیت")
    price = models.DecimalField(max_digits=30, null=True, decimal_places=0,verbose_name="قیمت")
    pic = models.ImageField(upload_to = "images/", verbose_name="عکس اصلی")
    categor = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="انتخاب کتگوری", related_name="products")
    color_id = models.ManyToManyField(color)
    img_id = models.ManyToManyField(img, related_name="img")


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shopping:detail", kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("cart:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("cart:remove-from-cart", kwargs={'slug': self.slug})
    


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    Prod = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)



    def __str__(self):
        return f"{self.quantity} of {self.Prod.title}"

    def get_total_product_price(self):
        return self.quantity * self.Prod.price

    def get_final_price(self):
        return self.get_total_product_price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username




def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
