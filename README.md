# alx-backend-security

## Project Overview
This project implements security features for a Django backend application.  
The focus is on **IP logging, blacklisting, geolocation analytics, rate limiting, and anomaly detection** using Celery.

## Features Implemented

### Task 0: Basic IP Logging Middleware
- Implemented custom middleware to log:
  - IP address
  - Timestamp
  - Request path  
- Added `RequestLog` model in `ip_tracking/models.py`.
- Middleware registered in `settings.py`.

### Task 1: IP Blacklisting
- Added `BlockedIP` model to block malicious IPs.
- Middleware updated to return `403 Forbidden` if IP is blacklisted.
- Added custom management command `block_ip` to add IPs into the blacklist.

### Task 2: IP Geolocation Analytics
- Installed **django-ip-geolocation** for geolocation lookup.
- Extended `RequestLog` model with `country` and `city` fields.
- Middleware updated to populate location data with caching (24h).

### Task 3: Rate Limiting by IP
- Installed **django-ratelimit** for rate limiting.
- Configured limits:
  - **10 requests/minute** for authenticated users.
  - **5 requests/minute** for anonymous users.
- Applied rate limiting to `login_view` in `ip_tracking/views.py`.

### Task 4: Anomaly Detection
- Configured Celery in the project (`alx_backend_security/celery.py`).
- Created periodic Celery task in `ip_tracking/tasks.py` to run **hourly**.
- Task flags suspicious IPs if:
  - They exceed **100 requests/hour**.
  - They access sensitive paths (`/admin`, `/login`).
- Added `SuspiciousIP` model with fields: `ip_address`, `reason`.

## Technologies Used
- Django 5.x
- Celery 5.x
- Redis (as broker & cache)
- django-ip-geolocation
- django-ratelimit

## Repository Structure
```
alx-backend-security/
│── ip_tracking/
│   ├── middleware.py
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   └── management/
│       └── commands/
│           └── block_ip.py
│── alx_backend_security/
│   ├── celery.py
│   ├── settings.py
│   └── urls.py
└── README.md
```

## Running the Project
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Start Redis (required for Celery):
   ```bash
   redis-server
   ```

4. Start Django server:
   ```bash
   python manage.py runserver
   ```

5. Start Celery worker with beat scheduler:
   ```bash
   celery -A alx_backend_security worker -B -l info
   ```

## License
This project is developed for educational purposes under the ALX Software Engineering program.
