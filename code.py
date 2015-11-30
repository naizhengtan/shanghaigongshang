#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
from web import form
import search, sys
import os
import os.path
from subprocess import call

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

render = web.template.render('template/')
        
urls = (
    '/', 'index',
    '/log', 'log',
    '/result', 'result',
    '/download', 'download',
)
app = web.application(urls, globals())

info = form.Form(
        form.Textbox('keyword'),
        form.Textbox('start'),
        form.Textbox('end'),
)


class index:        
    def GET(self):
        f = info()
        return render.index(f) # index is the name of template
    def POST(self):
        f = info()
        f.validates()
        args = [f['start'].value, f['end'].value, f['keyword'].value]
        result = search.searchMain(args)
        # clear
        if os.path.isfile('run.log'):
          os.remove('run.log')
        # gen the tar ball
        call(['./tar-and-rm.sh'])
        return result

class log:        
    def GET(self):
        content = "No query"
        if os.path.isfile('run.log'):
            with open('run.log', 'r') as content_file:
                content = content_file.read()
        return content

class result:        
    def GET(self):
        web.header("Content-Type","text/csv;charset=utf-8") #content-type
        web.header("Content-Disposition","attachment;filename=doc.csv")
        with open('doc.csv', 'r') as content_file:
                content = content_file.read()
        return content

class download:
    def GET(self):
        web.header("Content-Type","text/csv;charset=utf-8") #content-type
        web.header("Content-Disposition","attachment;filename=docs.tar")
        with open('docs.tar', 'rb') as content_file:
                content = content_file.read()
        return content


if __name__ == "__main__":
    app.run()
