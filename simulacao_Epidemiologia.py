import random

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

TAMANHO_GRADE = 50
GERACOES = 100 #Dias de simulação

# Parâmetros da Doença
TAXA_TRANSMISSAO = 0.15      # 30% de chance de infectar vizinho
TEMPO_BASE_DOENCA = 20        # Dias que a doença dura sem ajuda
PROB_PERDA_IMUNIDADE = 0.01   # Chance de voltar a ser suscetível (1%)

# VARIÁVEL DE INTERVENÇÃO
# Quanto maior, mais rápido o infectado se cura.
# Ex: 0 = Cura em 10 dias. 5 = Cura em 5 dias.
FATOR_CAPACIDADE_HOSPITALAR = 2

cores = ['#4682B4', '#DC143C', "#9DF1B9"]
mapa_cores = mcolors.ListedColormap(cores)
limites = [0, 1, 2, 3]
norma = mcolors.BoundaryNorm(limites, mapa_cores.N)

class AutomatoEpidemia:
    def __init__(self, tamanho):
        self.grade = np.zeros((tamanho, tamanho), dtype=int)
        self.tempo_infectado = np.zeros((tamanho, tamanho), dtype=int)
        self.tamanho = tamanho

    def inicializador_grade(self):
        # Inicializa com 5% Infectados no início
        num_infectados = int(self.tamanho * self.tamanho * 0.05)
        inds = random.sample(range(self.tamanho * self.tamanho), num_infectados)
        for ind in inds:
            l, c = divmod(ind, self.tamanho)
            self.grade[l, c] = 1 

    def contar_vizinhos_infectados(self, l, c):
        count = 0
        # Vizinhança de Moore (8 vizinhos)
        for i in range(max(0, l-1), min(self.tamanho, l+2)):
            for j in range(max(0, c-1), min(self.tamanho, c+2)):
                if (i, j) != (l, c) and self.grade[i, j] == 1:
                    count += 1
        return count

    def atualizar(self):
        nova_grade = self.grade.copy()
        
        #Fator humano reduz o tempo de doença
        tempo_cura = max(1, TEMPO_BASE_DOENCA - FATOR_CAPACIDADE_HOSPITALAR)

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                estado = self.grade[i, j]

                # 0 = Suscetível -> Tenta virar 1 (Infectado)
                if estado == 0:
                    vizinhos = self.contar_vizinhos_infectados(i, j)
                    if vizinhos > 0:
                        prob = 1 - (1 - TAXA_TRANSMISSAO) ** vizinhos
                        if random.random() < prob:
                            nova_grade[i, j] = 1

                # 1 = Infectado -> Tenta virar 2 (Recuperado)
                elif estado == 1:
                    self.tempo_infectado[i, j] += 1
                    if self.tempo_infectado[i, j] >= tempo_cura:
                        nova_grade[i, j] = 2
                        self.tempo_infectado[i, j] = 0

                # 2 = Recuperado -> Tenta virar 0 (Perde Imunidade)
                elif estado == 2:
                    if random.random() < PROB_PERDA_IMUNIDADE:
                        nova_grade[i, j] = 0

        self.grade = nova_grade

    def executar_simulacao(self):
        fig, ax = plt.subplots()
        ax.set_title(f'Simulação Epidemia')
        ax.set_xticks([]); 
        ax.set_yticks([])
        
        img = ax.imshow(self.grade, cmap=mapa_cores, norm=norma, animated=True)

        # Legenda
        patches = [plt.Rectangle((0,0),1,1, fc=c) for c in cores]
        rotulos = ['Suscetível', 'Infectado', 'Recuperado']
        rotulos_variaveis = ['Fator Hospitalar:\n' + str(FATOR_CAPACIDADE_HOSPITALAR), 'Taxa Transmissão:\n' + str(int(TAXA_TRANSMISSAO*100)) + '%']
        legend_obj = ax.legend(patches, rotulos, loc='upper left', bbox_to_anchor=(1.01, 0.78), borderaxespad=0)
        
        # Adiciona variáveis como texto
        texto_variaveis = '\n'.join(rotulos_variaveis)
        ax.text(1.01, 0.99, texto_variaveis, transform=ax.transAxes, fontsize=10, verticalalignment='top')
        
        legend_texts = legend_obj.get_texts()
        
        leg_geracao = ax.text(1.01, 0.80, '', transform=ax.transAxes, fontsize=10, verticalalignment='bottom')
        
        hist_s, hist_i, hist_r = [], [], []

        def atualizar_plot(geracao):
            self.atualizar()
            img.set_array(self.grade)
            leg_geracao.set_text(f'Dia: {geracao+1}/{GERACOES}')
            
            # Atualiza textos da legenda
            tot = self.tamanho**2
            s = np.count_nonzero(self.grade == 0)
            i = np.count_nonzero(self.grade == 1)
            r = np.count_nonzero(self.grade == 2)
            
            legend_texts[0].set_text(f'Suscetível:\n{(s/tot)*100:.0f}%')
            legend_texts[1].set_text(f'Infectado:\n{(i/tot)*100:.0f}%')
            legend_texts[2].set_text(f'Recuperado:\n{(r/tot)*100:.0f}%')
            
            hist_s.append(s); hist_i.append(i); hist_r.append(r)

            # Plota o gráfico final na última geração
            if geracao + 1 == GERACOES:
                plt.figure() # Abre nova janela para o gráfico
                plt.plot(hist_s, label='Suscetível', c=cores[0])
                plt.plot(hist_i, label='Infectado', c=cores[1])
                plt.plot(hist_r, label='Recuperado', c=cores[2])
                plt.legend()
                plt.title("Curvas da Epidemia")
                plt.show()

            return img, leg_geracao, *legend_texts

        animacao = FuncAnimation(fig, atualizar_plot, frames=GERACOES, interval=100, repeat=False, blit=False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    sim = AutomatoEpidemia(TAMANHO_GRADE)
    sim.inicializador_grade()
    sim.executar_simulacao()