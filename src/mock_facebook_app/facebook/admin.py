from django.contrib import admin

from facebook.models import Post, Like, Comment


class PostAdmin(admin.ModelAdmin):
    fields = ['user', 'text', 'datetime']
    list_display = ('user', 'text', 'datetime')


class LikeAdmin(admin.ModelAdmin):
    fields = ['user', 'post']
    list_display = ('user', 'post')


class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'post', 'text', 'datetime']
    list_display = ('user', 'post', 'text', 'datetime')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
