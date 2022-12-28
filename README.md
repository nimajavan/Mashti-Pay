# Mashti-Pay

you need python3.11

#1

install virtualenv with pip

active virtual enviroment 


#2

pip install -r requirement.txt


#3

run command in root folder:

in windows:

#1: celery -A pm worker --loglevel=INFO --pool-solo

#2: celery -A pm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

in linux:

#1: celery -A pm worker --loglevel=INFO

#2: celery -A pm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler


#4

run command in root folder:

python manage.py makemigrations

python manage.py migrate

python manage.py runserver



