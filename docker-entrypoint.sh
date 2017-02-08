#!/bin/bash

ls  -a /app/app
PY_SITE="`python /app/app/weatherWeb.py runserver`"
