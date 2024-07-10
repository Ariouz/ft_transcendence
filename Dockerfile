FROM alpine:3.20

# Install Nginx
RUN apk update && apk add nginx

# Copy the Nginx config
COPY nginx/default.conf /etc/nginx/http.d/default.conf
COPY src /usr/share/nginx/html

EXPOSE 80/tcp

# Run the Nginx server
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
