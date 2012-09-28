# Create your views here.
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import *

def main(request):
    return render_to_response('main.html')

@csrf_exempt
def dataimport(request):
    #assert False
    File=''
    f=''
    if request.method == 'POST':
        if request.POST.has_key('seller'):
            seller = request.POST['seller']
            from getASIN_seller import *
            getData_seller(seller)
            importFile(seller)
        if request.POST.has_key('ASIN'):
            ASIN = request.POST['ASIN']
            importData(ASIN)
        if request.FILES:
            File = request.FILES.get('file',None)
            f=File.field_name()
            #assert False
    #File = request.FILES
    #assert False
    return render_to_response('import.html',{'File':f})

def List(cate):
    a=asin()
    if cate==0:
        list=a.getList()
    else:
        list=a.getList(category=cate)
    Li=[]
    for i in range(0,len(list),3):
        li=list[i:i+3]
        Li.append(li)
    return Li
@csrf_exempt
def operate(request,offset=0):
    a=asin()
    category=a.getCategory()
    Li=List(offset)
    if request.method == 'POST':
        if request.POST.has_key('delete'):
            ASIN = request.POST['delete']
            a.deleteByASIN(ASIN)
    return render_to_response('operate.html',{'category':category,'list':Li})
@csrf_exempt    
def operateDetail(request,offset):
    a=asin()
    category=a.getCategory()
    detail=a.findByASIN(offset)
    if request.method == 'POST':
        if request.POST.has_key('submit'):
            note = request.POST['note']
            ASIN = request.POST['submit']
            a.pushNote(ASIN,note)
        if request.POST.has_key('delete'):
            ASIN = request.POST['delete']
            a.deleteByASIN(ASIN)
    return render_to_response('operate.html',{'category':category,'detail':detail})

@csrf_exempt
def dataimport_file(request):
    if request.method == 'POST':
        # save new post
        File = request.FILES
        Post = request.POST
        
        #post = Post(File=File)
        #post.save() 
        #assert False
    return render_to_response('file.html', {'file': File,'Post':Post})
if __name__=="__main__":
    test=[]