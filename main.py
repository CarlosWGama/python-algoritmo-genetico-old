from ag import *


# [Nome, Peso, Valor]
conteudos = [
    {'conteudo':'Lapis', 'peso':2, 'valor':3.5},
    {'conteudo':'Caderno', 'peso':6, 'valor':3.5},
    {'conteudo':'Borracha', 'peso':1, 'valor':3.5},
    {'conteudo':'Carro', 'peso':14, 'valor':3.5},
    {'conteudo':'Livro', 'peso':3, 'valor':6},
    {'conteudo':'Chinelo', 'peso':4, 'valor':4},
]

#Função que irá calcular o Fitness
def funcaoFitness(conteudo, genes):
    fitness = 0 
    pesoAcumulado = 0
    for x in range(len(genes)):
        if (genes[x] == 1):
            fitness += conteudo[x]['valor'] #Valor da bolsa
            pesoAcumulado += conteudo[x]['peso'] #Peso Acumulado

        if (pesoAcumulado > 20):
            fitness = 0
    return fitness


ag = AlgoritmoGenetico(conteudos, 10, funcaoFitness)
ag.iniciaPopulacao()
ag.exibePopulacao()
print("Calcula Fitness")
ag.calculaFitness()
ag.exibePopulacao()

for x in range(2, 10):
    print(x)


for geracao in range(100):
    print(geracao)
    #print("REPRODUÇÃO")
    ag.reproducao(MetodoSelecao.Roleta)

    #print("Corte")
    ag.selecionaNovaPopulacao()
    ag.exibePopulacao()
    

