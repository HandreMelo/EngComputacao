import facerec6
import os.path
import cherrypy
from cherrypy.lib import static
#https://www.programcreek.com/python/example/401/base64.b64decode

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class facerecServer(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def cadastrar(self, ufile, uname, *args, **post):
        upload_path = ufile.file
        return facerec6.cadastrar(upload_path,uname)

    @cherrypy.expose
    def procurar(self, ufile):
        upload_path = ufile.file#.read()
        return facerec6.procurar(upload_path)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': ''
        },
        'global': 
            {'server.socket_host': '0.0.0.0'} #IP do servirdor da máquina para acessar remotamente (na mesma rede local), 192.168.0.3 por exemplo
        
    }

    cherrypy.quickstart(facerecServer(), '/', conf)
