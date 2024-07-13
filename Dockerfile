# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        gcc \
        libc-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install New Relic agent
RUN pip install newrelic==9.12.0

# Copy the Django project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Copy New Relic configuration
COPY bouncead/newrelic.ini /code/newrelic.ini

# Expose port
EXPOSE 80

# Start Gunicorn with New Relic and Nginx
CMD ["sh", "-c", "newrelic-admin run-program gunicorn bouncead.wsgi:application --bind 0.0.0.0:8000 & nginx -g 'daemon off;'"]
