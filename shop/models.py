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
    price_discount = models.IntegerField(default=0, verbose_name="تخفیف")
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

    """def discount(self):
        if self.price_discount == 0:
            return self.price
        elif self.price_discount != 0:
            disc = self.price * self.price_discount 
            disct =  disc - self.price
            return disct

"""


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

    def get_total_item_price(self):
        return self.quantity * self.Prod.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    username_recive = models.CharField(verbose_name="نام دریافت کننده", max_length=100)
    phone_number = models.IntegerField(verbose_name="شماره همراه")
    code_posti = models.IntegerField(verbose_name="کدپستی")
    address = models.CharField(max_length=250, verbose_name="آدرس")
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
