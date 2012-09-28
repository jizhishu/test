'''
Created on 2012-7-26

@author: jizhishu

'''
import re
import urllib2
import string
#import sys
import time

def noteDelete(page_content):
    noteContentArray = re.compile('<!--(.*?)-->', re.S).findall(page_content)
    for each in noteContentArray:
        page_content = page_content.replace("<!--" + each + "-->", "")
    noteContentArray = re.compile('<!--(.*?)-->', re.S).findall(page_content)
    if len(noteContentArray) == 0:
        #print "note delete work is finished!"
        return page_content
    else:
        #print "note delete work is failed!!" + len(noteContentArray)
        return 0

def page(page_content):
    regex_results=r'Showing(.+?)sults';
    regex_result=r'\s(.+?)Re';
    regex_find=r'(of)';
    regex_result_2=r'of (.+?)\s';
    results=re.compile(regex_results,re.S).findall(page_content)
    for content in results:
        result=re.compile(regex_result).findall(content)
        for content2 in result:
            find=re.compile(regex_find).search(content2)
            if find:
                result=re.compile(regex_result_2).search(content2)
            else:
                result=re.compile(regex_result).search(content)
        result=result.group(1)
    #print result
    s=result.split(',')
    result=''.join(s)
    result=string.atoi(result)
    mod=result%24
    if mod==0:
        page=result/24
    else:
        page=result/24+1
    print page
    return page
    
url="http://www.amazon.com/cell-phones-service-plans-accessories/b?ie=UTF8&me=A19R3BN6ZSO9A1&node=2335752011"
time1=time.clock()
#url=sys.argv[1]
req=urllib2.Request(url)
fd=urllib2.urlopen(req)
page_content=fd.read()
page_content=noteDelete(page_content)
page=page(page_content)
asin_list=[]
for i in range(1,page+1):
    result=url+"&page="+str(i)
    req=urllib2.Request(result)
    print 'page:'+str(i)
    fd=urllib2.urlopen(req)
    page_content=fd.read()
    page_content=noteDelete(page_content)
    regex_asins=r'<div id="(.+?)" class="productTitle">'
    regex_asin=r'srProductTitle_(.+?)_'
    asins=re.compile(regex_asins,re.S).findall(page_content)
    for content in asins:
        asin=re.compile(regex_asin).search(content)
        asin=asin.group(1)
        asin_list.append(asin)
        print asin
print len(asin_list)
time2=time.clock()
print time1
print time2
print time2-time1
'''
import httplib 
import re
import urllib2
import time
def getUseMYI(seller):
    url="http://www.amazon.com/gp/aag/main?seller="+seller
    req=urllib2.Request(url)
    fd=urllib2.urlopen(req)
    page_content=fd.read()
    regex_results=r'useMYI: \'(.)\'\};';
    results=re.compile(regex_results,re.S).findall(page_content)
    useMYI=results[0]
    return useMYI
def getData(seller,page,useMYI):
    params = "seller="+seller+"&currentPage="+str(page)+"&useMYI="+useMYI
    headers = { 
               "Accept": "*/*", 
               "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", 
               "Host": "www.amazon.com", 
               } 
    con2 = httplib.HTTPConnection("www.amazon.com") 
    con2.request("POST", "/gp/aag/ajax/searchResultsJson.html", params, headers) 
    r2 = con2.getresponse() 
    if r2.status == 200: 
        #print "Success", "\n"
        data=r2.read()
        if len(eval(data)):
            for i in range(0,len(eval(data))):
                print eval(data)[i]
            print len(eval(data))
            return eval(data)
        else:
            return 0
    else: 
        print "Failed", "\n" 
    con2.close()
seller='AN8LN2YPKS7DF'
page=1
time1=time.clock()
useMYI=getUseMYI(seller)
while getData(seller,page,useMYI):
    page=page+1
print "OK"
time2=time.clock()
print time1
print time2
print time2-time1
'''