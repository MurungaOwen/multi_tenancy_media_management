from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_encrypted_batch, name='upload_encrypted_batch'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:doc_id>/view/', views.view_document, name='view_document')
]
