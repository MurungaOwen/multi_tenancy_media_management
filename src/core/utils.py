from cryptography.fernet import Fernet
from .models import TenantDocument, TenantKey
def encrypt_data(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)

def decrypt_data(data: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(data)

def rotate_tenant_key_and_reencrypt():
    tenant_key = TenantKey.objects.get(name='default')
    old_key = tenant_key.fernet_key
    new_key = Fernet.generate_key()

    updated_docs = []
    for doc in TenantDocument.objects.all():
        with open(doc.file_path, "rb") as f:
            try:
                decrypted = decrypt_data(f.read(), old_key)
                new_encrypted = encrypt_data(decrypted, new_key)
                with open(doc.file_path, "wb") as fw:
                    fw.write(new_encrypted)
                updated_docs.append(doc.name)
            except Exception:
                continue

    tenant_key.fernet_key = new_key
    tenant_key.save()
    return updated_docs