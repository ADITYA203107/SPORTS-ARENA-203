# Django Project Setup

This is a Django environment set up in `c:\Users\ThinkPad\OneDrive\Desktop\Folder`.

## Setup

### Virtual Environment
The project uses a Python virtual environment (`.venv`) for isolated dependencies.

### Installation
1. Activate the virtual environment:
   ```bash
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
```
project/
├── config/              # Django configuration
│   ├── settings.py      # Settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application
├── apps/                # Django apps
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (do not commit)
├── .env.example         # Example environment variables
└── .gitignore           # Git ignore rules
```

## Configuration

Edit the `.env` file to configure:
- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Change this to a secure random key in production
- `ALLOWED_HOSTS`: Add your domain(s) here

## Creating a New App

```bash
python manage.py startapp myapp apps/myapp
```

Then add `myapp` to `INSTALLED_APPS` in `config/settings.py`.

## Database

The project uses SQLite by default. To switch databases, update the `DATABASES` setting in `config/settings.py`.

## Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
