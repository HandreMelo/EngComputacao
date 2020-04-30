import facerec6
import os.path
import cherrypy
import cherrypy_cors
import json

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def cadastrar(self, ufile, uname, *args, **post):
        datafile = json.loads(ufile)
        dataname = json.loads(uname)
        upload_path = os.path.dirname(datafile)
        return facerec6.cadastrar(datafile,dataname)
    
    @cherrypy.expose
    def procurar(self, ufile, *args, **post):
        upload_path = os.path.dirname(ufile)
        return facerec6.procurar(ufile)

if __name__ == '__main__':
    cherrypy_cors.install()
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        'global': {
            'server.socket_host': '192.168.1.105',
            'server.socket_port': 8080,
            'cors.expose.on': True
        }
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)
