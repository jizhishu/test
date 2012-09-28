#from django.db import models

# Create your models here.

from mongoengine import *
from MongoDB import mongo_utility
from MongoDB import node_item
import getDetail_ASIN

connect('test',host='192.168.1.110')
connection=mongo_utility.MongoUtility(serverip='192.168.1.110')
    
class Procurement(Document):
    ASIN=StringField(primary_key=True)
    title=StringField()
    price=FloatField()
    rating=FloatField()
    nodeID=StringField()
    nodeName=StringField()
    image=ListField(URLField())
    note=ListField(StringField())

def getNode(nodeID):
    test=node_item.NodeItem(connection)
    result=test.search('_id',nodeID)
    for a in result:
        r={
           'id'     :   nodeID,
           'name'   :   a['name'],
           }
    if r:
        return r
    else:
        return {'id':nodeID,'name':'more'}

class asin():
    def total(self):
        return Procurement.objects.all().count()
    
    def getList(self,page=1):
        result=Procurement.objects.all().order_by('ASIN').skip((page-1)*24).limit(24)
        List=[]
        if result:
            for re in result:
                nodeID=re['nodeID']
                nodeName=getNode(nodeID)['name']
                res={
                     'ASIN'     :   re['ASIN'],
                     'title'    :   re['title'],
                     'price'    :   re['price'],
                     'rating'   :   re['rating'],
                     'nodeID'   :   nodeID,
                     'nodeName' :   nodeName,
                     'image'    :   re['image'],
                     'note'     :   re['note']
                     }
                List.append(res)
            return List
        else:
            return []
        
    def updateNote(self,asin,note):
        test=Procurement.objects(ASIN=asin)
        if test.update(set__note=[note]):
            return 1
        else:
            return 0
        
    def pushNote(self,asin,note):
        test=Procurement.objects(ASIN=asin)
        if test.update(push__note=note):
            return 1
        else:
            return 0
        
    def saveList(self,list):
        test=Procurement(
                        ASIN    =   list['ASIN'],
                        title   =   list['title'],
                        price   =   list['price'],
                        rating  =   list['rating'],
                        nodeID  =   list['nodeID'],
                        nodeName=   list['nodeName'],
                        image   =   list['image']
                        )
        if test.save():
            return 1
        else:
            return 0
        
    def deleteByASIN(self,asin):
        Procurement.objects(ASIN=asin).delete()
        
    def findByASIN(self,asin):
        result=Procurement.objects(ASIN=asin)
        list=[]
        if result:
            for t in result:
                r={
                   'ASIN'   :   t.ASIN,
                   'title'  :   t.title,
                   'price'  :   t.price,
                   'rating' :   t.rating,
                   'nodeID' :   t.nodeID,
                   'nodeName':  t.nodeName,
                   'image'  :   t.image,
                   'note'   :   t.note
                    }
                list.append(r)
            return list
        else:
            return 0

def importData(ASIN):
     a=asin()
     detail=getDetail_ASIN.getDetail(ASIN)
     if a.saveList(detail):
         return 1
     else:
         return 0

def importFile(filename):
    pass
if __name__=='__main__':
    a=asin()
    detail=getDetail_ASIN.getDetail('9981731838')
    print detail
    print getNode('172282')['name']
    importData('9981731838')
    print a.findByASIN('9981731838')
    print getNode(detail['nodeID'])