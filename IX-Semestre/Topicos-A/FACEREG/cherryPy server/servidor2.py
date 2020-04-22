#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import lerArquivo
import os, os.path
import random
import string
import networkx as nx
import matplotlib.pyplot as plt
import cherrypy

grafo = {}
entregas = {}

def plotGraphGenerator():
    g = nx.Graph()
    g.add_edge('A','B',wight=5)
    g.add_edge('B','A',wight=5)
    g.add_edge('B','C',wight=5)
    g.add_edge('C','B',wight=5)

    pos = nx.spring_layout(g)
    nx.draw_networkx(g,pos,node_size=500)
    elarge = [(u,v) for (u,v,d) in g.edges(data=True) if d['wight'] >5]
    esmall = [(u,v) for (u,v,d) in g.edges(data=True) if d['wight'] <=5]
    nx.draw_networkx_edges(g,pos,edgelist=elarge,width=6)
    nx.draw_networkx_edges(g,pos,edgelist=esmall,width=6, alpha=0.5, edge_color='b', style='dashed')
    nx.draw_networkx_labels(g,pos, font_size=20,font_family='sans-serif')
    plt.axis('off')
    plt.show()

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
        grafoJson = json.dumps(entregas)
        plotGraphGenerator()
        return grafoJson

    @cherrypy.expose
    def alterarArquivo(self, another_string):
        cherrypy.session['mystring'] = another_string

    @cherrypy.expose
    def deletarArquivo(self):
        cherrypy.session.pop('mystring', None)


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