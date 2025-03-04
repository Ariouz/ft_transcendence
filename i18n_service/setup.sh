#!/bin/bash

PYTHON=python3
PIP=pip3
MANAGE="${PYTHON} ${PROJECT_NAME}/manage.py"

DJANGO_APP="${PROJECT_NAME}_app"
ADDRESS="0.0.0.0:${APP_PORT}"

CMD_INSTALL="apk add --update --no-cache"


cd /${PROJECT_NAME} || exit


echo "Install Python and dependencies"
$CMD_INSTALL python3 python3-dev py3-pip postgresql-dev libffi-dev

$PYTHON -m ensurepip
$PIP install --no-cache --upgrade pip setuptools

echo "Create virtual environment"
$PYTHON -m venv .venv

echo "Activate virtual environment"
source .venv/bin/activate

echo "Install dependencies"
$PIP install -r requirements.txt

echo "Setup database"
$MANAGE makemigrations $DJANGO_APP
$MANAGE migrate

echo "Collect static files"
if [ ! -d "$PROJECT_NAME/static" ] || [ ! "$(ls -A $PROJECT_NAME/static)" ]; then
    echo "Static folder is empty or does not exist. Running collectstatic..."
    $MANAGE collectstatic --noinput
else
    echo "Static folder is not empty. Skipping collectstatic."
fi

echo "Run tests"
if ! $MANAGE test $DJANGO_APP; then
    echo "Tests failed. Exiting."
    exit 1
fi

echo "Create admin user"
$MANAGE createsuperuser --no-input

echo "Start Django server"
$MANAGE runserver_plus $ADDRESS --cert-file=/etc/ssl/certs/django-selfsigned.crt --key-file=/etc/ssl/private/django-selfsigned.key