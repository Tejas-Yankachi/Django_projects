# Crop & Fertilizer Recommendation System

This project is a Django-based web application designed to help users manage crop and fertilizer recommendations based on soil type and other agricultural parameters.

## Features

- Crop management
- Soil type management
- Fertilizer management
- Recommendation engine for suitable fertilizers based on crop and soil type
- Admin interface for data management
- User authentication
- Captcha integration for forms
- Responsive UI with Bootstrap 5 and Crispy Forms

## Technologies Used

- Python 3.11+
- Django 5.x
- MySQL (default database, configurable to SQLite)
- Bootstrap 5
- Crispy Forms
- django-simple-captcha

## Getting Started

1. **Clone the repository**
2. **Create and activate a virtual environment**
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure the database in [`cemproj/settings.py`](cemproj/cemproj/settings.py)**
5. **Run migrations**
   ```sh
   python manage.py migrate
   ```
6. **Start the development server**
   ```sh
   python manage.py runserver
   ```

## Project File Structure

```
cms/
├── myenv/
│   └── cemproj/
│       ├── cemapp/
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── forms.py
│       │   ├── migrations/
│       │   ├── models.py
│       │   ├── templates/
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── views.py
│       ├── cemproj/
│       │   ├── __init__.py
│       │   ├── asgi.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── db.sqlite3
│       ├── manage.py
│       └── README.md
└── requirements.txt
```

## License

This project is for educational purposes.

