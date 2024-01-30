from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่ออุปกรณ์")
    description = models.TextField(verbose_name="รายละเอียด")
    image = models.ImageField(upload_to='Item_images/', blank=True, null=True, verbose_name="รูปภาพ")
    quantity = models.PositiveIntegerField(default=0, verbose_name="จำนวน")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="เวลาที่เพิ่ม")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="เวลาที่อัปเดต")

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=100, null=True, verbose_name="คำนำหน้า")
    first_name = models.CharField(max_length=100, null=True, verbose_name="ชื่อ")
    last_name = models.CharField(max_length=100, null=True, verbose_name="นามสกุล")
    email = models.EmailField(max_length=50, null=True, default="user@example.com", verbose_name="อีเมล")
    id_student = models.CharField(max_length=11, null=True, verbose_name="รหัสนักศึกษา")
    faculty = models.CharField(max_length=100, null=True, verbose_name="คณะ")

    def __str__(self):
        return self.user.username

# สร้างหรืออัปเดตโปรไฟล์ผู้ใช้อัตโนมัติเมื่อผู้ใช้ถูกสร้างหรืออัปเดต
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     instance.userprofile.save()