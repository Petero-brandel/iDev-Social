from django.contrib import admin
from .models import Profile, Friend, Project, Post, Comment, Messages, Room, Topic

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'image')
    search_fields = ('user__username', 'bio')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'image')
    search_fields = ('title', 'description', 'user__username')

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__username', 'content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('user__username', 'content')

class LikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Messages)


