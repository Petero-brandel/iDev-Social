from django.contrib import admin
from .models import Profile, Friend, Project, Post, Comment, Group, Conversations
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
    
class ConversationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'body', 'created_at' 'updated_at')
    search_fields = ('user__username', 'content')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Group)
admin.site.register(Conversations)

