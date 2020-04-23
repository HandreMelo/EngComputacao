import facerec6
import os.path
import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')
#
#    @cherrypy.expose
#    def enviarArquivo(self, ufile):
#        upload_path = os.path.dirname(__file__)
#        #resposta = facerec6.lerArquivo(ufile)
#        facerec6.lerArquivo(ufile)

    @cherrypy.expose
    def enviarArquivo(self, ufile, uname, *args, **post):
        upload_path = os.path.dirname(__file__)
        facerec6.lerArquivo(ufile,uname)
             
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