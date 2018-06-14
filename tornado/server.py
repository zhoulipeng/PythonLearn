import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import hashlib
import time 
from json import loads
from json import dumps
from tornado.options import define, options
define("port", default=8885, help="run on the given port", type=int)


HashKey = 'beebeejump2018getrich'

class ValidationHandler(tornado.web.RequestHandler):
    def hash_valid(self, values):
        if not ('validationRequest' in values):
            print 'not ValidationRequest'
            return False

        data = values['validationRequest']

        if not ('referenceID' in data):
            print 'not referenceID'
            return False

        if not ('otherDetails' in data):
            print 'not otherDetails'
            return False

        if not ('hash' in data):
            print 'not hash'
            return False

        if not ('Phoneno' in data['otherDetails']):
            print 'not Phoneno'
            return False

        if not ('Product' in data['otherDetails']):
            print 'not product'
            return False


        hash_str = data['referenceID'] + data['otherDetails']['Phoneno'] + \
        str(data['otherDetails']['Product']) + HashKey

        print 'recv hash is:' + hash_str + '\n'

        if data['hash'] == hashlib.sha512(hash_str).hexdigest():
            return True
        else:
            return False
    
    def response(self, values):
        data = values['validationRequest']
        data['CustomerName'] = 'Adeoye Ibukunoluwa'
        data['otherDetails']['Amount'] = '129355.32'
        data['otherDetails']['Charge'] = '0'
    
        data['totalAmount'] = '129355.32'
        data['Currency'] = '566'
        data['statusCode'] = '00'
        data['statusMessage'] = 'success'
        hash_str = data['referenceID'] + data['CustomerName'] + \
        data['totalAmount'] + data['Currency'] + \
        data['statusCode'] + data['statusMessage'] + HashKey

        data['hash'] = hashlib.sha512(hash_str).hexdigest()

        response = {}
        response['validateResponse'] = data 
        self.write(dumps(response))
    
    def response_invalid(self, values):
        data = values['validationRequest']
    
        data['statusCode'] = '01'
        data['statusMessage'] = 'invalid'

        response = {}
        response['validateResponse'] = data 
        self.write(dumps(response))

    def post(self):
        values = loads(self.request.body)
        print "Play:", values
        if self.hash_valid(values):
            self.response(values)
        else:
            self.response_invalid(values)


class UpdateHandler(tornado.web.RequestHandler):
    def hash_valid(self, values):
        if not ('paymentUpdateRequest' in values):
            print 'not paymentUpdateRequest'
            return False
        
        data = values['paymentUpdateRequest']

        if not ('transReference' in data):
            print 'not transReference'
            return False

        if not ('totalAmount' in data):
            print 'not totalAmount'
            return False

        if not ('Currency' in data):
            print 'not Currency'
            return False

        if not ('otherDetails' in data):
            print 'not otherDetails'
            return False

        if not ('hash' in data):
            print 'not hash'
            return False

        if not ('Phoneno' in data['otherDetails']):
            print 'not Phoneno'
            return False

        if not ('Product' in data['otherDetails']):
            print 'not product'
            return False

        hash_str = data['referenceID'] + \
            data['transReference'] + \
            data['totalAmount'] + \
            str(data['Currency']) + HashKey

        print 'recv hash is:' + hash_str + '\n'

        if data['hash'] == hashlib.sha512(hash_str).hexdigest():
            return True
        else:
            return False

        return True

    def response(self, values):
        data1 = values['paymentUpdateRequest']
        data = {}
    
        data['referenceID'] = data1['referenceID'] 
        data['transReference'] = data1['transReference'] 
        data['PaymentReference'] = hashlib.md5(data1['transReference'] + \
                str(time.time())).hexdigest()
        data['responseCode'] = '00'
        data['responseDesc'] = 'success'
        print data['responseDesc'] + ' hello'
        print data['transReference']
        print data['PaymentReference']
        print data['responseCode']
        print HashKey
        hash_str = data['referenceID'] + data['transReference'] + \
            data['PaymentReference'] + data['responseCode'] + \
            data['responseDesc'] + HashKey


        data['hash'] = hashlib.sha512(hash_str).hexdigest()

        response = {}
        response['PaymentUpdateResponse'] = data 
        self.write(dumps(response))
    
    def response_invalid(self, values):
        data = values['validationRequest']
    
        data['statusCode'] = '01'
        data['statusMessage'] = 'invalid'

        response = {}
        response['validateResponse'] = data 
        self.write(dumps(response))

    def post(self):
        print "hello world:"
        values = loads(self.request.body)
        print "Play:", values
        if self.hash_valid(values):
            self.response(values)
        else:
            self.response_invalid(values)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/ussd/gt/validation", ValidationHandler),
        (r"/ussd/gt/update", UpdateHandler)])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

