#coding=utf-8
'''
Created on 2012-6-26
product information item
@author: xcl
'''
import copy,types
import snapshot_statistics_item
import item
class Product(item.Item):
    
    _title=None#product's name
    _brand=None#product's brand
    _manufacturer=None#product's manufacturer
    _description=None#product's description
    _other_details=None#other details of product
    _DHI=0.0#product's DHI
    
    _features=None#product's features, such as size, color
    _snapshot_statistics=snapshot_statistics_item.Snapshot_statistics()#statistics
    _category=[]#category
    _simi=[]#similarity
        
    def __init__(self,useConnection):
        '''fun: initialize product_item
        connect to 'product' collection
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('product')
      
    def getTitle(self):
        return self._title
    
    def setTitle(self,intitle):
        if type(intitle) is types.StringType:
            self._title=intitle
            return 1
        else:
            print 'Title must be string type'
            return 0
        
    def getBrand(self):
        return self._brand
    
    def setBrand(self,inbrand):
        if type(inbrand) is types.StringType:
            self._brand=inbrand
            return 1
        else:
            print 'Brand must be string type'
            return 0
        
    def getManufacturer(self):
        return self._manufacturer
    
    def setManufacturer(self,inmanufacturer):
        if type(inmanufacturer) is types.StringType:
            self._manufacturer=inmanufacturer
            return 1
        else:
            print 'Manufacturer must be string type'
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
    
    def getOtherDetails(self):
        return self._other_details
    
    def setOtherDetails(self,inotherDetails):
        if type(inotherDetails) is types.StringType:
            self._other_details=inotherDetails
            return 1
        else:
            print 'OtherDetails must be string type'
            return 0
    
    def getDHI(self):    
        return self._DHI
    
    def setDHI(self,inDHI):
        if type(inDHI) is types.FloatType or type(inDHI) is types.IntType:    
            self._DHI=inDHI
            return 1
        else:
            print 'DHI must be integer type'
            return 0
            
    def getFeature(self):
        return self._features
    
    def setFeature(self,infeature):
        if type(infeature) is types.StringType:
            self._features=infeature
            return 1
        else:
            print 'Feature must be string type'
            return 0
        
    def getSnapshot_statistics(self):
        return self._snapshot_statistics
    
    def setSnapshot_statistics(self,insnapshot_statistics):
        if type(insnapshot_statistics) is type(snapshot_statistics_item.Snapshot_statistics()):
            self._snapshot_statistics=copy.deepcopy(insnapshot_statistics)
            return 1
        else:
            print 'Snapshot_statistics must be Snapshot_statistics type'
            return 0
        
    def getCategory(self):
        return self._category
    
    def setCategory(self,incategory):
        if type(incategory)is types.ListType:
            self._category=copy.deepcopy(incategory)
            return 1
        else:
            print 'Category must be list type'
            return 0
        
    def getSimi(self):
        return self._simi
    
    def setSimi(self,insimi):
        if type(insimi)is types.ListType:
            self._simi=copy.deepcopy(insimi) 
            return 1
        else:
            print 'Similarity must be list type'
            return 0 
        
    def assemble(self):
        '''fun: assemble self (an product object) to a document
        assemble self to a document based on mongoDB format
        '''
        assembled_postdoc={
                 "_id": self.getASIN(),
                 "title":self.getTitle(),
                 "brand":self.getBrand(),
                 "manufacturer":self.getManufacturer(),
                 "description":self.getDescription(),
                 "otherDetails":self.getOtherDetails(),
                 "DHI":self.getDHI(),
                 
                 "feature":self.getFeature(),
                 "snapshot_statistics":{
                                        'median':self.getSnapshot_statistics().median,
                                        'maximum':self.getSnapshot_statistics().maximum,
                                        'minimum':self.getSnapshot_statistics().minimum,
                                        'plural':self.getSnapshot_statistics().plural
                                        },
                 "category":self.getCategory(),                
                 "simi":self.getSimi()
                 }
        return assembled_postdoc
        
    def searchByTitle(self):
        '''fun: search by product's title
        '''
        return self._item_connect.search("title",self.getTitle())
    
    def searchByBrand(self):
        '''fun: search by brand
        '''
        return self._item_connect.search("brand",self.getBrand())
    
    def searchByManufacturer(self):
        '''fun: search by manufacturer
        '''
        return self._item_connect.search("manufacturer",self.getManufacturer())
    