#!/usr/bin/env bash

gunicorn -c deploy/gunicorn.conf  geekHouse.wsgi