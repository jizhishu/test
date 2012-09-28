#coding=utf-8
'''
Created on 2012-7-19
deals class
@author: xcl
'''
import types
import item
class Deals(item.Item):

    _name=None
    _price=0.0
    _expiration_time=None
    _content=None
    
    def __init__(self,useConnection):
        self._item_connect=useConnection#
        self._item_connect.useCollection('deals')
        
    def getName(self):
        return self._name
    
    def setName(self,name):
        if type(name) is types.StringType:
            self._name=name
            return 1
        else:
            print 'Name must be string type'
            return 0
        
    def getPrice(self):
        return self._price
    
    def setPrice(self,price):
        if (type(price) is types.FloatType) or (type(price) is types.IntType):
            self._price=price
            return 1
        else:
            print 'Price must be float type'
            return 0
            
    def getExpiration_time(self):
        return self._expiration_time
    
    def setExpiration_time(self,time):
        self._expiration_time=time
        return 1
        
    def getContent(self):
        return self._content
    
    def setContent(self,content):
        if type(content) is types.StringType:
            self._content=content
            return 1
        else:
            print 'Content must be string type'
            return 0
        
    def assemble(self):
        '''功能：把self组装成一个商品+评论列表的文档，用于插入数据库
        '''
        postdoc={
                 "_id":self.getASIN(),
                 "name":self.getName(),
                 "price":self.getPrice(),
                 "expiration_time":self.getExpiration_time(),
                 "content":self.getContent()
                 }
        return postdoc
        
    def delete(self,key,value):
        if value==None or key==None:
            print 'Delete error: value and key can not be none!'
            return 0
        else:
            self._item_connect.delete(key,value)
            return 1
        
    def searchByName(self):
        '''功能：按name搜索文档
        '''
        if self.getName()==None or self.getName()=='':
            return None
        else:
            return self._item_connect.search("name",self._name)
        
    def searchLikeByContent(self,value):
        '''功能：按value模糊搜索content
        '''
        return self._item_connect.searchLike("content",value)
    
    def searchAll(self):
        '''功能：按name搜索文档
        '''
        return self._item_connect.searchAll()