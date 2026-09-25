from collections.abc import Callable

from .models import SearchResult
from .problem import WeightedGrid

Heuristic = Callable[[tuple[int, int], tuple[int, int]], float]


def bfs(problem: WeightedGrid) -> SearchResult:
    """Busca em Largura. Implemente conforme a especificação do trabalho."""
    goal = problem.goal
    queue = []
    visited = set([])
    father = [[None for _ in range(problem.width)] for _ in range(problem.height)]

    # Caso especial: se o estado inicial já for o objetivo
    if problem.start == goal:
        return SearchResult(
            found=True,
            algorithm="BFS",
            path=[problem.start],
            actions=[],
            cost=0,
            generated=1,
            expanded=0,
            peak_frontier=1,
            peak_stored_states=1,
        )

    queue.append(problem.start)
    visited.add(problem.start)

    # 1. Inicialização das métricas obrigatórias
    # - generated: 1 pois o nó inicial já foi inserido na fronteira
    # - expanded: 0 pois nenhum nó foi retirado e explorado ainda
    # - peak_frontier: 1 pois a fila começa com 1 elemento
    # - peak_stored_states: 1 pois o conjunto de visitados possui o estado inicial
    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored_states = 1

    while queue:
        atual = queue.pop(0)

        # 2. Contabilização da expansão
        # O nó foi retirado da fronteira e terá seus sucessores gerados
        expanded += 1

        sucessors_temp = problem.successors(atual)
        for acao, proxima_pos, custo in sucessors_temp:
            if proxima_pos not in visited:
                father[proxima_pos[0]][proxima_pos[1]] = (atual, acao, custo)
                queue.append(proxima_pos)
                visited.add(proxima_pos)

                # 3. Atualização das métricas na geração
                # Cada inserção válida na fila conta como nó gerado
                generated += 1
                peak_frontier = max(peak_frontier, len(queue))
                peak_stored_states = len(visited)

                # 4. Verificação de objetivo e reconstrução do caminho
                if proxima_pos == goal:
                    path = []
                    actions = []
                    total_cost = 0
                    curr = goal

                    # Percorre os ponteiros de pai de trás para frente até o início
                    while curr != problem.start:
                        path.append(curr)
                        parent_pos, action, step_cost = father[curr[0]][curr[1]]
                        actions.append(action)
                        total_cost += step_cost
                        curr = parent_pos

                    path.append(problem.start)

                    # Inverte para obter o caminho ordenado do início ao fim
                    path.reverse()
                    actions.reverse()

                    return SearchResult(
                        found=True,
                        algorithm="BFS",
                        path=path,
                        actions=actions,
                        cost=total_cost,
                        generated=generated,
                        expanded=expanded,
                        peak_frontier=peak_frontier,
                        peak_stored_states=peak_stored_states,
                    )

    # 5. Caso a fila esvazie sem encontrar o objetivo (mapa sem solução)
    return SearchResult(
        found=False,
        algorithm="BFS",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored_states,
    )


def dfs(problem: WeightedGrid) -> SearchResult:
    """Busca em Profundidade. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente DFS.")


def uniform_cost(problem: WeightedGrid) -> SearchResult:
    """Busca de Custo Uniforme. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente UCS.")


def greedy(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca Gulosa pelo melhor primeiro."""
    raise NotImplementedError("Implemente Busca Gulosa.")


def astar(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca A*."""
    raise NotImplementedError("Implemente A*.")
