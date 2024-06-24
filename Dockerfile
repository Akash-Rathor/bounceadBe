# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# # Copy .env file
# COPY .env .env

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        gcc \
        libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Expose port
EXPOSE 80

# Start Gunicorn and Nginx separately
CMD gunicorn bouncead.wsgi:application --bind 0.0.0.0:8000 & nginx -g "daemon off;"
