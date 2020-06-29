import facerec6
import os.path
import cherrypy
from cherrypy.lib import static
import webcam_cp as wc
import requisicao as req
#https://www.programcreek.com/python/example/401/base64.b64decode

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class facerecServer(object):
    @cherrypy.expose
    def index(self):
        return open('indexVue.html')

    @cherrypy.expose
    def cadastrar(self, ufile, uname, *args, **post):
        print(type(ufile.file), uname)
        upload_path = ufile.file
        resultado = facerec6.cadastrar(upload_path,uname)
        return resultado 

    @cherrypy.expose
    def procurar(self):
        resultado = wc.acesso()
        print(resultado)
        #if resultado != "404" and resultado != "Ninguem cadastrado":
           # req.acesso("liberar")
            
        return resultado
    
    @cherrypy.expose
    def bloquear(self):
        req.acesso("bloquear")
    
    @cherrypy.expose
    def liberar(self):
        req.acesso("liberar")
        
    @cherrypy.expose
    def deletar(self, uname):
        resultado = facerec6.deletar(uname)
        return resultado

    @cherrypy.expose
    def atualizar(self, ufile, uname, *args, **post):
        upload_path = ufile.file
        resultado = facerec6.atualizar(upload_path,uname)
        return '''<html><body><h1>Foto tualizada com sucesso</h1><button onclick="goBack()">VOLTAR</button>
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
            {'server.socket_host': 'localhost'}
        
    }

    cherrypy.quickstart(facerecServer(), '/', conf)