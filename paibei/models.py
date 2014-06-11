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

cities = (u'上海', u'北京', u'天津')


class Product(Document):
    name = StringField(required=True, unique=True)
    place = StringField(choices=places, default='TW', required=True)
    elements = StringField()
    image = ImageField(size=(1024, 768, True), thumbnail_size=(200, 200, True))


class Batch(Document):
    time = DateTimeField(default=datetime.datetime.now)
    product = ReferenceField(Product, required=True)
    dist_place = StringField(choices=cities, required=True)
    count = IntField(required=True)
    verify_time = IntField(default=3)


class Record(Document):
    batch = ReferenceField(Batch, required=True)
    index = IntField(required=True)
    serial_num = StringField(min_length=6, max_length=6, required=True)
    left_time = IntField(required=True)
