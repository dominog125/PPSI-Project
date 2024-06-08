from django.contrib import admin
from .models import User, Category, Thread, Post, Like, PrivateMessage, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(PrivateMessage)
admin.site.register(Comment)
