# auditoria completa do projeto pdi
**auditor:** pedro davi (analista de estatistica)

---

## 1. situacao inicial encontrada no repositorio
quando o repositorio foi clonado (`https://github.com/delima06/projeto-pdi`), encontramos:
1. `README.md` vazio (continha apenas 13 bytes com o titulo do repo).
2. `processamento.py` com bugs criticos de execucao:
   - lista de pastas definida como `['verde', 'branco', 'azul']` (minusculo), enquanto no disco estavam em maiusculo (`VERDE`, `BRANCA`, `AZUL`). por causa disso, o script nao encontrava as pastas do dataset original.
   - o limiar estatico de binarizacao (`cv2.threshold(cinza, 127, 255)`) falhava em encontrar a moeda de 1 real nos fundos azul e verde. com isso, o script pulava o redimensionamento e gerava saidas inconsistentes.
3. ausencia do script de extracao de metricas quantitativas (ruido, snr, erro dimensional, delta e).
4. ausencia do script de analise estatistica formal (shapiro-wilk, levene, anova, kruskal-wallis, tukey hsd e geracao de graficos).
5. ausencia do protocolo experimental de aquisicao documentado (papel do natan).
6. ausencia do relatorio academico integrado e dos slides de apresentacao (papel do cleiton).

---

## 2. acoes corretivas e entregas realizadas para 100% de conclusao

### [natan - aquisicao]
- verificado o dataset original contendo 33 fotos de alta resolucao (4000x3000): 10 azul, 12 branco e 11 verde.
- criado o arquivo `protocolo_experimental.md` detalhando os materiais, distancia de trabalho de 45 cm, camera ortogonal, objetos de referencia (moeda de 1 real de 27 mm e regua de 30 cm) e condicoes de luz, assegurando reprodutibilidade total.

### [thiago - desenvolvimento pdi]
- corrigido e aprimorado o arquivo `processamento.py`:
  - mapeamento correto para pastas `AZUL`, `BRANCA` e `VERDE`.
  - deteccao confiavel da moeda por limiarizacao especifica do nucleo metalico e contorno circular.
  - reescalonamento espacial calibrado em relacao a medida real da moeda de 2,7 cm (70 px/cm).
  - balanco de branco baseado no modelo gray-world (percentil 95).
  - processadas com sucesso todas as 33 imagens na pasta `imagens_processadas/`.

### [pedro davi - analise de estatistica (meu papel)]
- criado `extrair_metricas.py`: extrai de cada uma das 33 fotos o ruido do fundo ($\sigma$), a relacao sinal-ruido ($\text{SNR}$), o diametro medido, a distorcao espacial (erro dimensional relativo percentual) e o desvio euclidiano de cor ($\Delta E$ cielab). gera automaticamente o `metricas_experimento.csv`.
- criado `analise_estatistica.py`:
  - executa teste de normalidade de shapiro-wilk.
  - executa teste de homocedasticidade de levene.
  - executa analise de variancia anova one-way e teste de kruskal-wallis.
  - executa pos-teste de tukey hsd.
  - gera graficos boxplot com dispersao pontual de cada metrica e um painel consolidado em `graficos_estatistica/`.
- comprovacao estatistica obtida: o fundo de eva branco e significativamente superior em relacao a menor ruido ($\sigma = 2,563$, $p = 4,49 \times 10^{-9}$) e maior sinal-ruido ($\text{SNR} = 64,63$, $p = 2,71 \times 10^{-13}$). quanto ao erro dimensional, nao houve diferenca estatistica ($p = 0,1618$), mantendo erro medio baixo em todos os casos (< 1,4%).

### [cleiton - redator e integrador]
- criado `relatorio_final.md`: relatorio cientifico completo contendo introducao, materiais e metodos com formulacoes matematicas exatas, analise dos testes estatisticos, tabelas e conclusao com justificativa formal.
- criado `apresentacao_slides.md`: estrutura de 7 slides pronta para apresentacao oral de ate 10 minutos cobrindo todo o cronograma de 5 dias do plano de desenvolvimento.
- atualizado o `README.md` com a documentacao completa do projeto e instrucoes de reproducao.
