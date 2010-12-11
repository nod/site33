
from markdown import Markdown
from viewlib import route, BaseHandler, async_yield

about_text = """
### 33ad actually comes from a year

Thirty Three A.D.  The common belief is that
Christ was 33 years old when he was crucified, and since we count years from
his (aproximated) birth, then 33AD would have been the year of his crucifiction
and resurrection.  Sooo, that's where 33ad.org comes from.

The interesting thing is that some scholars think that the monk that did the
whole counting on the year thing was actually about 3 years off.  So, that
would mean the death of Christ would have been about AD 30 instead.
However, [here's a link](http://www.xenos.org/essays/sejanus.htm) that gives
some really interesting arguments for why 33 CE seems the right year.

### So in a nut shell...

33ad.org is a loose conglomeration of websites run by a group of friends and
named after a year 2000 years ago.  It provides email addresses to the guys and
their spouses, but also serves as a central place to put up information for the
mass public and for sharing certain projects that they're working on.  """

@route(r'/about')
class AboutHandler(BaseHandler):
    def get(self):
        self.render(
            'about.html',
            about_text = Markdown(['codehilite']).convert(about_text),
            )

