import tornado.ioloop
import pyrestful.rest

from pyrestful import mediatypes
from pyrestful.rest import get,post

class EchoService(pyrestful.rest.RestHandler):
     @post('/echo','application/json','application/json')
     def sayHello(self,doc):
         return doc

if __name__ == '__main__':
     try:
          print("Start the echo service")
          app = pyrestful.rest.RestService([EchoService])
          app.listen(8080)
          tornado.ioloop.IOLoop.instance().start()
     except KeyboardInterrupt:
          print("\nStop the echo service")
