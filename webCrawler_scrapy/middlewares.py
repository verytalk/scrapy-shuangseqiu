# -*- coding: utf-8 -*-

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:1087"