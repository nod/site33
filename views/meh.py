

import datetime
import json
import bloglib

newblog = bloglib.Blog('/tmp/blogdata0.sqlite3')
bdata = json.load(open('/Users/jeremy/Work/import33/blog.json'))

for k,p in bdata.iteritems():
  t = p['post_title'] or 'no-title'
  cat = datetime.datetime(*p['post_issue_date'][:4])
  newblog.new_post(title=t, content=p['post_content'], c_at=cat)

