class Graph:
    """class to represent a directed, unweighted graph"""
    def __init__(self):
        self.g = {}
    
    def add_edge(self, source, target):
        if source in self.g and target in self.g[source]:
            return None # Edge already in graph, therefore do not execute method
        if source not in self.g.keys():
            self.g[source] = []
        self.g[source].append(target)
        return self
    
    def path_exists(self, source, target):
        """returns True if target node can be reached from source node, otherwise False"""

        # Implementation of BFS starting from the source node
        visited, queue = [], [source]
        while queue:
            curr_node = queue.pop(0)
            if curr_node == target:
                return True
            
            for neighbour in self.g[curr_node]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)

        return False

    def all_reachables(self, source):
        """returns a list of all nodes reachable from the source node"""
        reachables = []
        for vertex in self.g.keys():
            if vertex != source and self.path_exists(source, vertex):
                reachables.append(vertex)
        return reachables

    def get_vertices(self):
        return list(self.g.keys())
