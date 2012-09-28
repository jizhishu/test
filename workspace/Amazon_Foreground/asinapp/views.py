# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from models import *

def main(request):
    return render_to_response('main.html')

def dataimport(request):
    return render_to_response('import.html')

def List(cate):
    a=asin()
    if a==0:
        list=a.getList()
    else:
        list=a.getList(category=cate)
    Li=[]
    for i in range(0,len(list),3):
        li=list[i:i+3]
        Li.append(li)
    return Li

def operate(request,offset=0):
    category=getCategory()
    Li=List(offset)
    return render_to_response('operate.html',{'category':category,'list':Li})
    
def operateDetail(request,offset):
    category=getCategory()
    a=asin()
    detail=a.findByASIN(offset)
    return render_to_response('operate.html',{'category':category,'detail':detail})
@csrf_exempt
def dataimport_seller(request):
    return render_to_response("seller.html")

@csrf_exempt
def dataimport_file(request):
    if request.method == 'POST':
        # save new post
        File = request.FILES
        Post = request.POST
        
        #post = Post(File=File)
        #post.save() 
        #assert False
    return render_to_response('file.html', {'file': File,'Post':Post},
                              context_instance=RequestContext(request))
if __name__=="__main__":
    test=[]