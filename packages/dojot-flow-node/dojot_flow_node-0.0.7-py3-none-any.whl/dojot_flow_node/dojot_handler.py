# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import traceback

import zmq
import zmq.asyncio
from zmq.asyncio import Context


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class DojotHandler:
    def __init__(self, data_handler):
        self.ctx = Context.instance()
        self.port = 5555
        self.handler = data_handler
        asyncio.get_event_loop().run_until_complete(asyncio.wait([
            self.router()
        ]))

    async def router(self):
        socket = self.ctx.socket(zmq.REP)
        socket.bind('tcp://*:' + str(self.port))
        print('zmq listening on %s' % str(self.port))

        try:
            # keep listening to all published message on topic 'world'
            while True:
                packet = await socket.recv()
                # parse packet
                try:
                    request = json.loads(packet.decode('utf-8'))
                except Exception as e:
                    print('Invalid JSON format. Discarding request: %s. Error:', str(packet), e)
                    continue

                try:
                    response = self.handle_request(request)
                    socket.send(json.dumps(response).encode('utf8'))
                except Exception as e:
                    socket.send(json.dumps({'error': str(e)}).encode('utf8'))

        except Exception as e:
            print('Error with sub world')
            logging.error(traceback.format_exc())
            print()

        finally:
            # TODO disconnect dealer/router
            pass

    def handle_request(self, request):
        if request['command'] == 'locale':
            return self.handle_locale(request)
        elif request['command'] == 'metadata':
            return self.handle_metadata()
        elif request['command'] == 'message':
            return self.handle_message(request)
        elif request['command'] == 'html':
            return self.handle_html()
        else:
            raise Exception('Unknown command')

    def handle_html(self):
        path = self.handler.get_node_representation_path()
        with open(path, encoding='utf-8') as f:
            return {'payload': f.read()}

    def handle_metadata(self):
        return {'payload': self.handler.get_metadata()}

    def handle_locale(self, data):
        data_locale = self.handler.get_locale_data(data['locale'])
        return {'payload': data_locale}

    def handle_message(self, data):
        return self.handler.handle_message(data['config'], data['message'], data['metadata'])
