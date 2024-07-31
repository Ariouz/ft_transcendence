FROM alpine:3.20

EXPOSE 8080/tcp

RUN apk update && apk add nginx

# debug tools
RUN apk update && apk add curl wget net-tools iputils-ping vim nano

COPY nginx/default.conf /etc/nginx/http.d/default.conf

ENTRYPOINT [ "/usr/sbin/nginx" ]
CMD [ "-g", "daemon off;"]
