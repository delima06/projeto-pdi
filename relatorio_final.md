# relatorio final do projeto: avaliacao experimental das condicoes de aquisicao em pdi
**disciplina:** processamento digital de imagens (pdi)  
**equipe:**  
- natan (especialista em aquisicao)  
- thiago (desenvolvedor pdi)  
- pedro davi (analista de estatistica)  
- cleiton (redator e integrador)  

---

## 1. introducao e objetivos
o desempenho de pipelines de visao computacional e processamento digital de imagens depende diretamente da qualidade da aquisicao de imagens no mundo real. a escolha da cor do plano de fundo onde os objetos sao posicionados e iluminados altera fenomenos opticos cruciais, tais como reflexoes difusas, contraste de bordas, dispersao cromatica e estimacao de escalas espaciais.

o objetivo deste trabalho e avaliar experimentalmente tres cores de fundo em eva (azul claro, branco e verde claro) e determinar, com rigor estatistico e significancia comprovada (nivel de significancia alpha = 0,05), qual cor proporciona as melhores condicoes de estabilidade, menor ruido, maior fidelidade de cor e menor erro dimensional de objetos padronizados.

---

## 2. materiais e metodos

### 2.1 materiais e cenario experimental
- folhas de eva nas cores: azul claro, branco e verde claro.
- objeto de referencia dimensional: moeda de 1 real (diametro real conhecido = 27,0 mm ou 2,70 cm).
- instrumento de medicao visual: regua milimetrada de 30 cm.
- dispositivo de captura: camera digital em suporte ortogonal fixo a 45 cm do plano de captura, gerando imagens com resolucao de 4000 x 3000 pixels.
- conjunto amostral: 33 imagens experimentais coletadas sob iluminacao controlada (10 fotos com eva azul, 12 com eva branco e 11 com eva verde).

### 2.2 pipeline computacional de processamento
o processamento computacional foi implementado em python com opencv e numpy:
1. **padronizacao de orientacao:** deteccao de imagens em orientacao horizontal e correcao automatica para orientacao vertical uniforme.
2. **segmentacao e deteccao da moeda:** segmentacao por limiarizacao do nucleo metalico da moeda (cinza < 85), extracao de contornos, ajuste de circulo circunscrito minimo (diametro em pixels) e bounding box.
3. **calibracao espacial e redimensionamento:** conversao de pixels para unidade real (cm) a partir do diametro real de 2,7 cm e reescalonamento para resolucao padronizada (70 px/cm).
4. **correcao cromatica (balanco de branco):** aplicacao do algoritmo gray-world balanceado baseado no percentil 95 das altas luzes.

### 2.3 formulacao matematica das metricas quantitativas
para a quantificacao analitica, foram definidas e calculadas quatro metricas fundamentais:
- **ruido do fundo (desvio padrao sigma):** medido em uma regiao de interesse (roi) central homogenea de 600 x 600 pixels do fundo de eva:
  $$\sigma = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N} (I_i - \bar{I})^2}$$
  onde menor sigma indica fundo com menor dispersao e textura espuria.
- **relacao sinal-ruido do fundo (snr):**
  $$\text{SNR} = \frac{\bar{I}}{\sigma}$$
  quanto maior o snr, mais nitido e puro e o sinal da imagem em relacao a variacoes ruidosas do sensor.
- **distorcao espacial e erro dimensional relativo ($E_{\text{rel}}$):**
  $$E_{\text{rel}} = \frac{|D_{\text{medido}} - D_{\text{real}}|}{D_{\text{real}}} \times 100\%$$
  onde $D_{\text{real}} = 27,0\text{ mm}$ e $D_{\text{medido}}$ e o diametro obtido via ajuste circular do contorno da moeda.
- **fidelidade e similaridade de cor ($\Delta E$ no espaco cielab):** medido no centro do miolo prateado da moeda em relacao ao padrao medio do conjunto:
  $$\Delta E = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}$$

### 2.4 planejamento estatistico e testes de hipoteses
definiram-se formalmente os testes de hipoteses para cada metrica:
- **hipotese nula ($H_0$):** a cor do fundo em eva nao afeta o desempenho da metrica ($\mu_{\text{azul}} = \mu_{\text{branco}} = \mu_{\text{verde}}$).
- **hipotese alternativa ($H_1$):** pelo menos uma das cores de fundo difere significativamente das demais.
- **criterio de decisao:** nivel de significancia de $\alpha = 0,05$ ($p < 0,05$ rejeita $H_0$).
- **protocolo de validacao dos pressupostos:**
  1. teste de normalidade de shapiro-wilk para cada cor de fundo.
  2. teste de homogeneidade de variancias (homocedasticidade) de levene entre os grupos.
  3. teste parametrico anova one-way acompanhado pelo teste nao-parametrico kruskal-wallis.
  4. teste post-hoc de tukey hsd para identificacao par a par das diferencas estatisticamente significativas.

---

## 3. resultados e discussao

### 3.1 sintese dos dados e resultados dos testes

| metrica | fundo azul (media +- dp) | fundo branco (media +- dp) | fundo verde (media +- dp) | anova p-valor | kruskal p-valor | conclusao estatistica |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ruido ($\sigma$)** | 3,340 +- 0,333 | **2,563 +- 0,132** | 4,105 +- 0,637 | **4,49e-09** | **3,89e-06** | **rejeita $H_0$** (fundo branco possui menor ruido) |
| **snr (sinal-ruido)** | 47,03 +- 4,87 | **64,63 +- 3,19** | 37,09 +- 6,62 | **2,71e-13** | **2,25e-06** | **rejeita $H_0$** (fundo branco e amplamente superior) |
| **erro dimensional (%)** | **0,669% +- 0,475%** | 1,322% +- 0,935% | 0,946% +- 0,818% | 0,1618 | 0,2273 | **aceita $H_0$** (sem diferenca significativa) |
| **fidelidade cor ($\Delta E$)** | 5,414 +- 3,119 | 4,618 +- 1,312 | **2,798 +- 1,334** | **0,0176** | **0,0105** | **rejeita $H_0$** (verde tem menor dispersao pontual) |

### 3.2 analise aprofundada das comparacoes multiplas (tukey hsd)
- **ruido de fundo ($\sigma$):** todas as comparacoes bilaterais foram altamente significativas ($p < 0,001$). a diferenca media entre branco e azul foi de $-0,776$ ($p = 0,0004$) e entre branco e verde foi de $-1,541$ ($p < 0,0001$). o fundo de eva branco apresentou homogeneidade muito superior e menor microporosidade refletida na camera.
- **relacao sinal-ruido (snr):** o fundo branco alcancou a marca de $64,63$, contra $47,03$ do azul e $37,09$ do verde ($p < 0,0001$). isso demonstra que a reflexao difusa branca melhora o alcance dinamico captado pelo sensor do celular.
- **erro dimensional:** os erros medios foram inferiores a $1,4\%$ em todos os fundos, e o teste estatistico indicou $p = 0,1618$ na anova e $p = 0,2273$ no kruskal-wallis. portanto, o algoritmo computacional de segmentacao conseguiu calibrar a escala e medir o objeto com precisao submilimetrica independentemente da cor de fundo.
- **fidelidade cromatica:** o pos-teste comprovou diferenca significativa apenas entre azul e verde ($p = 0,0166$), enquanto branco e azul apresentaram comportamento similar ($p = 0,6362$).

graficos gerados e salvos:
- `graficos_estatistica/boxplot_ruido_std.png`
- `graficos_estatistica/boxplot_snr_fundo.png`
- `graficos_estatistica/boxplot_erro_dimensional_relativo.png`
- `graficos_estatistica/boxplot_delta_e.png`
- `graficos_estatistica/painel_consolidado_metricas.png`

---

## 4. conclusao
os experimentos e as analises estatisticas comprovaram conclusivamente que o **fundo de eva branco** e o fundo otimo para a aquisicao de imagens no sistema avaliado. ele apresentou o menor nivel de ruido de fundo ($\sigma = 2,563$), a maior razao sinal-ruido ($\text{SNR} = 64,63$) com significancia de $p < 10^{-8}$, alem de garantir medicao dimensional acurada com erro relativo medio proximo de $1\%$.
recomenda-se para trabalhos futuros o uso do eva branco com iluminacao difusa e calibracao automatica de escala.
