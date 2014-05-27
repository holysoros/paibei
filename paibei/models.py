# -*- coding: utf-8 -*-
from mongoengine import *
import datetime


class User(Document):
    name = StringField(required=True, unique=True)
    password = StringField(min_length=6, required=True)
    time = DateTimeField(default=datetime.datetime.now)


places = (('TW', u'台湾'),
          ('SH', u'上海'),
          ('US', u'美国'))


class Product(Document):
    name = StringField(required=True, unique=True)
    place = StringField(choices=places, default='TW', required=True)
    elements = StringField()
    image = ImageField(size=(1024, 768, True), thumbnail_size=(200, 200, True))
