from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import Likes

@receiver(post_save, sender=Likes)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        blog = instance.blog
        user = instance.user
        message = f'{user.username} sizning bu blogingizga layk bosdi: {blog.title}.'
        messages.success(instance.blog.author, message)
