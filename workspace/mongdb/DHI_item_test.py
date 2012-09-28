'''
Created on 2012-8-9
DHI_item unit test
@author: xcl
'''
import unittest
import pymongo
import DHI_item,mongo_utility

class DHIItemTest(unittest.TestCase):
    test_connection=pymongo.Connection('localhost',27017)
    test_db=test_connection.test1
    test_collection = test_db.DHI
    
    def setUp(self):
        self.connect = mongo_utility.MongoUtility(serverip='localhost', dbname='test1', collectionname='test1')
        self.DHI=DHI_item.DHI(self.connect)
        
    def testSet(self):
        assert self.DHI.setBrowsenodeID(1)==0,"browse node check type error"
        assert self.DHI.setBrowsenodeID('123')==1
        assert self.DHI.setASIN_list('1')==0
        assert self.DHI.setASIN_list([])==1
        
    def testAssemble(self):
        self.DHI.setBrowsenodeID('123')
        self.DHI.setASIN_list(['223','224'])
        assert self.DHI.assemble()=={
                                     "_id":'123',
                                     "ASIN_list":['223','224']
                                     }
    
    def testSave(self):
        assert self.DHI.saveToDB()==-1
        self.DHI.setBrowsenodeID('123')
        self.DHI.setASIN_list(['223','224'])
        assert self.DHI.saveToDB()==1
        assert self.test_collection.find({"_id":'123'}).count()==1
        self.test_collection.remove()
        
    def testUpdate(self):
        doc={
             "_id":'123',
             "ASIN_list":['223','224']
             }
        self.test_collection.insert(doc,safe=True)
        self.DHI.setBrowsenodeID('123')
        self.DHI.setASIN_list(['225'])
        self.DHI.updateToDb()
        assert self.test_collection.find({"_id":"123"})[0]['ASIN_list']==['225']
        self.test_collection.remove()
        
    def testDelete(self):
        doc={
             "_id":'123',
             "ASIN_list":['223','224']
             }
        self.test_collection.insert(doc,safe=True)
        self.DHI.setBrowsenodeID('123')
        assert self.DHI.deleteByBrowsenodeID()==1
        
    def testSearch(self):    
        doc={
             "_id":'123',
             "ASIN_list":['223','224']
             }
        self.test_collection.insert(doc,safe=True)
        
        self.DHI.setBrowsenodeID('123')
        assert self.DHI.searchByBrowsenodeID().count()==1
        assert self.DHI.searchList('223').count()==1
        self.test_collection.remove()
        
def suite():
    suite=unittest.TestSuite()
    suite.addTest(DHIItemTest('testSet'))
    suite.addTest(DHIItemTest('testAssemble'))
    suite.addTest(DHIItemTest('testSave'))
    suite.addTest(DHIItemTest('testUpdate'))
    suite.addTest(DHIItemTest('testDelete'))
    suite.addTest(DHIItemTest('testSearch'))
    return suite
 
if __name__=="__main__":
    unittest.TextTestRunner().run(suite())   