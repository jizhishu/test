#coding=utf-8
'''
Created on 2012-7-19
deals_item.py unitest
@author: xcl
'''
import unittest
import mongo_utility
import pymongo
import deals_item,datetime

class DealsItemTest(unittest.TestCase):
    
    #test_connection=pymongo.Connection('192.168.1.110',27017)
    test_connection = mongo_utility.MongoUtility(serverip='192.168.1.110')
    #test_db=test_connection.test1
    #test_collection = test_db.deals
    
    def setUp(self):
        #self.connect = mongo_utility.MongoUtility(serverip='localhost', dbname='test1', collectionname='test1')
        self.deal=deals_item.Deals(self.test_connection)
        
    def testSet(self):
        assert self.deal.setASIN(1)==0,'ASIN check type error'
        assert self.deal.setASIN('123')==1,'Set ASIN error'
        assert self.deal.setName(True)==0,'Name check type error'
        assert self.deal.setName('EA')==1,'Set name error'
        assert self.deal.setPrice('a')==0,'Price check type error'
        assert self.deal.setPrice(1.1)==1
        assert self.deal.setExpiration_time(datetime.datetime.now())==1
        assert self.deal.setContent(1)==0
        assert self.deal.setContent('content')==1
        
    def testAssemble(self):
        self.deal.setASIN('123')
        self.deal.setContent('hello')
        self.deal.setName('lego')
        self.deal.setPrice(150)
        time=datetime.datetime.now()
        self.deal.setExpiration_time(time)
        assert self.deal.assemble()=={
                                      '_id':'123',
                                      'name':"lego",
                                      'price':150,
                                      'expiration_time':time,
                                      'content':'hello'
                                      }
    
    def testSave(self):
        assert self.deal.saveToDB()==-1
        self.deal.setASIN('123')
        self.deal.setContent('hello')
        self.deal.setName('lego')
        self.deal.setPrice(150)
        time=datetime.datetime.now()
        self.deal.setExpiration_time(time)
        assert self.deal.saveToDB()==1
        assert self.test_collection.find({'_id':'123'}).count()==1
        self.test_collection.remove()
    
    def testSearchLike(self):
        doc1={
                 "_id":'123',
                 "name":'LEGO',
                 "price":12,
                 "expiration_time":datetime.datetime.now(),
                 "content":'hello, my name is alien'
                 }
        doc2={
                 "_id":'1234',
                 "name":'LEGO',
                 "price":12,
                 "expiration_time":datetime.datetime.now(),
                 "content":'hello, my name is alienbre'
                 }
        doc3={
                 "_id":'12345',
                 "name":'LEGO',
                 "price":12,
                 "expiration_time":datetime.datetime.now(),
                 "content":'hello, my name is bre'
                 }
        self.test_collection.insert(doc1,safe=True)
        self.test_collection.insert(doc2,safe=True)
        self.test_collection.insert(doc3,safe=True)
        result=self.deal.searchLikeByContent('alien')
        #self.test_collection.remove()
        assert result.count()==2
        print result[1]['content']
        self.test_collection.remove()
    def testSearch(self):
        doc1={
                 "_id":'123',
                 "name":'LEGO',
                 "price":12,
                 "expiration_time":datetime.datetime.now(),
                 "content":'hello, my name is alien'
                 }
        self.test_collection.insert(doc1,safe=True)
        self.deal.setASIN('123')
        self.deal.setName('LEGO')
        result1=self.deal.searchByASIN()
        result2=self.deal.searchByName()
        assert result1.count()==1
        assert result2.count()==1
        assert result1[0]["_id"]==result2[0]["_id"]
        assert result1[0]["content"]==result2[0]["content"]
        self.test_collection.remove()
        
    def testDelete(self):
        assert self.deal.deleteByASIN()==None
        self.deal.setASIN('123')
        self.deal.setContent('hello, my name is alien')
        doc1={
                 "_id":'123',
                 "name":'LEGO',
                 "price":12,
                 "expiration_time":datetime.datetime.now(),
                 "content":'hello, my name is alien'
                 }
        self.test_collection.insert(doc1,safe=True)
        assert self.deal.deleteByASIN()==1
        assert self.test_collection.find({'_id':'123'}).count()==0
        self.test_collection.insert(doc1,safe=True)
        assert self.deal.delete(None,None)==0
        assert self.deal.delete("content", 'hello, my name is alien')==1
        assert self.test_collection.find({'_id':'123'}).count()==0

    def testUpdate(self):
        doc1={
                 "_id":'123',
                 "name":'LEGO',
                 "price":12,
                 "expiration_time":datetime.datetime.now(),
                 "content":'hello, my name is alien'
                 }
        #self.test_collection.insert(doc1,safe=True)
        self.deal.setContent('End')
        assert self.deal.updateToDb()==0
        self.deal.setASIN('123')
        assert self.deal.updateToDb()==1
        assert self.test_collection.find({"_id":'123'})[0]['content']=='End'
        self.test_collection.remove()
        
def suite():  
    suite = unittest.TestSuite()
    suite.addTest(DealsItemTest('testSet'))
    suite.addTest(DealsItemTest('testAssemble'))
    suite.addTest(DealsItemTest('testSave'))
    suite.addTest(DealsItemTest('testSearchLike'))
    suite.addTest(DealsItemTest('testSearch'))
    #suite.addTest(DealsItemTest('testDelete'))
    suite.addTest(DealsItemTest('testUpdate'))
    return suite
    
if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())