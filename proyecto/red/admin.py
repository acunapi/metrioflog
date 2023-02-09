from django.contrib import admin
from .models import Post, Profile, Relationships
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Relationships)
