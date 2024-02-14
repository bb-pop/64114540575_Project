from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from maindemo.models import BorrowRecord, Item, UserProfile
from maindemo.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .forms import UserProfileForm
from django.db.models import F

def home(request):
    if request.user.is_authenticated: 
        return redirect('/index')  # Assuming 'index' is the name of your URL pattern
    return render(request, "home.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def index(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, "index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # รับข้อมูลจาก POST และ FILES (สำหรับรูปภาพ)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ItemForm()
    context = {
        'form': form
    }
    return render(request, "create.html", context)

@login_required
def edit(request, id):
    it = Item.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=it)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ItemForm(instance=it)
    
    context = {
        'it': it,
        'form': form
    }
    return render(request, 'edit.html', context)

@login_required  
def delete(request,id):
    it = Item.objects.get(pk=id)
    it.delete()
    return redirect('index')

@login_required 
@receiver(user_logged_in)
def create_or_update_user_profile_on_login(sender, user, **kwargs):
    UserProfile.objects.get_or_create(user=user)

@login_required
def edit_user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # ส่งกลับไปยังหน้าโปรไฟล์หรือหน้าอื่น
            return redirect('index')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def contact(request):
    return render(request, "contact.html")

@login_required
def detail(request, id):
    it = Item.objects.get(pk=id)
    context = {
        'it': it,
    }
    return render(request, 'item_detail.html', context)

@login_required
def confirm(request, id):
    it = Item.objects.get(pk=id)
    context = {
        'it': it,
    }
    return render(request, 'confirm.html', context)

# @login_required
# def borrow_item(request, item_id):
#     # ตรวจสอบว่าอุปกรณ์ที่ต้องการยืมมีอยู่จริงหรือไม่
#     try:
#         item = Item.objects.get(pk=item_id)
#     except Item.DoesNotExist:
#         return HttpResponse('Item does not exist', status=404)

#     # สร้างหรืออัปเดต BorrowRecord
#     if request.method == 'POST':
#         quantity_to_borrow = int(request.POST.get('quantity', 1))
        
#         # ตรวจสอบว่ามีอุปกรณ์เพียงพอให้ยืมหรือไม่
#         if item.quantity < quantity_to_borrow:
#             return HttpResponse('Not enough items available', status=400)
        
#         # สร้าง record การยืมใหม่
#         borrow_record = BorrowRecord.objects.create(
#             item=item,
#             borrower=request.user.userprofile,  # สมมติว่าผู้ใช้มี UserProfile เชื่อมโยงกับ User
#             quantity=quantity_to_borrow,
#             status='pending'  # หรืออาจตั้งค่าเป็น 'borrowed' ตามกระบวนการอนุมัติของคุณ
#         )
        
#         # อัปเดตจำนวนอุปกรณ์ที่เหลือ
#         item.quantity -= quantity_to_borrow
#         item.save()

#         return redirect('/')
#     else:
#         # แสดงฟอร์มหรือข้อมูลการยืมหากเป็น GET request
#         return render(request, 'confirm.html', {'item': item})

# @login_required
# def confirm(request, id):
#     # Correctly get the item using its ID
#     item = get_object_or_404(Item, pk=id)
    
#     if request.method == 'POST':
#         # Assuming 'borrower_id' comes from the form or session, if not, adjust accordingly
#         borrower_id = request.POST.get('borrower_id', request.user.userprofile.id)
#         quantity = int(request.POST.get('quantity', 1))
        
#         # It's safe to assume the borrower is the logged-in user, adjust if necessary
#         borrower = get_object_or_404(UserProfile, pk=borrower_id)
        
#         # Create a new BorrowRecord with the item already defined
#         borrow_record = BorrowRecord(
#             item=item,
#             borrower=borrower,
#             quantity=quantity,
#             status='pending'  # or 'borrowed', depending on your application flow
#         )
        
#         try:
#             borrow_record.save()
#             messages.success(request, "Item borrowed successfully.")
#         except ValueError as e:
#             messages.error(request, str(e))
        
#         # Redirect to 'index' or another appropriate view
#         return redirect('index')
#     else:
#         # If not a POST request, render your form and pre-select the item
#         # Ensure 'id' is passed correctly for form action and other uses
#         return render(request, 'confirm.html', {'it': item, 'id': item.id})

@login_required
def confirm(request, id):
    item = get_object_or_404(Item, pk=id)
    
    if request.method == 'POST':
        borrower_id = request.POST.get('borrower_id', request.user.userprofile.id)  # Adjust as needed
        quantity = int(request.POST.get('quantity', 1))
        
        borrower = get_object_or_404(UserProfile, pk=borrower_id)
        
        # Check if the item has enough quantity for borrowing
        if item.quantity >= quantity:
            # Proceed with creating the BorrowRecord
            borrow_record = BorrowRecord(
                item=item,
                borrower=borrower,
                quantity=quantity,
                status='pending'  # Adjust based on your application's logic
            )
            
            try:
                borrow_record.save()  # This also updates the item quantity
                
                # After saving, manually decrease the item's quantity and save
                # Using F() ensures the operation is atomic and avoids race conditions
                item.quantity = F('quantity') - quantity
                item.save()
                
                # Update item instance to reflect the new quantity
                item.refresh_from_db()
                
                messages.success(request, "Item borrowed successfully.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            # Not enough items available
            messages.error(request, "Not enough items available to borrow.")
        
        return redirect('index')
    else:
        return render(request, 'confirm.html', {'it': item, 'id': item.id})
