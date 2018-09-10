from django.contrib import admin

# Register your models here.

[('Danyil', 'example@edu.com')]
from .models import User, Posts

admin.site.register(User)
admin.site.register(Posts)
