'''
Created on 2012-7-26

@author: xcl
'''
import types

class Item():
    _ASIN=None
    
    _item_connect=None
    
    def __init__(self,useConnection):
        '''fun: initialize product_item
        connect to 'test' collection
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('test')
        
    def getASIN(self):
        return self._ASIN
    
    def setASIN(self,asin):
        if type(asin) is types.StringType:
            self._ASIN=asin
            return 1
        else:
            print 'ASIN must be string type'
            return 0
    
    
    def assemble(self):
        '''fun: assemble self to a document
        assemble self to a document based on mongoDB format
        '''
        assembled_postdoc={"_id": self.getASIN()}
        return assembled_postdoc
    
    def saveToDB(self):
        '''save self to mongoDb
        will use self.assemble() to assemble self to a document
        return value:
        -2: if no connection to mongoDB
        -1: if ASIN is none
         0: document's id has already in mongoDB, won't be saved to db
        1: save to database 
        '''
        if self._item_connect==None:
            print "No connection!"
            return -2
        if self.getASIN()!=None and self.getASIN()!="":
            postdoc=self.assemble()
            result=self._item_connect.insertDocument(postdoc)
            return result
        else:
            print "ASIN can not be none!"
            return -1
        
    def deleteByASIN(self):   
        '''fun: delete by ASIN
        return value:
         0: delete error
         1: delete success
        None: ASIN is none or ""
        '''
        return self._item_connect.delete('_id',self.getASIN())
    
    def update(self,postdoc):
        '''update postdoc into db by ASIN
        return value:
        -1: if no connection to mongoDB
        0: update fail
        1: update success
        '''
        if self._item_connect==None:
            print "No connection!"
            return -1
        
        if self.getASIN()!=None:
            #postdoc=self.assemble()
            return self._item_connect.simpleUpdate(self.getASIN(), postdoc)
        else:
            print 'ASIN can not be none!'
            return 0
    
    def updateToDb(self):
        '''update self into db by ASIN
        return value:
        -1: if no connection to mongoDB
        0: update fail
        1: update success
        '''
        if self._item_connect==None:
            print "No connection!"
            return -1
        
        if self.getASIN()!=None:
            postdoc=self.assemble()
            return self._item_connect.simpleUpdate(self.getASIN(), postdoc)
        else:
            print 'ASIN can not be none!'
            return 0
        
    def searchByASIN(self):
        '''fun: search by ASIN
        '''
        if self.getASIN()==None or self.getASIN()=='':
            print 'ASIN can not be none!'
            return None
        else:
            return self._item_connect.search("_id",self.getASIN())
        
    def search(self,key,value):
        '''fun: search
        '''
        return self._item_connect.search(key,value)
    
    def searchLike(self,key,value):
        '''fun: Fuzzy search
        '''
        return self._item_connect.searchLike(key,value)