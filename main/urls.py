from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/<str:username>/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('add_post/', views.add_post, name='add-post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
