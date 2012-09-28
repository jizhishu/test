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
    r=0
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
    
    def getList(self,category=0,page=1):
        if category:
            result=Procurement.objects(nodeID=category).order_by('-rating').skip((page-1)*6).limit(6)
        else:
            result=Procurement.objects.all().order_by('-rating').skip((page-1)*6).limit(6)
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
        
    def saveList(self,doc):
        nodeName=getNode(doc['nodeID'])['name']
        test=Procurement(
                        ASIN    =   doc['ASIN'],
                        title   =   doc['title'],
                        price   =   doc['price'],
                        rating  =   doc['rating'],
                        nodeID  =   doc['nodeID'],
                        nodeName=   nodeName,
                        image   =   doc['image']
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
      
    def getCategory(self):
        node=[]
        Node=[]
        result=Procurement.objects.all()
        for i in result():
            if i['nodeID'] in node:
                pass
            else:
                nodeID=i['nodeID']
                nodeName=i['nodeName']
                node.append(nodeID)
                BNode={'nodeID':nodeID,'nodeName': nodeName}
                Node.append(BNode)
        return Node
def importData(ASIN):
    a=asin()
    detail=getDetail_ASIN.getDetail(ASIN)
    if a.saveList(detail):
        return 1
    else:
        return 0

def importFile(filename):
    f=open(filename)
    asins=f.read()
    asins=asins.split('\n')
    asins.pop()
    for each in asins:
        print each
        importData(each)
    
if __name__=='__main__':
    a=asin()
    #detail=getDetail_ASIN.getDetail('B004PNPNZK')
    #print detail
    #importData('B004PNPNZK')
    #print a.findByASIN('9981731838')
    #print getNode(detail['nodeID'])
    #importFile('A3SNNXCKUIW1O2')
    a.deleteByASIN('B000U0JCUE')
    #for aa in a.getNode():
    #    print aa.nodeName
    print a.getCategory()