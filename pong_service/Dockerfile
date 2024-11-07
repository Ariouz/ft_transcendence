FROM python:3.12-alpine

EXPOSE 8002/tcp

# debug tools
RUN apk update && apk add curl wget net-tools iputils-ping vim nano openssl

RUN mkdir /${PROJECT_NAME}

# RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#     -keyout /etc/ssl/private/django-selfsigned.key -out /etc/ssl/certs/django-selfsigned.crt \
#     -subj "/C=FR/ST=State/L=City/O=Organization/OU=Department/CN=localhost"

COPY ./setup.sh /tmp

CMD ["sh", "/tmp/setup.sh"]
