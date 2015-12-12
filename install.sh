#! /bin/bash

apt-get update
apt-get install -y python3-pip rabbitmq-server
apt-get install -y git libpq-dev postgresql-client
sudo chown -R ubuntu:ubuntu /opt/

mkdir /opt/virtualenvs
git clone git@github.com:groupthinkk/squad-api.git
git checkout master
git pull

pip3 install virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=/opt/virtualenvs/
source /usr/local/bin/virtualenvwrapper.sh 
cd /opt/squad-api && mkvirtualenv squad-api && workon squad-api
workon squad-api
pip3 install -r requirements.txt

mkdir /opt/uwsgi
sudo chown -R ubuntu:ubuntu /opt/

workon squad-api
cd /opt/squad-api/squadapi
export DJANGO_SETTINGS_MODULE=squadapi.production
python manage.py migrate
python manage.py loaddata users.json
python manage.py collectstatic --noinput
uwsgi --stop /tmp/squadapi-master.pid
uwsgi --ini /opt/squad-api/uwsgi-production.ini 

apt-get install -y nginx
ln -sf /opt/squad-api/nginx-squadapi-production.conf /etc/nginx/sites-enabled/default
service nginx restart
