import tornado.ioloop
import pyrestful.rest

from pyrestful import mediatypes
from pyrestful.rest import get,post

class Person:
    name = str
    lastname = str
    age = int

class EchoService(pyrestful.rest.RestHandler):
    @post('/echo',{'types':[Person],'format':'json'},_catch_fire=True)
    def sayHello(self,doc):
        print(doc)
        return doc

if __name__ == '__main__':
     try:
          print("Start the echo service")
          app = pyrestful.rest.RestService([EchoService])
          app.listen(8080)
          tornado.ioloop.IOLoop.instance().start()
     except KeyboardInterrupt:
          print("\nStop the echo service")
