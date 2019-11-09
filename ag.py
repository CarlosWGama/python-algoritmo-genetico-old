from enum import Enum
import random

class MetodoSelecao(Enum):
    Roleta = 1,
    Classificacao = 2,
    Aleatorio = 3

class AlgoritmoGenetico:

    def __init__(self, conteudos, tamanhoPopulacao, funcaoFitness):
        """Inicia o Algoritmo Genético

        Parameters:
            conteudos (array): Conteúdo com os dados dos elementos que devem compor os cromossomos
            tamanhoPopulacao (int): Quantos cromossomos serão gerados
            funcaoFitness (funcao): Função que irá calcular a importancia do cromosso
        """
        self._conteudos = conteudos
        self._tamanhoPopulacao = tamanhoPopulacao
        self._funcaoFitness = funcaoFitness
        self._tamanhoCromossomo = len(conteudos)
        self._geracao = 0
        self._populacao = []

    @property
    def geracao(self):
        return self._geracao

    def iniciaPopulacao(self):
        """ Inicia a primeira população """
        #Cria N cromossos na população
        for i in range(self._tamanhoPopulacao):
            cromossomo = {
                'fitness': 0,
                'genes': []
            }
            for x in range(len(self._conteudos)):
                cromossomo['genes'].append(random.randint(0, 1))
            
            #Adiciona o cromossomo a população
            self._populacao.append(cromossomo)

    def exibePopulacao(self):
        """ Exibe a população gerada """
        for cromossomo in self._populacao:
            print(cromossomo)

    def melhorResultado(self):
        return self._populacao[0]

    def calculaFitness(self):
        """ Calcula o Fitness de cada cromossomo da população """
        #Calcula o fitness de cada cromossomo
        for cromossomo in self._populacao:
            cromossomo['fitness'] = self._funcaoFitness(self._conteudos, cromossomo['genes'])
            
        #Ordena pelo fitness
        self._populacao = sorted(self._populacao, key=lambda c: c['fitness'], reverse=True)

    def reproducao(self, metodo):
        """ Realiza o Processo de Reprodução """
        #Quantos novos filhos precisará criar (igual ao tamanho da população)
        for x in range(self._tamanhoPopulacao):
            cromossoPai1 = None
            cromossoPai2 = None
            if (metodo == MetodoSelecao.Roleta):
                cromossoPai1 = self.selecaoRoleta()
                cromossoPai2 = self.selecaoRoleta()
            elif (metodo == MetodoSelecao.Aleatorio):
                cromossoPai1 = self.selecaoAleatoria()
                cromossoPai2 = self.selecaoAleatoria()
            else:
                cromossoPai1 = self.selecaoClassificacao()
                cromossoPai2 = self.selecaoClassificacao()

            #Seleciona uma posiçaõ de corte entre o 2 e penultimo número
            posicaoCorte = random.randint(1, self._tamanhoCromossomo-1)

            filho = {
                'fitness':0,
                'genes':[]
            }
            #Recupera os genes do PAI1
            for i in range(0, posicaoCorte):
                filho['genes'].append(cromossoPai1['genes'][i])
            #Recupera os genes do PAI2
            for i in range(posicaoCorte, self._tamanhoCromossomo):
                filho['genes'].append(cromossoPai2['genes'][i])
            filho = self.mutacao(filho)
            self._populacao.append(filho)
        
        #Recalcula o Fitness com os filhos
        self.calculaFitness()

    def mutacao(self, cromossomo):
        """ Ocorrerá uma mutação com de 5% de chance """
        numeroSorteado = random.randrange(0, 100)
        # Caso o número sorteado seja até, ocorre uma mutação
        if (numeroSorteado <= 5):
        
            geneAleatorio = random.randint(0, self._tamanhoCromossomo-1)
            cromossomo['genes'][geneAleatorio] = 1 if (cromossomo['genes'][geneAleatorio] == 0) else 0
            print("Sofreu mutação")
            print(cromossomo)
        return cromossomo

    def selecionaNovaPopulacao(self):
        self._populacao = self._populacao[0:(self._tamanhoPopulacao-1)]
        self._geracao+=1


    def selecaoRoleta(self):
        # Avalia o total de fitness
        total = sum(c['fitness'] for c in self._populacao)
        
        #Identifica a porcentagem de cada um
        porcentagens = []
        atual = 0
        for c in self._populacao:
            porcentagem = (c['fitness'] * 100)/total
            atual += porcentagem
            porcentagens.append(atual)
        
        #Seleciona de forma aleatória um valor entre 0 e 100 (É a porcentagem escolhida)
        escolhaAleatoria = random.randint(0, 100)
        indexSelecionado = 0
        for x in range(0, self._tamanhoPopulacao):
            indexSelecionado = x
            if escolhaAleatoria <= porcentagens[x]:
                break

        return self._populacao[indexSelecionado]
    
    def selecaoClassificacao(self):
        #Monta a roleta de classificação
        atual = 0
        classificacoes = []
        for x in range(1, self._tamanhoPopulacao):
            atual += x
            classificacoes.append(atual)

        #Seleciona de forma aleatória um valor entre 0 e 100 (É a porcentagem escolhida)
        escolhaAleatoria = random.randint(1, atual)
        indexSelecionado = 0
        for x in range(0, self._tamanhoPopulacao):
            indexSelecionado = x
            if escolhaAleatoria <= classificacoes[x]:
                break
        return self._populacao[indexSelecionado]


    def selecaoAleatoria(self):
        """ Retorna um Cromossomo aleatório """
        return self._populacao[random.randint(0, self._tamanhoPopulacao-1)]
   
