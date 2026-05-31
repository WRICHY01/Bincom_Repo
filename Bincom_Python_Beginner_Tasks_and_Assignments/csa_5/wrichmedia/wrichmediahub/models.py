from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="Posts"
        )

    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-date_uploaded"]

    def __str__(self):
        return f"{self.title} by {self.author.username}"
    


class MediaItem(models.Model):
    
    MEDIA_TYPES = [
        ("text", "Text"),
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Video")
    ]

    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE,
                             related_name="media_items"
                             )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    text_content = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to="images/", blank=True, null=True)
    audio_file = models.FileField(upload_to="audios/", blank=True, null=True)
    video_file = models.FileField(upload_to="videos/", blank=True, null=True)

    def __str__(self):
        return f"{self.media_type} Item - {self.post.title}"

