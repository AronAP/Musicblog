from django.contrib import admin

# Register your models here.

[('Danyil', 'danikdanik20133@gmail.com')]
from .models import User, Posts

admin.site.register(User)
admin.site.register(Posts)
