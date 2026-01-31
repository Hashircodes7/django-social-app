from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from insta.models import customusermodel,Post,Comment,Like,Follower,Profile
# Register your models here.
@admin.register(customusermodel)
class CustomUserAdmin(UserAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'is_staff', 'is_superuser']
    search_fields = ['username','first_name','last_name']
    
@admin.register(Profile)
class profileregistermodel(admin.ModelAdmin):
    list_display = ['id','user', 'bio', 'avatar']
    search_fields = ['user__username', 'bio']


@admin.register(Post)
class postregistermodel(admin.ModelAdmin):
    list_display=['id','user','text','created_at']
    search_fields=['user__username','created_at']
    
@admin.register(Comment)
class commentregistermodel(admin.ModelAdmin):
    list_display=['id','post','user','text','created_at']
    search_fields=['post__text','user__username','created_at']
@admin.register(Like)
class likeregistermodel(admin.ModelAdmin):
    list_display=['id','user','post','comment']
    search_fields=['post__text','comment__text']
@admin.register(Follower)
class followerregistermodel(admin.ModelAdmin):
    list_display=['id','follower_user','following_user']
    search_fields=['follower_user__username','following_user__username']
