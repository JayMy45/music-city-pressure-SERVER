#!/bin/bash

rm db.sqlite3
rm -rf ./mcpressureapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations mcpressureapi
python3 manage.py migrate mcpressureapi
python3 manage.py loaddata user
python3 manage.py loaddata tokens
python3 manage.py loaddata customer
python3 manage.py loaddata location
python3 manage.py loaddata progress
python3 manage.py loaddata equipment
python3 manage.py loaddata service_type
python3 manage.py loaddata specialty
python3 manage.py loaddata employee
python3 manage.py loaddata appointments
python3 manage.py loaddata employee_service_specialty
python3 manage.py loaddata reviews
python3 manage.py loaddata service_type_equipment