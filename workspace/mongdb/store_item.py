'''
Created on 2012-9-27

@author: jizhishu
'''
import types,datetime
import item
class Store(item.Item):
    '''
    store
    '''
    
    _name=None  #data acquisition #Analytic #new product
    _value=None
    _updatetime=None

    def __init__(self,useConnection):
        '''
        Constructor
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('store')
        
         
    def getName(self):
        return self._name
    
    def setName(self,inname):
        if type(inname) is types.StringType:
            self._name=inname
            return 1
        else:
            print 'Name must be string type'
            return 0
       
    def getValue(self):
        return self._value
    
    def setValue(self,invalue):
        if type(invalue) is types.StringType:
            self._value=invalue
            return 1
        else:
            print 'Value must be string type'
            return 0
    
    def getUpdatetime(self):
        return self._updatetime
    
    def setUpdatetime(self,inupdatetime):
        #if type(inupdatetime) is type(datetime.datetime.now()):
        if type(inupdatetime) is types.StringType:
            self._updatetime=inupdatetime
            return 1
        else:
            print 'Updatetime must be string type'
            return 0
    def assemble(self):
        '''fun: assemble self (an system object) to a document
        assemble self to a document based on mongoDB format
        '''
        assembled_postdoc={
                 "_id": self.getASIN(),
                 "name":self.getName(),
                 "value":self.getValue(),
                 "updatetime":self.getUpdatetime(),
                 }
        return assembled_postdoc
        
    def searchByName(self):
        '''fun: search by name
        '''
        return self._item_connect.search("name",self.getName())
    
    def searchByValue(self):
        '''fun: search by value
        '''
        return self._item_connect.search("value",self.getValue())
    
    def searchByUpdatetime(self):
        '''fun: search by updatetime
        '''
        return self._item_connect.search("updatetime",self.getUpdatetime())

import mongo_utility
if __name__=="__main__":
    #connection=mongo_utility.MongoUtility(serverip='localhost')
    connection=mongo_utility.MongoUtility(serverip='192.168.1.110')
    test=System(connection)
    test.setASIN('1234')
    test.setName('Analytic')
    test.setValue('t')
    #test.setUpdatetime(datetime.datetime.now())
    test.setUpdatetime('20120816')
    test.saveToDB()
    result=test.searchByASIN()
    if result.count()>0: print result[0]
    test.setName('new product')
    test.updateToDb()
    result=test.searchByName()
    if result.count()>0: print result[0]['name']
    test.deleteByASIN()
    result=test.searchByASIN()
    if result.count()>0: print result[0]   
        