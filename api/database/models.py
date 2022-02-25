from mongoengine import *

class Checkpoint(Document):
    distance = FloatField(required=True)
    location = StringField()
    open_time = DateTimeField(required=True)
    close_time = DateTimeField(required=True)

class Brevet(Document):
    length = FloatField(required=True)
    start_time = DateTimeField(required=True)
    checkpoints = ListField(Checkpoint, required=True)