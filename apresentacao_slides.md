# roteiro de apresentacao do projeto pdi (slides / pitch - 10 minutos)
**equipe:** natan, thiago, pedro davi, cleiton

---

### slide 1: titulo e equipe (tempo: 1 min)
- **titulo:** avaliacao experimental das condicoes de aquisicao em pdi: comparacao estatistica de fundos de eva
- **autores:** natan (aquisicao), thiago (desenvolvimento), pedro davi (estatistica), cleiton (redacao e apresentacao)
- **contexto:** disciplina de processamento digital de imagens

### slide 2: motivacao e problema (tempo: 1.5 min)
- por que o cenario de aquisicao importa tanto? qualquer erro de iluminacao, reflexao ou cor de fundo impacta diretamente a segmentacao, medidas espaciais e cores.
- **desafio:** qual e a melhor cor de fundo de eva (azul, branco ou verde) para aquisicao de imagens com precisao dimensional e baixo ruido?

### slide 3: materiais e protocolo experimental - natan (tempo: 1.5 min)
- **cenario:** folhas de eva (azul claro, branco, verde claro), regua padrao e moeda de 1 real (diametro real = 27,0 mm).
- **captura controlada:** camera fixa a 45 cm perpendicular, iluminacao uniforme e 33 imagens no total (10 azul, 12 branco, 11 verde).
- garantia de reprodutibilidade conforme `protocolo_experimental.md`.

### slide 4: processamento digital de imagens - thiago (tempo: 2 min)
- **script desenvolvido:** `processamento.py`
- correcao automatica de orientacao.
- deteccao robusta de contorno da moeda via limiarizacao e ajuste de circulo minimo.
- calibracao espacial (relacao pixel por centimetro) e redimensionamento padrao.
- balanco de branco baseado no modelo gray-world no percentil 95.
- todas as 33 imagens salvas na pasta `imagens_processadas/`.

### slide 5: formulacao das metricas e testes estatisticos - pedro davi (tempo: 2 min)
- **metricas quantitativas:**
  1. ruido do fundo: desvio padrao ($\sigma$) em roi homogenea central de 600x600 px.
  2. relacao sinal-ruido (snr): media / sigma.
  3. distorcao espacial: erro dimensional relativo percentual contra o diametro nominal de 27 mm.
  4. fidelidade de cor: distancia euclidiana $\Delta E$ no espaco cielab no miolo da moeda.
- **metodologia estatistica:**
  - teste de normalidade (shapiro-wilk) e teste de homocedasticidade (levene).
  - analise de variancia anova one-way e kruskal-wallis ($\alpha = 0,05$).
  - pos-teste de tukey hsd para comparacoes pareadas.

### slide 6: resultados e comparacoes (tempo: 1 min)
- exibir o grafico consolidado: `graficos_estatistica/painel_consolidado_metricas.png`
- **ruido ($\sigma$):** branco = 2,563 vs azul = 3,340 vs verde = 4,105 ($p = 4,49 \times 10^{-9}$ - diferenca comprovada!).
- **snr:** branco = 64,63 vs azul = 47,03 vs verde = 37,09 ($p = 2,71 \times 10^{-13}$).
- **erro dimensional:** sem diferenca estatistica entre os fundos ($p = 0,1618$), todos com erro menor que 1,4% (algoritmo estavel).

### slide 7: conclusao e recomendacao final (tempo: 1 min)
- comprovacao por significancia estatistica: o **fundo de eva branco** e o vencedor.
- menor ruido, maior snr e excelente estabilidade geometrica.
- codigo aberto, documentado e reproduzivel no repositorio.
