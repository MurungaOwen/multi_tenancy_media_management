# 🔐 Multi-Tenant Encrypted Document Management System

A Django-based system that enables secure, multi-tenant document handling with per-tenant file encryption using Fernet. Each tenant operates in complete isolation with their own PostgreSQL schema and unique encryption keys.

## 🏗️ Architecture Overview

This system provides:

- **Multi-tenant isolation** via `django-tenants` with separate PostgreSQL schemas
- **Per-tenant encryption** using Fernet keys managed by the `TenantKey` model
- **Secure file storage** with tenant-specific directories and on-the-fly encryption
- **RESTful API** built with Django REST Framework
- **Dependency management** with Poetry

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- Poetry

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MurungaOwen/multi_tenancy_media_management.git
   cd multi_tenancy_media_management
   ```

1. **Install dependencies**
   ```bash
   poetry install
   poetry shell
   ```

2. **Configure environment**
   
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgres://youruser:yourpassword@localhost:5432/yourdb
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```
Then move to src folder
```sh
cd src
```
3. **Apply initial migrations** this is for the shared apps and migrations that clients share
   ```bash
   python manage.py migrate_schemas --shared
   ```

4. **Create your first tenant**
   ```bash
   python manage.py create_tenant \
     --schema_name=tenant1 \
     --domain_url=tenant1.localhost \
     --name="Tenant One"
   ```

   or You can create all at once using 
   ```sh
   python manage.py create_tenant_with_domain
   ```

5. **Configure local DNS**
   Add to your `/etc/hosts` file:
   ```
   127.0.0.1 tenant1.localhost
   ```

   ## for windows users you run this command in you root dir of project
   ```sh
   python add_domain.py
   ```
   YOU will be prompted for domain and there you enter eg. tenant1.localhost to add to local DNS

6. **Start the development server**
    ```sh
    cd src
    ```
   ```bash
   python manage.py runserver
   ```

7. **Access your tenant**
   
   Navigate to: `http://tenant1.localhost:8000`

## 📋 Usage

### Document Upload

The system supports both web UI and API-based document uploads:

- **Web Interface**: Access the upload form through your tenant's domain
- **Batch Operations**: Multiple files can be uploaded simultaneously

### Security Features

- **Automatic Encryption**: All uploaded files are encrypted using tenant-specific Fernet keys
- **Secure Storage**: Documents are stored in tenant-isolated directories
- **On-demand Decryption**: Files are only decrypted when accessed by authorized users
- **Key Rotation Support**: Built-in support for Fernet key rotation using `MultiFernet`

## 🔧 API Documentation


## 🗃️ Database Management

### Schema Exploration

Access the database shell:
```bash
poetry run python manage.py dbshell
```

View tables for a specific tenant schema:
```sql
\dt tenant1.*
```

### Tenant Management

Create additional tenants:
```bash
python manage.py create_tenant \
  --schema_name=tenant2 \
  --domain_url=tenant2.localhost \
  --name="Tenant Two"
```

## 🔐 Security Architecture

### Encryption Model

- Each tenant has a unique Fernet encryption key stored in the `TenantKey` model
- Files are encrypted before being written to disk
- Encryption keys are never stored alongside the encrypted data
- Support for key rotation without data loss

### Multi-tenancy

- Complete schema isolation using `django-tenants`
- Tenant-specific file storage directories
- Domain-based tenant resolution
- No cross-tenant data access possible


## 🛠️ Development

### Dependencies

This project uses Poetry for dependency management. Key dependencies include:

- Django
- django-tenants
- djangorestframework
- drf-yasg
- cryptography (Fernet)
- psycopg2

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.