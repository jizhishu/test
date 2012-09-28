#coding=utf-8
'''
Created on 2012-7-5
reviewlist_item.py unitest
@author: xcl
'''
import unittest,reviewlist_item,mongo_utility,review_item,pymongo,copy


class ReviewitemTest(unittest.TestCase):

    test_connection=pymongo.Connection('localhost',27017)
    test_db=test_connection.test1
    test_collection=test_db.review
    
    def setUp(self):
        self.connect=mongo_utility.MongoUtility(serverip='localhost',dbname='test1',collectionname='test1')
        self.product_rev=reviewlist_item.ReviewList(self.connect)
        
    def testSetASIN(self):
        assert self.product_rev.setASIN(1)==0,'ASIN check type error'
        assert self.product_rev.setASIN('123')==1,'set ASIN error'
        
    def testSetEevlist(self):
        test_list1={}
        assert self.product_rev.setRevlist(test_list1)==0,'list type check error'
        test_rev1=review_item.Review()
        test_rev2=review_item.Review()
        test_rev3='no type'
        test_list2=[test_rev1,test_rev2]
        assert self.product_rev.setRevlist(test_list2)==1,'set review list error'
        test_list2.append(test_rev3)
        assert self.product_rev.setRevlist(test_list2)==-1,'check review type error'

    def testAssemble(self):
        self.product_rev.setASIN('123')
        self.product_rev.setProductName('Lego')
        test_rev1=review_item.Review()
        test_rev1.setAuthor('Mr. D')     
        test_rev2=review_item.Review()
        test_rev2.setAuthor('Mr. W')
        test_list2=[test_rev1,test_rev2]
        self.product_rev.setRevlist(test_list2)
        checkdic={
             "_id":'123',
             "product_name":'Lego',
             "revlist":[{
                     "author":'Mr. D',
                     "star":None,
                     "date":None,
                     "title":None,
                     "content":None,
                     "helpful":None
                     },
                        {
                     "author":'Mr. W',
                     "star":None,
                     "date":None,
                     "title":None,
                     "content":None,
                     "helpful":None
                     }]
             }
        assert self.product_rev.assemble()==checkdic,'assemble error'
    
    def testAssembleOnereview(self):
        test_review=review_item.Review()
        test_review.setAuthor('a')
        test_review.setContent('b')
        test_review.setDate('c')
        test_review.setHelpful('d')
        
        checkdic={"author":'a',
                     "star":None,
                     "date":'c',
                     "title":None,
                     "content":'b',
                     "helpful":'d'         
                  }
        assert self.product_rev.assembleOnereview(test_review)==checkdic,'assember one review error'

    def testSaveToDB_Append(self):
        self.product_rev.setASIN('12345')
        review=[]
        rev1=review_item.Review()
        rev1.setAuthor("Doc. W")
        rev1.setContent("This product is good, I like it.")
        rev1.setDate("2012-2-12")
        rev1.setHelpful("12 of 1922 people fell helpful")
        rev1.setStar("4.0 out of 5.0 stars")
        rev1.setTitle("This product is good")
        review.append(rev1)
        
        rev2=review_item.Review()
        rev2.setAuthor("Mr. W")
        rev2.setContent("This product is easy to use, I like it.")
        rev2.setDate("2012-5-12")
        rev2.setHelpful("12 of 19 people fell helpful")
        rev2.setStar("4.0 out of 5.0 stars")
        rev2.setTitle("This product is easy to use")
        review.append(rev2)
        self.product_rev.setRevlist(review)
        self.product_rev.saveToDB()
        
        result=self.test_collection.find({'_id':'12345'})
        assert result.count()==1,'save to db error'
        assert result[0]['_id']=='12345','save to db error'
        assert result[0]['revlist']==[self.product_rev.assembleOnereview(rev1),                                     
                                      self.product_rev.assembleOnereview(rev2)
                                      ],'save to db error'
        rev3=review_item.Review()
        rev3.setAuthor("Mr. XXX")
        rev3.setContent("This product is easy to use, I like it.")
        rev3.setDate("2012-1-12")
        rev3.setHelpful("1 of 19 people fell helpful")
        rev3.setStar("5.0 out of 5.0 stars")
        rev3.setTitle("This product is easy to use")
        
        self.product_rev.appendToDb('12345', rev3)
        assert result[0]['revlist']==[self.product_rev.assembleOnereview(rev1),                                     
                                      self.product_rev.assembleOnereview(rev2),
                                      self.product_rev.assembleOnereview(rev3)
                                      ],'append to db error'
        self.test_collection.remove({'_id':'12345'})
        
    def testDeleteByASIN(self):
        self.test_collection.insert({'_id':'987'},safe=True)
        self.product_rev.setASIN('987')
        assert self.product_rev.deleteByASIN()==1,'Delete error'
        self.product_rev.setASIN('')
        assert self.product_rev.deleteByASIN()==None,'check None error'
        self.test_collection.remove({'_id':'987'},safe=True)
        
    def testSearchByASIN(self):
        self.product_rev.setASIN('')
        assert self.product_rev.searchByASIN()==None,'check None error'
        self.test_collection.insert({'_id':'123'},safe=True)
        self.product_rev.setASIN('123')
        result1=self.product_rev.searchByASIN()
        result2=self.test_collection.find({'_id':'123'})
        num=result1.count()
        for i in range(0,num):
            assert result1[i]==result2[i],'search error'
        self.test_collection.remove({'_id':'123'},safe=True)
        
    def testUpdateToDb(self): 
        self.product_rev.setASIN(None)
        assert self.product_rev.updateToDb()==0,'check None error'
        self.product_rev.setASIN('9123')
        self.product_rev.setProductName('Lego')
        review=[]
        rev1=review_item.Review()
        rev1.setAuthor("Doc. W")
        rev1.setContent("This product is good, I like it.")
        rev1.setDate("2012-2-12")
        rev1.setHelpful("12 of 1922 people fell helpful")
        rev1.setStar("4.0 out of 5.0 stars")
        rev1.setTitle("This product is good")
        review.append(rev1)
        self.product_rev.setRevlist(review) 
        self.product_rev.saveToDB()
        rev2=copy.deepcopy(rev1)
        rev2.setAuthor("Doc. D")
        review.append(rev2)
        self.product_rev.setRevlist(review)
        self.product_rev.updateToDb()
        result=self.test_collection.find({'_id':'9123'})
        testlist=result[0]['revlist']
        for i in range(0,len(testlist)):
            assert testlist[i]==self.product_rev.assembleOnereview(review[i]),'update error'
        
        
def suite():  
    suite = unittest.TestSuite()
    suite.addTest(ReviewitemTest('testSetASIN'))
    suite.addTest(ReviewitemTest('testSetEevlist'))
    suite.addTest(ReviewitemTest('testAssemble'))
    suite.addTest(ReviewitemTest('testAssembleOnereview'))
    suite.addTest(ReviewitemTest('testSaveToDB_Append'))
    suite.addTest(ReviewitemTest('testDeleteByASIN'))
    suite.addTest(ReviewitemTest('testSearchByASIN'))
    suite.addTest(ReviewitemTest('testUpdateToDb'))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.TextTestRunner().run(suite())