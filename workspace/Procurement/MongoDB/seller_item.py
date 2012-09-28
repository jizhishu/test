#coding=utf-8
'''
Created on 2012-7-9

@author: xcl
'''
import types

class Seller():
    seller_name=None
    seller_url=None
    seller_price=0.0
    seller_rating=None#卖家的得分
    is_fulfillment_by_amazon=False
    shipping=0.0#运费
    is_eligible_for_prime=False
    