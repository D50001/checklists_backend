#!/bin/bash

cd auto_checklist

python3 manage.py migrate

gunicorn auto_checklist.wsgi:application -b 0.0.0.0 -w 4