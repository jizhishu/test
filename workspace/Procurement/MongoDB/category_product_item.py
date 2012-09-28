'''
Created on 2012-8-1
content:product information from list HTMLs in product category graph
@author: zxb
'''

import types
import item
import mongo_utility

class CategoryProductItem(item.Item):
    '''
    used to save product data as items
    which are parsed from the list page(HTML)
    '''
    _product_name = None    # string(product name, may be very long)
    _category_path = None   # string list array(all paths arrived the product in the category graph) 
    _ancestor = None        # string list(relevant product categories)
    _root_category = None   #string list(root category)
    _record_time = None     #string(record product time)
    _importance = 0         #ASIN's importance
    _salesranks={}
#    _exist_item = None #documtent(the item exists in the db with the same ASIN )
    
    def __init__(self, useConnection):
        '''fun: initialize product_item
        connect to 'category_product' collection
        '''
        self._item_connect = useConnection
        self._item_connect.useCollection('ASIN')   
    
    def getSalesranks(self):
        return self._salesranks
    
    def setSalesranks(self,salesdict):
        if type(salesdict)is types.DictionaryType:
            self._salesranks=salesdict
            return 1
        else:
            return 0   
                
    def getProductName(self):
        return self._product_name
    
    def setProductName(self, name_temp):
        ''' 1 : success
            0 : error - type is not string 
            '''
        if type(name_temp) is types.StringType:
            self._product_name = name_temp
            return 1
        else:
            return 0         
          
    def getCategoryPath(self):
        return self._category_path
    
    def setCategoryPath(self, path_temp):
        ''' 1 : success
            0 : error - type is not list array 
            '''
        if type(path_temp) is types.ListType:
            self._category_path = path_temp
            return 1
        else:
            return 0             
        
    def getAncestor(self):
        return self._ancestor

    def setAncestor(self, ancestor_temp):
        ''' 1 : success
            0 : error - type is not string 
            '''
        if type(ancestor_temp) is types.ListType:
            self._ancestor = ancestor_temp
            return 1
        else:
            return 0   
      
    def getRecordTime(self):
        return self._record_time
    
    def setRecordTime(self, time_temp):
        ''' 1 : success
            0 : error - type is not string 
            '''
        if type(time_temp) is types.StringType:
            self._record_time = time_temp
            return 1
        else:
            return 0  

    def getRootCategory(self):
        return self._root_category
    
    def setRootCategory(self, category_temp):
        ''' 1 : success
            0 : error - type is not string 
            '''
        if type(category_temp) is types.ListType:
            self._root_category = category_temp
            return 1
        else:
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
          
    def deleteByProductName(self):
        '''fun: delete by product_name
        '''
        return self._item_connect.delete('product_name',self.getProductName())

    def deleteRootCategory(self):
        '''fun: search by root_category
        '''
        return self._item_connect.delete('root_category',self.getRootCategory())

    def searchByProductName(self):
        '''fun: search by product name
        '''
        return self._item_connect.search("product_name",self.getProductName())        

    def mergeItem(self, oldItem, newItem):
        diff_item = oldItem
        #find new category path
        for i in newItem.getCategoryPath():
            flag = True
            for j in oldItem.getCategoryPath():
                if j == i:
                    flag = False #not new element
                    break
            if flag:
                diff_item.setCategoryPath(diff_item.getCategoryPath().append(i))
        #find new ancestor
        for i in newItem.getAncestor():
            flag = True
            for j in oldItem.getAncestor():
                if j == i:
                    flag = False #not new element
                    break
            if flag:
                diff_item.setAncestor(diff_item.getAncestor().append(i))  
        #find new root category
        for i in newItem.getRootCategory():
            flag = True
            for j in oldItem.getRootCategory():
                if j == i:
                    flag = False #not new element
                    break
            if flag:
                diff_item.setRootCategory(diff_item.getRootCategory().append(i))  
        return diff_item

    def assemble(self):     
        postdoc={
                 "_id":self.getASIN(),
                 "product_name": self.getProductName(),
                 "root_category": self.getRootCategory(),
                 "category_path": self.getCategoryPath(),
                 "ancestor": self.getAncestor(),
                 "record_time": self.getRecordTime(),
                 "salesranks": self.getSalesranks(),
                 "importance": self.getImportance()
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
        if self._item_connect==None:
            print "No connection!"
            return -2
        print self.getASIN()
        if self.getASIN()!=None and self.getASIN()!="":
            ancestor_cursor = self._item_connect.search("_id", self.getASIN())
            #if there exists a product with the same ASIN, we merge two product's browsenode information
            #we assume that one ASIN points to only one product
            if ancestor_cursor.count() > 0:
                olditem = CategoryProductItem(self._item_connect)
                olditem.setASIN(str(ancestor_cursor[0]["_id"]))
                olditem.setAncestor(ancestor_cursor[0]["ancestor"])
                olditem.setCategoryPath(ancestor_cursor[0]["category_path"])
                olditem.setProductName(str(ancestor_cursor[0]["product_name"]))
                olditem.setRecordTime(str(ancestor_cursor[0]["record_time"]))
                olditem.setRootCategory(ancestor_cursor[0]["root_category"])
                olditem.setImportance(ancestor_cursor[0]["importance"])
                #merge old item and new item and update database
                result = self._item_connect.simpleUpdate(self.getASIN(), self.mergeItem(olditem, self).assemble())
                if  result == 1:
                    print "Update success!!"
                else:
                    return result
            else:         
                postdoc=self.assemble()
                result=self._item_connect.insertDocument(postdoc)
                return result
        else:
            print "ASIN can not be none!"
            return -1
    
if __name__ == "__main__":
    connect = mongo_utility.MongoUtility(serverip='local', dbname='amazon', collectionname='ASIN')
    categoryItem = CategoryProductItem(connect)
#    categoryItem._item_connect.setField("importance", "10000000")
    categoryItem.setASIN("3")
    categoryItem.setAncestor(["3"])
    categoryItem.setCategoryPath([["A1,A2","A1,A3"]])
    categoryItem.setProductName("wahaaha")
    categoryItem.setRootCategory(["R1", "R2"])
    categoryItem.setRecordTime("2012-08-06")