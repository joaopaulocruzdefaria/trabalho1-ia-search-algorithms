"""Script para reproduzir e gerar as tabelas de experimentos do trabalho."""

import statistics
import sys
import time
from pathlib import Path
from random import Random

# Adiciona o diretório raiz ao path para importação dos módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.eight_queens import apply_move, conflicts, initial_board, moves, render
from src.heuristics import euclidean, manhattan
from src.hill_climbing import HillResult, hill_climbing, random_restart
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

MAP = Path("data/mapa_teste.txt")
REPETITIONS = 30
NUM_SEEDS_QUEENS = 100


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
        res = runner()

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


def run_part2_experiments(num_seeds: int = NUM_SEEDS_QUEENS) -> dict:
    hill_results: list[tuple[int, HillResult]] = []
    restart_results: list[tuple[int, HillResult]] = []

    for seed in range(num_seeds):
        # Hill Climbing básico
        rng_hill = Random(seed)
        board_hill = initial_board(rng_hill)
        res_hill = hill_climbing(board_hill)
        hill_results.append((seed, res_hill))

        # Random-Restart Hill Climbing
        rng_restart = Random(seed)
        res_restart = random_restart(rng_restart, max_restarts=50)
        restart_results.append((seed, res_restart))

    # Métricas agregadas do Hill Climbing
    hill_success = sum(1 for _, r in hill_results if r.success)
    hill_iters = [r.iterations for _, r in hill_results]
    hill_evals = [r.evaluated_states for _, r in hill_results]

    # Métricas agregadas do Random Restart
    restart_success = sum(1 for _, r in restart_results if r.success)
    restart_iters = [r.iterations for _, r in restart_results]
    restart_evals = [r.evaluated_states for _, r in restart_results]
    restart_counts = [r.restarts for _, r in restart_results]

    # Identifica casos de falha do Hill Climbing
    failed_cases = [(s, r) for s, r in hill_results if not r.success]

    summary = {
        "num_seeds": num_seeds,
        "hill": {
            "success_count": hill_success,
            "success_rate": (hill_success / num_seeds) * 100.0,
            "mean_iterations": statistics.mean(hill_iters),
            "median_iterations": statistics.median(hill_iters),
            "mean_evaluated": statistics.mean(hill_evals),
        },
        "restart": {
            "success_count": restart_success,
            "success_rate": (restart_success / num_seeds) * 100.0,
            "mean_iterations": statistics.mean(restart_iters),
            "median_iterations": statistics.median(restart_iters),
            "mean_evaluated": statistics.mean(restart_evals),
            "mean_restarts": statistics.mean(restart_counts),
            "max_restarts": max(restart_counts),
        },
        "failed_cases": failed_cases,
    }

    return summary


def print_markdown_table_part1(results: list[dict]) -> None:
    print("\n### Tabela de Resultados - Parte 1 (data/mapa_teste.txt)\n")
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


def print_markdown_table_part2(summary: dict) -> None:
    print("\n### Tabela de Resultados - Parte 2 (8 Rainhas - Sementes 0 a 99)\n")
    h = summary["hill"]
    r = summary["restart"]
    n = summary["num_seeds"]

    print("| Métrica | Hill Climbing | Random Restart |")
    print("|---|---:|---:|")
    print(f"| Execuções | {n} | {n} |")
    print(f"| Soluções encontradas | {h['success_count']} | {r['success_count']} |")
    print(f"| Taxa de sucesso (%) | {h['success_rate']:.1f}% | {r['success_rate']:.1f}% |")
    print(f"| Média de iterações | {h['mean_iterations']:.2f} | {r['mean_iterations']:.2f} |")
    print(f"| Mediana de iterações | {h['median_iterations']:.1f} | {r['median_iterations']:.1f} |")
    print(f"| Média de estados avaliados | {h['mean_evaluated']:.2f} | {r['mean_evaluated']:.2f} |")
    print(f"| Média de reinícios | N/A | {r['mean_restarts']:.2f} |")
    print(f"| Máximo de reinícios | N/A | {r['max_restarts']} |")

    # Exibe análise de um caso de falha do Hill Climbing
    if summary["failed_cases"]:
        seed, failed = summary["failed_cases"][0]  # primeiro caso de falha
        print(f"\n#### Análise de Falha do Hill Climbing (Semente {seed}):")
        print(f"- Estado inicial: {failed.initial} (h = {failed.initial_conflicts})")
        print(f"- Estado final: {failed.final} (h = {failed.final_conflicts})")
        print(f"- Iterações: {failed.iterations}, Estados avaliados: {failed.evaluated_states}")
        print(f"- Histórico de h: {failed.history}")

        # Avalia os vizinhos do estado final para demonstrar que nenhum melhora
        neighbor_conflicts = [
            conflicts(apply_move(failed.final, mv)) for mv in moves(failed.final)
        ]
        min_neighbor_h = min(neighbor_conflicts)
        same_h_count = neighbor_conflicts.count(failed.final_conflicts)
        worse_h_count = sum(1 for c in neighbor_conflicts if c > failed.final_conflicts)

        print(f"- Menor h entre os 56 vizinhos: {min_neighbor_h}")
        print(
            f"- Distribuição dos 56 vizinhos: {same_h_count} vizinhos com h={failed.final_conflicts} (empate/ombro), {worse_h_count} vizinhos com h > {failed.final_conflicts} (piores)."
        )
        print(
            "Como não são permitidos movimentos laterais e nenhum vizinho possui h estritamente menor, o algoritmo é forçado a parar."
        )


def main() -> None:
    print("=" * 70)
    print("EXECUTANDO EXPERIMENTOS DO TRABALHO 01")
    print("=" * 70)

    print(f"\n[1/2] Experimentos da Parte 1 no mapa: {MAP}")
    results_p1 = run_part1_experiments()
    print_markdown_table_part1(results_p1)

    print(f"\n[2/2] Experimentos da Parte 2 (8 Rainhas, sementes 0 a {NUM_SEEDS_QUEENS - 1})")
    summary_p2 = run_part2_experiments()
    print_markdown_table_part2(summary_p2)


if __name__ == "__main__":
    main()
