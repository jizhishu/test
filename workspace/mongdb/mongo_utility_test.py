#coding=utf-8
'''
Created on 2012-7-2
unitest of mongo_utility.py 
@author: xcl
'''
import unittest
import mongo_utility
import pymongo

class MongoUtilityTest(unittest.TestCase):

    test_connection=pymongo.Connection('192.168.1.110',27017)
    test_db=test_connection.test1
    test_collection=test_db.test1

    def setUp(self):
        self.utility = mongo_utility.MongoUtility(serverip='192.168.1.110',dbname='test1',collectionname='test1')
    
    def tearDown(self):
        self.utility=None
    
    def testGetCollectionName(self):
        assert self.utility.getCollectionName()=='test1','incorrect collection name'
        
    def testUseDB(self):      
        self.assertEqual(self.utility.useDB('anydb'),self.test_connection.anydb)
        print
    
    def testUseCollection(self):
        
        self.assertEqual(self.utility.useCollection('anycollection'), self.test_db.anycollection)
        
    def testFind(self):
        document1={
                  '_id':'1'
                  }
        document2={
                  '_id':'2'
                  }
        
        self.test_collection.insert(document1,safe=True)
        self.test_collection.insert(document2,safe=True)
        result1=self.utility.find()
        result2=self.test_collection.find()
        num=result1.count()
        for i in range(0,num):
            self.assertEqual(result1[i],result2[i])
        self.test_collection.remove({'_id':'1'},safe=True)
        self.test_collection.remove({'_id':'2'},safe=True)
    
    def testSearch(self):
        document={
                  '_id':'123'
                  }
        self.test_collection.insert(document,safe=True)
        result1=self.utility.search('_id','123')
        result2=self.test_collection.find({'_id':'123'})
        num=result1.count()
        for i in range(0,num):
            assert result1[i]==result2[i],'search error'
        self.assertEqual(self.utility.search(None, None),None)
        self.assertEqual(self.utility.search(None, '123'),None)
        self.assertEqual(self.utility.search('_id', None),None)
        self.test_collection.remove({'_id':'123'},safe=True)
        
    def testInsertDocument(self):
        document={
                  '_id':'1234'
                  }
        result1=self.utility.insertDocument(document)
        
        result2=self.utility.insertDocument(document)
        self.test_collection.remove({'_id':'1234'},safe=True)
        assert result1==1,'insert error'
        assert result2==0,'due key check error'
        document2={
                   'hello':'123'
                   }
        result3=self.utility.insertDocument(document2)
        assert result3==-1,'_id check error'

    def testSimpleUpdate(self):
        document={
                  '_id':'12345',
                  'content':'hello'
                  }
        self.test_collection.insert(document,safe=True)
        updatedoc={
                   'content':'goodbye'
                   }
        self.utility.simpleUpdate('12345', updatedoc)
        result=self.test_collection.find({'_id':'12345'})
        assert result[0]['content']=='goodbye','update error'
        self.test_collection.remove({'_id':'12345'},safe=True)
    
    def testDelete(self):
        result1=self.utility.delete(None, None)
        assert result1==None,'check error'
        result1=self.utility.delete('1', None)
        assert result1==None,'check error'
        result1=self.utility.delete(None, '1')
        assert result1==None,'check error'
        document={
                  '_id':'12345',
                  'content':'hello'
                  }
        self.test_collection.insert(document,safe=True)
        result1=self.utility.delete('content', 'hello')
        assert result1==1,'delete error'

    def testAddToSet(self):
        document={
                  '_id':'12345',
                  'content':[1,2,3]
                  }
        self.test_collection.insert(document,safe=True)
        self.utility.addToSet('12345', 'content', 4)
        result=self.test_collection.find({'_id':'12345'})[0]
        assert result['content']==[1,2,3,4],'addtoset error'
        self.utility.addToSet('12345', 'content', 2)
        result2=self.test_collection.find({'_id':'12345'})[0]
        assert result2['content']==[1,2,3,4],'addtoset error'
        self.test_collection.remove({'_id':'12345'},safe=True)
        
    def testPush(self):
        document={
                  '_id':'12345',
                  'content':[1,2,3]
                  }
        self.test_collection.insert(document,safe=True)
        self.utility.push('12345', 'content', 4)
        result=self.test_collection.find({'_id':'12345'})[0]
        assert result['content']==[1,2,3,4],'push error'
        self.utility.push('12345', 'content', 2)
        result2=self.test_collection.find({'_id':'12345'})[0]
        print result2['content']
        assert result2['content']==[1,2,3,4,2],'push error'
        self.test_collection.remove({'_id':'12345'},safe=True)

def suite():  
    suite = unittest.TestSuite()      
    suite.addTest(MongoUtilityTest("testGetCollectionName"))  
    suite.addTest(MongoUtilityTest("testUseDB")) 
    suite.addTest(MongoUtilityTest("testUseCollection")) 
    suite.addTest(MongoUtilityTest("testFind"))
    suite.addTest(MongoUtilityTest("testSearch"))  
    suite.addTest(MongoUtilityTest("testInsertDocument"))
    suite.addTest(MongoUtilityTest("testSimpleUpdate"))
    suite.addTest(MongoUtilityTest("testDelete"))
    suite.addTest(MongoUtilityTest("testAddToSet"))
    suite.addTest(MongoUtilityTest("testPush"))
    return suite 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    unittest.TextTestRunner().run(suite())

#    for i in range(1000):
##        try:
#        print i
#        ty = mongo_utility.MongoUtility(serverip='localhost',dbname='test1',collectionname='test1')
#        ty.getCollectionName()
#            #ty.disconnect()
##        except Exception,e:
##            print e
##            i=i-1
    