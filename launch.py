#!/usr/bin/env python

import sys
from optparse import OptionParser

import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import settings
from views import routes

def start_instance(settings, routes):
    app = tornado.web.Application(routes, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(settings['port'])
    try: tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: pass


if __name__ == "__main__":
    from tornroutes import route
    parser = OptionParser()
    parser.add_option("-r", "--routes", action="store_true",
            help="print list of routes and exit")
    parser.add_option("-p", "--port", help="specify httpd port")
    (options, args) = parser.parse_args()

    if options.routes:
        L = max( len(r._path) for r in routes ) # len of longest path
        fmt_ = "    %%-%ds => %%s" % L
        for r in routes:
            c = r.handler_class
            print fmt_ % (r._path, ".".join((c.__module__, c.__name__)))
        sys.exit(0)
    elif options.port:
        try: settings['port'] = int(options.port)
        except: pass
    elif args:
        try: settings['port'] = int(args[0])
        except: pass
    print "starting Tornado on port", settings['port']
    start_instance(settings, routes)
