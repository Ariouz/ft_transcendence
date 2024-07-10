FROM alpine:3.20

RUN apk update && apk add nginx

COPY nginx/default.conf /etc/nginx/http.d/default.conf
COPY src /usr/share/nginx/html

EXPOSE 8080/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
