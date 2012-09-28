'''
Created on 2012-9-19

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
    data = r1.read() 
    #print data
    conn.close() 
    return data
def image(ASIN):
    import re
    page_content=use_httplib(ASIN)
    regex_results=r'src=.+?images/I/(.+?)._.+?_.jpg';#<img onclick=.+?
    results=re.compile(regex_results,re.S).findall(page_content)
    print results
if __name__ == "__main__": 
     image('B006E8MKZU')