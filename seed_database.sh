#!/bin/bash

rm db.sqlite3
rm -rf ./mcpressureapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations mcpressureapi
python3 manage.py migrate mcpressureapi