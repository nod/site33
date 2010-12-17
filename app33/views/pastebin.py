
from datetime import datetime
from tokyo import cabinet as tc

from useful import gen_key
from viewlib import route, BaseHandler

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from tornado.escape import xhtml_escape as html_escape


langlist = dict((
    ('', 'No highlight'),
    ('bash', 'Bash'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('html', 'HTML'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
    ('nasm', 'NASM'),
    ('objc', 'Objective-C'),
    ('php', 'PHP'),
    ('python', 'Python'),
    ('pycon', 'Python console session'),
    ('pytb', 'Python Traceback'),
    ('sql', 'SQL'),
    ('xml', 'XML'),
    ))

class TDBMixin(object):
    _dbpath = None

    def db(self, writable=False):
        assert( self._dbpath )
        if writable: flags = tc.TDBOWRITER|tc.TDBOCREAT
        else: flags = tc.TDBOCREAT
        db_ = tc.TDB()
        db_.open(self._dbpath, flags)
        return db_

    def dbsave(self, d, db=None):
        assert type(d) is dict
        if db: db_ = db
        else: db_ = self.db(writable=True)
        if 'key' not in d:
            d['key'] = gen_key()
        db_[d['key']] = d


class Paste(object):
    def __init__(self, text=None, key=None, hilite=None, created_at=None):
        self.text = text
        self.hilite = hilite
        self.key = key or gen_key()
        self.created_at = created_at or datetime.now()
        if type(self.created_at) is str:
            self.created_at = datetime.strptime(
                self.created_at,
                '%Y-%m-%dT%H:%M:%S.%f' )

    def display_text(self):
        if self.hilite:
            lexer = get_lexer_by_name(self.hilite, stripall=True)
            return highlight(
                self.text,
                lexer,
                HtmlFormatter(linenos='inline', cssclass='codehilite') )
        else: return '<pre>' + self.text.replace('<', '&lt;') + '</pre>'

    def to_d(self):
        d = self.__dict__.copy()
        d['created_at'] = self.created_at.isoformat()
        return d


@route('/pb/__all')
class AllHandler(BaseHandler, TDBMixin):

    def prepare(self):
        self._dbpath = '/tmp/pastebin.tokyo'

    def get(self):
        db_ = self.db()
        pastes = (Paste(**db_[p]) for p in db_)
        self.render('pastebin_all.html', pastes=pastes)


@route('/pb/?(?P<pbkey>[a-zA-Z0-9]*)')
class IndexHandler(BaseHandler, TDBMixin):

    def prepare(self):
        self._dbpath = '/tmp/pastebin.tokyo'

    def get(self, pbkey=None):
        paste = None
        if pbkey:
            db_ = self.db()
            if pbkey in db_:
                paste = Paste(**db_[pbkey])
        self.render('pastebin.html', paste=paste, langs=langlist)

    def post(self, pbkey=None):

        is_human = self.get_argument('human2','') and \
                    not self.get_argument('human1','')

        if not is_human:
            self.write('not human? back and try again bot type person')
            return

        text = self.get_argument('_paste', '')
        hilite = self.get_argument('hilite', '')

        if hilite and hilite not in langlist:
            self.write('bogus hilite. back atcha, try again.')
            return
        p = Paste(text=text, hilite=hilite)
        db_ = self.db(writable=True)
        self.dbsave(p.to_d(), db_)
        self.redirect('/pb/%s' % p.key)

        # let's go ahead and remove old ones now
        # q = db_.query()
        # q.sort('created_at', tc.TDBQOSTRASC)

