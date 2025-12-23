from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class customusermodel(AbstractUser):
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(customusermodel, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username



class Post(models.Model):
    user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='posts')
    text=models.TextField()
    image=models.ImageField(upload_to='post_images/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='comments')
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    follower_user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='follower')
    following_user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='following')

    class Meta:
        unique_together=['follower_user','following_user']

class Like(models.Model):
    user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='userwholiked')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_likes',null=True,blank=True)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='comment_likes',null=True,blank=True)
    
    def clean(self):
        if not self.post and self.comment:
            raise ValidationError("Like must be for post or comment")
    class Meta:
        unique_together=(
        ('user','post'),
        ('user','comment')
        )


