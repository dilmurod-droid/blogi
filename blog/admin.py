from django.contrib import admin
from blog.models import Category,Tag,Blog,Comment,Likes,Contact,Notification
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Contact)
admin.site.register(Notification)
