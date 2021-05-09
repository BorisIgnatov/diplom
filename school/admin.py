from django.contrib import admin
from school.models import *
# Register your models here.

admin.site.register(Image)
admin.site.register(CustomUser)
admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Schedule)
admin.site.register(Quarter)

