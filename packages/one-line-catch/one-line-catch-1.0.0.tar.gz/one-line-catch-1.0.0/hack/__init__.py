#!/usr/bin/env python
# coding=utf-8


class Olc(object):
    def __init__(self):
        pass

    def nonlocals(self):

        import inspect

        stack = inspect.stack()
        if len(stack) < 3:
            return {}
        f = stack[2][0]
        res = {}
        
        while f.f_back:
            res.update({k:v for k, v in f.f_locals.items() if k not in res})
            f = f.f_back

        return res

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, trackback):

        from ipdb import set_trace

        nonlocals = self.nonlocals()
        if exc_type: 
            set_trace()

        return true

