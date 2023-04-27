class UnionFind:
    """Implementaãço lenta da estrutura de dados Union-Find"""

    def __init__(self, list):
        self.parent = {}
        for x in list:
            self.parent[x] = x

    def union(x, y):
        """x sempre vai ser o pai de y"""
        self.parent[y] = x

    def find(x):
        return x if self.parent[x] == x else find(self.parent[x])

    def detach(x):
        self.parent[x] = x

    def add(x):
        self.parent[x] = x