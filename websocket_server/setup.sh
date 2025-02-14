#!/bin/bash

PYTHON=python3
PIP=pip3
MANAGE="${PYTHON} ${PROJECT_NAME}/manage.py"
DAPHNE="${PROJECT_NAME}/.venv/bin/daphne"
FT_REQUESTS_VERSION="0.1"
FT_REQUESTS_WHEEL="ft_requests-${FT_REQUESTS_VERSION}-py3-none-any.whl"

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

echo "Copy ssl certs"
cp /etc/ssl/certs/selfsigned.crt /usr/local/share/ca-certificates/
update-ca-certificates

echo "Start Django server and Daphne"

cd ${PROJECT_NAME} && daphne -e ssl:7000:privateKey=/etc/ssl/private/selfsigned.key:certKey=/etc/ssl/certs/selfsigned.crt websocket_server.asgi:application