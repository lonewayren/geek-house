#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# __author__ = 'renxiang03'

# init WeRoBot
from lib.robot import WeRoBot
from django.conf import settings

robot_instance = WeRoBot()
robot_instance.config.from_object(settings)
