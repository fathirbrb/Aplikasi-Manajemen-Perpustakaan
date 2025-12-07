class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = []

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            if v2 not in self.vertices[v1]:
                self.vertices[v1].append(v2)
            if v1 not in self.vertices[v2]:
                self.vertices[v2].append(v1)

    def bfs(self, start):
        if start not in self.vertices:
            return []
        visited = set()
        queue = [start]
        visited.add(start)
        result = []
        while queue:
            v = queue.pop(0)
            result.append(v)
            for neighbor in self.vertices[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result
