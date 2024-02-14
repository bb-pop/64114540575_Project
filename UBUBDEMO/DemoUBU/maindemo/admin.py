from django.contrib import admin
from django.contrib.admin import AdminSite
from . import models
from maindemo.models import Item, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'prefix', 
        'email', 
        'first_name', 
        'last_name',
        'id_student',
        'faculty',
        'created_at',
        'updated_at',
    )
    
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'description', 
        'image', 
        'quantity',
        'max_borrow_time',
        'created_at',
        'updated_at',
    )
    
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = (
        'item', 
        'borrower', 
        'borrow_date', 
        'return_date',
        'quantity',
        'status',
        'updated_at',
    )

# admin.site.register(Item,ItemAdmin)
# admin.site.register(UserProfile,UserProfileAdmin)

class DemoAdminArea(admin.AdminSite):
    site_header = "Demo Admin Area"
    login_template = 'demo/admin/login.html'
    
demo_site = DemoAdminArea(name='DemoAdmin')

demo_site.register(models.Item,ItemAdmin)
demo_site.register(models.UserProfile,UserProfileAdmin)
demo_site.register(models.BorrowRecord,BorrowRecordAdmin)