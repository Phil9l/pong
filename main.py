#!/usr/bin/env python

# import time
# from game.models import Field
#
# if __name__ == '__main__':
#     field = Field(800, 800)
#
#     while True:
#         print(field._ball._body.position)
#
#         time.sleep(1)

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.concurrent
import tornado.gen
import json
import logging
from game.models import Field


field = None


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        logging.info('New connection.')

    def on_message(self, message):
        response = {'position': field._ball._body.position.int_tuple}
        self.write_message(json.dumps(response))

    def on_close(self):
        logging.info('Connection was closed.')


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


@tornado.gen.engine
def refresh():
    # print('Sleeping...')
    yield tornado.gen.sleep(0.1)
    field.update(0.1)
    tornado.ioloop.IOLoop.instance().add_callback(refresh)


def make_app():
    return tornado.web.Application([
        (r'/', IndexPageHandler),
        (r'/websocket', WebSocketHandler)
    ], template_path='templates', autoreload=True, debug=True)


if __name__ == "__main__":
    field = Field(800, 800)

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().add_callback(refresh)
    tornado.ioloop.IOLoop.current().start()
