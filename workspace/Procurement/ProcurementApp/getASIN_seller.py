'''
Created on 2012-9-19

get ASIN from Merchants
http://www.amazon.com/gp/aag/main?seller=(sellerID)
input:    sellerID
output:   ASIN save in file, which name is sellerID

@author: jizhishu
'''
'''
sellerID from URL:
http://www.amazon.com/gp/browse.html?me=(sellerID)
http://www.amazon.com/gp/search?me=(sellerID)
http://www.amazon.com/gp/aag/main?seller=(sellerID)
'''

import httplib 
import re
import urllib2

def getUseMYI(seller):
    url="http://www.amazon.com/gp/aag/main?seller="+seller
    req=urllib2.Request(url)
    fd=urllib2.urlopen(req)
    page_content=fd.read()
    regex_results=r'useMYI: \'(.)\'\};';
    results=re.compile(regex_results,re.S).findall(page_content)
    useMYI=results[0]
    return useMYI

def getData(seller,page,file):
    useMYI=getUseMYI(seller)
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
                #print eval(data)[i]            #ASIN
                file.write(eval(data)[i]+'\n')
            #print len(eval(data))
            return eval(data)
        else:
            return 0
    else: 
        #print "Failed", "\n" 
        return 0
    con2.close()
    
def getData_seller(seller):
    file=open(seller,'w')
    page=1
    while getData(seller,page,file):
        page=page+1
    file.close()

if __name__ == '__main__':
    seller='A3SNNXCKUIW1O2'
    #seller='A2VLI2DYODPTDA'
    data=getData_seller(seller)
