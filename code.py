#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
from web import form
import search, sys
import os

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

render = web.template.render('template/')
        
urls = (
    '/', 'index',
    '/log', 'log',
    '/result', 'result',
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
        os.remove('run.log')
        return result

class log:        
    def GET(self):
        with open('run.log', 'r') as content_file:
                content = content_file.read()
        return content

class result:        
    def GET(self):
        with open('doc.csv', 'r') as content_file:
                content = content_file.read()
        return content

if __name__ == "__main__":
    app.run()
