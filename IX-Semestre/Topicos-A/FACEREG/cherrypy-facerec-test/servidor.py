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
        return open('index-crud.html')

    @cherrypy.expose
    def cadastrar(self, ufile, uname, *args, **post):
        upload_path = ufile.file
        resultado = facerec6.cadastrar(upload_path,uname)
        return '''<html><body><img src="/static/smile.jpg"><h1>'''+resultado+'''</h1><button onclick="goBack()">VOLTAR</button>
        <script>function goBack() {
  window.history.back();
}</script></body></html>'''

    @cherrypy.expose
    def procurar(self, ufile):
        upload_path = ufile.file
        resultado = facerec6.procurar(upload_path)
        return '''<html><body><img src="/static/smile.jpg"><h1>Resultado : '''+resultado+'''</h1><button onclick="goBack()">VOLTAR</button>
        <script>function goBack() {
  window.history.back();
}</script></body></html>'''

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        'global': 
            {'server.socket_host': '192.168.1.X'}
        
    }

    cherrypy.quickstart(facerecServer(), '/', conf)
