from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    def __str__(self):
        return self.username

class Prompt(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300)
    text = models.TextField()
    model = models.CharField(max_length=100)
    image = models.ImageField(upload_to='prompt_images/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_trending = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.title} by {self.username}"
    
    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = f"/media/{self.image.name}"
        super().save(*args, **kwargs)
