from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('learn/', views.learn, name='learn-page'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/<str:username>/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('add_friend/<str:user_id>/', views.add_friend, name='add-friend'),
    path('project_upload/', views.project_upload, name='add-project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete-project'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete-post'),
    path('add_post/', views.add_post, name='add_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('create_group/', views.create_group, name='create-group'),
    path('group_in/<str:pk>/', views.group_details, name='group-in'),
    path('group/<int:pk>/join/', views.join_group, name='join-group'),
    path('delete_group/<str:pk>/', views.delete_group, name='delete-group'),
    # path('edit_group/<str:pk>/', views.edit_group, name='edit_group'),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
