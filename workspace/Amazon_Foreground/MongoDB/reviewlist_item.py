#coding=utf-8
'''
Created on 2012-6-28
product+review_list item
@author: xcl
'''
import copy,review_item
import types
import item
class ReviewList(item.Item):
    
    _product_name=None
    _revlist=[]
    
    def __init__(self,useConnection):
        '''fun: initialize product_item
        connect to 'review' collection
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('review')
    
    def getProductName(self):
        return self._product_name
    
    def setProductName(self,name):
        '''fun: set product name
        return value:
         1: set successful
         0: set fail
        '''
        if type(name) is types.StringType:
            self._product_name=name
            return 1
        else:
            print 'Product name must be string type'
            return 0
        
    def getRevlist(self):
        return self._revlist
    
    def setRevlist(self,revlist):
        '''fun: set review list
        return value:
         0: if review list is not list type
         -1: one of objects in review list is not Review()
         1: set successful
        '''
        if type(revlist)is types.ListType:#check whether revlist is list
            temp=copy.deepcopy(revlist)
            testType2=review_item.Review()
            old_revlist=copy.deepcopy(self._revlist)
            self._revlist=copy.deepcopy([])
            for each in temp:
                #check each review is Review() type
                if not(type(each)==type(testType2)):
                    self._revlist=copy.deepcopy(old_revlist)
                    print 'Each review in review list must be a Review() object type'
                    return -1
                dic=self.assembleOnereview(each)
                self._revlist.append(dic)
            return 1
        else:
            print 'Review list\'s type must be a list type!'
            return 0
       
    def assemble(self):
        '''fun: assemble self to a document
        '''
        postdoc={
                 "_id":self.getASIN(),
                 "product_name":self.getProductName(),
                 "revlist":self.getRevlist()
                 }
        return postdoc
    
    def assembleOnereview(self,one_review):
        '''fun: assemble one review
        说明：用于追加评论到某个商品评论列表最后
        参数：需要提供一个评论对象one_review（是一个review_item.Review()对象）'''
        one_review={
                   "author":one_review.getAuthor(),
                 "star":one_review.getStar(),
                 "date":one_review.getDate(),
                 "title":one_review.getTitle(),
                 "content":one_review.getContent(),
                 "helpful":one_review.getHelpful()                   
                   }
        return one_review
    
    def appendToDb(self,ASIN,one_review):
        '''功能：把一条评论追加到ASIN对应的评论列表revlist的最后
        说明：将会调用assembleOnereview函数组装好one_review
        参数：需要提供AISN和想要添加的评论one_review（一个review_item.Review()对象）'''
        search=self._item_connect.search('_id',ASIN)
        if search.count()>0:
            self._item_connect.addToSet(ASIN,'revlist',self.assembleOnereview(one_review))
            return 1
        else:
            print 'No this _ASIN: '+ASIN
            return 0
        
import mongo_utility
if __name__=="__main__":
    connect=mongo_utility.MongoUtility(serverip='localhost')
    product_rev=ReviewList(connect)
    
    relist=[]
    rev1=review_item.Review()
    rev1.setAuthor("Doc. W")
    rev1.setContent("This product is good, I like it.")
    rev1.setDate("2012-2-12")
    rev1.setHelpful("12 of 1922 people fell helpful")
    rev1.setStar("4.0 out of 5.0 stars")
    rev1.setTitle("This product is good")
    relist.append(rev1)
    
    rev2=review_item.Review()
    rev2.setAuthor("Mr. W")
    rev2.setContent("This product is easy to use, I like it.")
    rev2.setDate("2012-5-12")
    rev2.setHelpful("12 of 19 people fell helpful")
    rev2.setStar("4.0 out of 5.0 stars")
    rev2.setTitle("This product is easy to use")
    relist.append(rev2)
    
    
    rev3=review_item.Review()
    rev3.setAuthor("Mr. XXX")
    rev3.setContent("This product is easy to use, I like it.")
    rev3.setDate("2012-1-12")
    rev3.setHelpful("1 of 19 people fell helpful")
    rev3.setStar("5.0 out of 5.0 stars")
    rev3.setTitle("This product is easy to use")
    
    if(product_rev.setRevlist(relist)==1 and product_rev.setASIN('12345')==1 and product_rev.setProductName('lego toy')):    
        product_rev.saveToDB()   
        product_rev.appendToDb(product_rev.getASIN(), rev3)
        
        searchresult=product_rev.searchByASIN()
        print '搜索结果总数',searchresult.count()
        print '结果',searchresult[0]
        
        rev3.setStar("4.0 out of 5.0 stars")
        relist.append(rev3)
        product_rev.setRevlist(relist)
        print '列表长度',len(relist)
        if(product_rev.saveToDB()!=1):
            product_rev.updateToDb()
        
        if(product_rev.setASIN('234')==1):
            product_rev.saveToDB()
            product_rev.deleteByASIN()