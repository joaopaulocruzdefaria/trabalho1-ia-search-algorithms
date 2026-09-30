from collections.abc import Callable
import heapq

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
    goal = problem.goal
    stack = []
    visited = set([])
    father = [[None for _ in range(problem.width)] for _ in range(problem.height)]

    # Caso especial: se o estado inicial já for o objetivo
    if problem.start == goal:
        return SearchResult(
            found=True,
            algorithm="DFS",
            path=[problem.start],
            actions=[],
            cost=0,
            generated=1,
            expanded=0,
            peak_frontier=1,
            peak_stored_states=1,
        )

    stack.append(problem.start)
    visited.add(problem.start)

    # 1. Inicialização das métricas obrigatórias
    # - generated: 1 pois o nó inicial já foi inserido na fronteira
    # - expanded: 0 pois nenhum nó foi retirado e explorado ainda
    # - peak_frontier: 1 pois a pilha começa com 1 elemento
    # - peak_stored_states: 1 pois o conjunto de visitados possui o estado inicial
    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored_states = 1

    while stack:
        atual = stack.pop()

        # 4. Verificação de objetivo e reconstrução do caminho ao retirar da fronteira
        if atual == goal:
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
                algorithm="DFS",
                path=path,
                actions=actions,
                cost=total_cost,
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored_states,
            )

        # 2. Contabilização da expansão
        # O nó foi retirado da fronteira e terá seus sucessores gerados
        expanded += 1

        sucessors_temp = list(problem.successors(atual))
        # Para que a ordem efetiva de expansão em LIFO seja Norte -> Leste -> Sul -> Oeste,
        # inserimos os sucessores na pilha na ordem inversa (Oeste -> Sul -> Leste -> Norte).
        for acao, proxima_pos, custo in reversed(sucessors_temp):
            if proxima_pos not in visited:
                father[proxima_pos[0]][proxima_pos[1]] = (atual, acao, custo)
                stack.append(proxima_pos)
                visited.add(proxima_pos)

                # 3. Atualização das métricas na geração
                # Cada inserção válida na pilha conta como nó gerado
                # peak_frontier guarda o maior tamanho que a pilha atingiu
                # peak_stored_states guarda o maior tamanho que o conjunto de visitados atingiu
                generated += 1
                peak_frontier = max(peak_frontier, len(stack))
                peak_stored_states = len(visited)

    # 5. Caso a pilha esvazie sem encontrar o objetivo (mapa sem solução)
    return SearchResult(
        found=False,
        algorithm="DFS",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored_states,
    )


def uniform_cost(problem: WeightedGrid) -> SearchResult:
    """Busca de Custo Uniforme. Implemente conforme a especificação do trabalho."""
    goal = problem.goal
    heap = []
    insertion_counter = 0
    # guardar o melhor custo g(n) para cada estado {(0, 0): 0, (0, 1): 1, (1, 2): 4}
    best_g = {}
    # guardar os estados que já foram explorados, usamos um set para facilitar a verificação
    explored = set([])
    father = [[None for _ in range(problem.width)] for _ in range(problem.height)]

    # Caso especial: se o estado inicial já for o objetivo
    if problem.start == goal:
        return SearchResult(
            found=True,
            algorithm="UCS",
            path=[problem.start],
            actions=[],
            cost=0,
            generated=1,
            expanded=0,
            peak_frontier=1,
            peak_stored_states=1,
        )

    # 1. Inicialização da fila de prioridade: (g(n), ordem_de_inserção, estado)
    best_g[problem.start] = 0
    heapq.heappush(heap, (0, insertion_counter, problem.start))
    insertion_counter += 1

    # 1. Inicialização das métricas obrigatórias
    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored_states = 1

    while heap:
        cost, _, atual = heapq.heappop(heap)

        # 2. Entradas obsoletas da fila de prioridade devem ser ignoradas e não contam como expansão
        if atual in explored or cost > best_g[atual]:
            continue

        # 3. Verificação de objetivo e reconstrução do caminho ao retirar da fronteira
        if atual == goal:
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
                algorithm="UCS",
                path=path,
                actions=actions,
                cost=total_cost,
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored_states,
            )

        # 4. Contabilização da expansão
        # O nó foi retirado da fronteira e terá seus sucessores gerados
        explored.add(atual)
        expanded += 1

        #Retorna os sucessores do nó atual (ação, próxima posição, custo)
        sucessors_temp = problem.successors(atual)
        for acao, proxima_pos, step_cost in sucessors_temp:
            novo_custo = cost + step_cost

            # Atualiza o custo e predecessor se encontrar um caminho de menor custo
            if proxima_pos not in explored:
                # Se for o primeiro caminho para o estado OU um caminho de menor custo
                if proxima_pos not in best_g or novo_custo < best_g[proxima_pos]:
                    best_g[proxima_pos] = novo_custo
                    father[proxima_pos[0]][proxima_pos[1]] = (atual, acao, step_cost)
                    heapq.heappush(heap, (novo_custo, insertion_counter, proxima_pos))
                    insertion_counter += 1

                    # 5. Atualização das métricas na geração / melhora de caminho
                    generated += 1
                    distinct_frontier = len(best_g) - len(explored)
                    peak_frontier = max(peak_frontier, distinct_frontier)
                    peak_stored_states = max(peak_stored_states, len(best_g))

    # 6. Caso a fila esvazie sem encontrar o objetivo (mapa sem solução)
    return SearchResult(
        found=False,
        algorithm="UCS",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored_states,
    )


def greedy(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca Gulosa pelo melhor primeiro."""
    raise NotImplementedError("Implemente Busca Gulosa.")


def astar(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca A*."""
    raise NotImplementedError("Implemente A*.")
