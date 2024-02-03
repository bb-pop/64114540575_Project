from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from maindemo.models import Item, UserProfile
from maindemo.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .forms import UserProfileForm

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