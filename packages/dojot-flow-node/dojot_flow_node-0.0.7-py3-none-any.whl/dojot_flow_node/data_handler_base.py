# -*- coding: utf-8 -*-
import re


class DataHandlerBase:

    def get_node_representation_path(self):
        raise Exception('You have to implement the method get_node_representation_path!')
    
    def get_locale_data(self):
        raise Exception('You have to implement the method get_locale_data!')

    def get_metadata(self):
        raise Exception('You have to implement the method get_metadata!')

    def handle_message(self):
        raise Exception('You have to implement the method handle_message!')

    def _get(self, field, target):
        source = re.findall(r'([^.]+)', field)
        if len(source) == 0:
            at = field
        else:
            at = source.pop(0)
        data = target
        while at:
            if at not in data:
                raise Exception('Unknown property %s requested' % field)
            data = data[at]
            if len(source) == 0:
                at = None
            else:
                at = source.pop(0)
        return data


    def _set(self, field, value, target):
        source = re.findall(r'([^.]+)', field)
        if len(source) == 0:
            key = field
        else:
            key = source.pop(0)
        at = target
        while key:
            if len(source):
                if key not in at:
                    at[key] = {}
                at = at[key]
            else:
                at[key] = value
            if len(source) == 0:
                key = None
            else:
                key = source.pop(0)
