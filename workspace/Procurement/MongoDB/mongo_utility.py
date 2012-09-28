#coding=utf-8
'''
Created on 2012-6-26
mongoDB Utility
@author: xcl
'''
import pymongo
import logging
import mongo_config

class MongoUtility():
    
    _connection=None#connection to mongoDB
    _db=None#mongoDB database
    _collection=None#mongoDB table
    _dbname=None#database's name
    _collectionname=None#table's name
    logger=logging.getLogger('function_get_idf.py')#python log
    console=None
       
    def __init__(self,serverip=mongo_config.serverip,port=mongo_config.serverport,dbname='amazon',collectionname='test'):
        '''fun： initialize mongoDB
        
        make a connection to default server ip、default server port、default dbname、default collection name''' 
        self.console = logging.FileHandler(mongo_config.log_mongoDB_path)
        self.console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.console.setFormatter(formatter)
        self.logger.addHandler(self.console)  
        try:
            self._connection=pymongo.Connection(serverip,port)
            exec "self._db=self._connection."+str(dbname)
            exec "self._collection=self._db."+str(collectionname)
            
        except Exception, e:
            self.logger.error(e)
            print e
            raise
        self._dbname=dbname
        self._collectionname=collectionname
        
    def __del__(self):  
        self.logger.removeHandler(self.console)
        self.console.close()
        self._connection.close()
        
        
    def getCollectionName(self):
        return self._collectionname
    
    def ensureIndex(self,indexlist):
        '''each time you use this fun, you can create One Index. 
        The index's Keys and directions are in the indexlist
        indexlist： a list like: [(key1,pymongo.ASCENDING),(key2,pymongo.DESCENDING)]
        '''
        try:
            self._collection.ensure_index(indexlist)
        except Exception, e:
            self.logger.error('Ensure_index error: '+str(e))
            print 'Ensure_index error:',e
            raise
        
    def dropIndex(self,indexlist):
        '''each time you use this fun, you can Drop One Existed Index.
        indexlist： a list like: [(key1,pymongo.ASCENDING),(key2,pymongo.DESCENDING)]
        '''
        try:
            self._collection.drop_index(indexlist)
        except Exception, e:
            self.logger.error('drop_index error: '+str(e))
            print 'drop_index error:',e
            raise
    
    def useDB(self,dbname):
        '''fun: switch current database
        Parameter: dbname, string type'''
        try:
            exec "self._db=self._connection."+str(dbname)
            self._dbname=str(dbname)
            return self._db
        except Exception, e:
            self.logger.error('Switch database error: '+str(e))
            print 'Switch database error:',e
            raise
              
    def useCollection(self,collectionname):
        '''fun: switch current collection
        Parameter: collectionname, string type'''
        exec "self._collection=self._db."+str(collectionname)
        self._collectionname=str(collectionname)
        return self._collection
            
    def find(self,doc={},skipnum=0,limitnum=0,collection=None):
        '''fun: search current collection, and return all records in it
        '''
        if collection!=None:
            self.useCollection(collection)
        try:
            return self._collection.find(doc,timeout=False).skip(skipnum).limit(limitnum)
        except Exception, e:
            self.logger.error('Search all error: '+str(e))
            print 'Search all error:',e
            raise
            return None
    
    def search(self,key,value,collection=None):
        '''fun: simple search function
        search by the pair of key and value
        Parameter: key,value, both are string type'''
        if (key!=None and value!=None):
            if collection!=None:
                self.useCollection(collection)
            try:
                search=self._collection.find({key:value},timeout=False)
                return search
            except Exception, e:
                self.logger.error('Search error: '+str(e))
                print 'Search error:',e
                raise
                return None
        else:
            print 'key or value is none!'
            return None
        
    def searchLike(self,key,like_value,collection=None):
        '''fun: Fuzzy search
        Parameter: 
         key: search key
         like_value: Fuzzy search key word
         collection: if collection is None, use self's collection, otherwise switch collection'''      
        if (key!=None and key!=''and like_value!=None and like_value!=''):
            if collection!=None:
                self.useCollection(collection)
            try:
                search=self._collection.find({key:{"$regex": like_value}})
                return search
            except Exception, e:
                self.logger.error('Fuzzy search error: '+str(e))
                print 'Fuzzy search error:',e
                raise
                return None
        else:
            return None
    
    def insert(self,doclist,collection=None):
        '''Bulk insert
        '''
        if collection!=None:
            self.useCollection(collection)
        try:
            self._collection.insert(doclist,safe=True)
            print 'Insert success!'
            return 1
        except Exception, e:
            self.logger.error('Insert error: '+str(e))
            print 'Insert error:',e
            raise
            return None
        
    def save(self,doc,collection=None):
        '''save, if due key, then replace the record
        '''
        if collection!=None:
            self.useCollection(collection)
        try:
            self._collection.save(doc,safe=True)
            print 'Insert success!'
            return 1
        except Exception, e:
            self.logger.error('Insert error: '+str(e))
            print 'Insert error:',e
            raise
            return None
        
    def insertDocument(self,document,collection=None):
        '''fun: insert one document to current collection  
        return value: 
         -1: if item didn't have _id
         0: if _id has already in database
         1: Insert success
         None: insert exception
        Parameter: assembled document'''
        if collection!=None:
            self.useCollection(collection)
            
        if document.get('_id','N/A')=='N/A':
            print "_id hasn't been defined!"
            return -1
        search=self._collection.find({"_id":document['_id']})
        if(search.count()>0):
            print "_id "+document['_id']+" is already exist!"
            return 0
        else:
            try:
                self._collection.insert(document,safe=True)
                print 'Insert success!'
                return 1
            except Exception, e:
                self.logger.error('Insert one document error: '+str(e))
                print 'Insert one document error:',e
                raise
                return None
        
    def simpleUpdate(self,in_id,document,upsert_flag=False,collection=None):
        '''fun: simple update
        Parameter: 
         update _id: string
         document: assembled doc into mongoDB'''
        if collection!=None:
            self.useCollection(collection)
        try:
            self._collection.update({"_id":in_id},document,upsert=upsert_flag,safe=True)
            return 1
        except Exception, e:
            self.logger.error('Update error: '+str(e))
            print 'Update error:',e
            raise
            return None
        
    def renameField(self,oldname,newname):
        '''rename field from oldname to newname
        '''
        try:
            self._collection.update({},{"$rename":{oldname:newname}},safe=True,multi=True)
        except Exception, e:
            self.logger.error('Rename error: '+str(e))
            print e
            raise
        
    def setField(self,field_name,default_value,doc={}):
        try:
            self._collection.update(doc,{"$set":{field_name:default_value}},safe=True,multi=True)
        except Exception, e:
            self.logger.error('Set field error: '+str(e))
            print e
            raise
        
    def unsetField(self,field_name,doc={}):
        try:
            self._collection.update(doc,{"$unset":{field_name:1}},safe=True,multi=True)
        except Exception, e:
            self.logger.error('Unset field error: '+str(e))
            print e
            raise
        
    def delete(self,key,value,collection=None):
        '''fun: delete record by the pair of key and value
        fun will check whether key or value is none or "", if one is none or "", fun won't delete anything
        return value:
         0: delete fail
         1: delete success
         None: key or value is none or ''
        Parameter: pair of key and value
        '''
        if collection!=None:
            self.useCollection(collection)
            
        if (key!=None and key!=''and value!=None and value!=''):
            try:
                self._collection.remove({key:value},safe=True)
            except Exception, e:
                self.logger.error('Delete error: '+str(e))
                print 'Delete error:',e
                raise
            if self.search(key, value).count()!=0:  
                print "Delete fail!"
                return 0
            else:
                print "Delete success!"
                return 1
        else:
            print 'key or value is None!'
            return None
        
    def addToSet(self,ASIN,key,value,collection=None):
        '''fun: add value to a list in one document, will check double value
        说明：向已有key对应的数组添加数据value
        参数：要追加数据的id（ASIN），数组键名key，添加的数据value
        '''
        if collection!=None:
            self.useCollection(collection)
        try:
            self._collection.update({"_id":ASIN},{"$addToSet":{key:value}},safe=True)
        except Exception, e:
            self.logger.error('AddToSet error: '+str(e))
            print 'AddToSet error:',e  
            raise
        
    def push(self,ASIN,key,value,collection=None):
        '''fun: push value to a list in one document
        说明：向已有key对应的数组追加数据value到末尾
        参数：要追加数据的id（ASIN），数组键名key，
        value: push value
        '''
        if collection!=None:
            self.useCollection(collection)
        try:
            self._collection.update({"_id":ASIN},{"$push":{key:value}},safe=True)
        except Exception, e:
            self.logger.error('Push error: '+str(e))
            print 'Push error:',e 
            raise 
 
if __name__ == "__main__":
    i=MongoUtility(serverip=1)           