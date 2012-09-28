#coding=utf-8
'''
Created on 2012-6-26
product_sort information item
@author: LSW
'''
import copy,types
import snapshot_statistics_item
import item
class Productsort(item.Item):


    _ASIN=None
    _title=None
    _ancestorList = []
    _last_price = 0.0
    _current_lowest_price = 0.0
    _priceList = []
    _DHI = 0.0
    _salerank = 0.0
    _shipping = 0.0
    
    def __init__(self,useConnection):
        '''fun: initialize product_item
        connect to 'product' collection
        '''
        self._item_connect=useConnection
        self._item_connect.useCollection('product_sort')

    def get_asin(self):
        return self.__ASIN


    def get_title(self):
        return self.__title


    def get_ancestor_list(self):
        return self.__ancestorList


    def get_last_price(self):
        return self.__last_price


    def get_current_lowest_price(self):
        return self.__current_lowest_price


    def get_price_list(self):
        return self.__priceList


    def get_dhi(self):
        return self.__DHI


    def get_salerank(self):
        return self.__salerank


    def get_shipping(self):
        return self.__shipping


    def set_asin(self, value):
        self.__ASIN = value


    def set_title(self, value):
        self.__title = value


    def set_ancestor_list(self, value):
        self.__ancestorList = value


    def set_last_price(self, value):
        self.__last_price = value


    def set_current_lowest_price(self, value):
        self.__current_lowest_price = value


    def set_price_list(self, value):
        self.__priceList = value


    def set_dhi(self, value):
        self.__DHI = value


    def set_salerank(self, value):
        self.__salerank = value


    def set_shipping(self, value):
        self.__shipping = value

    def assemble(self):
        '''功能：把self组装成一个productsort列表的文档，用于插入数据库
        '''
        productsort={
            "_ASIN": self.get_asin(),
            "_title":self.get_title(),
            "_ancestorList" : self.get_ancestor_list(),
            "_last_price" : self.get_last_price(),
            "_current_lowest_price" :self.get_current_lowest_price(),
            "_priceList":self.get_price_list(),
            "_DHI" :self.get_dhi(),
            "_salerank": self.get_salerank(),
            "_shipping" : self.get_shipping()
                 }
        return productsort
        
    def delete(self,key,value):
        if value==None or key==None:
            print 'Delete error: value and key can not be none!'
            return 0
        else:
            self._item_connect.delete(key,value)
            return 1
        
    def searchByASIN(self):
        '''功能：按ASIN搜索文档
        '''
        if self.get_asin() ==None or self.get_asin()=='':
            return None
        else:
            return self._item_connect.search("ASIN",self._name)        
    
 