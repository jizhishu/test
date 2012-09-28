'''
Created on 2012-7-26
ASIN item
@author: xcl
'''
import types,datetime
import item,copy

class ASIN(item.Item):
    
    _product_name=None#product name
    _root_category=[]#product root category
    _find_time=None#find ASIN time
    _importance=0#ASIN's importance
    
    def __init__(self,useConnection):
        '''fun: initialize product_item
        connect to 'review' collection
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('ASIN')
        
    def getProductName(self):
        return self._product_name
        
    def setProductName(self,name): 
        if type(name) is types.StringType:
            self._product_name=name
            return 1
        else:
            print 'Name must be string type'
            return 0   
        
    def getRootCategory(self):   
        return self._root_category
    
    def setRootCategory(self,root_category):
        if type(root_category) is types.ListType:
            self._root_category=copy.deepcopy(root_category)
            return 1
        else:
            print 'Root category must be string type'
            return 0  
        
    def getFindTime(self):
        return self._find_time
    
    def setFindTime(self,find_time):
        if type(find_time) is type(datetime.datetime.now()):
            self._find_time=find_time
            return 1
        else:
            print 'Find time must be TIME type'
            return 0  
    
    def getImportance(self):
        return self._importance
    
    def setImportance(self,importance):
        if type(importance) is types.IntType:
            self._importance=importance
            return 1
        else:
            print 'Importance must be integer type'
            return 0  
        
    def assemble(self):
        postdoc={
                 "_id":self.getASIN(),
                 "product_name":self.getProductName(),
                 "root_category":self.getRootCategory(),
                 "find_time":self.getFindTime(),
                 "importance":self.getImportance()
                 }
        return postdoc
    
    def deleteByName(self):
        '''fun: delete by product_name
        '''
        return self._item_connect.delete('product_name',self.getProductName())
    
    def deleteRootCategory(self):
        '''fun: search by root_category
        '''
        return self._item_connect.delete('root_category',self.getRootCategory())
        
    def searchByName(self):
        '''fun: search by product name
        '''
        return self._item_connect.search("product_name",self.getProductName())

import mongo_utility        
if __name__=="__main__":
    connection=mongo_utility.MongoUtility(serverip='localhost')
    testASIN=ASIN(connection)
    testASIN.setASIN('1234')
    testASIN.setProductName('lego')
    testASIN.setRootCategory('toys')
    testASIN.setFindTime(datetime.datetime.now())
    testASIN.setImportance(1)
    testASIN.saveToDB()
    result=testASIN.searchByASIN()
    if result.count()>0: print result[0]
    testASIN.setProductName('hasbro')
    testASIN.updateToDb()
    result=testASIN.searchByASIN()
    if result.count()>0: print result[0]['product_name']