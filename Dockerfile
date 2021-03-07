FROM tiangolo/uwsgi-nginx-flask:python3.8

# Increase timeout (thanks https://github.com/tiangolo/uwsgi-nginx-flask-docker/issues/120#issuecomment-459857072)
RUN echo "uwsgi_read_timeout 180;" > /etc/nginx/conf.d/custom_timeout.conf

COPY ./app /app