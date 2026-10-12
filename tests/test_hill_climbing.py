import unittest
from random import Random

from src.eight_queens import conflicts, initial_board
from src.hill_climbing import hill_climbing, random_restart


class HillClimbingTests(unittest.TestCase):
    def test_hill_climbing_already_solved(self):
        solution = [0, 4, 7, 5, 2, 6, 1, 3]
        result = hill_climbing(solution)
        self.assertTrue(result.success)
        self.assertEqual(result.final_conflicts, 0)
        self.assertEqual(result.iterations, 0)
        self.assertEqual(result.evaluated_states, 1)  # apenas o inicial
        self.assertEqual(result.restarts, 0)

    def test_hill_climbing_strict_improvement(self):
        # Seed 42 cai em um mínimo local com 1 conflito
        rng = Random(42)
        initial = initial_board(rng)
        result = hill_climbing(initial)

        self.assertFalse(result.success)
        self.assertEqual(result.final_conflicts, 1)
        self.assertEqual(result.iterations, 4)
        # 1 estado inicial + 4 iterações aceitas * 56 vizinhos + 1 checagem sem melhora * 56 vizinhos = 1 + 5 * 56 = 281
        self.assertEqual(result.evaluated_states, 281)
        self.assertEqual(len(result.history), 5)
        # Verifica melhora estrita a cada passo
        for i in range(len(result.history) - 1):
            self.assertLess(result.history[i + 1], result.history[i])

    def test_random_restart_success(self):
        # Com seed 42, a tentativa 0 falha e a tentativa 1 (1 reinício) encontra solução
        rng = Random(42)
        result = random_restart(rng, max_restarts=50)

        self.assertTrue(result.success)
        self.assertEqual(result.final_conflicts, 0)
        self.assertEqual(result.restarts, 1)
        self.assertEqual(conflicts(result.final), 0)
        # Iterações acumuladas: 4 (tentativa 0) + 5 (tentativa 1) = 9
        self.assertEqual(result.iterations, 9)
        # Estados avaliados acumulados: 281 + 281 = 562
        self.assertEqual(result.evaluated_states, 562)

    def test_random_restart_limit_reached(self):
        # Se max_restarts for 0 e a tentativa falhar, deve parar após 0 reinícios
        rng = Random(42)
        result = random_restart(rng, max_restarts=0)
        self.assertFalse(result.success)
        self.assertEqual(result.restarts, 0)
        self.assertEqual(result.iterations, 4)
        self.assertEqual(result.evaluated_states, 281)


if __name__ == "__main__":
    unittest.main()
