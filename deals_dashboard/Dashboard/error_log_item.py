'''
Created on 2012-7-31

@author: jizhishu
'''

import types,datetime
import item

class Error_log(item.Item):
    '''
    error handing
    '''
    _type=None
    _rank=0
    _description=None
    _time=None

    def __init__(self,useConnection):
        '''
        Constructor
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('error_log')
        
    def getType(self):
        return self._type
    
    def setType(self,intype):
        if type(intype) is types.StringType:
            self._type=intype
            return 1
        else:
            print 'Type must be string type'
            return 0
        
    def getRank(self):
        return self._rank
    
    def setRank(self,inrank):
        if type(inrank) is types.IntType:
            self._rank=inrank
            return 1
        else:
            print 'rank must be integer type'
            return 0
        
    def getDescription(self):
        return self._description
    
    def setDescription(self,indescription):
        if type(indescription) is types.StringType:
            self._description=indescription
            return 1
        else:
            print 'Description must be string type'
            return 0
        
    def getTime(self):
        return self._time
    
    def setTime(self,intime):
        #if type(intime) is type(datetime.datetime.now()):
        if type(intime) is types.StringType:
            self._time=intime
            return 1
        else:
            print 'Time must be time type'
            return 0
        
    def assemble(self):
        '''fun: assemble self (an system object) to a document
        assemble self to a document based on mongoDB format
        '''
        assembled_postdoc={
                 "_id": self.getASIN(),
                 "type":self.getType(),
                 "rank":self.getRank(),
                 "description":self.getDescription(),
                 "time":self.getTime(),
                 }
        return assembled_postdoc
        
    def searchByType(self):
        '''fun: search by type
        '''
        return self._item_connect.search("type",self.getType())
    
    def searchByTime(self):
        '''fun: search by time
        '''
        return self._item_connect.search("time",self.getTime())

import mongo_utility
if __name__=="__main__":
    connection=mongo_utility.MongoUtility(serverip='192.168.1.110')
    test=Error_log(connection)
    test.setASIN('134')
    test.setType('500')
    test.setRank(7)
    test.setDescription('t')
    #test.setTime(datetime.datetime.now()) 
    test.setTime('20120815') 
    test.saveToDB()
    result=test.searchByASIN()
    if result.count()>0: print result[0]
    test.setType('500')
    test.updateToDb()
    result=test.searchByType()
    if result.count()>0: print result[0]['type']
    test.deleteByASIN()
    result=test.searchByASIN()
    if result.count()>0: print result[0]