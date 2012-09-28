'''
Created on 2012-8-9
each browesenodo's top DHI ASIN LIST
@author: xcl
'''

import types
import copy

class DHI():
    
    _browsenode_id=None
    _ASIN_list=[]
    
    def __init__(self,useConnection):
        self._item_connect=useConnection
        self._item_connect.useCollection('DHI')
    
    def getBrowsenodeID(self):
        return self._browsenode_id
    
    def setBrowsenodeID(self,bid):
        if type(bid) is types.StringType:
            self._browsenode_id=bid
            return 1
        else:
            print 'Browse node id must be string type'
            return 0
        
    def getASIN_list(self):
        return self._ASIN_list
    
    def setASIN_list(self,A_list):
        if type(A_list) is types.ListType:
            self._ASIN_list=copy.deepcopy(A_list)
            return 1
        else:
            print 'ASIN list must be list type'
            return 0
        
    def assemble(self):
        postdoc={
                 "_id":self.getBrowsenodeID(),
                 "ASIN_list":self.getASIN_list()
                 }
        return postdoc
    
    def saveToDB(self):
        '''save self to mongoDb
        will use self.assemble() to assemble self to a document
        return value:
        -2: if no connection to mongoDB
        -1: if BrowsenodeID is none
         0: document's id has already in mongoDB, won't be saved to db
        1: save to database 
        '''
        if self._item_connect==None:
            print "No connection!"
            return -2
        if self.getBrowsenodeID()!=None and self.getBrowsenodeID()!="":
            postdoc=self.assemble()
            result=self._item_connect.insertDocument(postdoc)
            return result
        else:
            print "ASIN can not be none!"
            return -1
    
    
    def deleteByBrowsenodeID(self):
        
        return self._item_connect.delete('_id',self.getBrowsenodeID())
    
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
        
        if self.getBrowsenodeID()!=None and self.getBrowsenodeID()!='':
            postdoc=self.assemble()
            return self._item_connect.simpleUpdate(self.getBrowsenodeID(), postdoc)
        else:
            print 'Browse node id can not be none!'
            return 0
    
    def searchByBrowsenodeID(self):
        return self._item_connect.search("_id",self.getBrowsenodeID())
    
    def searchList(self,ASIN):
        return self._item_connect.search("ASIN_list",ASIN)
    
    