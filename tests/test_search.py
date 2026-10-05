import unittest
from pathlib import Path

from src.heuristics import euclidean, manhattan
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class SearchMandatoryTests(unittest.TestCase):
    """
    Testes obrigatórios:
    1. Início adjacente ao objetivo;
    2. Mapa sem solução;
    3. Mapa com ciclos;
    4. Existência de rotas distintas com o mesmo número de ações;
    5. Existência de uma rota curta e cara e outra mais longa e barata.
    """

    def test_1_adjacent_start_goal(self):
        """1. Início adjacente ao objetivo: /mapa_adjacente.txt."""
        grid = WeightedGrid.from_file(DATA_DIR / "mapa_adjacente.txt")
        algorithms = [
            ("BFS", bfs(grid)),
            ("DFS", dfs(grid)),
            ("UCS", uniform_cost(grid)),
            ("Greedy-Manhattan", greedy(grid, manhattan)),
            ("Greedy-Euclidean", greedy(grid, euclidean)),
            ("A*-Manhattan", astar(grid, manhattan)),
            ("A*-Euclidean", astar(grid, euclidean)),
        ]

        for name, res in algorithms:
            with self.subTest(algorithm=name):
                self.assertTrue(res.found, f"{name} deveria encontrar o objetivo")
                self.assertEqual(res.steps, 1, f"{name} deveria resolver em exatamente 1 passo")
                self.assertEqual(res.cost, 1, f"{name} deveria ter custo 1")
                self.assertEqual(res.actions, ["L"])
                self.assertEqual(res.path, [(0, 0), (0, 1)])

    def test_2_no_solution(self):
        """2. Mapa sem solução: /mapa_sem_solucao.txt."""
        grid = WeightedGrid.from_file(DATA_DIR / "mapa_sem_solucao.txt")
        algorithms = [
            ("BFS", bfs(grid)),
            ("DFS", dfs(grid)),
            ("UCS", uniform_cost(grid)),
            ("Greedy-Manhattan", greedy(grid, manhattan)),
            ("Greedy-Euclidean", greedy(grid, euclidean)),
            ("A*-Manhattan", astar(grid, manhattan)),
            ("A*-Euclidean", astar(grid, euclidean)),
        ]

        for name, res in algorithms:
            with self.subTest(algorithm=name):
                self.assertFalse(res.found, f"{name} não deveria encontrar caminho")
                self.assertEqual(res.cost, float("inf"), f"{name} deve indicar custo infinito")
                self.assertEqual(res.path, [], f"{name} deve retornar caminho vazio")
                self.assertEqual(res.actions, [], f"{name} deve retornar ações vazias")
                self.assertGreater(res.generated, 0, f"{name} deve contabilizar nós gerados")
                self.assertGreater(res.expanded, 0, f"{name} deve contabilizar nós expandidos")

    def test_3_map_with_cycles(self):
        """3. Mapa com ciclos: /mapa_ciclos.txt."""
        grid = WeightedGrid.from_file(DATA_DIR / "mapa_ciclos.txt")
        algorithms = [
            ("BFS", bfs(grid)),
            ("DFS", dfs(grid)),
            ("UCS", uniform_cost(grid)),
            ("Greedy-Manhattan", greedy(grid, manhattan)),
            ("Greedy-Euclidean", greedy(grid, euclidean)),
            ("A*-Manhattan", astar(grid, manhattan)),
            ("A*-Euclidean", astar(grid, euclidean)),
        ]

        for name, res in algorithms:
            with self.subTest(algorithm=name):
                self.assertTrue(res.found, f"{name} deveria resolver mapa com ciclos")
                self.assertGreater(len(res.path), 0)
                self.assertEqual(res.path[0], grid.start)
                self.assertEqual(res.path[-1], grid.goal)
                self.assertEqual(len(res.path), len(set(res.path)))

    def test_4_equal_length_routes(self):
        """4. Existência de rotas distintas com o mesmo número de ações: data/mapa_rotas_iguais.txt."""
        grid = WeightedGrid.from_file(DATA_DIR / "mapa_rotas_iguais.txt")
        res_bfs = bfs(grid)
        res_dfs = dfs(grid)
        res_ucs = uniform_cost(grid)

        self.assertTrue(res_bfs.found)
        self.assertTrue(res_dfs.found)
        self.assertTrue(res_ucs.found)

        self.assertEqual(res_bfs.steps, 4)
        self.assertEqual(res_ucs.steps, 4)
        self.assertEqual(res_bfs.cost, 4)
        self.assertEqual(res_ucs.cost, 4)

        # Ordem de sucessores obrigatória: N -> L -> S -> O.
        self.assertEqual(res_bfs.actions[0], "L", "BFS deve priorizar Leste antes de Sul")

    def test_5_short_expensive_vs_long_cheap(self):
        """
        5. Rota curta e cara vs. rota longa e barata: data/mapa_curta_cara.txt.
        """
        grid = WeightedGrid.from_file(DATA_DIR / "mapa_curta_cara.txt")
        res_bfs = bfs(grid)
        res_ucs = uniform_cost(grid)
        res_astar_m = astar(grid, manhattan)
        res_astar_e = astar(grid, euclidean)

        # BFS prioriza o menor número de ações (passos)
        self.assertTrue(res_bfs.found)
        self.assertEqual(res_bfs.steps, 2, "BFS deve escolher a rota mais curta em ações (2 passos)")
        self.assertEqual(res_bfs.cost, 7, "BFS escolhe a rota mais cara (custo 7)")
        self.assertEqual(res_bfs.actions, ["L", "L"])

        # UCS prioriza o menor custo total acumulado g(n)
        self.assertTrue(res_ucs.found)
        self.assertEqual(res_ucs.cost, 4, "UCS deve encontrar o menor custo (custo 4)")
        self.assertEqual(res_ucs.steps, 4, "UCS escolhe a rota mais longa em ações (4 passos)")
        self.assertEqual(res_ucs.actions, ["S", "L", "L", "N"])

        # A* com heurística admissível deve encontrar a solução de custo ótimo
        self.assertTrue(res_astar_m.found)
        self.assertEqual(res_astar_m.cost, 4, "A* (Manhattan) deve encontrar a rota de custo ótimo (4)")
        self.assertEqual(res_astar_m.steps, 4)

        self.assertTrue(res_astar_e.found)
        self.assertEqual(res_astar_e.cost, 4, "A* (Euclidiana) deve encontrar a rota de custo ótimo (4)")
        self.assertEqual(res_astar_e.steps, 4)


if __name__ == "__main__":
    unittest.main()
