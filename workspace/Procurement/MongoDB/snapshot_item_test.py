#coding=utf-8
'''
Created on 2012-7-9
snapshot_item.py unitest
@author: xcl
'''
import unittest
import mongo_utility
import pymongo
import snapshot_item
import datetime

class SnapshotitemTest(unittest.TestCase):
    
    test_connection=pymongo.Connection('localhost',27017)
    test_db=test_connection.test1
    test_collection=test_db.snapshot
    
    def setUp(self):
        self.connect=mongo_utility.MongoUtility(serverip='localhost',dbname='test1',collectionname='snapshot')
        self.snapshotitem=snapshot_item.Snapshot(self.connect)
        
    def testSet(self):
        assert self.snapshotitem.setASIN(1)==0,'ASIN check type error'
        assert self.snapshotitem.setASIN('1234')==1,'Set ASIN error'
#        assert self.snapshotitem.setPrice('2')==0,'Price check type error'
#        assert self.snapshotitem.setPrice(1.1)==1,'Set price error'
        assert self.snapshotitem.setListPrice('1')==0,'ListPrice check type error'
        assert self.snapshotitem.setListPrice(2.12)==1,'Set ListPrice error'
        assert self.snapshotitem.setSalesrank(1.1)==0,'Sales rank check type error'
        assert self.snapshotitem.setSalesrank(1)==1,'Set sales rank check type error'
        assert self.snapshotitem.setSeller_count(True)==0,'Seller count check type error'
        assert self.snapshotitem.setSeller_count(1)==1,'Set seller count error'
        assert self.snapshotitem.setIf_amazon_seller(0)==0,'If_amazon_seller check type error'
        assert self.snapshotitem.setIf_amazon_seller(True)==1,'Set If_amazon_seller error'
        assert self.snapshotitem.setCurrent_lowest_price(True)==0
        assert self.snapshotitem.setCurrent_lowest_price(1.1)==1
        assert self.snapshotitem.setCurrent_second_lowest_price(True)==0
        assert self.snapshotitem.setCurrent_second_lowest_price(1.1)==1
        assert self.snapshotitem.setMediumprice(True)==0
        assert self.snapshotitem.setMediumprice(1)==1
        assert self.snapshotitem.setEffect_seller_count(1.1)==0
        assert self.snapshotitem.setEffect_seller_count(1)==1
        assert self.snapshotitem.setTimestamp(1)==0
        assert self.snapshotitem.setTimestamp(datetime.datetime.now())==1
        assert self.snapshotitem.setSeller_list([])==1
        
    def testAssemble(self):
        self.snapshotitem.setASIN('1234')
#        self.snapshotitem.setPrice(1.1)
        self.snapshotitem.setListPrice(2.12)
        self.snapshotitem.setSalesrank(1)
        self.snapshotitem.setSeller_count(1)
        self.snapshotitem.setIf_amazon_seller(True)
        self.snapshotitem.setCurrent_lowest_price(1.1)
        self.snapshotitem.setCurrent_second_lowest_price(1.2)
        self.snapshotitem.setMediumprice(3.1)
        self.snapshotitem.setEffect_seller_count(1)
        times=datetime.datetime.now()
        self.snapshotitem.setTimestamp(times)
        self.snapshotitem.setSeller_list([])
        assert self.snapshotitem.assemble()=={
                  "_id":'1234'+str(times),'ASIN':'1234',                            
#                    "price":1.1,
                    "list_price":2.12,
                    "salesrank":1,"seller_count":1,
                    "if_amazon_seller":True,"current_lowest_price":1.1,
                    "current_second_lowest_price":1.2,"medium_price":3.1,
                    "effect_seller_count":1,
                    "timestamp":times,"seller_list":[]}
    
    def testSaveToDB(self):
        self.snapshotitem.setASIN('1234')
#        self.snapshotitem.setPrice(1.1)
        self.snapshotitem.setListPrice(2.12)
        self.snapshotitem.setSalesrank(1)
        self.snapshotitem.setSeller_count(1)
        self.snapshotitem.setIf_amazon_seller(True)
        self.snapshotitem.setCurrent_lowest_price(1.1)
        self.snapshotitem.setCurrent_second_lowest_price(1.2)
        self.snapshotitem.setMediumprice(3.1)
        self.snapshotitem.setEffect_seller_count(1)
        times=datetime.datetime.now()
        self.snapshotitem.setTimestamp(times)
        self.snapshotitem.setSeller_list([])
        self.snapshotitem.saveToDB()
        result=self.test_collection.find({'ASIN':'1234'})
        assert result[0]['list_price']==2.12
        self.test_collection.remove({'ASIN':'1234'},safe=True)
    
    def testDelete(self):
        times=datetime.datetime.now()
        doc={
                  "_id":'1234'+str(times),'ASIN':'1234',                            
#                    "price":1.1,
                    "list_price":2.12,
                    "salesrank":1,"seller_count":1,
                    "if_amazon_seller":True,"current_lowest_price":1.1,
                    "current_second_lowest_price":1.2,"medium_price":3.1,
                    "effect_seller_count":1,
                    "timestamp":times,"seller_list":[]
                                              }
        self.test_collection.insert(doc,safe=True)
        self.snapshotitem.delete('list_price', 2.12)
        assert self.test_collection.find().count!=0
    
    def testUpdateToDb(self): 
        times=datetime.datetime.now()
        doc={
                  "_id":'1234'+str(times),'ASIN':'1234',                      
#                    "price":1.1,
                    "list_price":2.12,
                    "salesrank":1,"seller_count":1,
                    "if_amazon_seller":True,"current_lowest_price":1.1,
                    "current_second_lowest_price":1.2,"medium_price":3.1,
                    "effect_seller_count":1,
                    "timestamp":times,"seller_list":[]
                                              }
        self.test_collection.insert(doc,safe=True)
        self.snapshotitem.setASIN('1234')
        self.snapshotitem.setTimestamp(times)
        self.snapshotitem.setListPrice(3.1)
        assert self.snapshotitem.updateToDb()==1
        assert self.test_collection.find({'ASIN':'1234'})[0]["list_price"]==3.1
        self.test_collection.remove({'ASIN':'1234'},safe=True)
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(SnapshotitemTest('testSet'))
    suite.addTest(SnapshotitemTest('testAssemble'))
    suite.addTest(SnapshotitemTest('testSaveToDB'))
    suite.addTest(SnapshotitemTest('testDelete'))
    suite.addTest(SnapshotitemTest('testUpdateToDb'))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())