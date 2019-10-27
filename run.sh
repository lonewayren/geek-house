#!/usr/bin/env bash

if [ ! -d /var/run/project ]; then
    sudo mkdir /var/run/project && sudo chown -R $USER:$USER /var/run/project
fi
gunicorn -c deploy/gunicorn.conf  geekHouse.wsgi