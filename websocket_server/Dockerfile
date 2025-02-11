FROM python:3.12-alpine

EXPOSE 7000/tcp

RUN mkdir /${PROJECT_NAME}

RUN update-ca-certificates

COPY ./setup.sh /tmp

CMD ["sh", "/tmp/setup.sh"]
