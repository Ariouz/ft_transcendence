FROM alpine:3.20

EXPOSE 8080/tcp

RUN apk update && apk add nginx

COPY nginx/default.conf /etc/nginx/http.d/default.conf

ENTRYPOINT [ "/usr/sbin/nginx" ]
CMD [ "-g", "daemon off;"]
