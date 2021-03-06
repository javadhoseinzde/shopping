from django.contrib import admin
from .models import Category, color, img, Item,Order, UserProfile, OrderItem, Order

admin.site.register(UserProfile)
admin.site.register(OrderItem)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Order, OrderAdmin)


admin.site.register(Category)
admin.site.register(color)
admin.site.register(img)
admin.site.register(Item)