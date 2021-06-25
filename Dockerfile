FROM tiangolo/uwsgi-nginx-flask:python3.8

# Increase timeout (thanks https://github.com/tiangolo/uwsgi-nginx-flask-docker/issues/120#issuecomment-459857072)
RUN echo "uwsgi_read_timeout 120;" > /etc/nginx/conf.d/custom_timeout.conf

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

RUN apt-get update
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs
RUN export GIT_LFS_SKIP_SMUDGE=1

COPY ./app /app
COPY test/kg2c-test.json /app/kg2c-test.json

RUN python -u /app/app/build_indexes.py
