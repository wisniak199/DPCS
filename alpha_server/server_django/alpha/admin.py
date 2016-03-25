from django.contrib import admin
from .models import CrashGroup, Application, CrashReport, SystemInfo, Solution
# Register your models here.

admin.site.register(CrashGroup)
admin.site.register(Application)
admin.site.register(CrashReport)
admin.site.register(SystemInfo)
admin.site.register(Solution)