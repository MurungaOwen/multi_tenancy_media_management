from django.db import models
from cryptography.fernet import Fernet
# Create your models here.

class TenantKey(models.Model):
    name = models.CharField(max_length=100, default='default', unique=True)
    fernet_key = models.BinaryField()

    def regenerate_key(self):
        self.fernet_key = Fernet.generate_key()
        self.save()

    @classmethod
    def get_or_create_current_key(cls):
        obj, created = cls.objects.get_or_create(name='default')
        if created:
            obj.fernet_key = Fernet.generate_key()
            obj.save()
        return obj.fernet_key

class TenantDocument(models.Model):
    """decsribes the document uploaded by client"""
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    mime_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)