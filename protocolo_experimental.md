# protocolo experimental de aquisicao de imagens
# elaborado para garantir reprodutibilidade completa por qualquer outro grupo

## 1. objetivo experimental
avaliar o impacto de diferentes cores de fundo (eva) nas metricas de ruido de imagem, distorcao dimensional e fidelidade de cor em condicoes laboratoriais controladas.

## 2. materiais e equipamentos
- folhas de eva: cores azul claro, branco e verde claro (dimensoes ~40 x 60 cm).
- objeto padrao dimensional: moeda de 1 real brasileira (diametro nominal de 27,0 mm ou 2,7 cm; espessura 1,95 mm; borda bronzeada e nucleo de aco inoxidavel).
- objeto padrao linear adicional: regua milimetrada de plastico cristal transparente de 30 cm.
- sensor de captura: smartphone com sensor de 12 mp (resolucao nativa de 3000 x 4000 pixels, modo retrato, formato jpeg sem compressao destrutiva manual).
- suporte/estabilizacao: suporte vertical fixo mantendo o eixo optico a 90 graus (ortogonal a superficie do eva).
- distancia de trabalho: 45 cm entre a lente do sensor e a superficie do eva.
- iluminacao: fonte de luz superior difusa, evitando sombras duras na regiao central do cenario.

## 3. protocolo de captura (passo a passo)
1. posicionar a folha de eva sobre uma bancada plana, lisa e sem ondulacoes.
2. posicionar a regua milimetrada alinhada na extremidade superior ou inferior da folha.
3. posicionar a moeda de 1 real em posicao definida (sem oclusao).
4. fixar a camera do dispositivo perpendicularmente ao plano do eva na distancia de 45 cm.
5. bloquear o foco e a exposicao manual (evitando que o celular altere iso/tempo de obturacao aleatoriamente entre disparos).
6. realizar disparos repetidos para cada cor de fundo garantindo um numero amostral n >= 10:
   - fundo azul: 10 capturas registradas
   - fundo branco: 12 capturas registradas
   - fundo verde: 11 capturas registradas
   - total: 33 imagens experimentais de alta resolucao (4000 x 3000 pixels)
7. salvar as imagens originais mantendo os metadados e estrutura de pastas em `dataset_original/{AZUL, BRANCA, VERDE}`.
