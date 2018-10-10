#-*- encoding:utf-8 -*-
import http.client
import hashlib
import json

def validate():

    conn = http.client.HTTPConnection("192.168.100.109:8885")
    
    HashKey = "beebeejump2018getrich"
    
    request = {}
    data={'validationRequest':{'referenceID':'sn123', 'otherDetails':{'Phoneno': '8034364466',
        'Product':'7' }}}
    
    hash_str = data['validationRequest']['referenceID'] + \
        data['validationRequest']['otherDetails']['Phoneno'] + \
        str(data['validationRequest']['otherDetails']['Product']) + HashKey
    
    print hash_str + '\n'
    
    data['validationRequest']['hash'] = hashlib.sha512(hash_str).hexdigest()
    print data['validationRequest']['hash']
    # print hashlib.sha512(hashstr).hexdigest()
    
    jstr = json.dumps(data)
    print jstr
    
    conn.request("POST", "/ussd/gt/validation", jstr)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read()
    print(data1)

def update():

    conn = http.client.HTTPConnection("134.119.178.199:8885")
    
    HashKey = "beebeejump2018getrich"
    
    request = {}
    data={'paymentUpdateRequest':{'referenceID':'sn123', 'otherDetails':{'Phoneno': '8034364466',
        'Product':'7' }, 'transReference':'50001963102', 'Currency':'566',
        'totalAmount':'566'}}

    pdata = data['paymentUpdateRequest']
    hash_str = pdata['referenceID'] + \
        pdata['transReference'] + \
        pdata['totalAmount'] + \
        str(pdata['Currency']) + HashKey
    
    print hash_str + '\n'
    
    pdata['hash'] = hashlib.sha512(hash_str).hexdigest()
    print data['paymentUpdateRequest']['hash']
    # print hashlib.sha512(hashstr).hexdigest()
    
    jstr = json.dumps(data)
    print jstr
    
    conn.request("POST", "/ussd/gt/update", jstr)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read()
    print(data1)

if __name__ == '__main__':
    print 'hello world'
    #validate()
    update()

