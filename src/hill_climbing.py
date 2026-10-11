from dataclasses import dataclass, field
from random import Random
from typing import List

from .eight_queens import Board, apply_move, conflicts, moves


@dataclass
class HillResult:
    success: bool
    initial: Board
    final: Board
    initial_conflicts: int
    final_conflicts: int
    iterations: int
    evaluated_states: int
    restarts: int = 0
    history: List[int] = field(default_factory=list)


def hill_climbing(initial: Board) -> HillResult:
    """
    Hill Climbing básico, sem movimentos laterais.
    Deve escolher o primeiro melhor vizinho conforme a ordem de vizinhança definida.
    """
    tabuleiro_atual = initial.copy()
    conflitos_atual = conflicts(tabuleiro_atual)
    
    conflitos_iniciais = conflitos_atual
    iteracoes = 0
    estados_avaliados = 1  # Conta o estado inicial
    historico = [conflitos_atual]

    while True:
        # Se já é uma solução (zero conflitos), terminamos a busca com sucesso
        if conflitos_atual == 0:
            break

        melhor_vizinho = None
        menor_conflitos_vizinho = float("inf")

        # Avalia todos os 56 vizinhos gerados na ordem obrigatória
        for movimento in moves(tabuleiro_atual):
            tabuleiro_vizinho = apply_move(tabuleiro_atual, movimento)
            conflitos_vizinho = conflicts(tabuleiro_vizinho)
            estados_avaliados += 1

            # Mantém o primeiro melhor vizinho encontrado (em caso de empate, mantém o primeiro graças ao <)
            if conflitos_vizinho < menor_conflitos_vizinho:
                menor_conflitos_vizinho = conflitos_vizinho
                melhor_vizinho = tabuleiro_vizinho

        # Critério de subida: só avança se houver melhora estrita (sem movimentos laterais)
        if menor_conflitos_vizinho < conflitos_atual:
            tabuleiro_atual = melhor_vizinho
            conflitos_atual = menor_conflitos_vizinho
            iteracoes += 1
            historico.append(conflitos_atual)
        else:
            # Atingiu um ótimo local ou platô (nenhum vizinho é estritamente melhor)
            break

    sucesso = conflitos_atual == 0

    return HillResult(
        success=sucesso,
        initial=initial,
        final=tabuleiro_atual,
        initial_conflicts=conflitos_iniciais,
        final_conflicts=conflitos_atual,
        iterations=iteracoes,
        evaluated_states=estados_avaliados,
        restarts=0,
        history=historico,
    )


def random_restart(rng: Random, max_restarts: int = 50) -> HillResult:
    """
    Execute Hill Climbing com reinícios aleatórios até encontrar solução
    ou atingir max_restarts.
    """
    raise NotImplementedError("Implemente Random-Restart Hill Climbing.")
