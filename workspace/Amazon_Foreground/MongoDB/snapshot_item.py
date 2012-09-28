#coding=utf-8
'''
Created on 2012-6-27
snapshot item
@author: xcl
'''

import types,datetime,copy,seller_item
import item
class Snapshot(item.Item):
    
    #_price=0.0
    _list_price=0.0
    _salesrank=0
    _seller_count=0
    _if_amazon_seller=False
    _current_lowest_price=0.0
    _current_second_lowest_price=0.0
    _medium_price=0.0
    _effect_seller_count=0
    _timestamp=None#Snapshot time
    _seller_list=[]#seller_list,each item in seller_list must be seller_item.Seller()
    
    def __init__(self,useConnection):
        self._item_connect=useConnection
        self._item_connect.useCollection('snapshot')
        
#    def getPrice(self):
#        return self._price
#    
#    def setPrice(self,price):
#        if (type(price) is types.FloatType) or (type(price) is types.IntType):
#            self._price=price
#            return 1
#        else:
#            print 'Price must be float or integer type'
#            return 0
        
    def getListPrice(self):
        return self._list_price
    
    def setListPrice(self,inlist_price):
        if (type(inlist_price) is types.FloatType)or (type(inlist_price) is types.IntType):
            self._list_price=inlist_price
            return 1
        else:
            print 'ListPrice must be float or integer type'
            return 0
    
    def getSalesrank(self):
        return self._salesrank
    
    def setSalesrank(self,inrank):
        if type(inrank) is types.IntType:
            self._salesrank=inrank
            return 1
        else:
            print 'salesrank must be integer type'
            return 0
        
    def getSeller_count(self):
        return self._seller_count
        
    def setSeller_count(self,incount):
        if type(incount) is types.IntType:
            self._seller_count=incount
            return 1
        else:
            print 'seller count must be integer type'
            return 0
        
    def getIf_amazon_seller(self):    
        return self._if_amazon_seller
    
    def setIf_amazon_seller(self,value):
        if type(value) is types.BooleanType:
            self._if_amazon_seller=value
            return 1
        else:
            print value,'is not a boolean type'
            return 0
            
    def getCurrent_lowest_price(self):
        return self._current_lowest_price
    
    def setCurrent_lowest_price(self,invalue):
        if (type(invalue) is types.FloatType)or(type(invalue) is types.IntType):
            self._current_lowest_price=invalue
            return 1
        else:
            print 'current_lowest_price must be float or integer type'
            return 0
        
    def getCurrent_second_lowest_price(self):
        return self._current_second_lowest_price
    
    def setCurrent_second_lowest_price(self,invalue):
        if (type(invalue) is types.FloatType)or (type(invalue) is types.IntType):
            self._current_second_lowest_price=invalue
            return 1
        else:
            print 'current_lowest_price must be float or integer type'
            return 0

    def getMediumprice(self):
        return self._medium_price
    
    def setMediumprice(self,inprice):
        if (type(inprice) is types.FloatType)or (type(inprice) is types.IntType):
            self._medium_price=inprice
            return 1
        else:
            print "medium price must be float or integer type"
            return 0
    
    def getEffect_seller_count(self):
        return self._effect_seller_count
    
    def setEffect_seller_count(self,ineffect_seller_count):
        if type(ineffect_seller_count) is types.IntType:
            self._effect_seller_count=ineffect_seller_count
            return 1
        else:
            print 'seller count must be integer type'
            return 0

    def getTimestamp(self):
        return self._timestamp
    
    def setTimestamp(self,intimestamp):
        if type(intimestamp) is type(datetime.datetime.now()):
            self._timestamp=intimestamp
            return 1
        else:
            print 'timestamp count must be time type'
            return 0
        
    def getSeller_list(self):
        return self._seller_list
    
    def setSeller_list(self,inseller_list):
        '''set seller list
        0：if seller list isn't list type
        -1：item in seller list is not seller_item.Seller() object
        1：set success
        '''
        if type(inseller_list) is types.ListType:
            temp=copy.deepcopy(inseller_list)
            testSeller=seller_item.Seller()
            old_list=copy.deepcopy(self._seller_list)
            self._seller_list=copy.deepcopy([])
            for each in temp:
                if not(type(each)==type(testSeller)):
                    self._seller_list=copy.deepcopy(old_list)
                    print 'Each seller in review list must be a Seller() object'
                    return -1
                dic={
                     "seller_name":each.seller_name,
                     "seller_url":each.seller_url,
                     "seller_price":each.seller_price,
                     "seller_rating":each.seller_rating,
                     "is_fulfillment_by_amazon":each.is_fulfillment_by_amazon,
                     "shipping":each.shipping,
                     "is_eligible_for_prime":each.is_eligible_for_prime
                    }
                self._seller_list.append(dic)
            return 1
        else:
            print 'seller_list count must be list type'
            return 0

    def assemble(self):
        postdoc={
                 "_id":self.getASIN()+str(self.getTimestamp()),
                 "ASIN":self.getASIN(),
                 #"price":self.getPrice(),
                 "list_price":self.getListPrice(),
                 "salesrank":self.getSalesrank(),
                 "seller_count":self.getSeller_count(),
                 "if_amazon_seller":self.getIf_amazon_seller(),
                 "current_lowest_price":self.getCurrent_lowest_price(),
                 "current_second_lowest_price":self.getCurrent_second_lowest_price(),
                 "medium_price":self.getMediumprice(),
                 "effect_seller_count":self.getEffect_seller_count(),
                 "timestamp":self.getTimestamp(),
                 "seller_list":self.getSeller_list()
                 }
        return postdoc
    
    def delete(self,key,value):
        return self._item_connect.delete(key,value)
            
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
            return self._item_connect.simpleUpdate(self.getASIN()+str(self.getTimestamp()), postdoc)
        else:
            print "ASIN is None!"
            return 0
        
    def searchByTime(self):
        return self._item_connect.search("ASIN",self._ASIN)
              
if __name__=='__main__':
    isnap=Snapshot().setTimestamp(datetime.datetime.utcnow())
    print datetime.datetime.now(),isnap