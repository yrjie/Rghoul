from django.contrib import admin
from models import Picture, Comment

class PictureAdmin(admin.ModelAdmin):
    list_display = ("picName", "date", "mealTime", "floor", "like", "dislike")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "context", "parent", "date")

admin.site.register(Picture, PictureAdmin)
admin.site.register(Comment, CommentAdmin)