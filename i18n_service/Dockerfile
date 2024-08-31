FROM python:3.12-alpine

EXPOSE 8001/tcp

# debug tools
RUN apk update && apk add curl wget net-tools iputils-ping vim nano

RUN mkdir /${PROJECT_NAME}
COPY ./setup.sh /tmp

CMD ["sh", "/tmp/setup.sh"]
