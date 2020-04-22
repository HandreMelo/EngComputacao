import os, os.path
import random
import string

import cherrypy

grafo = {}
entregas = {}
class StringGenerator(object):


    @cherrypy.expose
    def index(self):
        return open('indexTest.html')

    @cherrypy.expose
    def mostrarArquivo(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def enviarArquivo(self, ufile):
        upload_path = os.path.dirname(__file__)

        grafo, entregas = lerArquivo.ler_arquivo(ufile)
        if entregas == "Error":
            out = '''
                    <!DOCTYPE html>
                    <html lang="en" xmlns:p="http://www.w3.org/1999/html">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <meta http-equiv="X-UA-Compatible" content="ie=edge">
                            <link rel="stylesheet" href="/static/css/grafo.css">
                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                            <title>RenderGraphus</title>
                        </head>
                        <body>
                            <div id="container">
                                <div class="container text-white">
                                    <div id="svg">
                                        <div class="label text-center" style="margin-left: 200px; margin-top: 300px;" >%s</div>
                                      </div>
                                      <div id="canvas">
                                        <div class="label text-center" style="margin-left: 300px; margin-top: 300px;" >%s</div>
                                    </div>          
                                </div>
                            </div>
                            <div class="offset-sm-3 col-sm-6 text-center rodape">
                                <form>
                                    <button id="alterar" class="btn btn-primary"><a href="/index">Voltar</a></button>
                                </form>
                            </div>
                        <body>
                    <html>
                        '''
            return out % (entregas, grafo )
        else:
            grafoJson = json.dumps(grafo)
            entregaJs = json.dumps(entregas)
            job = []
            job = graphLogic.menores_caminhos(entregas, grafo, job)
            job.append(graphLogic.Job(0, 0, 0, []))

            lucro_max, lucro_list, job = graphLogic.schedule(job)
            entrega_realizada = len(lucro_list)
            dic_lucros = {}
            i = 0
            for indice in lucro_list:
                dic_lucros[job[indice].path[0][-1]] = job[indice].path[0]
                i+=1
            dic_lucrosJs = json.dumps(dic_lucros)
            out = '''
            <!DOCTYPE html>
            <html lang="en" xmlns:p="http://www.w3.org/1999/html">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta http-equiv="X-UA-Compatible" content="ie=edge">
                    <link rel="stylesheet" href="/static/css/grafo.css">
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                    <title>RenderGraphus</title>
                </head>
                <body>
                    <div class="geral">
                      <div id="container">
                        <div class="container text-white">
                            <div id="svg">
                                <div class="label text-center" style="margin-left: 200px;" >Grafo entregas Feitas</div>
                              </div>
                              <div id="canvas">
                                <div class="label text-center" style="margin-left: 300px;" >Grafo</div>
                            </div>          
                        </div>
                      </div>
                      <div class="offset-sm-3 col-sm-6 text-center rodape">
                          <form>
                              <button id="alterar" class="btn btn-primary"><a href="/index">Voltar</a></button>
                          </form>
                      </div>
                      
                    </div>
                    <div>
                        <p>Grafo Montado:</p>
                        <p id="grafo">%s</p>
                        <p id="entregas">Entregas:</p>
                        <p>%s</p> 
                        <p>Entregas realizadas: %s</p>
                        <p>Lucro maximo: %s</p>
                        <p>Caminho das entregas feitas: </p>
                        <p id="caminho_entregado">%s</p>
                    </div>
                    <script src="/static/js/jquery.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/sigma.core.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/conrad.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/utils/sigma.utils.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/utils/sigma.polyfills.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/sigma.settings.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/classes/sigma.classes.dispatcher.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/classes/sigma.classes.configurable.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/classes/sigma.classes.graph.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/classes/sigma.classes.camera.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/classes/sigma.classes.quad.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/classes/sigma.classes.edgequad.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/captors/sigma.captors.mouse.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/captors/sigma.captors.touch.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/sigma.renderers.canvas.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/sigma.renderers.webgl.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/sigma.renderers.svg.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/sigma.renderers.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/webgl/sigma.webgl.nodes.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/webgl/sigma.webgl.nodes.fast.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/webgl/sigma.webgl.edges.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/webgl/sigma.webgl.edges.fast.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/webgl/sigma.webgl.edges.arrow.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.labels.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.hovers.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.nodes.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edges.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edges.curve.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edges.arrow.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edges.curvedArrow.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edgehovers.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edgehovers.curve.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edgehovers.arrow.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.edgehovers.curvedArrow.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/canvas/sigma.canvas.extremities.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/svg/sigma.svg.utils.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/svg/sigma.svg.nodes.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/svg/sigma.svg.edges.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/svg/sigma.svg.edges.curve.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/svg/sigma.svg.labels.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/renderers/svg/sigma.svg.hovers.def.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/middlewares/sigma.middlewares.rescale.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/middlewares/sigma.middlewares.copy.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/misc/sigma.misc.animation.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/misc/sigma.misc.bindEvents.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/misc/sigma.misc.bindDOMEvents.js"></script>
                    <script src="/static/sigma.js-1.2.1/src/misc/sigma.misc.drawHovers.js"></script>
                    <script type="text/javascript" src="/static/js/grafo.js"></script>
                    <script type="text/javascript" src="/static/js/grafoTwo.js"></script>
                </body>
            </html>
            '''
            grafo.clear()
            entregas.clear()
            return out % (str(grafoJson), str(entregaJs), str(entrega_realizada), str(lucro_max), str(dic_lucrosJs))

    @cherrypy.expose
    def alterarArquivo(self, another_string):
        cherrypy.session['mystring'] = another_string

    @cherrypy.expose
    def deletarArquivo(self):
        cherrypy.session.pop('mystring', None)


if __name__ == '__main__':

    import json
    import networkx as nx
    import lerArquivo
    import graphLogic
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.caching.on': False
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.quickstart(StringGenerator(), '/', conf)