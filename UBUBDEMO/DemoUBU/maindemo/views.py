from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from maindemo.models import Item
from maindemo.forms import ItemForm
from django.contrib.auth.decorators import login_required

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
