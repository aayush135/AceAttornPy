#!/bin/bash
# python manage.py runserver 0.0.0.0:80
gunicorn aceattorn.wsgi:application --bind 0.0.0.0:80
