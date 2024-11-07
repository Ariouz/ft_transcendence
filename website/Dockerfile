FROM alpine:3.20

EXPOSE 8080/tcp

RUN apk update && apk add nginx

# debug tools
RUN apk update && apk add curl wget net-tools iputils-ping vim nano

# RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#     -keyout /etc/ssl/private/nginx-selfsigned.key \
#     -out /etc/ssl/certs/nginx-selfsigned.crt \
#     -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"

COPY nginx/default.conf /etc/nginx/http.d/default.conf

ENTRYPOINT [ "/usr/sbin/nginx" ]
CMD [ "-g", "daemon off;"]
