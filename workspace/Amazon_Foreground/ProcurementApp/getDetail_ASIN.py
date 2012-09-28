'''
Created on 2012-9-20

@author: jizhishu
'''
import getImage_ASIN
#import urllib2
import re

def use_httplib(ASIN): 
    import httplib 
    conn = httplib.HTTPConnection("www.amazon.com") 
    i_headers = {
                 "Accept": "*/*", 
                 "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", 
                 "Host": "www.amazon.com", 
                 } 
    conn.request("GET", "/gp/product/"+ASIN, headers = i_headers) 
    r1 = conn.getresponse() 
    if r1.status == 200:
        data = r1.read() 
        #print data
        if data:
            return data
        else:
            return 0
    else:
        return 0
    conn.close()
def getDetail(ASIN):
    page_content=use_httplib(ASIN)
    regex_title     =   r'<span id="btAsinTitle".+?>(.+?)</span>'
    regex_price     =   r'<b class="priceLarge">\$(.+?)</b>'
    regex_rating    =   r'<a style="cursor:pointer;text-decoration:none".+?><span class="swSprite s_star_.+? " title="(.+?)\sout of 5 stars" ><span>'
    regex_nodeID    =   r'http://.+?asin='+ASIN+r'.+?nodeID=(.+?)&'
    result_title=re.compile(regex_title,re.S).findall(page_content)
    result_price=re.compile(regex_price,re.S).findall(page_content)
    result_rating=re.compile(regex_rating,re.S).findall(page_content)
    result_nodeID=re.compile(regex_nodeID,re.S).findall(page_content)
    result_image=getImage_ASIN.image(ASIN)
    rating=0
    if result_rating:
        for rate in result_rating:
            rating=float(rate)
    for node in result_nodeID:
        nodeID=node
    for pri in result_price:
        price=float(pri)
    for tit in result_title:
        title=tit
    result={
            'ASIN'  : ASIN,
            'title' : title,
            'price' : price,
            'rating': rating,#result_rating,
            'nodeID': nodeID,
            'image' : result_image,
            }
    return result

if __name__ == '__main__':
    detail=getDetail('B009A8BFM0')
    print 'ASIN:',detail['ASIN']
    print 'title:',detail['title']
    print 'price:',detail['price']
    print 'rating:',detail['rating']
    print 'nodeID:',detail['nodeID']
    print 'image:',detail['image']
    
    '''
    B009A8BFM0 B005HXUSS4 9981731838
    '''
    #pass