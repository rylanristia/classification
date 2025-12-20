from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard),
    path("datakotor/", views.datakotor),
    path("cleansing-result/", views.cleansingResult),
    path("transformasi/", views.transformasi),
    path("klasifikasi/", views.klasifikasi),
    path("add-new-data/", views.addnewdata),
    path("test-new-data/", views.testnewdata),
]
