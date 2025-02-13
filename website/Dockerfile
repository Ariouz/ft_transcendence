FROM alpine:3.20

EXPOSE 8080/tcp

RUN apk update && apk add nginx sudo

COPY nginx/default.conf /tmp

COPY ./setup.sh /tmp

CMD ["sh", "/tmp/setup.sh"]
