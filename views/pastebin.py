
from datetime import datetime

from databag import DataBag
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from tornado.escape import xhtml_escape as html_escape

from .useful import gen_key
from .viewlib import BaseHandler
from . import route

langlist = {
    ''        :'No highlight',
    'bash'    :'Bash',
    'c'       :'C',
    'cpp'     :'C++',
    'html'    :'HTML',
    'irc'     :'IRC',
    'java'    :'Java',
    'js'      :'JavaScript',
    'nasm'    :'NASM',
    'objc'    :'Objective-C',
    'php'     :'PHP',
    'python'  :'Python',
    'pycon'   :'Python console session',
    'pytb'    :'Python Traceback',
    'ruby'    :'Ruby',
    'sql'     :'SQL',
    'xml'     :'XML',
    }

class Paste(object):
    def __init__(self, text, hi=None, key=None, c_at=None):
        self.key = key or gen_key()
        self.text = text
        self.hi = hi
        self.c_at = c_at or datetime.now()

    def _d(self):
        return {'text': self.text, 'hi':self.hi, 'key':self.key}

    def display_text(self):
        if self.hi:
            lexer = get_lexer_by_name(self.hi, stripall=True)
            return highlight(
                self.text,
                lexer,
                HtmlFormatter(linenos='inline', cssclass='codehilite') )
        else: return '<pre>' + self.text.replace('<', '&lt;') + '</pre>'

@route('/pb/__all')
class AllHandler(BaseHandler):

    def prepare(self):
        self._bag = DataBag('DataBag', self.application.settings['dbpaste'])

    def get(self):
        pastes = (Paste(**d) for k,d in self._bag.by_created())
        self.render('pastebin_all.html', pastes=pastes)


@route('/pb/?(?P<pbkey>[a-zA-Z0-9]*)')
class PasteHandler(BaseHandler):

    def prepare(self):
        self._bag = DataBag('DataBag', self.application.settings['dbpaste'])

    def get(self, pbkey=None):
        if pbkey: paste = Paste(**self._bag[pbkey])
        else: paste = None
        if self.get_argument('raw', False):
            # self.content_type = 'text/plain'
            self.set_header("Content-Type", "text/plain")
            return self.write(paste.text)
        self.render('pastebin.html', paste=paste,  langs=langlist)

    def post(self, pbkey=None):

        is_human = self.get_argument('human2',None) and \
                    not self.get_argument('human1',None)

        if not is_human:
            self.write('not human? back and try again bot type person')
            return

        text = self.get_argument('_paste')
        hilite = self.get_argument('hilite', '')

        if hilite and hilite not in langlist:
            return self.write('bogus hilite. back atcha, try again.')
        p = Paste(text, hilite)
        self._bag[p.key] = p._d()
        self.redirect('/pb/%s' % p.key)

