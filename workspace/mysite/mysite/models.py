'''
Created on 2012-9-5

@author: jizhishu
'''
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField()
    