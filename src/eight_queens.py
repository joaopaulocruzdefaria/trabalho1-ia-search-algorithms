from random import Random
from typing import Iterable, List, Tuple

Board = List[int]
Move = Tuple[int, int]  # (coluna, nova_linha)
N = 8


def initial_board(rng: Random) -> Board:
    """Geração padronizada: uma rainha aleatória por coluna."""
    return [rng.randrange(N) for _ in range(N)]


def conflicts(board: Board) -> int:
    """Retorne o número de pares não ordenados de rainhas que se atacam."""
    total_conflitos = 0
    for coluna_a in range(N):
        linha_a = board[coluna_a]
        for coluna_b in range(coluna_a + 1, N):
            linha_b = board[coluna_b]
            mesma_linha = linha_a == linha_b
            mesma_diagonal = abs(linha_a - linha_b) == (coluna_b - coluna_a)
            if mesma_linha or mesma_diagonal:
                total_conflitos += 1
    return total_conflitos


def moves(board: Board) -> List[Move]:
    """
    Gere a vizinhança na ordem obrigatória:
    coluna 0..7; dentro de cada coluna, linha 0..7, exceto a linha atual.
    """
    movimentos_possiveis = []
    for coluna in range(N):
        linha_atual = board[coluna]
        for nova_linha in range(N):
            if nova_linha != linha_atual:
                movimentos_possiveis.append((coluna, nova_linha))
    return movimentos_possiveis


def apply_move(board: Board, move: Move) -> Board:
    col, row = move
    if not 0 <= col < N or not 0 <= row < N:
        raise ValueError("Movimento fora do tabuleiro.")
    new_board = board.copy()
    new_board[col] = row
    return new_board


def render(board: Board) -> str:
    rows = []
    for r in range(N):
        rows.append(" ".join("Q" if board[c] == r else "." for c in range(N)))
    return "\n".join(rows)
