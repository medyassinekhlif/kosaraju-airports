from collections import defaultdict

# List of airports
airports = ["BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN", "JFK",
            "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD"]

# One-way routes between airports
routes = [
    ["DSM", "ORD"], ["ORD", "BGI"], ["BGI", "LGA"], ["SIN", "CDG"], ["CDG", "SIN"],
    ["CDG", "BUD"], ["DEL", "DOH"], ["DEL", "CDG"], ["TLV", "DEL"], ["EWR", "HND"],
    ["HND", "ICN"], ["HND", "JFK"], ["ICN", "JFK"], ["JFK", "LGA"], ["EYW", "LHR"],
    ["LHR", "SFO"], ["SFO", "SAN"], ["SFO", "DSM"], ["SAN", "EYW"],
]

def airports_to_partner(start_airport):
    # Build graph
    graph = defaultdict(list)
    for u, v in routes:
        graph[u].append(v)

    # Kosaraju's algorithm
    def kosaraju(nodes, graph):
        visited = set()
        stack = []

        def dfs(u):
            visited.add(u)
            for v in graph[u]:
                if v not in visited:
                    dfs(v)
            stack.append(u)

        for node in nodes:
            if node not in visited:
                dfs(node)

        # Reverse graph
        rev_graph = defaultdict(list)
        for u in graph:
            for v in graph[u]:
                rev_graph[v].append(u)

        visited.clear()
        sccs = []

        def rev_dfs(u, component):
            visited.add(u)
            component.append(u)
            for v in rev_graph[u]:
                if v not in visited:
                    rev_dfs(v, component)

        while stack:
            node = stack.pop()
            if node not in visited:
                component = []
                rev_dfs(node, component)
                sccs.append(component)

        return sccs

    sccs = kosaraju(airports, graph)

    # Map airport to its SCC
    scc_index = {node: i for i, comp in enumerate(sccs) for node in comp}

    # Count incoming edges for SCCs
    scc_incoming = [0] * len(sccs)
    for u, v in routes:
        u_scc = scc_index[u]
        v_scc = scc_index[v]
        if u_scc != v_scc:
            scc_incoming[v_scc] += 1

    # Determine partner airports
    start_scc = scc_index[start_airport]
    partners = [comp[0] for i, comp in enumerate(sccs) if scc_incoming[i] == 0 and i != start_scc]

    return partners

# Example usage
start = "SFO"
print("Airports to partner with from", start, ":", airports_to_partner(start))
