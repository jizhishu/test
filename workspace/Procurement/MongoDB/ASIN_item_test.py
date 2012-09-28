#coding=utf-8
'''
Created on 2012-7-27
ASIN item unit test
@author: xcl
'''
import unittest
import datetime
import pymongo
import ASIN_item,mongo_utility

class ASINItemTest(unittest.TestCase):
    test_connection=pymongo.Connection('localhost',27017)
    test_db=test_connection.test1
    test_collection = test_db.ASIN
    
    def setUp(self):
        self.connect = mongo_utility.MongoUtility(serverip='localhost', dbname='test1', collectionname='test1')
        self.ASIN=ASIN_item.ASIN(self.connect)
        
    def testSet(self):
        assert self.ASIN.setASIN(1)==0,"ASIN check type error"
        assert self.ASIN.setASIN('123')==1,"Set ASIN error"
        assert self.ASIN.setProductName(True)==0,"Production Name check error"
        assert self.ASIN.setProductName('name')==1,"Set product name error"
        assert self.ASIN.setRootCategory(1)==0,"Root category check type error"
        assert self.ASIN.setRootCategory([])==1,"Set root category error"
        assert self.ASIN.setImportance('importance')==0
        assert self.ASIN.setImportance(1)==1
        assert self.ASIN.setFindTime(1)==0
        assert self.ASIN.setFindTime(datetime.datetime.now())==1
        
    def testAssemble(self):
        self.ASIN.setASIN('123')
        self.ASIN.setProductName('name')
        self.ASIN.setRootCategory([])
        self.ASIN.setImportance(1)
        time=datetime.datetime.now()
        self.ASIN.setFindTime(time)
        assert self.ASIN.assemble()=={
                                      "_id":'123',
                                      "product_name":'name',
                                      "root_category":[],
                                      "find_time":time,
                                      "importance":1
                                      }

    def testSave(self):
        assert self.ASIN.saveToDB()==-1
        self.ASIN.setASIN('123')
        self.ASIN.setProductName('name')
        self.ASIN.setRootCategory([])
        self.ASIN.setImportance(1)
        time=datetime.datetime.now()
        self.ASIN.setFindTime(time)
        assert self.ASIN.saveToDB()==1
        assert self.test_collection.find({'_id':'123'}).count()==1
        self.test_collection.remove()
        
    def testDelete(self):
        time=datetime.datetime.now()
        doc={
                                      "_id":'123',
                                      "product_name":'name',
                                      "root_category":[],
                                      "find_time":time,
                                      "importance":1
                                      }
        self.ASIN.setASIN('123')
        self.ASIN.setProductName('name')
        self.ASIN.setRootCategory([])
        self.ASIN.setImportance(1)
        self.ASIN.setFindTime(time)
        self.test_collection.insert(doc,safe=True)
        assert self.ASIN.deleteByASIN()==1
        self.test_collection.insert(doc,safe=True)
        assert self.ASIN.deleteByName()==1
        self.test_collection.insert(doc,safe=True)
        assert self.ASIN.deleteRootCategory()==1
    
    def testSearch(self):
        time=datetime.datetime.now()
        doc={
                                     "_id":'123',
                                     "product_name":'name',
                                     "root_category":'root_category',
                                     "find_time":time,
                                     "importance":1
                                     }
        self.test_collection.insert(doc,safe=True)
        self.ASIN.setASIN('123')
        self.ASIN.setProductName('name')
        assert self.ASIN.searchByASIN().count()==1
        assert self.ASIN.searchByName().count()==1
        self.test_collection.remove()
     
    def testUpdate(self): 
        time=datetime.datetime.now()
        doc={
                                     "_id":'123',
                                     "product_name":'name',
                                     "root_category":'root_category',
                                     "find_time":time,
                                     "importance":1
                                     }
        self.test_collection.insert(doc,safe=True)
        self.ASIN.setASIN('123')
        self.ASIN.setProductName('name!')
        self.ASIN.updateToDb()
        assert self.test_collection.find({"_id":"123"})[0]['product_name']=='name!'
        self.test_collection.remove()
        
def suite():
    suite=unittest.TestSuite()
    suite.addTest(ASINItemTest('testSet'))
    suite.addTest(ASINItemTest('testAssemble'))
    suite.addTest(ASINItemTest('testSave'))
    suite.addTest(ASINItemTest('testDelete'))
    suite.addTest(ASINItemTest('testSearch'))
    suite.addTest(ASINItemTest('testUpdate'))
    return suite

if __name__=="__main__":
    unittest.TextTestRunner().run(suite())