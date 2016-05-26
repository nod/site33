from datetime import datetime
from json import dumps as json_dumps
from os import mkdir
from shutil import move

import human_checks as human
from useful import gen_key, slugify
from viewlib import BaseHandler

from . import route


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
        randname = self.get_argument('random', False)
        hum = self.get_argument('human','')
        is_json = self.get_argument('json', False)
        if not human.verify(hum):
            return self.write('fail')
        tmp_ = gen_key()
        dest_dir = '{}/{}'.format(
            self.application.settings.get('tmpdown'),
            tmp_ )
        mkdir(dest_dir)
        fff = self.request.files['upfile'][0]
        fn = fff['filename']
        parts = (fn or 'up.file').split('.')
        if randname:
            fname = '{}.{}'.format(gen_key(), slugify(parts[-1]))
        else:
            if len(parts) > 1:
                fname = slugify(''.join(parts[:-1])) + "." + slugify(parts[-1])
            else: fname = slugify(parts[0])
        fh = open('{}/{}'.format(dest_dir, fname), 'wb')
        fh.write(fff['body'])
        fh.close()
        fileuri = "https://33ad.org/tmp/%s/%s" % (tmp_, fname)

        if is_json:
            self.write(json_dumps({ 'uri': fileuri }))
        else:
            self.render(
                'tmp_done.html',
                fileuri = fileuri,
                )



