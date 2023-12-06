
# Equisy API 🚀

## Project Overview 📋
Equisy API is a Django-based web application designed to provide robust and scalable API services with a focus on multi-tenancy. Utilizing Django 4.2.7 and Django Tenants, this API offers a flexible and secure environment for handling multiple tenants in a single instance.

## Key Features 🔑
- **Multi-Tenant Architecture**: Separated `tenant` and `web` applications for efficient data isolation and management. 🏢
- **Extensive Use of Django Framework**: Leverages the latest features of Django for robust web application development. 🛠️
- **Azure Key Vault Integration**: Secure handling of secrets and credentials using Azure Key Vault. 🔒
- **Custom User Model**: Tailored authentication and user management. 👥

## Technology Stack 💻
- Django 4.2.7
- Django Tenants for Multi-Tenancy
- PostgreSQL (assumed, based on Django Tenants usage)

## Getting Started 🚦

### Prerequisites
- Python 3.x
- Pip (Python package manager)
- Virtualenv (recommended for creating isolated Python environments)
- PostgreSQL Database (version supporting schema-based multi-tenancy)
- Azure Key Vault account (for managing secrets)

### Installation and Setup 🛠️
1. **Clone the Repository**: 
   ```
   git clone https://github.com/RuchitMicro/equisy-api.git
   cd equisy-api
   ```
2. **Set up a Virtual Environment**:
   ```
   virtualenv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
4. **Environment Configuration**: 
   - Set up the Azure Key Vault and retrieve necessary credentials.
   - Configure the `DATABASES` setting in `settings.py` or a separate settings file for development and production.

5. **Database Setup**: 
   - Create a PostgreSQL database.
   - Run migrations to set up the database schema for multi-tenancy.
   ```
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```
   python manage.py runserver
   ```

## Models Overview 📊
The application consists of two primary Django apps: `tenant` and `web`. 

- **Tenant Models**: Define models specific to each tenant.
- **Web Models**: Include models for managing the tenants and global settings.
