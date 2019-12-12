from pyeasyga import pyeasyga
import grafo6 as g6
import time
# a lista de entregas tem de estar ordenadas do maior para o menor pelo tempo final
# setup data
#'entrada-trabalho - complexa.csv'
#'entrada-trabalho - complexa - entrada 2.csv'
#'grafo.txt'
first=time.time()
file ='entrada-trabalho - complexa - entrada 2.csv'
grafo, entregas, job = g6.main(file)
data=[]
tp=()

job = sorted(job, key = lambda j: j.finish)
job.reverse()

for i in range(0, len(job)-1):
    inicio = int(job[i].start)
    final = int(job[i].finish)
    lucro = int(job[i].profit)
    tp += (inicio,final,lucro)
    data.append(tp)
    tp = ()

ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data

# define a fitness function
def fitness(individual, data):
    saida, final, lucro = 0, 0, 0
    saida_anterior = 99999
    lucro_total = 0
    nao_deu=0

    for (selected, item) in zip(individual, data):
        if selected:
            saida = item[0]
            final = item[1]
            lucro_total += item[2]
            if final > saida_anterior:
                nao_deu = 1
            saida_anterior = saida
    if nao_deu: lucro_total = 0
    return lucro_total

print("\n============== ALGORITMO GENÉTICO ==============\n")
print("Numero de geraçoes : 500")
print("Tamanho populacional : 15")
print("Lista de entregas : ",data)
ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
lista_GA = ga.best_individual()
lucro,cromossomos = lista_GA
#print("Lucro e cromossomo pelo GA : ", lista_GA) # print the GA's best solution
#print("Lucro e cromossomo pelo GA : ", lista_GA)
print("Lucro : ", lucro)
print("Cromossomos : ", cromossomos)
print("Caminho : ", end ='')
for (selected, item) in zip(cromossomos, data):
    if selected:
        print(item, end = "<--")