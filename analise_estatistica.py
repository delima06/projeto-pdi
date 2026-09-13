# script de analise estatistica completa para o projeto pdi
# feito por pedro davi (analista de estatistica)
# calcula testes de normalidade, homogeneidade, anova, kruskal-wallis, tukey hsd e gera graficos

import os
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns

# configurar estilo basico dos graficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'Arial', 'font.size': 11})

def executar_analise_estatistica(arquivo_csv='metricas_experimento.csv', pasta_graficos='graficos_estatistica'):
    os.makedirs(pasta_graficos, exist_ok=True)
    
    if not os.path.exists(arquivo_csv):
        print(f"erro: arquivo {arquivo_csv} nao encontrado. rode extrair_metricas.py primeiro.")
        return
        
    df = pd.read_csv(arquivo_csv)
    
    print("=================================================================")
    print("        RELATORIO DE ANALISE ESTATISTICA - PROJETO PDI           ")
    print("        Responsavel: Pedro Davi (Analista de Estatistica)        ")
    print("=================================================================\n")
    
    print(f"Total de amostras analisadas: {len(df)}")
    print(f"Distribuicao por cor de fundo:\n{df['cor_fundo'].value_counts()}\n")
    
    metricas = [
        ('ruido_std', 'Ruido do Fundo (Desvio Padrao da Intensidade)', 'Nivel de Ruido (sigma)'),
        ('snr_fundo', 'Relacao Sinal-Ruido do Fundo (SNR)', 'SNR (adimensional)'),
        ('erro_dimensional_relativo', 'Erro Dimensional Relativo (%)', 'Erro Relativo (%)'),
        ('delta_e', 'Fidelidade de Cor do Alvo (Delta E CIELAB)', 'Delta E')
    ]
    
    resultados_resumo = []
    
    for col, nome_completo, label_eixo in metricas:
        print("-----------------------------------------------------------------")
        print(f" ANALISE METRICA: {nome_completo}")
        print("-----------------------------------------------------------------")
        
        # 1. estatistica descritiva
        desc = df.groupby('cor_fundo')[col].agg(['count', 'mean', 'std', 'median', lambda x: stats.iqr(x)])
        desc.columns = ['N', 'Media', 'Desvio_Padrao', 'Mediana', 'IQR']
        print("\nEstatistica Descritiva por Fundo:")
        print(desc.to_string())
        
        # 2. teste de normalidade (shapiro-wilk)
        print("\nTeste de Normalidade de Shapiro-Wilk (alpha = 0.05):")
        normalidades = {}
        todos_normais = True
        for cor, grupo in df.groupby('cor_fundo'):
            stat_w, p_w = stats.shapiro(grupo[col])
            eh_normal = p_w > 0.05
            normalidades[cor] = eh_normal
            if not eh_normal:
                todos_normais = False
            print(f" - {cor.capitalize():<8}: W = {stat_w:.4f}, p-valor = {p_w:.4f} -> {'Normal' if eh_normal else 'Nao-Normal'}")
            
        # 3. teste de homogeneidade de variancias (levene)
        grupos_dados = [grupo[col].values for _, grupo in df.groupby('cor_fundo')]
        stat_l, p_l = stats.levene(*grupos_dados)
        homocedastico = p_l > 0.05
        print(f"\nTeste de Homogeneidade de Variancias (Levene):")
        print(f" - Estatistica = {stat_l:.4f}, p-valor = {p_l:.4f} -> {'Homocedastico' if homocedastico else 'Heterocedastico'}")
        
        # 4. teste de diferenca entre grupos (anova one-way e kruskal-wallis)
        stat_f, p_f = stats.f_oneway(*grupos_dados)
        stat_k, p_k = stats.kruskal(*grupos_dados)
        
        print("\nTestes de Significancia Global:")
        print(f" - ANOVA One-Way (parametrico):    F = {stat_f:.4f}, p-valor = {p_f:.4e} -> {'Significativo (rejeita H0)' if p_f < 0.05 else 'Nao significativo'}")
        print(f" - Kruskal-Wallis (nao-parametrico): H = {stat_k:.4f}, p-valor = {p_k:.4e} -> {'Significativo (rejeita H0)' if p_k < 0.05 else 'Nao significativo'}")
        
        # 5. pos-teste de tukey hsd
        print("\nPos-teste de Comparacoes Multiplas (Tukey HSD - alpha = 0.05):")
        tukey = pairwise_tukeyhsd(endog=df[col], groups=df['cor_fundo'], alpha=0.05)
        print(tukey)
        
        # armazenar dados para sintese
        melhor_fundo = desc['Media'].idxmin() if 'erro' in col or 'ruido' in col or 'delta' in col else desc['Media'].idxmax()
        resultados_resumo.append({
            'Metrica': col,
            'p_valor_ANOVA': p_f,
            'p_valor_Kruskal': p_k,
            'Melhor_Fundo': melhor_fundo,
            'H0_Rejeitada': p_f < 0.05 or p_k < 0.05
        })
        
        # 6. gerar graficos (boxplot + swarmplot)
        fig, ax = plt.subplots(figsize=(7, 5))
        paleta = {'azul': '#4A90E2', 'branco': '#D8D8D8', 'verde': '#50E3C2'}
        
        sns.boxplot(x='cor_fundo', y=col, data=df, palette=paleta, ax=ax, width=0.4, boxprops=dict(alpha=0.7))
        sns.stripplot(x='cor_fundo', y=col, data=df, color='black', alpha=0.6, jitter=0.2, size=6, ax=ax)
        
        ax.set_title(f"{nome_completo}\nComparacao entre Cores de EVA", fontsize=12, fontweight='bold')
        ax.set_xlabel("Cor do Fundo EVA", fontsize=11)
        ax.set_ylabel(label_eixo, fontsize=11)
        
        nome_arquivo_fig = os.path.join(pasta_graficos, f"boxplot_{col}.png")
        plt.tight_layout()
        plt.savefig(nome_arquivo_fig, dpi=300)
        plt.close()
        print(f"Grafico salvo: {nome_arquivo_fig}\n")
        
    # gerar grafico consolidado comparativo com 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    paleta = {'azul': '#4A90E2', 'branco': '#D8D8D8', 'verde': '#50E3C2'}
    
    for i, (col, nome_completo, label_eixo) in enumerate(metricas):
        sns.boxplot(x='cor_fundo', y=col, data=df, palette=paleta, ax=axes[i], width=0.4, boxprops=dict(alpha=0.7))
        sns.stripplot(x='cor_fundo', y=col, data=df, color='black', alpha=0.5, jitter=0.2, size=5, ax=axes[i])
        axes[i].set_title(nome_completo, fontsize=11, fontweight='bold')
        axes[i].set_xlabel("Fundo EVA", fontsize=10)
        axes[i].set_ylabel(label_eixo, fontsize=10)
        
    plt.tight_layout()
    consolidado_path = os.path.join(pasta_graficos, "painel_consolidado_metricas.png")
    plt.savefig(consolidado_path, dpi=300)
    plt.close()
    print(f"Painel consolidado salvo em: {consolidado_path}")
    
    print("\n=================================================================")
    print("                 CONCLUSAO ESTRUTURADA (PEDRO)                  ")
    print("=================================================================")
    df_resumo = pd.DataFrame(resultados_resumo)
    print(df_resumo.to_string(index=False))
    print("\nAnalise estatistica finalizada com exito!")

if __name__ == '__main__':
    executar_analise_estatistica()
