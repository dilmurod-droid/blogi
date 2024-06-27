from django.conf import settings
from django.core.validators import FileExtensionValidator
from myapp.models import CustomUser
from django.utils.text import slugify
from django.db import models
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table="categories"
        ordering=['-id']

class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags"
        ordering = ['-id']

class Blog(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    body=models.TextField()
    photo=models.ImageField(upload_to='blogs/img/',null=True,blank=True)
    video=models.FileField(upload_to='blogs/video/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,blank=True)
    slug=models.SlugField(unique=True, blank=True, null=True)
    created_time=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.author}:{self.title}"

    class Meta:
        db_table = "blogs"
        ordering = ['-created_time']

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,related_name='comments',on_delete=models.CASCADE)
    body=models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author}:{self.blog.title}"

    class Meta:
        db_table = "comments"
        ordering = ['-created_time']
class Likes(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,related_name='likes',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author}:{self.blog}"

    class Meta:
        db_table = "likes"
        ordering = ['-created_time']
        unique_together = ('author', 'blog')
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_time']
class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
