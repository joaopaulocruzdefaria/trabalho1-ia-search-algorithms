import unittest
from random import Random

from src.eight_queens import (
    N,
    apply_move,
    conflicts,
    initial_board,
    moves,
    render,
)


class EightQueensTests(unittest.TestCase):
    def test_initial_board_dimensions_and_reproducibility(self):
        rng1 = Random(42)
        b1 = initial_board(rng1)
        self.assertEqual(len(b1), N)
        self.assertTrue(all(0 <= row < N for row in b1))

        rng2 = Random(42)
        b2 = initial_board(rng2)
        self.assertEqual(b1, b2)

    def test_conflicts_zero_for_valid_solution(self):
        # Solução clássica das 8 rainhas
        solution = [0, 4, 7, 5, 2, 6, 1, 3]
        self.assertEqual(conflicts(solution), 0)

        solution2 = [6, 2, 7, 1, 4, 0, 5, 3]
        self.assertEqual(conflicts(solution2), 0)

    def test_conflicts_all_same_row(self):
        # 8 rainhas na mesma linha: combinação C(8,2) = 28 conflitos
        board = [0] * 8
        self.assertEqual(conflicts(board), 28)

    def test_conflicts_all_same_diagonal(self):
        # 8 rainhas na diagonal principal: C(8,2) = 28 conflitos
        board = list(range(8))
        self.assertEqual(conflicts(board), 28)

        # 8 rainhas na diagonal secundária
        board_sec = list(reversed(range(8)))
        self.assertEqual(conflicts(board_sec), 28)

    def test_conflicts_specific_board(self):
        # Tabuleiro inicial gerado pela seed 42: [1, 0, 4, 3, 3, 2, 1, 1]
        rng = Random(42)
        board = initial_board(rng)
        self.assertEqual(board, [1, 0, 4, 3, 3, 2, 1, 1])
        self.assertEqual(conflicts(board), 10)

    def test_moves_count_and_order(self):
        board = [0, 1, 2, 3, 4, 5, 6, 7]
        all_moves = moves(board)
        # Cada estado deve ter 8 * 7 = 56 vizinhos
        self.assertEqual(len(all_moves), 56)

        # Ordem obrigatória: coluna 0..7 e em cada coluna linha 0..7 ignorando a atual
        expected = []
        for c in range(N):
            for r in range(N):
                if r != board[c]:
                    expected.append((c, r))
        self.assertEqual(all_moves, expected)

    def test_apply_move(self):
        board = [0, 4, 7, 5, 2, 6, 1, 3]
        new_board = apply_move(board, (2, 1))
        # O tabuleiro original não deve ser modificado
        self.assertEqual(board[2], 7)
        self.assertEqual(new_board[2], 1)
        self.assertEqual(new_board[:2], board[:2])
        self.assertEqual(new_board[3:], board[3:])

        with self.assertRaises(ValueError):
            apply_move(board, (-1, 0))
        with self.assertRaises(ValueError):
            apply_move(board, (0, 8))

    def test_render(self):
        board = [0, 1, 2, 3, 4, 5, 6, 7]
        rendered = render(board)
        lines = rendered.splitlines()
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0].split()[0], "Q")
        self.assertEqual(lines[1].split()[1], "Q")


if __name__ == "__main__":
    unittest.main()
