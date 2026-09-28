# Relatório Final: Avaliação Experimental das Condições de Aquisição em Processamento Digital de Imagens

**Disciplina:** TAD0018 - Processamento Digital de Imagens (Turma 01 - 2026.2)  
**Instituição:** Escola Agrícola de Jundiaí (EAJ) — Universidade Federal do Rio Grande do Norte (UFRN)  
**Professor Responsável:** Prof. Dr. Antonino Feitosa  
**Equipe de Trabalho:**  
- **Natan** (Especialista em Aquisição e Protocolo Experimental)  
- **Thiago** (Desenvolvedor de Processamento Digital de Imagens)  
- **Pedro Davi** (Analista de Métricas e Modelagem Estatística)  
- **Cleiton** (Redator Técnico e Integrador de Documentação)  

---

## 1. Introdução e Objetivos

O desempenho de sistemas modernos de Visão Computacional e Processamento Digital de Imagens (PDI) é fortemente condicionado pela qualidade da etapa inicial de aquisição óptica. Fenômenos físicos do mundo real — tais como reflexões difusas, variações na dispersão cromática, contraste de bordas e vinhetagem óptica — afetam diretamente a capacidade de segmentação e a acurácia de medições espaciais automatizadas.

Neste trabalho, realizou-se uma avaliação experimental comparativa de três cores de plano de fundo em folhas de EVA (azul claro, branco e verde claro), com o objetivo de determinar, com base exclusivamente nas técnicas elementares ministradas nas **Aulas 01 a 06 (Unidade 1)** da disciplina, qual material proporciona:
1. Menor nível de ruído estocástico introduzido pelo sensor e pela textura do material;
2. Maior relação sinal-ruído ($\text{SNR}$);
3. Maior fidelidade e estabilidade cromática ($\Delta E$ CIELAB);
4. Menor erro dimensional relativo na padronização espacial e métrica.

---

## 2. Materiais e Métodos

### 2.1 Cenário Experimental e Materiais
O protocolo experimental foi estruturado no Laboratório de TADS para garantir total reprodutibilidade:
- **Superfícies de Fundo:** Folhas de EVA nas cores azul claro, branco e verde claro (dimensões de aproximadamente $40 \times 60\text{ cm}$).
- **Objeto Padrão Dimensional:** Moeda brasileira de 1 Real com diâmetro nominal conhecido de $27,0\text{ mm}$ ($2,70\text{ cm}$), espessura de $1,95\text{ mm}$, anel externo de aço revestido de bronze e núcleo de aço inoxidável.
- **Instrumento de Referência Linear:** Régua milimetrada de plástico cristal transparente de $30\text{ cm}$.
- **Dispositivo de Captura:** Smartphone Samsung Galaxy S25 FE fixado em suporte vertical ortogonal a $45\text{ cm}$ de distância da bancada, operando em resolução nativa de $4000 \times 3000$ pixels (12 MP, proporção 4:3) sob iluminação difusa controlada com flash ativo.
- **Amostragem:** Conjunto amostral de 33 fotografias no total (10 fotos no fundo azul, 12 no fundo branco e 11 no fundo verde).

### 2.2 Pipeline Computacional de Processamento (Aulas 01 a 06)
O processamento computacional foi implementado em Python utilizando estritamente as bibliotecas OpenCV (`cv2`) e NumPy, em conformidade com o cronograma da Unidade 1:
1. **Padronização de Orientação (Aula 02):** Leitura de imagem via `cv2.imread` e verificação das dimensões espaciais, aplicando rotação de 90° no sentido horário (`cv2.rotate`) quando a imagem original apresentava largura superior à altura, garantindo orientação vertical padrão de $3000 \times 4000$ pixels.
2. **Segmentação e Medição do Alvo (Aulas 02 e 04):** Conversão da imagem para escala de cinza (`cv2.cvtColor`) e binarização simples por limiar estático (`cv2.threshold` com limiar $I < 85$) para isolar o núcleo metálico escuro da moeda. A mensuração dimensional foi obtida pela contagem de pixels da máscara binária ($A = \sum \text{pixels}$) associada à fórmula elementar da área do círculo ($D = 2\sqrt{A / \pi}$), dispensando detectores de contorno vetoriais ou descritores morfológicos de unidades posteriores.
3. **Calibração Espacial e Redimensionamento (Aula 04):** Cálculo da resolução espacial observada (pixels/cm) e redimensionamento métrico com interpolação linear (`cv2.resize` com `cv2.INTER_LINEAR`, conforme apresentado no Slide 28 da Aula 04), fixando a resolução uniforme de 70 pixels por centímetro.
4. **Padronização Cromática com Gray World (Aula 05 - Slide 56):** Decomposição dos canais com `cv2.split`, cálculo das médias individuais de cada canal ($\bar{R}, \bar{G}, \bar{B}$) e da média neutra cinza da cena:
   $$\text{gray} = \frac{\bar{R} + \bar{G} + \bar{B}}{3}$$
   Determinação dos fatores multiplicativos $k_c = \text{gray} / \bar{C}$ e correção por multiplicação matricial, com saturação estrita no intervalo $[0, 255]$ através da operação `np.clip` (Aula 04 - Slide 30), finalizando com a recombinação dos canais via `cv2.merge`.

### 2.3 Formulação Matemática das Métricas Quantitativas
- **Ruído do Fundo (Desvio Padrão $\sigma$ - Aulas 01 e 02):** Extraído em uma Região de Interesse (ROI) central homogênea de $600 \times 600$ pixels sobre o EVA:
  $$\sigma = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N} (I_i - \bar{I})^2}$$
  onde menores valores de $\sigma$ representam menor interferência estocástica do sensor e menor microporosidade do suporte.
- **Relação Sinal-Ruído do Fundo ($\text{SNR}$ - Aula 02):**
  $$\text{SNR} = \frac{\bar{I}}{\sigma}$$
  Razão adimensional que quantifica a nitidez e pureza do sinal refletido em relação às flutuações de ruído.
- **Erro Dimensional Relativo ($E_{\text{rel}}$ - Aula 04):**
  $$E_{\text{rel}} = \frac{|D_{\text{medido}} - D_{\text{real}}|}{D_{\text{real}}} \times 100\%$$
  onde $D_{\text{real}} = 27,0\text{ mm}$ e $D_{\text{medido}}$ é a estimativa obtida após a calibração de escala.
- **Fidelidade Cromática ($\Delta E$ no Espaço CIELAB - Aula 05 - Slide 59):** Medida no centro do núcleo da moeda pela distância euclidiana CIE76 em relação ao padrão neutro de referência:
  $$\Delta E = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}$$
- **Análise Espectral de Intensidade (Aula 06):** Avaliação das curvas de distribuição dos níveis de cinza através de histogramas normalizados calculados com `cv2.calcHist`.

---

## 3. Resultados Experimentais e Discussão

### 3.1 Síntese Estatística dos Dados Coletados

| Métrica Analisada | Fundo Azul (Média ± DP) | Fundo Branco (Média ± DP) | Fundo Verde (Média ± DP) | Valor-p (ANOVA) | Conclusão Estatística |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Nível de Ruído ($\sigma$)** | $3,340 \pm 0,333$ | **$2,563 \pm 0,132$** | $4,105 \pm 0,637$ | **$4,49 \times 10^{-9}$** | Diferença altamente significativa; o branco possui menor dispersão. |
| **Sinal-Ruído ($\text{SNR}$)** | $47,03 \pm 4,87$ | **$64,63 \pm 3,19$** | $37,09 \pm 6,62$ | **$2,71 \times 10^{-13}$** | O fundo branco apresentou sinal luminoso amplamente superior. |
| **Erro Dimensional ($E_{\text{rel}}$)**| **$0,685\% \pm 0,272\%$** | $0,831\% \pm 0,818\%$ | $0,693\% \pm 0,723\%$ | $0,8415$ | Sem diferença estatística; escala espacial preservada com erro $< 1\%$. |
| **Fidelidade de Cor ($\Delta E$)** | $12,17 \pm 7,25$ | $13,45 \pm 8,68$ | $19,54 \pm 13,23$ | $0,2095$ | Comportamento estável e homogeneizado pelo modelo Gray World. |

### 3.2 Análise e Interpretação dos Resultados
- **Comportamento do Ruído e do Sinal:** O fundo de EVA branco demonstrou superioridade incontestável. Com um desvio padrão médio de $\sigma = 2,563$, revelou-se $23,3\%$ menos ruidoso que o azul ($3,340$) e $37,6\%$ menos ruidoso que o verde ($4,105$). Essa estabilidade reflexiva se traduziu em uma relação sinal-ruído de $64,63$, contra $47,03$ do azul e $37,09$ do verde. A homogeneidade da dispersão de luz branca difusa elimina gradientes indesejados no sensor.
- **Perfil dos Histogramas de Intensidade (Aula 06):** A análise visual em `graficos_estatistica/histogramas_intensidade_fundos.png` elucida perfeitamente esse comportamento: a curva do fundo branco exibe um pico acentuado, estreito e uniforme concentrado na faixa de 155 a 175 níveis de cinza. Em contraste, os fundos verde e azul sofrem absorção seletiva da radiação eletromagnética emitida pelo flash, alargando a cauda da distribuição e aumentando a variância local por pixel.
- **Acurácia Geométrica da Calibração:** O erro dimensional relativo médio permaneceu abaixo de $0,85\%$ em todos os tratamentos ($0,685\%$ no azul, $0,831\%$ no branco e $0,693\%$ no verde). A ausência de significância estatística na ANOVA ($p = 0,8415$) comprova que o método computacional de redimensionamento linear da Aula 04 atinge precisão submilimétrica independente da cor do fundo de suporte.

---

## 4. Conclusão

Comprovou-se experimentalmente que o **fundo de EVA branco** constitui a melhor condição laboratorial para aquisição digital de imagens no sistema avaliado. Ele proporciona o menor nível de ruído estocástico ($\sigma = 2,563$) e a mais alta relação sinal-ruído ($\text{SNR} = 64,63$) com significância estatística rigorosa ($p < 10^{-8}$), mantendo erro dimensional submétrico e excelente compatibilidade com o algoritmo clássico de Gray World.

Recomenda-se para pesquisas subsequentes a adoção preferencial de superfícies brancas com acabamento mate difuso em estações laboratoriais de PDI.
