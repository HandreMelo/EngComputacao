grafo = {}
entregas = {}

def ler_arquivo(arquivo):#O(n2)
    vetor_ler = []
    
    try:
        #arquivo_destino = open('entrada-trabalho - complexa.csv', 'r')
        arquivo_destino = open(arquivo, 'r')
        for linha in arquivo_destino: #O(n)
            vetor_ler.append(linha.strip())

        arquivo_destino.close()

        vetor_ler = limpar_formatacao_arquivo_lido(vetor_ler) #O(n)
        grafo, entregas = montar_grafo_do_arquivo(vetor_ler)
    
    except ValueError:
        print("valor numérico inválido")
    except IndexError:
        print("matriz do arquivo não está no tamanho correto")
    except FileNotFoundError:
        print("Não encontrado arquivo especificado")
        
    return grafo,entregas

def limpar_formatacao_arquivo_lido(vetor_ler):
    for i in range(len(vetor_ler)):
        vetor_ler[i] = vetor_ler[i].replace("'", "").replace("‘", "").replace("’", "") #O(1)
    return vetor_ler
    
def montar_grafo_do_arquivo(vetor_ler):
    
    n_vertices,n_entregas,pesos,vertices = separar_dados_do_arquivo_lido(vetor_ler) #O(n) + O(n2)
    
    adjacentes = {}
    pesos_temp = {}
    
    #print(pesos)
    #print(vertices)
    for i in range(n_vertices): #O(n2)
        for j in range(n_vertices):
            if int(pesos[i][j]) > 0:
                adjacentes[vertices[j]] = 0
                adjacentes[vertices[j]] += int(pesos[i][j])
                #pesos_temp.append(pesos[i][j])
        grafo[vertices[i]] = adjacentes
        adjacentes = {}
        pesos_temp = {}
    #print(grafo)
    return grafo,entregas

def separar_dados_do_arquivo_lido(vetor_ler): #O(n)
    pesos = []
    vertices = []
    ler_entregas = []

    n_vertices = int(vetor_ler[0])
    n_entregas = int(vetor_ler[n_vertices + 2])

    for i in range(2, n_vertices + 2):
        pesos.append(vetor_ler[i].split(','))

    for i in range(0, n_entregas):
        ler_entregas.append(vetor_ler[n_vertices + 3 + i].split(','))

    for i in range(n_entregas):
        entregas[ler_entregas[i][1]] = [ler_entregas[i][0], ler_entregas[i][2]]

    vertices.append(vetor_ler[1].split(','))
    vertices = vertices[0]

    return n_vertices,n_entregas,pesos,vertices
