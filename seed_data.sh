#!/bin/bash

rm -rf arcanaapi/migrations
rm db.sqlite3
python manage.py makemigrations arcanaapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata signs
python manage.py loaddata tarotusers
python manage.py loaddata subscriptions
python manage.py loaddata layouts
python manage.py loaddata positions
python manage.py loaddata readings
python manage.py loaddata cards
python manage.py loaddata cardreadings
python manage.py loaddata comments

