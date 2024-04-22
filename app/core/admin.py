from django.contrib import admin
from .models import Cpqol
# Register your models here.



class CpqolAdmin(admin.ModelAdmin):
	list_display = ['codigo', 'user', ]
	list_filter = ['user']

admin.site.register(Cpqol, CpqolAdmin)