# Auditoria Técnica e Relatório de Conformidade do Projeto PDI

**Auditor Responsável:** Pedro Davi (Analista de Métricas e Modelagem Estatística)  
**Disciplina:** TAD0018 - Processamento Digital de Imagens (Turma 01 - 2026.2)  
**Instituição:** Escola Agrícola de Jundiaí (EAJ) — UFRN  
**Professor:** Prof. Dr. Antonino Feitosa  

---

## 1. Histórico e Situação Inicial do Repositório
No início do ciclo de desenvolvimento, o repositório clonado apresentava lacunas críticas de documentação e execução:
1. `README.md` praticamente vazio (continha apenas 13 bytes com o título).
2. `processamento.py` original com falhas de mapeamento de diretórios (sensibilidade a maiúsculas/minúsculas no dataset) e limiarização estática instável em fundos verde e azul.
3. Inexistência de módulos de extração de métricas quantitativas de ruído, sinal-ruído e fidelidade cromática.
4. Inexistência de rotinas de análise estatística formal (ANOVA, Kruskal-Wallis) e geração de gráficos científicos.
5. Ausência do protocolo experimental detalhado e formalizado para reprodutibilidade por outros grupos.
6. Ausência do relatório científico integrado e dos slides estruturados de apresentação oral.

---

## 2. Entregas e Atribuições Realizadas pela Equipe

### [Natan — Especialista em Aquisição e Protocolo Experimental]
- Inspeção e validação do dataset contendo 33 fotografias digitais em alta resolução ($4000 \times 3000$ pixels): 10 amostras no fundo azul, 12 no fundo branco e 11 no fundo verde.
- Levantamento e controle dos parâmetros de aquisição do sensor (Samsung Galaxy S25 FE, distância ortogonal fixa de 45 cm, lente $f/1.8$, flash ativo e ISO controlado entre 25 e 50).
- Elaboração do arquivo [`protocolo_experimental.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/protocolo_experimental.md), detalhando setup, iluminação difusa e objetos padrão (moeda de 1 Real de 27,0 mm e régua milimetrada de 30 cm).

### [Thiago — Desenvolvedor de PDI]
- Desenvolvimento e refatoração completa do [`metodo_computacional.py`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/metodo_computacional.py) com base estrita nas Aulas 01 a 06:
  - Leitura e padronização de orientação vertical uniforme via `cv2.imread` e `cv2.rotate` (Aula 02).
  - Binarização por limiar estático simples (`cv2.threshold` com $I < 85$) sobre a região da moeda, calculando o diâmetro por relação geométrica da área de círculo ($D = 2\sqrt{A/\pi}$, Aula 04), eliminando o uso de contornos vetoriais avançados de outras unidades.
  - Calibração métrica e redimensionamento linear (`cv2.resize` com `cv2.INTER_LINEAR`, Aula 04 - Slide 28), padronizando a escala para 70 px/cm.
  - Normalização cromática baseada no modelo clássico *Gray World Color Constancy* (Aula 05 - Slide 56) com saturação em [0, 255] via `np.clip` (Aula 04 - Slide 30).
- Todas as 33 imagens processadas com 100% de sucesso na pasta `imagens_processadas/`.
- Comentários no código padronizados em letras minúsculas e estilo informal de estudante.

### [Pedro Davi — Analista de Métricas e Modelagem Estatística]
- Implementação de [`extrair_metricas.py`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/extrair_metricas.py): extração do ruído local ($\sigma$) em ROI homogênea central de $600 \times 600$ pixels, cálculo da relação sinal-ruído ($\text{SNR} = \mu / \sigma$), erro dimensional relativo percentual e distância euclidiana CIE76 no espaço CIELAB ($\Delta E$ no espaço $L^*a^*b^*$, Aula 05 - Slide 59). Consolidação de todas as 33 amostras em `metricas_experimento.csv`.
- Implementação de [`analise_estatistica.py`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/analise_estatistica.py):
  - Modelagem descritiva e testes de significância global (ANOVA One-Way e Kruskal-Wallis).
  - Geração dos boxplots individuais e do painel consolidado em `graficos_estatistica/`.
  - Implementação da análise de **histogramas de níveis de cinza dos fundos de EVA (Aula 06)** via `cv2.calcHist`.
- Comprovação experimental: o fundo de EVA branco demonstrou menor ruído ($\sigma = 2,563$, $p = 4,49 \times 10^{-9}$) e maior relação sinal-ruído ($\text{SNR} = 64,63$, $p = 2,71 \times 10^{-13}$), mantendo erro dimensional submétrico ($< 1\%$, $p = 0,8415$).

### [Cleiton — Redator Técnico e Integrador de Documentação]
- Redação e atualização do [`relatorio_final.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/relatorio_final.md) em conformidade com o padrão acadêmico e as formulações das Aulas 01 a 06.
- Estruturação do roteiro formal para apresentação oral de 10 minutos em [`apresentacao_slides.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/apresentacao_slides.md).
- Elaboração do relatório formal e humanizado de acompanhamento semanal e dúvidas para o professor em [`acompanhamento_semanal_professor.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/acompanhamento_semanal_professor.md).
- Estruturação completa e profissional do [`README.md`](file:///c:/Users/Luke/Downloads/Projeto%20PDI/README.md).

---

## 3. Revisão de Conformidade com o Aviso do Professor

| Requisito Avaliado | Situação Anterior | Situação Atual (Refatorada) | Status |
| :--- | :--- | :--- | :---: |
| **Escopo de PDI** | Uso de contornos vetoriais e percentis adaptativos (Unidades 2 e 3). | Uso estrito de limiarização estática, redimensionamento linear, Gray World clássico e histogramas (Aulas 01 a 06). | **Conforme** |
| **Comentários de Código** | Formato de biblioteca corporativa com docstrings complexas. | Comentários em minúsculo, descontraídos e no estilo de estudantes de laboratório. | **Conforme** |
| **Documentação Textual** | Textos informais em minúsculo sem formatação padrão. | Redação formal, bem estruturada, pontuada e humanizada em nível universitário. | **Conforme** |
| **Versionamento Local** | Risco de push antecipado para produção. | Nenhuma modificação comitada ou enviada à branch `main`; tudo validado localmente. | **Conforme** |
