
from viewlib import route, BaseHandler, async_yield

import index


@route('/yield')
class YieldExampleHandler(BaseHandler):
    """
    This is a simple example showing how to use the inline async call.
    """

    @async_yield
    def get(self):
        from tornado.httpclient import AsyncHTTPClient
        from tornado.escape import json_decode
        uri = "http://search.twitter.com/search.json?q=bcstx"
        yield AsyncHTTPClient().fetch(uri, self.yield_cb)
        if not self._yielded_args:
            self.render('fail.html')
            return
        tweets = json_decode(self._yielded_args[0].body)['results']
        self.render('yield_example.html', tweets=tweets)

# this needs to be the last line after all views are defined
routes = route.get_routes()
