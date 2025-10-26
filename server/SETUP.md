# GSoC Review Platform - Server Setup

## Setup Complete! ✅

The Django server has been successfully set up with the following configurations:

### Installed Dependencies
- Django 4.2.25
- Django REST Framework 3.14.0
- PyMongo 4.10.1
- dnspython 2.7.0

### Database Configuration
- **Current**: SQLite (db.sqlite3) - Recommended for development
- **Alternative**: MongoDB support available (requires djongo installation)

### Completed Setup Steps
1. ✅ Created `requirements.txt` with all necessary dependencies
2. ✅ Installed all Python packages
3. ✅ Configured database settings (SQLite for stability)
4. ✅ Ran database migrations successfully
5. ✅ Verified Django installation with system check

## Next Steps

### 1. Create a Superuser (Admin Account)
To access the Django admin panel, create a superuser account:

```bash
cd server
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 2. Start the Development Server
To run the server:

```bash
cd server
python manage.py runserver
```

The server will be available at: `http://127.0.0.1:8000/`
Admin panel: `http://127.0.0.1:8000/admin/`

### 3. MongoDB Configuration (Optional)
If you want to use MongoDB instead of SQLite:

1. Install MongoDB locally or use MongoDB Atlas
2. Install djongo (note: may have compatibility issues with Django 4.2):
   ```bash
   pip install djongo==1.3.6 pymongo==3.12.3 sqlparse==0.2.4
   ```
3. Update `server/settings.py` to use the MongoDB configuration (commented out in the file)
4. Run migrations again:
   ```bash
   python manage.py migrate
   ```

## Project Structure
```
server/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database (created after migrations)
├── server/               # Main project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
└── gsoc_review/         # Main application
    ├── models.py        # Database models
    ├── views.py         # View functions
    ├── admin.py         # Admin configuration
    └── migrations/      # Database migrations
```

## Environment Variables (Optional)
For production, consider setting:
- `SECRET_KEY`: Django secret key (currently using default - change for production!)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names
- `DATABASE_URL`: Database connection string

## Troubleshooting

### Issue: "Couldn't import Django"
- Make sure you're in the correct directory
- Verify Django is installed: `pip list | grep Django`
- Check if you're using the correct Python environment

### Issue: Database errors
- Delete `db.sqlite3` and run migrations again
- Check database configuration in `settings.py`

### Issue: Port already in use
- Use a different port: `python manage.py runserver 8080`
- Or kill the process using port 8000

## Development Tips
- Use `python manage.py shell` for interactive Python shell with Django context
- Use `python manage.py dbshell` to access database directly
- Run tests with `python manage.py test`
- Check for issues with `python manage.py check`

