'''
Created on 2012-7-26

@author: jizhishu
'''
import types,datetime

class ASIN():
    
    _ASIN=None#ASIN
    _product_name=None#product name
    _root_category=None#product root category
    _find_time=None#find ASIN time
    _importance=0#ASIN's importance
    
    def __init__(self,useConnection):
        '''fun: initialize product_item
        connect to 'review' collection
        '''
        self.__connection=useConnection
        self.__connection.useCollection('ASIN')
        
    def getASIN(self):
        return self._ASIN
    
    def setASIN(self,asin):
        if type(asin) is types.StringType:
            self._ASIN=asin
            return 1
        else:
            print 'ASIN must be string type'
            return 0
        
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
        if type(root_category) is types.StringType:
            self._root_category=root_category
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
    
    def saveToDB(self):
        '''save self to mongoDb
        will use self.assemble() to assemble self to a document
        return value:
        -2: if no connection to mongoDB
        -1: if ASIN is none
         0: document's id has already in mongoDB, won't be saved to db
        1: save to database 
        '''
        if self.__connection==None:
            print "No connection!"
            return -2
        if self.getASIN()!=None and self.getASIN()!="":
            postdoc=self.assemble()
            result=self.__connection.insertDocument(postdoc)
            return result
        else:
            print "ASIN is None!"
            return -1
        
    def deleteByASIN(self):
        '''fun: delete by ASIN
        '''
        return self.__connection.delete('_id',self.getASIN())
    
    def deleteByName(self):
        '''fun: delete by product_name
        '''
        return self.__connection.delete('product_name',self.getProductName())
    
    def deleteRootCategory(self):
        '''fun: search by root_category
        '''
        return self.__connection.delete('root_category',self.getRootCategory())
    
    def searchByASIN(self):
        '''fun: search by ASIN
        '''
        if self.getASIN()==None or self.getASIN()=='':
            return None
        else:
            return self.__connection.search("_id",self.getASIN())
        
    def searchByName(self):
        '''fun: search by product name
        '''
        return self.__connection.search("product_name",self.getProductName())
    
    def updateToDb(self):
        '''fun: update self into db by ASIN
        return value:
         return value:
        -1: if no connection to mongoDB
        0: update fail
        1: update success
        '''
        if self.__connection==None:
            print "No connection!"
            return -1
        
        if self.getASIN()!=None:
            postdoc=self.assemble()
            return self.__connection.simpleUpdate(self.getASIN(), postdoc)
        else:
            print "ASIN can not be none!"
            return 0

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