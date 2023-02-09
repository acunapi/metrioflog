from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_profile_image


urlpatterns = [
    path('', views.feed, name='feed'),
    path('upload_profile_image/', upload_profile_image, name='upload_profile_image'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage),
    path('logout/', views.logoutPage),
    path('post/', views.post, name='post'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('comment/', views.comment, name='comment'),
    path('like/', views.like, name='like'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #segun documentación: https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development

