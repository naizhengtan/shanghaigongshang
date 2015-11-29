#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
from web import form
import search, sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

render = web.template.render('template/')
        
urls = ( '/', 'index')
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
        return result

if __name__ == "__main__":
    app.run()
