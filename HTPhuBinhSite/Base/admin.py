from django.contrib import admin
from ThietLapNamHocMoi.models import HuynhTruong
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(HuynhTruong, UserAdmin)