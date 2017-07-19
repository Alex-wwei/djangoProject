from django.contrib import admin

# Register your models here.

from web01.models import *

admin.site.register(userInfo)
admin.site.register(orderInfo)
admin.site.register(orderProInfo)
admin.site.register(product)
admin.site.register(category)
admin.site.register(cart)
