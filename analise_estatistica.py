# script de analise estatistica das fotos do experimento
# feito por pedro davi (analista de estatistica)
# calcula a estatistica descritiva e testes das metricas de pdi
# gera os graficos boxplot e os histogramas de intensidade da aula 6

import os
import cv2
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# configura estilo simples para os graficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

def gerar_histogramas_fundos(pasta_origem='dataset_original', pasta_saida='graficos_estatistica'):
    # funcao que aplica o conteudo da aula 6 (transformacoes de intensidade e histogramas)
    # compara o histograma dos niveis de cinza do fundo de cada cor de eva
    os.makedirs(pasta_saida, exist_ok=True)
    
    exemplos = {
        'azul': os.path.join(pasta_origem, 'AZUL', '20260908_085924.jpg'),
        'branco': os.path.join(pasta_origem, 'BRANCA', '20260908_090813.jpg'),
        'verde': os.path.join(pasta_origem, 'VERDE', '20260908_090542.jpg')
    }
    
    cores_plot = {'azul': '#1f77b4', 'branco': '#7f7f7f', 'verde': '#2ca02c'}
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    for nome_cor, caminho in exemplos.items():
        if not os.path.exists(caminho):
            continue
            
        img = cv2.imread(caminho)
        h, w = img.shape[:2]
        if w > h:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            h, w = img.shape[:2]
            
        # extrai a regiao central homogenea do eva (aula 1 e 2)
        cy, cx = h // 2, w // 2
        roi = img[cy - 300 : cy + 300, cx - 300 : cx + 300]
        cinza = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # calcula o histograma de niveis de cinza usando cv2.calcHist da aula 6
        hist = cv2.calcHist([cinza], [0], None, [256], [0, 256])
        # normaliza para comparar a distribuicao
        hist = hist / hist.sum()
        
        # grafico de linha do histograma
        axes[0].plot(hist, label=f'eva {nome_cor}', color=cores_plot[nome_cor], linewidth=2)
        
        # densidade de frequencia
        axes[1].hist(cinza.ravel(), bins=60, alpha=0.5, label=f'eva {nome_cor}', color=cores_plot[nome_cor], density=True)
        
    axes[0].set_title('histograma de intensidade dos fundos (aula 6)')
    axes[0].set_xlabel('nivel de intensidade de cinza (0-255)')
    axes[0].set_ylabel('frequencia normalizada')
    axes[0].set_xlim([0, 255])
    axes[0].legend()
    
    axes[1].set_title('distribuicao de intensidade do sinal (aula 6)')
    axes[1].set_xlabel('nivel de cinza')
    axes[1].set_ylabel('densidade')
    axes[1].legend()
    
    plt.tight_layout()
    caminho_hist = os.path.join(pasta_saida, 'histogramas_intensidade_fundos.png')
    plt.savefig(caminho_hist, dpi=300)
    plt.close()
    print(f"grafico de histogramas da aula 6 salvo em: {caminho_hist}")

def executar_analise_estatistica(arquivo_csv='metricas_experimento.csv', pasta_graficos='graficos_estatistica'):
    os.makedirs(pasta_graficos, exist_ok=True)
    
    if not os.path.exists(arquivo_csv):
        print(f"erro: {arquivo_csv} nao encontrado rode extrair_metricas.py primeiro")
        return
        
    df = pd.read_csv(arquivo_csv)
    
    print("=================================================================")
    print("      relatorio de analise estatistica - projeto pdi             ")
    print("      aluno: pedro davi (analista de estatistica)                ")
    print("=================================================================\n")
    
    print(f"total de amostras: {len(df)}")
    print(f"contagem por cor de fundo:\n{df['cor_fundo'].value_counts()}\n")
    
    metricas = [
        ('ruido_std', 'ruido do fundo (desvio padrao sigma)', 'desvio padrao sigma'),
        ('snr_fundo', 'relacao sinal-ruido do fundo (snr)', 'snr (adimensional)'),
        ('erro_dimensional_relativo', 'erro dimensional relativo (%)', 'erro relativo (%)'),
        ('delta_e', 'fidelidade de cor do alvo (delta e cielab)', 'delta e')
    ]
    
    paleta = {'azul': '#4A90E2', 'branco': '#D8D8D8', 'verde': '#50E3C2'}
    
    # 1. loop para calcular estatisticas e gerar boxplots individuais
    for col, nome_completo, label_eixo in metricas:
        print("-----------------------------------------------------------------")
        print(f"metrica analisada: {nome_completo}")
        print("-----------------------------------------------------------------")
        
        # estatistica descritiva basica
        desc = df.groupby('cor_fundo')[col].agg(['count', 'mean', 'std', 'median'])
        desc.columns = ['n', 'media', 'desvio_padrao', 'mediana']
        print("\nestatistica descritiva:")
        print(desc.to_string())
        
        # teste anova one-way e kruskal-wallis
        grupos = [grupo[col].values for _, grupo in df.groupby('cor_fundo')]
        f_stat, p_anova = stats.f_oneway(*grupos)
        k_stat, p_kruskal = stats.kruskal(*grupos)
        
        print(f"\ntestes de significancia global:")
        print(f" - anova one-way: f = {f_stat:.4f}, p-valor = {p_anova:.4e}")
        print(f" - kruskal-wallis: h = {k_stat:.4f}, p-valor = {p_kruskal:.4e}")
        if p_anova < 0.05:
            print(" -> diferenca estatisticamente significativa (rejeita h0)")
        else:
            print(" -> sem diferenca estatistica (aceita h0)")
            
        # gera grafico boxplot
        fig, ax = plt.subplots(figsize=(6, 4.5))
        sns.boxplot(x='cor_fundo', y=col, data=df, hue='cor_fundo', palette=paleta, ax=ax, width=0.4, boxprops=dict(alpha=0.7), legend=False)
        sns.stripplot(x='cor_fundo', y=col, data=df, color='black', alpha=0.7, size=5, jitter=0.15, ax=ax)
        ax.set_title(nome_completo)
        ax.set_xlabel('cor do fundo (eva)')
        ax.set_ylabel(label_eixo)
        plt.tight_layout()
        caminho_fig = os.path.join(pasta_graficos, f"boxplot_{col}.png")
        plt.savefig(caminho_fig, dpi=300)
        plt.close()
        print(f"grafico salvo: {caminho_fig}\n")
        
    # 2. gera painel consolidado com as quatro metricas
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.ravel()
    
    for idx, (col, nome_completo, label_eixo) in enumerate(metricas):
        sns.boxplot(x='cor_fundo', y=col, data=df, hue='cor_fundo', palette=paleta, ax=axes[idx], width=0.4, boxprops=dict(alpha=0.7), legend=False)
        sns.stripplot(x='cor_fundo', y=col, data=df, color='black', alpha=0.6, size=4, jitter=0.15, ax=axes[idx])
        axes[idx].set_title(nome_completo, fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('cor do fundo (eva)')
        axes[idx].set_ylabel(label_eixo)
        
    plt.tight_layout()
    painel_caminho = os.path.join(pasta_graficos, 'painel_consolidado_metricas.png')
    plt.savefig(painel_caminho, dpi=300)
    plt.close()
    print(f"painel consolidado salvo: {painel_caminho}")
    
    # 3. gera o grafico de histogramas da aula 6
    gerar_histogramas_fundos(pasta_saida=pasta_graficos)
    print("\nanalise estatistica finalizada com sucesso!")

if __name__ == '__main__':
    executar_analise_estatistica()
