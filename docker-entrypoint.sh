#!/bin/bash


python /app/app/weatherWeb.py runserver --host 0.0.0.0
python /app/app/crontab.py
