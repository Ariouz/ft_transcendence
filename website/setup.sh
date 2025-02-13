cp /tmp/default.conf /etc/nginx/http.d/default.conf

tail -n +4 /etc/nginx/nginx.conf > tempfile && echo "user root;" | cat - tempfile > tempfile2 && mv tempfile2 /etc/nginx/nginx.conf

sudo chmod -R 0755 /usr/share/nginx/html/

/usr/sbin/nginx -g "daemon off;"
