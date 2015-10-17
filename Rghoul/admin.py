from django.contrib import admin
from models import Picture, Comment, Dish, Poll

class PictureAdmin(admin.ModelAdmin):
    list_display = ("picName", "date", "mealTime", "floor", "like", "dislike")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "context", "parent", "date")

class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "booth", "ingredient", "energy", "price", "date", "mealTime", "floor", "like", "dislike")

class PollAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "open", "parent", "code", "result", "count")

admin.site.register(Picture, PictureAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Poll, PollAdmin)
