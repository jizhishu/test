from mongoengine import *
from blog.settings import DBNAME

connect(DBNAME,host='192.168.1.110')

class Post(Document):
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=500, required=True)
    last_update = DateTimeField(required=True)
    tags = ListField(StringField(max_length=30))

