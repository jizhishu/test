#coding=utf-8
'''
Created on 2012-9-21
deals class
@author: WLS
'''

import types
import item

class MyDeals(item.Item):
    _id = None
    ASIN =None
    content =None
    last_price = 0.0
    current_price = 0.0
    name = None
    deal_title = None
    start_time = None
    expiration_time = None
    img_link = None
    link = None
    stores = None
    category = []
    audiences = None
    like = 0
    dislike = 0
    DHI = 0.0
    type = 'manual'  # auto
    expired = False
    
    def __init__(self,useConnection):
        self._item_connect=useConnection#
        self._item_connect.useCollection('deals')


    def assemble(self):
        '''功能：把self组装成一个商品+评论列表的文档，用于插入数据库
        '''
        postdoc={
                 "_id":self.get_id(),
                 "ASIN":self.get_asin(),
                 "content":self.get_content(),
                 "last_price":self.get_last_price(),
                 "current_price":self.get_current_price(),
                 "name":self.get_name(),
                 "deal_title":self.get_deal_title(),
                 "start_time":self.get_start_time(),
                 "expiration_time":self.get_expiration_time(),
                 "link":self.get_link(),
                 "stores":self.get_stores(),
                 "category":self.get_category(),
                 "audiences":self.get_audiences(),
                 "like":self.get_like(),
                 "dislike":self.get_dislike(),
                 "img_link":self.get_img_link(),
                 "DHI":self.get_DHI(),
                 "type":self.get_type(),
                 "expired":self.get_expired()
                 }
        return postdoc 
    
    def save(self):
        return self._item_connect.save( self.assemble())
    
    def savelist(self,dealslist):
        result = None
        for each in dealslist:
            postdoc = MyDeals()
            postdoc.set_asin(each['ASIN'])
            postdoc.set_audiences(each['audience'])
            postdoc.set_category(each['category'])
            postdoc.set_content(each['content'])
            postdoc.set_deal_title(each['deal_title'])
            postdoc.set_expiration_time(each['expiration_time'])
            postdoc.set_link(each['link'])
            postdoc.set_name(each['name'])
            postdoc.set_last_price(each['last_price'])
            postdoc.set_lcurrent_price(each['current_price'])
            postdoc.set_start_time(each['start_time'])
            postdoc.set_stores(each['stores'])
            postdoc.set_id(each['id'])
            postdoc.set_like(each['like'])
            postdoc.set_dislike(each['dislike'])
            postdoc.set_img_link(each['img_link'])
            postdoc.set_DHI(each['DHI'])
            postdoc.set_type(each['type'])
            postdoc.set_expired(each['expired'])
            result = postdoc.save()
            if(result != 1):
                return 0;
        return 1
    
    def searchbyType(self,type):
        return self._item_connect.search('type',type)
    
    def searchbyCategory(self,NodeID):
        return self._item_connect.search('category',NodeID)
    
    def searchCount(self):
        return self._item_connect.search().count() 
    
    def searchAll(self):
        '''功能：按name搜索文档
        '''
        return self._item_connect.searchAll() 
    
    def searchLikeByContent(self,value):
        '''功能：按value模糊搜索content
        '''
        return self._item_connect.searchLike("content",value)
    
    def searchByName(self):
        '''功能：按name搜索文档
        '''
        if self.getName()==None or self.getName()=='':
            return None
        else:
            return self._item_connect.search("name",self._name)   
        
    def updateByID(self,postdoc):
        '''update postdoc into db by ASIN
        return value:
        -1: if no connection to mongoDB
        0: update fail
        1: update success
        '''
        if self._item_connect==None:
            print "No connection!"
            return -1
        
        if self.get_id()!=None:
            #postdoc=self.assemble()
            return self._item_connect.simpleUpdate(self.get_id(), postdoc)
        else:
            print 'ASIN can not be none!'
            return 0   
    
    def delete(self,key,value): 
        if value==None or key==None:
            print 'Delete error: value and key can not be none!'
            return 0
        else:
            self._item_connect.delete(key,value)
            return 1
        

    def get_id(self):
        return self._id


    def get_asin(self):
        return self.ASIN


    def get_content(self):
        return self.content


    def get_last_price(self):
        return self.last_price

    def get_current_price(self):
        return self.current_price

    def get_name(self):
        return self.name


    def get_deal_title(self):
        return self.deal_title


    def get_start_time(self):
        return self.start_time


    def get_expiration_time(self):
        return self.expiration_time


    def get_link(self):
        return self.link


    def get_stores(self):
        return self.stores


    def get_category(self):
        return self.category


    def get_audiences(self):
        return self.audiences
    
    def get_like(self):
        return self.like
    
    def get_dislike(self):
        return self.dislike
    
    def get_img_link(self):
        return self.img_link
    
    def get_DHI(self):
        return self.DHI
    
    def get_type(self):
        return self.type
    
    def get_expired(self):
        return self.expired

    def set_id(self, value):
        self._id = value

    def set_asin(self, value):
        self.ASIN = value

    def set_content(self, value):
        self.content = value

    def set_last_price(self, value):
        self.last_price = value

    def set_current_price(self,value):
        self.current_price = value

    def set_name(self, value):
        self.name = value

    def set_deal_title(self, value):
        self.deal_title = value

    def set_start_time(self, value):
        self.start_time = value

    def set_expiration_time(self, value):
        self.expiration_time = value

    def set_link(self, value):
        self.link = value

    def set_stores(self, value):
        self.stores = value

    def set_category(self, value):
        self.category = value

    def set_audiences(self, value):
        self.audiences = value
        
    def set_like(self,value):
        self.like = value
        
    def set_dislike(self,value):
        self.dislike = value

    def set_img_link(self,value):
        self.img_link = value
        
    def set_type(self,value):
        self.type = value
        
    def set_expired(self,value):
        self.expired = value
