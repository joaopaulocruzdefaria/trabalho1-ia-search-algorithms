"""Script para reproduzir e gerar as tabelas de experimentos do trabalho."""

import statistics
import sys
import time
from pathlib import Path

# Adiciona o diretório raiz ao path para importação dos módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.heuristics import euclidean, manhattan
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

MAP = Path("data/mapa_teste.txt")
REPETITIONS = 30


def run_part1_experiments(map_path: Path = MAP, repetitions: int = REPETITIONS) -> list[dict]:
    grid = WeightedGrid.from_file(map_path)

    configs = [
        ("BFS", "-", lambda: bfs(grid)),
        ("DFS", "-", lambda: dfs(grid)),
        ("UCS", "-", lambda: uniform_cost(grid)),
        ("Gulosa", "Manhattan", lambda: greedy(grid, manhattan)),
        ("A*", "Manhattan", lambda: astar(grid, manhattan)),
        ("Gulosa", "Euclidiana", lambda: greedy(grid, euclidean)),
        ("A*", "Euclidiana", lambda: astar(grid, euclidean)),
    ]

    results = []

    for alg_name, heur_name, runner in configs:
        # Execução padrão para métricas estruturais
        res = runner()

        # Medição de tempo (mediana de `repetitions` execuções)
        times_ms = []
        for _ in range(repetitions):
            t0 = time.perf_counter()
            runner()
            t1 = time.perf_counter()
            times_ms.append((t1 - t0) * 1000.0)

        median_time = statistics.median(times_ms)

        results.append(
            {
                "algorithm": alg_name,
                "heuristic": heur_name,
                "found": res.found,
                "steps": res.steps,
                "cost": res.cost,
                "generated": res.generated,
                "expanded": res.expanded,
                "peak_frontier": res.peak_frontier,
                "peak_stored": res.peak_stored_states,
                "time_ms": median_time,
            }
        )

    return results


def print_markdown_table(results: list[dict]) -> None:
    print("\n### Tabela Preliminar de Resultados - Parte 1 (data/mapa_teste.txt)\n")
    header = "| Algoritmo | Heurística | Passos | Custo | Gerados | Expandidos | Pico Fronteira | Pico Memória | Tempo Mediano (ms) |"
    sep = "|---|---|---|---|---|---|---|---|---|"
    print(header)
    print(sep)
    for r in results:
        print(
            f"| {r['algorithm']:<9} | {r['heuristic']:<10} | {r['steps']:<6} | {r['cost']:<5} | "
            f"{r['generated']:<7} | {r['expanded']:<10} | {r['peak_frontier']:<14} | "
            f"{r['peak_stored']:<12} | {r['time_ms']:.4f} |"
        )


def main() -> None:
    print(f"Executando experimentos da Parte 1 no mapa: {MAP}")
    print(f"Número de repetições para o tempo de execução: {REPETITIONS}")
    results = run_part1_experiments()
    print_markdown_table(results)


if __name__ == "__main__":
    main()
