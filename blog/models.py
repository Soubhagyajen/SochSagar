from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # image=models.ImageField(upload_to="images/",blank=True,null=True)
    # image = models.BinaryField(null=True, blank=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)


    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post.title}"    
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    views = models.IntegerField(default=0)


class Poll(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)

    def total_votes(self):
        return self.votes1 + self.votes2
