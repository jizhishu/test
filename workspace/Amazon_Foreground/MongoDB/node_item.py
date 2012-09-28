'''
Created on 2012-8-7
content: save browse nodes information as item into mongodb
@author: zxb
'''
import item
import copy

class NodeItem(item.Item):
    '''
    browse node class to record attributes and save into database 
    '''
    
    _node_name = None   #string
    _node_id = None     #string
    _parents = []       #string list,upper layer nodes
    _children = []      #string list,next layer nodes
    _path = []          #path list, all paths can reach the node  
    
    def __init__(self, useConnection):
        self._item_connect=useConnection
        self._item_connect.useCollection('browsenode')  # select the collection
        
    def getNode_name(self):
        return self._node_name
    
    def setNode_name(self,nodename):
        self._node_name=nodename
        
    def getNode_id(self):
        return self._node_id
    
    def setNode_id(self,nodeid):
        self._node_id=nodeid
        
    def getAncestors(self):
        return self._ancestors
    
    def setAncestors(self,ancestors):
        self._ancestors=copy.deepcopy(ancestors)
        
    def getChildren(self):
        return self._children
    
    def setchildren(self,children):
        self._children=copy.deepcopy(children)
     
    def getPath(self):
        return self._path
    
    def setPath(self,path):
        self._path=copy.deepcopy(path)              

    def assemble(self):
        '''
    Function: information organized into a document, 
        used to insert database
        '''
        postdoc={
                 "node_id":self.getNode_id(),
                 "node_name":self.getNode_name(),
                 "ancestors":self.getAncestors(),
                 "children":self.getChildren(),
                 "path":self.getPath()
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
        '''
        Function : search document by name
        '''
        if self.getName()==None or self.getName()=='':
            return None
        else:
            return self._item_connect.search("name",self._name)
        
    def searchLikeByContent(self,value):
        '''
        Function: according to the value content fuzzy search
        '''
        return self._item_connect.searchLike("content",value)        