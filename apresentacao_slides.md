# Roteiro da Apresentação Oral de Projeto (Pitch de 10 Minutos)

**Disciplina:** TAD0018 - Processamento Digital de Imagens (Turma 01 - 2026.2)  
**Instituição:** Escola Agrícola de Jundiaí (EAJ) — Universidade Federal do Rio Grande do Norte (UFRN)  
**Professor Responsável:** Prof. Dr. Antonino Feitosa  
**Equipe de Apresentadores:** Natan, Thiago, Pedro Davi e Cleiton  

---

### Slide 1: Título e Identificação da Equipe (Duração: 1 min)
- **Título do Projeto:** Avaliação Experimental das Condições de Aquisição em PDI: Comparação Estatística de Fundos em EVA Utilizando Fundamentos das Aulas 01 a 06.
- **Integrantes e Funções:**
  - **Natan:** Especialista em Aquisição e Protocolo Experimental.
  - **Thiago:** Desenvolvedor de Processamento Digital de Imagens.
  - **Pedro Davi:** Analista de Métricas e Modelagem Estatística.
  - **Cleiton:** Redator Técnico e Integrador de Documentação.
- **Contextualização:** Projeto aplicado da Unidade 1, fundamentado no livro-texto de Gonzalez & Woods (2009) e nas aulas teóricas e práticas do laboratório.

---

### Slide 2: Motivação Teórica e Problema de Engenharia (Duração: 1,5 min)
- **Por que a etapa de aquisição é crítica?** Erros no posicionamento físico, reflexão difusa inadequada do suporte ou iluminação não controlada propagam ruídos espúrios e degradam todas as etapas subsequentes do pipeline (segmentação, extração de características e mensuração dimensional).
- **Problema Central:** Qual cor de fundo de EVA (azul claro, branco ou verde claro) proporciona o menor nível de ruído de sensor, a maior relação sinal-ruído e a maior acurácia espacial para calibração geométrica de imagens?

---

### Slide 3: Protocolo Experimental e Aquisição Laboratorial — Natan (Duração: 1,5 min)
- **Cenário Experimental:** Bancada fixa em laboratório mantendo a câmera perpendicular (ortogonal a 90°) a uma distância controlada de 45 cm do plano de captura.
- **Padrões de Referência:** Folhas de EVA de $40 \times 60\text{ cm}$, moeda de 1 Real (diâmetro real nominal conhecido de $27,0\text{ mm}$) e régua milimetrada de $30\text{ cm}$.
- **Dataset Coletado:** 33 imagens digitais em alta resolução ($4000 \times 3000$ pixels) capturadas com sensor Samsung Galaxy S25 FE (10 fotos em fundo azul, 12 em branco e 11 em verde).
- **Garantia de Reprodutibilidade:** Protocolo detalhado disponível em `protocolo_experimental.md`.

---

### Slide 4: Método Computacional de Padronização — Thiago (Duração: 2 min)
- **Script Implementado:** `metodo_computacional.py` (desenvolvido estritamente com conceitos das Aulas 01 a 06).
- **Etapas do Processamento:**
  1. *Padronização de Orientação (Aula 02):* Detecção de imagens na horizontal e rotação automática de 90° com `cv2.rotate` para orientação vertical uniforme ($3000 \times 4000$).
  2. *Segmentação e Medição do Alvo (Aulas 02 e 04):* Binarização simples por limiar estático (`cv2.threshold` com $I < 85$) e contagem matricial de pixels para obter o diâmetro pela geometria circular ($D = 2\sqrt{A/\pi}$), dispensando contornos vetoriais avançados de outras unidades.
  3. *Calibração Espacial e Redimensionamento (Aula 04):* Aplicação de `cv2.resize` com interpolação bilinear (`cv2.INTER_LINEAR`, Slide 28) para fixar a escala em 70 pixels por centímetro.
  4. *Normalização Cromática com Gray World (Aula 05 - Slide 56):* Cálculo da média cinza neutra $\text{gray} = (\bar{R}+\bar{G}+\bar{B})/3$, multiplicação matricial e saturação no intervalo [0, 255] via `np.clip` (Aula 04 - Slide 30).
- **Resultado:** 100% das 33 imagens processadas com êxito na pasta `imagens_processadas/`.

---

### Slide 5: Métricas Quantitativas e Formulação Estatística — Pedro Davi (Duração: 2 min)
- **Métricas Fundamentadas nas Aulas:**
  1. *Ruído do Fundo ($\sigma$ - Aulas 01 e 02):* Desvio padrão amostral em uma ROI central homogênea de $600 \times 600$ pixels.
  2. *Relação Sinal-Ruído ($\text{SNR}$ - Aula 02):* Razão $\mu / \sigma$ indicando a pureza do sinal luminoso captado.
  3. *Erro Dimensional Relativo ($E_{\text{rel}}$ - Aula 04):* Desvio percentual entre o diâmetro medido em pixels reescalonados e os $27,0\text{ mm}$ reais.
  4. *Fidelidade Cromática ($\Delta E$ CIELAB - Aula 05 - Slide 59):* Distância euclidiana CIE76 medida no núcleo da moeda.
  5. *Perfil Espectral de Intensidade (Aula 06):* Histogramas de níveis de cinza extraídos via `cv2.calcHist`.
- **Modelagem Estatística:** Estatística descritiva e testes de análise de variância ANOVA One-Way ($\alpha = 0,05$).

---

### Slide 6: Resultados Experimentais e Discussão (Duração: 1 min)
- **Exibição dos Gráficos:** Painel integrado 2x2 (`painel_consolidado_metricas.png`) e perfil de histogramas (`histogramas_intensidade_fundos.png`).
- **Nível de Ruído ($\sigma$):** Branco ($2,563 \pm 0,132$) vs. Azul ($3,340 \pm 0,333$) vs. Verde ($4,105 \pm 0,637$) — Diferença altamente significativa ($p = 4,49 \times 10^{-9}$).
- **Relação Sinal-Ruído ($\text{SNR}$):** Fundo branco amplamente superior ($64,63 \pm 3,19$), superando o azul ($47,03$) e o verde ($37,09$) com $p = 2,71 \times 10^{-13}$.
- **Histogramas da Aula 06:** O fundo branco exibe distribuição compacta e deslocada para altas luzes, enquanto verde e azul espalham a distribuição devido à absorção seletiva da energia luminosa.
- **Acurácia Espacial:** Erro dimensional relativo abaixo de $0,85\%$ em todos os fundos, sem diferença estatística ($p = 0,8415$), validando a robustez da calibração métrica elementar.

---

### Slide 7: Conclusões e Recomendações — Cleiton (Duração: 1 min)
- **Veredito Experimental:** O **fundo em EVA branco** é categoricamente a melhor escolha para aquisição de imagens no arranjo laboratorial avaliado.
- **Justificativa Técnica:** Proporciona menor ruído de sensor, máxima pureza de sinal ($\text{SNR}$), excelente convergência para o balanço de cores Gray World e medição métrica com erro submétrico ($< 1\%$).
- **Cumprimento do Escopo:** Projeto 100% reproduzível, documentado e rigorosamente construído sobre as técnicas das Aulas 01 a 06 de PDI.
