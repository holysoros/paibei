# -*- coding: utf-8 -*-
from mongoengine import *
from mongoengine.errors import NotUniqueError
import datetime


__all__ = ['places', 'cities', 'User', 'Product',
           'Batch', 'Record', 'NFCRecord']

class User(Document):
    name = StringField(required=True, unique=True)
    password = StringField(min_length=6, required=True)
    time = DateTimeField(default=datetime.datetime.now)


places = (u'台湾', u'上海', u'美国')
cities = (u'上海', u'北京', u'天津', u'重庆', u'安徽', u'福建',
          u'甘肃', u'广东', u'贵州', u'河北', u'黑龙江', u'河南',
          u'湖北', u'湖南', u'吉林', u'江西', u'江苏', u'辽宁',
          u'山东', u'陕西', u'山西', u'四川', u'云南', u'浙江',
          u'青海', u'海南', u'台湾', u'广西', u'内蒙古', u'宁夏',
          u'西藏', u'新疆')


class Product(Document):
    name = StringField(required=True, unique=True)
    place = StringField(choices=places, default=u'台湾', required=True)
    elements = StringField()
    image = ImageField(size=(1024, 1024, True), thumbnail_size=(200, 200, True))
    price = IntField()
    index = IntField(unique=True)

    def saveWithIncreasedIndex(self):
        index = 1
        while True:
            try:
                if not self.index:
                    self.index = index
                self.save()
                break
            except NotUniqueError:
                index += 1
                continue


class Batch(Document):
    time = DateTimeField(default=datetime.datetime.now)
    product = ReferenceField(Product, required=True)
    dist_place = StringField(choices=cities, required=True)
    count = IntField(required=True)
    verify_time = IntField(default=3)
    bid = StringField(required=True)
    url = URLField()


class Record(Document):
    batch = ReferenceField(Batch, required=True, reverse_delete_rule=CASCADE)
    index = IntField(required=True)
    serial_num = StringField(min_length=6, max_length=6, required=True)
    left_time = IntField(required=True)


class NFCRecord(Document):
    batch = ReferenceField(Batch, required=True, reverse_delete_rule=CASCADE)
    nfc_id = StringField(required=True)


class QrcodeHistory(Document):
    record = ReferenceField(Record, reverse_delete_rule=CASCADE)
    time = DateTimeField(default=datetime.datetime.now)
    type = StringField(choices=('ok', 'nok', 'invalid'))


class NFCHistory(Document):
    record = ReferenceField(NFCRecord, reverse_delete_rule=CASCADE)
    time = DateTimeField(default=datetime.datetime.now)
