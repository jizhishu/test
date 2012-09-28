'''
Created on 2012-9-10

@author: jizhishu
'''
from models import *
from django.shortcuts import render_to_response

def test():
    page = Page(title='Using MongoEngine')
    page.tags = ['mongodb', 'mongoengine']
    page.save()
    Page.objects().count()

def test1():
    storerating=StoreRating(
                ID='3',
                lifetime=10,
                Product_services_pricing=9,
                chance_of_future_purchase=8,
                shipping_packaging=9.0,
                customer_service=7.0,
                return_replacement_policy=10
                )
    
    store=Store(
                ID='4',
                name='hello22',
                image='meta/51x5WIRc38L._SL110_.jpg',
                url='http://www.dealmoon.com/Printable-coupon-roundup-Quiznos-Baskin-Robbins-Chilis-more/163671.html',
                rating=storerating
                )
                
    store.tags = ['mongodb', 'mongoengine']
    #storerating.tags = ['mongodb', 'mongoengine']
    #storerating.save()
    store.save()
    return Store.objects.all()

def show(request):
    a=Store.objects.all()
    img=a[1]['image']
    return render_to_response('test.html',locals())

def update():
    test=StoreRating.objects.all()
    for a in test:
        print a.ID
        print a.lifetime
    if test.update(set__lifetime=10):
        return 1
    else:
        return 0
a=Store.objects.all()
#print a[0]['name']
#print a[1]['image']
#print a[2]['rating']['lifetime']
#test1()
for b in a:
    c=b.image
    print b.rating.lifetime
    k=b.image.read()
    file=open('test.png','w')
    file.write(k)
    file.close()
#print test1()
#print update()
'''
    category = ReferenceField(StoreCategory)
    rating = ReferenceField(StoreRating)
    info = ReferenceField(StoreInfo)
'''