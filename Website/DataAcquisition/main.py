import tornado.ioloop
from tornado.options import define, options
from multiprocessing import Manager, freeze_support
import tornado.httpserver
import tornado.web
from urls import application

define("port", default=8000, help="run on the given port", type=int)

def main(first):
    #if os.fork() != 0:
    #    exit()
    if str(first) == 'duo':
        freeze_support()
        print("Quit the server with CONTROL-C.")
        app = application
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.bind(options.port)
        http_server.start(num_processes = 8)
        tornado.ioloop.IOLoop.instance().start()
    elif str(first) == 'dan':
        app = application
        app.listen(options.port)
        print ("Starting development server at http://172.29.152.3:" + str(options.port) )
        print ("Quit the server with CONTROL-C.")
        tornado.ioloop.IOLoop.instance().start()
    else:
        print ("error command: duo or dan?")


if __name__ == "__main__":
    main('dan')
    # application.listen(options.port)
    # print("Starting development server at http://127.0.0.1:"+str(options.port))
    # print("Quit the server with CONTROL-C.")
    # tornado.ioloop.IOLoop.instance().start()



