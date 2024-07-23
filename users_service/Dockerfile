FROM python:3.12-alpine

EXPOSE 8001/tcp

RUN mkdir /${PROJECT_NAME}
COPY ./setup.sh /tmp

CMD ["sh", "/tmp/setup.sh"]
