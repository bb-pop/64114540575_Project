from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home),
    path("logout/", views.logout_view),
    path('index/', views.index, name='index'),
    path('create/',  views.create, name='create'),
    path('delete/<int:id>/',  views.delete, name='delete'),
    path('edit/<int:id>/',  views.edit, name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

