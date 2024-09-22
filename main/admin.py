from django.contrib import admin
from .models import Profile, Project

# Customize Profile display in the admin panel
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'image')
    search_fields = ('user__username', 'bio')

# Customize Project display in the admin panel
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'image')
    search_fields = ('title', 'description', 'user__username')

# Register models with the admin site
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
