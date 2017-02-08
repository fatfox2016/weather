#!/bin/bash

LS  -a /app/app
PY_SITE="`python /app/app/weatherWeb.py runserver`"
