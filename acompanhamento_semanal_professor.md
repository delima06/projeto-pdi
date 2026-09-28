# Acompanhamento Semanal e Alinhamento Técnico de Projeto

**Disciplina:** TAD0018 - Processamento Digital de Imagens (Turma 01 - 2026.2)  
**Instituição:** Escola Agrícola de Jundiaí (EAJ) - Universidade Federal do Rio Grande do Norte (UFRN)  
**Professor Responsável:** Prof. Dr. Antonino Feitosa  
**Equipe de Desenvolvimento:**  
- **Natan** (Especialista em Aquisição e Protocolo Experimental)  
- **Thiago** (Desenvolvedor de Processamento Digital de Imagens)  
- **Pedro Davi** (Analista de Métricas e Modelagem Estatística)  
- **Cleiton** (Redator Técnico e Integrador de Documentação)  
**Período:** Sprint 1 — Unidade 1  

---

### Prezado Professor Antonino,

Esperamos que este relatório o encontre bem.

Em cumprimento às diretrizes de acompanhamento contínuo da disciplina, elaboramos este documento com o objetivo de prestar contas do progresso semanal da nossa equipe e, sobretudo, solicitar sua orientação acadêmica sobre decisões técnicas que tomamos durante o desenvolvimento.

Seguindo atentamente a sua recomendação sobre a restrição de escopo, revisamos toda a base de código e a metodologia para utilizar **estritamente os fundamentos e técnicas apresentados nas Aulas 01 a 06 (Unidade 1)**, apoiando-nos na literatura clássica de Gonzalez & Woods (2009) e nas implementações com OpenCV básico e NumPy.

Gostaríamos de compartilhar uma síntese do estágio atual dos trabalhos e submeter quatro questões técnicas para sua apreciação.

---

### 1. Síntese do Progresso Semanal da Equipe

1. **Protocolo Experimental e Aquisição (Natan):**
   - Estruturação e execução do protocolo laboratorial com suporte vertical fixo a 45 cm de distância ortogonal da superfície de apoio.
   - Aquisição de 33 fotografias digitais em modo retrato sob iluminação difusa controlada, contemplando os três cenários de fundo em folhas de EVA: azul claro (10 amostras), branco (12 amostras) e verde claro (11 amostras).
   - Inclusão dos padrões de referência física em todas as cenas: régua milimetrada de 30 cm e moeda brasileira de 1 Real (diâmetro nominal conhecido de 27,0 mm ou 2,70 cm).
   - Documentação rigorosa dos parâmetros de reprodução no arquivo [`protocolo_experimental.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/protocolo_experimental.md).

2. **Pipeline Computacional de Padronização (Thiago):**
   - Leitura de imagens com `cv2.imread` e correção automatizada de rotação para garantia de orientação vertical uniforme (Aula 02).
   - Localização do padrão métrico e estimativa dimensional via binarização por limiar estático (`cv2.threshold`, Aula 02) sobre a região de interesse do núcleo metálico, associada à relação geométrica básica da área circular ($D = 2\sqrt{A/\pi}$), dispensando algoritmos avançados de contorno vetorial de unidades posteriores.
   - Calibração métrica e reescalonamento espacial com interpolação linear (`cv2.resize` com `cv2.INTER_LINEAR`, Aula 04 - Slide 28), padronizando todas as amostras para a relação uniforme de 70 pixels por centímetro.
   - Normalização cromática baseada no modelo clássico *Gray World Color Constancy* (Aula 05 - Slide 56), aplicando multiplicação matricial com saturação no intervalo [0, 255] via `np.clip` (Aula 04 - Slide 30).
   - Processamento concluído com êxito para a totalidade do dataset em [`metodo_computacional.py`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/metodo_computacional.py).

3. **Métricas Quantitativas e Análise Estatística (Pedro Davi):**
   - Quantificação do ruído do sensor através da dispersão local (desvio padrão $\sigma$) e cálculo da relação sinal-ruído ($\text{SNR} = \mu / \sigma$) em região homogênea central de $600 \times 600$ pixels (Aulas 01 e 02).
   - Mensuração do erro dimensional relativo percentual em relação aos 27,0 mm nominais da moeda (Aula 04).
   - Avaliação da estabilidade cromática via distância euclidiana CIE76 no espaço de cores CIELAB ($\Delta E$ no espaço $L^*a^*b^*$, Aula 05 - Slide 59).
   - Implementação de análise comparativa de histogramas de intensidade em níveis de cinza com `cv2.calcHist` (Aula 06).
   - Consolidação dos dados experimentais em [`metricas_experimento.csv`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/metricas_experimento.csv) e geração de gráficos em [`analise_estatistica.py`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/analise_estatistica.py).

4. **Redação Científica e Integração (Cleiton):**
   - Estruturação do [`relatorio_final.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/relatorio_final.md) em formato acadêmico completo (Introdução, Fundamentação Teórica, Materiais e Métodos, Discussão Estatística e Conclusões).
   - Construção do roteiro de apresentação oral de 10 minutos em [`apresentacao_slides.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/apresentacao_slides.md).

---

### 2. Dúvidas Técnicas da Equipe para Orientação do Professor

Gostaríamos de contar com sua visão acadêmica a respeito de quatro decisões metodológicas que discutimos durante a semana:

#### Questão 1: Calibração Cromática — *Gray World* vs. *White Balance* com Patch de Fundo (Aula 05)
No Slide 54 da Aula 05, o senhor abordou a calibração por *Gray/White Balance* utilizando um cartão ou patch de referência neutro ($RGB_{\text{ref}} = (255, 255, 255)$, multiplicando os canais pelo fator de ganho $k = 255 / R_{\text{medido}}$). Já no Slide 56, vimos o *Gray World Color Constancy*, que assume que a média global dos canais de uma cena tende ao cinza neutro.  
Em nossos experimentos, como duas das folhas de EVA (verde e azul) possuem saturação cromática expressiva cobrindo grande parte do enquadramento, a hipótese de neutralidade global do *Gray World* sofre ligeira interferência do fundo predominante. O senhor consideraria mais adequado adotarmos o *White Balance* fixando o fundo branco como referência de iluminação para calibrar os demais cenários, ou a abordagem do *Gray World* clássico da Aula 05 é a mais indicada para evidenciar didaticamente essa limitação no relatório?

#### Questão 2: Método de Interpolação Espacial no Redimensionamento (Aula 04)
No Slide 28 da Aula 04, foram apresentados os três principais métodos de interpolação em OpenCV: vizinho mais próximo (`cv2.INTER_NEAREST`), bilinear (`cv2.INTER_LINEAR`) e bicúbica (`cv2.INTER_CUBIC`).  
Para realizar a padronização métrica para 70 px/cm, adotamos a interpolação bilinear por ser o padrão de mercado e oferecer excelente equilíbrio entre suavidade e custo computacional. Gostaríamos de confirmar se o senhor recomenda mantermos a bilinear ou se a bicúbica seria preferível para preservar com maior nitidez as transições de borda circular da moeda durante a apresentação.

#### Questão 3: Validação da Medição Geométrica Simplificada (Aulas 02 e 04)
Atendendo estritamente à sua orientação de evitar recursos que ainda não foram ministrados em aula (como detectores de contorno vetoriais ou descritores morfológicos de unidades futuras), adaptamos o método de medição da moeda para operar exclusivamente via binarização por limiar simples (`cv2.threshold` com $I < 85$, da Aula 02) associada ao fatiamento matricial da região densa e cálculo do diâmetro pela área de círculo ($D = 2\sqrt{A/\pi}$, da Aula 04).  
Essa abordagem obteve erro dimensional relativo médio inferior a $1\%$ em todos os cenários experimentais. O senhor considera essa formulação geométrica direta satisfatória e alinhada ao nível de formalismo esperado para a Unidade 1?

#### Questão 4: Pertinência dos Histogramas de Níveis de Cinza na Discussão (Aula 06)
Com a introdução da Aula 06 sobre Transformações de Intensidade e Contraste, incluímos no pipeline um comparativo de histogramas de intensidade dos fundos de EVA gerados com `cv2.calcHist`. O gráfico evidenciou que a folha branca apresenta uma distribuição compacta e deslocada para as altas luzes, enquanto as folhas azul e verde possuem distribuições mais amplas e achatadas devido à absorção seletiva de comprimento de onda sob o flash da câmera.  
O senhor considera que essa correlação entre o perfil de histograma (Aula 06) e a relação sinal-ruído (Aula 02) é um ponto interessante a ser destacado na apresentação de slides e no relatório final?

---

Agradecemos imensamente pela atenção, pelo incentivo e pelas orientações ao longo das aulas práticas. Permanecemos à disposição no horário de atendimento semanal e no laboratório da disciplina para eventuais esclarecimentos.

Respeitosamente,  
**Equipe do Projeto PDI — Turma 01**  
*Natan, Thiago, Pedro Davi e Cleiton*
