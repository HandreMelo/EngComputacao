import heapq
import ler_arquivo2

class Job:
    def __init__(self, start, finish, profit, path):
        self.start = start 
        self.finish = finish 
        self.profit = profit
        self.path = path

########## DIJKSTRA ###############

def dijkstra(graph, start, end):
    queue,seen = [(0, start, [])], set()
    while True:
        (cost, v, path) = heapq.heappop(queue)
        if v not in seen:
            path = path + [v]
            seen.add(v)
            if v == end:
                return cost, path
            for (next, c) in graph[v].items():
                heapq.heappush(queue, (cost + c, next, path))

##### MENORES CAMINHOS #####

def menores_caminhos(entregas,graph,job):
    inicio = list(graph.keys())[0];
    
    for destino in entregas: #O(e) * tudo abaixo
        try:
            tempo_ida, caminho_ida = dijkstra(graph,inicio, destino) #O((n+m)*logn)
            
            tempo_volta, caminho_volta = dijkstra(graph,destino, inicio)#O(idem)
            tempo_final = tempo_ida + tempo_volta#O(1)
            tempo_inicial = int(entregas[destino][0])#O(1)
            lucro_entrega = int(entregas[destino][1])#O(1)
            caminho = list([caminho_ida] + [caminho_volta])#O(1)
            job.append(Job(tempo_inicial, tempo_inicial + tempo_final, lucro_entrega, caminho))#O(algo)
        except:
            print("Não há caminho para a entrega : ",destino,"\n")
    return job

##### PREDECESSOR ###########

def Encontrar_Predecessor(job,start_index): #wis O(nlogn) ou O(n2)
    escolhido = 0
    for i in range(0, start_index-1):
        if ((job[i].finish <= job[start_index].start) and (job[i].profit >= job[escolhido].profit)):
            escolhido=i
    return escolhido

########## WIS ###############

def schedule(job): 

    job = merge_sort(job) #OK O(e log e)
    # for j in job: #O(e)
    #     print("Start :",j.start," Finish :",j.finish," Profit : ",j.profit)
    pre=0
    n = len(job)
    table_pre = [0 for _ in range(n)] #p(J)
    table_lucro = [0 for _ in range(n)] #v(J)
    table_max = [0 for _ in range(n)] #M[J]

    ### esse eh o wis ###
    for i in range(1,n): #O(e)
        table_lucro[i] = job[i].profit
        pre = Encontrar_Predecessor(job,i) #O(?)
        if pre != 0:    table_pre[i] = pre
        table_max[i] = max(table_lucro[i] + table_max[table_pre[i]], table_max[i - 1]) #O(1)

    # print("Table lucro,Tabela pre, Tabela Max :")
    # print(table_lucro)
    # print(table_pre)
    # print(table_max)
        
    #lucro_max,solution_list = Find_Solution(n-1,table_pre,table_lucro,table_max,job) #O(no slide)
    lucro_max=0
    lista_lucro = Find_Solution(n-1,table_pre,table_lucro,table_max,[])
    for indice in lista_lucro:
        lucro_max += int(job[indice].profit)

    return lucro_max,lista_lucro,job

#versão do prof. recursivo
########## FIND SOLUTION ###########

def Find_Solution(j,table_pre,table_lucro,table_max,lista_lucro): #O(n)
    if (j == 0):# or cont >= j):
        #print("fim")
        return lista_lucro
    elif ((table_lucro[j] + table_max[table_pre[j]]) > table_max[j-1]):
        #print(j)
        lista_lucro.append(j)
        return Find_Solution(table_pre[j],table_pre,table_lucro,table_max,lista_lucro)
    else: 
        return Find_Solution(j-1,table_pre,table_lucro,table_max,lista_lucro)

########## MERGE SORT ###############

def merge(llist, rlist):
        final = []
        while llist or rlist:
                # This verification is necessary for not try to compare
                # a NoneType with a valid type.
                if len(llist) and len(rlist):
                        if llist[0].finish < rlist[0].finish:
                                final.append(llist.pop(0))
                        else:
                                final.append(rlist.pop(0))
                if not len(llist):
                                if len(rlist): final.append(rlist.pop(0))

                if not len(rlist):
                                if len(llist): final.append(llist.pop(0))

        return final

def merge_sort(list):
        if len(list) < 2: return list
        mid = len(list) // 2
        return merge(merge_sort(list[:mid]), merge_sort(list[mid:]))

def main(file):
    graph,entregas = ler_arquivo2.ler_arquivo(file) #o(n2)
    print("Grafo\n", graph)
    print("Entregas\n", entregas,"\n")
    job = []
    job = menores_caminhos(entregas,graph,job) #O(e)*(2*(O((n+m)*logn))
    job.append(Job(0,0,0,[]))
    #(start, finish, profit, path)
    
    lucro_max, lucro_list, job = schedule(job)

    #print("Entregas realizadas : ", len(lucro_list))
    
    for indice in lucro_list:
        print("Para :", job[indice].path[0][-1], "Path : ", job[indice].path[0], "Com lucro = ", job[indice].profit)
        print("Tempo de inicio : ",job[indice].start, " e tempo final ", job[indice].finish)
    print("Totalizando : ", lucro_max," de lucro")

    return graph,entregas,job
    #print(Mod(graph).gr)

