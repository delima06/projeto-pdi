# projeto pdi - avaliacao experimental das condicoes de aquisicao de imagens

este repositorio contem o codigo, dados, analises estatisticas e relatorio do projeto experimental de processamento digital de imagens (pdi) para avaliacao de cores de fundo de eva (azul, branco e verde).

## estrutura do projeto
- `dataset_original/`: imagens de alta resolucao adquiridas no experimento (`AZUL`, `BRANCA`, `VERDE`).
- `imagens_processadas/`: imagens apos correcao de orientacao, calibracao espacial e balanco de branco.
- `graficos_estatistica/`: graficos boxplot gerados para os testes de hipoteses e painel consolidado.
- `processamento.py`: script de leitura, orientacao, calibracao espacial e balanceamento de cores.
- `extrair_metricas.py`: script que calcula o ruido do eva, distorcao dimensional e fidelidade de cor cielab.
- `analise_estatistica.py`: script que executa shapiro-wilk, levene, anova one-way, kruskal-wallis e tukey hsd.
- `metricas_experimento.csv`: tabela com as metricas extraidas de todas as 33 imagens.
- `protocolo_experimental.md`: descricao completa do setup de aquisicao de imagens (natan).
- `relatorio_final.md`: relatorio cientifico integrado em formato academico (cleiton).
- `apresentacao_slides.md`: roteiro de apresentacao de 10 minutos (slides).
- `auditoria_projeto.md`: auditoria tecnica do estado do repositorio e entregas.

## como reproduzir

1. instalar as dependencias necessarias:
```bash
pip install opencv-python numpy scipy statsmodels pandas matplotlib seaborn
```

2. executar o processamento de imagens:
```bash
python processamento.py
```

3. extrair as metricas de qualidade:
```bash
python extrair_metricas.py
```

4. rodar a analise estatistica e gerar os graficos:
```bash
python analise_estatistica.py
```

## resultado principal
o fundo de **eva branco** apresentou menor nivel de ruido ($p = 4,49 \times 10^{-9}$) e maior relacao sinal-ruido ($p = 2,71 \times 10^{-13}$), sendo comprovado com significancia estatistica como a melhor cor de fundo para aquisicao.