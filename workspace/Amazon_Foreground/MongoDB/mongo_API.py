#coding=utf-8
'''
Created on 2012-7-16
for小林的mongoAPI：高度集成版API函数

无需指定数据库、表名，函数名代表了对应功能
@author: xcl
'''
import mongo_utility,json,bson.json_util,sys
import snapshot_statistics_item
import product_item,reviewlist_item,review_item
import deals_item

connect=mongo_utility.MongoUtility(serverip='localhost')
def productInsert(prodoc):
    '''插入产品
    参数：
        doc：字典结构文档，可以通过调用json.loads(json字符串)获得
    '''
    product=product_item.Product(connect)
    
    set_check_flag=[]
    set_check_flag.append(product.setASIN(prodoc.get('ASIN')))
    set_check_flag.append(product.setTitle(prodoc.get('title')))
    set_check_flag.append(product.setBrand(prodoc.get('brand')))
    set_check_flag.append(product.setManufacturer(prodoc.get('manufacturer')))
    set_check_flag.append(product.setDescription(prodoc.get('description')))
    set_check_flag.append(product.setOtherDetails(prodoc.get("otherDetails")))
    set_check_flag.append(product.setVelocity(prodoc.get('velocity')))
    set_check_flag.append(product.setFeature(prodoc.get('feature')))
     
    statistics_item=snapshot_statistics_item.Snapshot_statistics()
    statistics_item.maximum=prodoc.get("snapshot_statistics").get("maximum")
    statistics_item.median=prodoc.get("snapshot_statistics").get("median")
    statistics_item.minimum=prodoc.get("snapshot_statistics").get("minimum")
    statistics_item.plural=prodoc.get("snapshot_statistics").get("plural")
    
    set_check_flag.append(product.setSnapshot_statistics(statistics_item))
    
    set_check_flag.append(product.setCategory(prodoc.get('category')))
    set_check_flag.append(product.setSimi(prodoc.get("simi")))
    
    for flag in set_check_flag:
        if flag!=1:
            temp_result={
                    'Set flag':'Fail'
                    }
            jsonresult=json.dumps(temp_result)
            print jsonresult
            return flag
        
    save_result=product.saveToDB()
    save_json=None
    if save_result==1:
        save_json='Success'
    else:
        save_json='Fail'
    temp_result={
                    'Save flag':save_json
                    }
    jsonresult=json.dumps(temp_result)
    print jsonresult
    return save_result
    
def productSearchByASIN(asin):
    '''按ASIN搜索产品
    返回的是搜索结果数组，数组成员是json字符串（不是pythonde字典结构体）
    '''
    product=product_item.Product(connect)
    if product.setASIN(asin)!=1:
        temp_result={
                   'Set flag':'Fail'
                   }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return    
    search_result=product.searchByASIN()
    result=[]
    for i in range(search_result.count()):
        one=search_result[i]
        result.append(one)
    jsonresult={
                'result':result              
                }
    jsonresult=json.dumps(jsonresult)
    print jsonresult
    return result

def productDeleteByASIN(asin):
    '''按ASIN删除产品
    '''
    product=product_item.Product(connect)
    if product.setASIN(asin)!=1:
        temp_result={
                    'Set flag':'Fail'
                    }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return
    delete_result=product.deleteByASIN()
    delete_json=None
    if delete_result==1:
        delete_json='Success'
    else:
        delete_json='Fail'
    temp_result={
                    'Delete flag':delete_json
                    }
    jsonresult=json.dumps(temp_result)
    print jsonresult
    return delete_result

def reviewlistInsert(revdoc):
    reviewlist=reviewlist_item.ReviewList(connect)
    
    set_check_flag=[]
    set_check_flag.append(reviewlist.setASIN(revdoc.get('ASIN')))
    
    revlist=revdoc.get('revlist')
    setlist=[]
    for each in revlist:
        review=review_item.Review()
        review.setAuthor(each.get('author'))
        review.setStar(each.get('star'))
        review.setDate(each.get('date'))
        review.setContent(each.get('content'))
        review.setHelpful(each.get('helpful'))
        review.setAuthor(each.get('author'))
        setlist.append(review)
        
    set_check_flag.append(reviewlist.setRevlist(setlist))
    
    for flag in set_check_flag:
        if flag!=1:
            temp_result={
                    'Set flag':'Fail'
                    }
            jsonresult=json.dumps(temp_result)
            print jsonresult
            return flag
    save_result=reviewlist.saveToDB()
    save_json=None
    if save_result==1:
        save_json='Success'
    else:
        save_json='Fail'
    temp_result={
                    'Save flag':save_json
                    }
    jsonresult=json.dumps(temp_result)
    print jsonresult
    return save_result
    
def reviewlistSearchByASIN(asin):
    reviewlist=reviewlist_item.ReviewList(connect)
    if reviewlist.setASIN(asin)!=1:
        temp_result={
                    'Set flag':'Fail'
                    }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return
    search_result=reviewlist.searchByASIN()
    result=[]
    for i in range(search_result.count()):
        one=search_result[i]
        result.append(one)
    jsonresult={
                'result':result              
                }
    jsonresult=json.dumps(jsonresult)
    print jsonresult
    return result

def reviewlistDeleteByASIN(asin):
    reviewlist=reviewlist_item.ReviewList(connect)
    if reviewlist.setASIN(asin)!=1:
        temp_result={
                    'Set flag':'Fail'
                    }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return
    delete_result=reviewlist.deleteByASIN()
    delete_json=None
    if delete_result==1:
        delete_json='Success'
    else:
        delete_json='Fail'
    temp_result={
                    'Delete flag':delete_json
                    }
    jsonresult=json.dumps(temp_result)
    print jsonresult
    return delete_result

def dealsInsert(dealdoc):
    deal=deals_item.Deals(connect)
    
    set_check_flag=[]
    set_check_flag.append(deal.setASIN(dealdoc.get('ASIN')))
    set_check_flag.append(deal.setName(dealdoc.get('name')))
    set_check_flag.append(deal.setPrice(dealdoc.get('price')))
    set_check_flag.append(deal.setExpiration_time(dealdoc.get('expiration_time')))
    set_check_flag.append(deal.setContent(dealdoc.get('content')))
    
    for flag in set_check_flag:
        if flag!=1:
            temp_result={
                    'Set flag':'Fail'
                    }
            jsonresult=json.dumps(temp_result)
            print jsonresult
            return flag
    
    save_result=deal.saveToDB()
    save_json=None
    if save_result==1:
        save_json='Success'
    else:
        save_json='Fail'
    temp_result={
                    'Save flag':save_json
                    }
    jsonresult=json.dumps(temp_result)
    print jsonresult
    return save_result

def dealsSearchByASIN(asin):
    deal=deals_item.Deals(connect)
    if deal.setASIN(asin) !=1:
        temp_result={
                    'Set flag':'Fail'
                    }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return
    
    search_result=deal.searchByASIN()
    result=[]
    for i in range(search_result.count()):
        #one=json.dumps(search_result[i],default=bson.json_util.default)
        one=search_result[i]
        result.append(one)
    #result=json.dumps(search_result[i],default=bson.json_util.default)
    jsonresult={
                'result':result              
                }
    jsonresult=json.dumps(jsonresult)
    print jsonresult
    return result

def dealsSearchByContent(asin,value):
    deal=deals_item.Deals(connect)
    if deal.setASIN(asin) !=1:
        temp_result={
                    'Set flag':'Fail'
                    }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return
    
    search_result=deal.searchLikeByContent(value)
    result=[]
    for i in range(search_result.count()):
        one=search_result[i]
        result.append(one)
    jsonresult={
                'result':result              
                }
    jsonresult=json.dumps(jsonresult)
    print jsonresult
    return result

def dealsDeleteByASIN(asin):
    deal=deals_item.Deals(connect)
    if deal.setASIN(asin) !=1:
        temp_result={
                    'Set flag':'Fail'
                    }
        jsonresult=json.dumps(temp_result)
        print jsonresult
        return
    delete_result= deal.deleteByASIN()
    delete_json=None
    if delete_result==1:
        delete_json='Success'
    else:
        delete_json='Fail'
    temp_result={
                    'Delete flag':delete_json
                    }
    jsonresult=json.dumps(temp_result)
    print jsonresult
    return delete_result

if __name__=="__main__":
    if len(sys.argv)>1:
        if sys.argv[1]=='productInsert':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                struct=json.loads(tempdoc)               
                productInsert(struct)
        if sys.argv[1]=='productSearchByASIN':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                productSearchByASIN(opinion['asin'])
        if sys.argv[1]=='productDeleteByASIN':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                productDeleteByASIN(opinion['asin'])
                
        if sys.argv[1]=='reviewlistInsert':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                struct=json.loads(tempdoc)               
                reviewlistInsert(struct)
        if sys.argv[1]=='reviewlistSearchByASIN':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                reviewlistSearchByASIN(opinion['asin'])
        if sys.argv[1]=='reviewlisttDeleteByASIN':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                reviewlistDeleteByASIN(opinion['asin'])
        
        if sys.argv[1]=='dealsInsert':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                struct=json.loads(tempdoc)               
                dealsInsert(struct)
        if sys.argv[1]=='dealsSearchByASIN':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                dealsSearchByASIN(opinion['asin'])
        if sys.argv[1]=='dealsSearchByContent':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                dealsSearchByContent(opinion['asin'],opinion['value'])
        if sys.argv[1]=='dealsDeleteByASIN':
            if len(sys.argv)>2:
                tempdoc=sys.argv[2]
                opinion=json.loads(tempdoc)               
                dealsDeleteByASIN(opinion['asin'])
#    doc = {
#               "ASIN": '123',
#               "title":'Star War',
#               "brand":'LEGO',
#               "manufacturer":'Denmark',
#               "description":'good toys',
#               "otherDetails":'total 1092 pieces',
#               "velocity":1,
#               "feature":{},
#               "snapshot_statistics":{
#                                      'median':1117,
#                                      'maximum':1234,
#                                      'minimum':1000,
#                                      'plural':1100},
#               "category":[],
#               "simi":[]
#               }
#    ee=productInsert(doc)
#    
#    res=productSearchByASIN('12345')
#    print res
#    res=productSearchByASIN('123')
#    print res
#    struct=json.loads(res[0])
#    print 'struct:',struct['brand']
#    productDeleteByASIN('123')
#    res=productSearchByASIN('123')
#    print res