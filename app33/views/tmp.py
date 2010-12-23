from os import mkdir
from shutil import move
from datetime import datetime

from viewlib import route, BaseHandler
from useful import gen_key, slugify

import human_checks as human

@route('/tmp/?')
class TmpHandler(BaseHandler):

    def get(self):
        self.render(
            'tmp.html',
            human_tests = human.build_list(),
            )


@route('/tmp/up')
class TmpUpHandler(BaseHandler):
    def post(self):
        hum = self.get_argument('human','')
        if not human.verify(hum):
            self.write('fail')
            return
        tmp_ = gen_key()
        dest_dir = '/data/sites/33ad.org/tmpdown/%s' % tmp_
        mkdir(dest_dir)
        parts = self.get_argument('upfile_name', 'uploaded.file').split('.')
        fname = slugify(''.join(parts[:-1])) + "." + slugify(parts[-1])
        move(self.get_argument('upfile_path'), '%s/%s' % (dest_dir, fname))

        self.render('tmp_done.html',
            fileuri = "http://33ad.org/tmp/%s/%s" % (tmp_, fname),
            )



