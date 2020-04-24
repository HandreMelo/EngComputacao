import facerec6
import os.path
import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def cadastrar(self, ufile, uname, *args, **post):
        upload_path = os.path.dirname(__file__)
        return facerec6.cadastrar(ufile,uname)
    
    @cherrypy.expose
    def procurar(self, ufile, *args, **post):
        upload_path = os.path.dirname(__file__)
        return facerec6.procurar(ufile)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.quickstart(StringGenerator(), '/', conf)
