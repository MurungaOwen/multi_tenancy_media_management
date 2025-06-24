from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from .models import TenantDocument, TenantKey
from .utils import encrypt_data, decrypt_data
from django.conf import settings
import os, mimetypes, io


def upload_encrypted_batch(request):
    if request.method == "POST":
        files = request.FILES.getlist("documents")
        fernet_key = TenantKey.get_or_create_current_key()

        schema_folder = request.tenant.schema_name
        folder_path = os.path.join(settings.MEDIA_ROOT, schema_folder)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            try:
                raw_data = file.read()
                encrypted_data = encrypt_data(raw_data, fernet_key)
                mime_type, _ = mimetypes.guess_type(file.name)
                file_name = f"{schema_folder}_{file.name}.enc"
                file_path = os.path.join(folder_path, file_name)

                with open(file_path, "wb") as f:
                    f.write(encrypted_data)

                TenantDocument.objects.create(
                    name=file.name,
                    file_path=file_path,
                    mime_type=mime_type or "application/octet-stream"
                )
            except Exception as e:
                print(f"Failed to process {file.name}: {str(e)}")
        return redirect("document_list")
    
    return render(request, "upload.html")


def document_list(request):
    docs = TenantDocument.objects.all().order_by("-uploaded_at")
    return render(request, "document_list.html", {"documents": docs})


def view_document(request, doc_id):
    try:
        doc = TenantDocument.objects.get(id=doc_id)
    except TenantDocument.DoesNotExist:
        raise Http404()

    fernet_key = TenantKey.get_or_create_current_key()
    with open(doc.file_path, "rb") as f:
        decrypted = decrypt_data(f.read(), fernet_key)

    return FileResponse(
        io.BytesIO(decrypted),
        content_type=doc.mime_type,
        filename=doc.name
    )
