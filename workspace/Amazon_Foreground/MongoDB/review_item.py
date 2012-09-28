#coding=utf-8
'''
Created on 2012-6-28
评论抽象
@author: xcl
'''

class Review():

    _author=None
    _star=None
    _date=None
    _title=None
    _content=None
    _helpful=None
    
    def getAuthor(self):
        return self._author
        
    def setAuthor(self,author):    
        self._author=author
        
    def getStar(self):
        return self._star
    
    def setStar(self,star):
        self._star=star
        
    def getDate(self):
        return self._date
    
    def setDate(self,date):
        self._date=date
    
    def getTitle(self):
        return self._title
        
    def setTitle(self,title):
        self._title=title
    
    def getContent(self):
        return self._content
    
    def setContent(self,content):
        self._content=content
        
    def getHelpful(self):
        return self._helpful
    
    def setHelpful(self,helpful):
        self._helpful=helpful
    
    
    