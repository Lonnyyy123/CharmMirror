from django.contrib import admin

# Register your models here.
from myapp.models import Moment, User
admin.site.register(Moment)
admin.site.register(User)

