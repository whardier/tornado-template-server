# -*- coding: UTF-8 -*-

from __future__ import print_function

import os
import sys

import pprint

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process
import tornado.options
import tornado.log
import tornado.escape

import tornado_data_uri.uimodules

from tornado.options import options
from tornado.options import define

## ┏━┓┏━┓╺┳╸╻┏━┓┏┓╻┏━┓
## ┃ ┃┣━┛ ┃ ┃┃ ┃┃┗┫┗━┓
## ┗━┛╹   ╹ ╹┗━┛╹ ╹┗━┛

def config_callback(path):
    options.parse_config_file(path, final=False)

define('config', type=str, help='Path to config file', callback=config_callback, group='Config file')

define('debug', default=False, help='Debug', type=bool, group='Application')

define('template_path', default='./templates/', help='Template Files Directory', type=str, group='Content')
define('static_path', default='./static/', help='Static Files Directory', type=str, group='Content')

define('listen_port', default=8000, help='Listen Port', type=int, group='HTTP Server')
define('listen_host', default='localhost', help='Listen Host', type=str, group='HTTP Server')

define('template_vars', default={'name': 'Tornado Template Server', 'brand': 'tornado-template-server'}, type=dict, group='Globals')

## ┏┓ ┏━┓┏━┓┏━╸╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
## ┣┻┓┣━┫┗━┓┣╸ ┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
## ┗━┛╹ ╹┗━┛┗━╸╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, *args, **kwargs):
        super(BaseHandler, self).initialize(*args, **kwargs)

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace.update({
            'template_vars': self.settings.get('template_vars'),
        })

        return namespace

## ┏━┓┏━┓┏━╸┏━╸┏━╸┏━┓┏━┓┏━┓┏━┓╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
## ┣━┛┣━┫┃╺┓┣╸ ┣╸ ┣┳┛┣┳┛┃ ┃┣┳┛┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
## ╹  ╹ ╹┗━┛┗━╸┗━╸╹┗╸╹┗╸┗━┛╹┗╸╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class PageErrorHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.send_error(self.kwargs['error'])

    def post(self, *args, **kwargs):
        self.send_error(self.kwargs['error'])

## ╺┳╸┏━╸┏┳┓┏━┓╻  ┏━┓╺┳╸┏━╸╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
##  ┃ ┣╸ ┃┃┃┣━┛┃  ┣━┫ ┃ ┣╸ ┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
##  ╹ ┗━╸╹ ╹╹  ┗━╸╹ ╹ ╹ ┗━╸╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class TemplateHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, path, *args, **kwargs):

        potential_paths = [
            os.path.join(self.get_template_path(), path + '.tpl'),
            os.path.join(self.get_template_path(), path),
            os.path.join(self.get_template_path(), path, 'index.html.tpl'),
            os.path.join(self.get_template_path(), path, 'index.html')
        ]

        for potential_path in potential_paths:
            if os.path.exists(potential_path) and os.path.isfile(potential_path):
                #Let this fail if needed
                self.render(potential_path)
                return

        self.send_error(404)

## ┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓
## ┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛
## ┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸

def main():

    tornado.options.parse_command_line()

    ## ┏━┓┏━╸╺┳╸╺┳╸╻┏┓╻┏━╸┏━┓
    ## ┗━┓┣╸  ┃  ┃ ┃┃┗┫┃╺┓┗━┓
    ## ┗━┛┗━╸ ╹  ╹ ╹╹ ╹┗━┛┗━┛

    static_path = 'static'
    template_path = 'templates'

    handlers = [
        ## Static File Serving
        tornado.web.url(r'/static/(css/.*)', tornado.web.StaticFileHandler, {'path': static_path}),
        tornado.web.url(r'/static/(ico/.*)', tornado.web.StaticFileHandler, {'path': static_path}),
        tornado.web.url(r'/static/(img/.*)', tornado.web.StaticFileHandler, {'path': static_path}),
        tornado.web.url(r'/static/(js/.*)', tornado.web.StaticFileHandler, {'path': static_path}),
        ## Main
        tornado.web.url(r'/(.*)$', TemplateHandler, name='template'),
    ]

    settings = dict(
        ui_modules = {'static_file_data_uri_base64': tornado_data_uri.uimodules.static_file_data_uri_base64},
        **options.as_dict()
    )

    tornado.log.gen_log.debug(pprint.pformat(settings))

    ## ┏━┓┏━┓┏━┓╻  ╻┏━╸┏━┓╺┳╸╻┏━┓┏┓╻
    ## ┣━┫┣━┛┣━┛┃  ┃┃  ┣━┫ ┃ ┃┃ ┃┃┗┫
    ## ╹ ╹╹  ╹  ┗━╸╹┗━╸╹ ╹ ╹ ╹┗━┛╹ ╹

    application = tornado.web.Application(handlers=handlers, **settings)

    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)

    http_server.listen(options.listen_port, address=options.listen_host)

    loop = tornado.ioloop.IOLoop.instance()

    try:
        loop_status = loop.start()
    except KeyboardInterrupt:
        loop_status = loop.stop()

    return loop_status

## ┏┳┓┏━┓╻┏┓╻
## ┃┃┃┣━┫┃┃┗┫
## ╹ ╹╹ ╹╹╹ ╹

def run():
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run()


