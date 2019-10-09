from django.db import models

# Create your models here.
import mongoengine


class Person(mongoengine.Document):
    name = mongoengine.StringField(max_length=10)
    age = mongoengine.IntField(default=0)

