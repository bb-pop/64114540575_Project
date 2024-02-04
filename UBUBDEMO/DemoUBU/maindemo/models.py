from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    image = models.ImageField(upload_to='Item_images/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=50, null=True, default="user@example.com")
    id_student = models.CharField(max_length=11, null=True)
    faculty = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username

# สร้างหรืออัปเดตโปรไฟล์ผู้ใช้อัตโนมัติเมื่อผู้ใช้ถูกสร้างหรืออัปเดต
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     instance.userprofile.save()