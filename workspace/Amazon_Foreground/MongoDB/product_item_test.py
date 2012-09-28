#coding=utf-8
'''
Created on 2012-7-6
product_item.py unitest
@author: xcl
'''
import unittest
import pymongo
import product_item
import mongo_utility
import snapshot_statistics_item


class ProductitemTest(unittest.TestCase):

    test_connection = pymongo.Connection('localhost', 27017)
    test_db = test_connection.test1
    test_collection = test_db.product
    
    def setUp(self):
        self.connect = mongo_utility.MongoUtility(serverip='localhost', dbname='test1', collectionname='test1')
        self.product = product_item.Product(self.connect)
    
    def testSet(self):
        assert self.product.setASIN(1) == 0, 'ASIN check type error'
        assert self.product.setASIN('123') == 1, 'Set ASIN error'
        assert self.product.setTitle(True) == 0, 'Title check type error'
        assert self.product.setTitle('hello') == 1, 'Set title error'
        assert self.product.setBrand(False) == 0, 'Brand check type error'
        assert self.product.setBrand('LEGO') == 1, 'Set brand error'
        assert self.product.setManufacturer(1) == 0, 'Manufacturer check type error'
        assert self.product.setManufacturer('Denmark') == 1, 'Set manufacturer error'
        assert self.product.setDescription(1) == 0, 'Description check type error'
        assert self.product.setDescription('good toys') == 1, 'Set description error'
        assert self.product.setOtherDetails(True) == 0, 'Other details check type error'
        assert self.product.setOtherDetails('1') == 1, 'Set other details error'
        assert self.product.setDHI('123') == 0, 'DHI check type error'
        assert self.product.setDHI(0.5) == 1, 'Set DHI error'
        assert self.product.setFeature('s') == 1, 'Set feature error'
        assert self.product.setFeature({}) == 0, 'Feature check type error'
        testStatic = snapshot_statistics_item.Snapshot_statistics()
        assert self.product.setSnapshot_statistics(1) == 0, 'Snapshot_statistics check type error'
        assert self.product.setSnapshot_statistics(testStatic) == 1, 'Set snapshot_statistics error'
        assert self.product.setCategory(1) == 0, 'Category check type error'
        assert self.product.setCategory([]) == 1, 'Set category error'
        assert self.product.setSimi(1) == 0, 'Similarity check type error'
        assert self.product.setSimi([]) == 1, 'Set similarity error'

    def testAssemble(self):
        self.product.setASIN('123')
        self.product.setTitle('Star War')
        self.product.setBrand('LEGO')
        self.product.setManufacturer('Denmark')
        self.product.setDescription('good toys')
        self.product.setOtherDetails('total 1092 pieces')
        self.product.setDHI(1)
        self.product.setFeature('s')
        testStatic = snapshot_statistics_item.Snapshot_statistics()
        testStatic.maximum = 1234
        testStatic.minimum = 1000
        testStatic.median = 1117
        testStatic.plural = 1100
        self.product.setSnapshot_statistics(testStatic)
        self.product.setCategory([])
        self.product.setSimi([])
        assert self.product.assemble() == {
                                             "_id": '123',
                                             "title":'Star War',
                                             "brand":'LEGO',
                                             "manufacturer":'Denmark',
                                             "description":'good toys',
                                             "otherDetails":'total 1092 pieces',
                                             "DHI":1,
                                             "feature":'s',
                                             "snapshot_statistics":{
                                                                    'median':1117,
                                                                    'maximum':1234,
                                                                    'minimum':1000,
                                                                    'plural':1100
                                                                    },
                                             "category":[],
                                             "simi":[]       
                                            }, 'Assemble error'
        
    def testSaveToDb(self):      
        result = self.product.saveToDB()
        assert result == -1, 'Check ASIN error'
        self.product.setASIN('123')
        result = self.product.saveToDB()
        assert result == 1, 'Save to db error'
        self.test_collection.remove({'_id':'123'})
        
    def testDeleteByASIN(self):
        self.test_collection.insert({'_id':'987'}, safe=True) 
        self.product.setASIN(None)
        assert self.product.deleteByASIN() == None, 'delete error'
        self.product.setASIN('987')
        assert self.product.deleteByASIN() == 1, 'delete error'
        
    def testUpdateToDb(self):
        doc = {
               "_id": '123',"title":'Star War',
               "brand":'LEGO',"manufacturer":'Denmark',
               "description":'good toys',"otherDetails":'total 1092 pieces',
               "DHI":1,"feature":'s',
               "snapshot_statistics":{
                                      'median':1117,'maximum':1234,
                                      'minimum':1000,'plural':1100},
               "category":[],"simi":[]
               }
        self.test_collection.insert(doc,safe=True)
        self.product.setASIN('123')
        self.product.setDHI(2)
        self.product.updateToDb()
        result=self.test_collection.find({'_id':'123'})[0]['DHI']
        self.test_collection.remove({'_id':'123'})
        assert result==2,'Update error'
    
    def testSearch(self):
        self.product.setASIN('123')
        self.product.setTitle('Star War')
        self.product.setBrand('LEGO')
        self.product.setManufacturer('Denmark')
        self.product.setDescription('good toys')
        self.product.setOtherDetails('total 1092 pieces')
        self.product.setDHI(1)
        self.product.setFeature('s')
        testStatic = snapshot_statistics_item.Snapshot_statistics()
        testStatic.maximum = 1234
        testStatic.minimum = 1000
        testStatic.median = 1117
        testStatic.plural = 1100
        self.product.setSnapshot_statistics(testStatic)
        self.product.setCategory([])
        self.product.setSimi([])
        self.test_collection.insert(self.product.assemble(),safe=True)
        assert self.test_collection.find({'_id':'123'}).count()==1
        assert self.product.searchByASIN()[0]['_id']=='123'
        assert self.product.searchByBrand()[0]['brand']=='LEGO'
        assert self.product.searchByManufacturer()[0]['manufacturer']=='Denmark'
        assert self.product.searchByTitle()[0]['title']=='Star War'
        self.test_collection.remove({'_id':'123'})
        
def suite():  
    suite = unittest.TestSuite()
    suite.addTest(ProductitemTest('testSet'))
    suite.addTest(ProductitemTest('testAssemble'))
    suite.addTest(ProductitemTest('testSaveToDb'))
    suite.addTest(ProductitemTest('testDeleteByASIN'))
    suite.addTest(ProductitemTest('testUpdateToDb'))
    suite.addTest(ProductitemTest('testSearch'))
    return suite
if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
