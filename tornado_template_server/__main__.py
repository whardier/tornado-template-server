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

import magic
import mimetypes

import tornado_data_uri.uimodules

from tornado.options import options
from tornado.options import define

mimetypes.init()

## ┏━┓┏━┓╺┳╸╻┏━┓┏┓╻┏━┓
## ┃ ┃┣━┛ ┃ ┃┃ ┃┃┗┫┗━┓
## ┗━┛╹   ╹ ╹┗━┛╹ ╹┗━┛

def config_callback(path):
    options.parse_config_file(path, final=False)

define('config', type=str, help='Path to config file', callback=config_callback, group='Config file')

define('debug', default=False, help='Debug', type=bool, group='Application')

define('show_source_keyword', default=None, help='GET keyword to show original source', type=str, group='Service')

define('template_path', default='./templates/', help='Template Files Directory', type=str, group='Content')
define('static_path', default='./static/', help='Static Files Directory', type=str, group='Content')

define('listen_port', default=8000, help='Listen Port', type=int, group='HTTP Server')
define('listen_host', default='localhost', help='Listen Host', type=str, group='HTTP Server')

define('template_vars', default={'name': 'Tornado Template Server', 'brand': 'tornado-template-server'}, type=dict, group='Template')

## ┏┓ ┏━┓┏━┓┏━╸╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
## ┣┻┓┣━┫┗━┓┣╸ ┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
## ┗━┛╹ ╹┗━┛┗━╸╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, *args, **kwargs):
        super(BaseHandler, self).initialize(*args, **kwargs)

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace.update({
            'template_vars': self.settings['template_vars'],
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
            path + '.tpl',
            path,
            os.path.join(path, 'index.html.tpl'),
            os.path.join(path, 'index.html')
        ]

        for potential_path in potential_paths:
            full_path = os.path.join(self.get_template_path(), potential_path)

            if os.path.exists(full_path) and os.path.isfile(full_path):
                #Let this fail if needed
                if self.settings['show_source_keyword'] and self.settings['show_source_keyword'] in self.request.arguments:
                    self.set_header("Content-Type", "text/plain")
                    self.write(open(full_path).read())
                else:
                    #Test with magic first
                    mime_type = magic.from_file(full_path, mime=True)

                    #If any of the listed try to do a mimetypes lookup
                    if mime_type in ['text/plain',]:
                        _type, _encoding = mimetypes.guess_type(full_path, strict=True)
                        if _type:
                            mime_type = _type

                    self.set_header("Content-Type", mime_type)
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


