from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('index/', views.index, name='index'),
    path('cv_maker/', views.cv_maker, name='cv_maker'),
    path('cv_download/', views.cv_download, name='cv_download'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)