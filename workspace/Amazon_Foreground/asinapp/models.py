#from django.db import models

# Create your models here.

from mongoengine import *
#from mongoengine import connect,Document,FileField,StringField,ListField,IntField
from MongoDB import mongo_utility

from MongoDB import ASIN_item
#from MongoDB import product_item
#from MongoDB import snapshot_item
from MongoDB import node_item

connect('test',host='192.168.1.110')
connection=mongo_utility.MongoUtility(serverip='192.168.1.110')
    
class Post(Document):
    File = FileField()
    name = StringField()

class asin_local(Document):
    _id=StringField()
    name=StringField()
    root_category=ListField()
    importance=IntField()
    note=ListField(StringField())
    
def getDetailFromASIN(asin):
    testASIN=ASIN_item.ASIN(connection)
    #testASIN.setASIN(asin)
    #result=testASIN.searchByASIN()
    result=testASIN.search('_id',asin)
    if result.count()>0: 
        return result[0]

def getDetail(asin):
    result1=getDetailFromASIN(asin)
    if result1:
        result={
                "_id" : asin,
                "name" : result1['product_name'],            #ASIN
                "root_category" :result1['root_category'],
                "importance" : result1['importance'],
                }
        return result
    else:
        return 0
def getCategory():
    test=node_item.NodeItem(connection)
    result=test.search('ancestors',[])
    list=[]
    for a in result:
        r={
           'id' : a['_id'],
           'name': a['name']
           }
        list.append(r)
    return list    

class asin():
    def total(self):
        return asin_local.objects.all().count()
    
    def getList(self,category=0,page=1):
        if category:
            result=asin_local.objects(root_category=category).order_by('_id').skip((page-1)*24).limit(24)
        else:
            result=asin_local.objects.all().order_by('_id').skip((page-1)*24).limit(24)
        List=[]
        if result:
            for re in result:
                res={
                     'id':re.id,
                     'name':re['name'],
                     'root_category':re['root_category'],
                     'importance':re['importance'],
                     'note':re['note']
                     }
                List.append(res)
            return List
        else:
            return []
        
    def updateNote(self,asin,note):
        test=asin_local.objects(_id=asin)
        if test.update(set__note=[note]):
            return 1
        else:
            return 0
        
    def pushNote(self,asin,note):
        test=asin_local.objects(_id=asin)
        if test.update(push__note=note):
            return 1
        else:
            return 0
        
    def saveList(self,list):
        test=asin_local(
                        _id=list['_id'],
                        name=list['name'],
                        root_category=list['root_category'],
                        importance=list['importance'],
                        )
        if test.save():
            return 1
        else:
            return 0
        
    def deleteByASIN(self,asin):
        asin_local.objects(_id=asin).delete()
        
    def findByASIN(self,asin):
        result=asin_local.objects(_id=asin)
        list=[]
        if result:
            for t in result:
                r={
                   'id':t.id,
                   'name':t.name,
                   'root_category':t.root_category,
                   'note':t.note
                    }
                list.append(r)
            return list
        else:
            return 0
        
if __name__=='__main__':
    #asin_local.drop_collection()
    #print getDetail('B006GG0RB4')
    
    a=asin()
    '''list={
          'importance': '22',
          '_id': 'iddddsd1',
          'name': 'Remy JeaddddJeans',
          'root_category': ['1036592']
          }
    a.saveList(list)#
    a.updateNote('id1','update2')#
    list={
          'importance': '10000000',
          '_id': 'iddsdddd2',
          'name': 'Remy Jdddean in Trip by Big Star Jeans',
          'root_category': ['1036592']
          }
    a.saveList(list)#
    '''
    print a.getList('672123011')
    print len(a.getList('672123011'))
    test=getDetail('B006FJU9TM')
    if test:
        a.saveList(test)#
    else:
        print 'false'
    '''
    list={
          'importance': '10000000',
          '_id': 'B00sds6dddGG0RB4',
          'name': 'Remy Jeddddan in Trip by Big Star Jeans',
          'root_category': ['10592']
          }
    a.saveList(list)
    '''
    '''
    while i:
        test=a.getList(i)
        for li in test:
            print li.id,li.name
        i=i-1
    '''
    '''
    test=a.getList()
    for li in test:
        print li.id,li.name
    print a.total()
    print a.deleteByASIN('B006GG0RB4')
    t=a.findByASIN('B00sds6dddGG0RB4')
    print t
    '''
    print getCategory()
    result=getCategory()
    for a in result:
        print a
        print type(a)
        #print a.name
        print a['id'],a['name']
    #asin_local.drop_collection()
    #asin_local.objects.delete()
    