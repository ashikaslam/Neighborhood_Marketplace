from django.contrib import admin

# Register your models here.
from .import models


from . import models
class  product_admin(admin.ModelAdmin):
    list_display=['user','title','category','id']


admin.site.register(models.Products,product_admin)