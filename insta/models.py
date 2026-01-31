from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from .validateimage import validate_image
# Create your models here.
class customusermodel(AbstractUser):
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(customusermodel, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, validators=[validate_image])
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='posts')
    text=models.TextField()
    image=models.ImageField(upload_to='post_images/',null=True,blank=True, validators=[validate_image])
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created_at}"
 
    

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='comments')
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on Post {self.post.id}"

class Follower(models.Model):
    follower_user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='followers')
    following_user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='following')

    class Meta:
        unique_together=['follower_user','following_user']

    def clean(self):
        if self.follower_user == self.following_user:
            raise ValidationError('User cannot follow themselves')

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)


class Like(models.Model):
    user=models.ForeignKey(customusermodel,on_delete=models.CASCADE,related_name='userwholiked')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_likes',null=True,blank=True)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='comment_likes',null=True,blank=True)
    
    def clean(self):
        if not self.post and not self.comment:
            raise ValidationError("Like must be for post or comment")
    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['user', 'post'],
            condition=models.Q(post__isnull=False),
            name='unique_post_like'
        ),
        models.UniqueConstraint(
            fields=['user', 'comment'],
            condition=models.Q(comment__isnull=False),
            name='unique_comment_like'
        ),
    ]

