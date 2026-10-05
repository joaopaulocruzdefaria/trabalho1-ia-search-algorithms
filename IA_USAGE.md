# Declaração de uso de Inteligência Artificial

Preencha esta seção para toda ferramenta de IA generativa utilizada durante o trabalho.

| Ferramenta | Finalidade | Arquivos/partes afetadas | Como o resultado foi verificado |
|---|---|---|---|
| Google Gemini | Esclarecimento conceitual sobre a teoria e o funcionamento dos algoritmos de busca antes da implementação | Concepção geral dos algoritmos (`src/search.py`) | Validação com as notas de aula e slides da disciplina |
| Google Gemini | Apoio na simplificação de trechos de código e esclarecimento de sintaxes e recursos idiomáticos em Python | `src/search.py`, `src/problem.py`, `scripts/run_experiments.py` | Testes manuais durante o desenvolvimento e validação posterior com a suíte de testes automatizados |
| Google Gemini | Auxílio na identificação e resolução de bugs durante o desenvolvimento dos algoritmos | `src/search.py` | Reexecução dos testes e validação de que o código voltou a funcionar corretamente após as correções |
| Google Gemini | Geração de instâncias de mapas adicionais para cenários de teste específicos (bordas, ciclos, caminhos sem solução, custos alternados) | Arquivos em `data/` (`mapa_ciclos.txt`, `mapa_sem_solucao.txt`, `mapa_curta_cara.txt`, etc.) | Inspeção visual dos arquivos de mapa e validação das saídas esperadas através de testes unitários |

## Declaração

Declaramos que as implementações dos algoritmos de busca solicitados foram desenvolvidas pela equipe e que todo uso de ferramentas externas ou de IA foi registrado acima.
