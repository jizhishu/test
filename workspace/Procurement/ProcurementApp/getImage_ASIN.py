'''
Created on 2012-9-19

get image from http://www.amazon.com/gp/product/images/(ASIN)
input:    ASIN
output:   image url, which type is list

@author: jizhishu
'''
def use_httplib(ASIN): 
    import httplib 
    conn = httplib.HTTPConnection("www.amazon.com") 
    i_headers = {
                 "Accept": "*/*", 
                 "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", 
                 "Host": "www.amazon.com", 
                 } 
    conn.request("GET", "/gp/product/images/"+ASIN, headers = i_headers) 
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
    
def image(ASIN):
    import re
    page_content=use_httplib(ASIN)
    if page_content:
        regex_results=r'images/I/(.+?)._.+?_.jpg'
        results=re.compile(regex_results,re.S).findall(page_content)
        img=[]
        for i in results:
            url="http://ecx.images-amazon.com/images/I/"+i+".jpg"
            if url not in img:
                img.append(url)
        if img:
            return img
        else:
            return []
    else:
        return []
    
if __name__ == "__main__":
    yes=image('B009A8BFM0')
    print yes
    if yes:
        for a in yes:
            print a
    else:
        print 'Sorry'
'''
B006E8MKZU    B009A8BFM0    B008FERRFO    B006GGN5SQ    B00591N52K    
B001W0Y4GI    B001FA1O0O    
'''
