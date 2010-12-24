from datetime import datetime
from json import dumps as json_dumps
from os import mkdir
from shutil import move

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
        is_json = self.get_argument('json', False)
        if not human.verify(hum):
            self.write(json_dumps('fail'))
            return
        tmp_ = gen_key()
        dest_dir = '/data/sites/33ad.org/tmpdown/%s' % tmp_
        mkdir(dest_dir)
        parts = self.get_argument('upfile_name', 'uploaded.file').split('.')
        if len(parts) > 1:
            fname = slugify(''.join(parts[:-1])) + "." + slugify(parts[-1])
        else: fname = slugify(parts[0])
        move(self.get_argument('upfile_path'), '%s/%s' % (dest_dir, fname))

        fileuri = "http://33ad.org/tmp/%s/%s" % (tmp_, fname)

        if is_json:
            self.write(json_dumps({ 'uri': fileuri }))
        else:
            self.render(
                'tmp_done.html',
                fileuri = fileuri,
                )



