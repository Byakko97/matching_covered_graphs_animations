class UnionFind:
    """Implementaãço lenta da estrutura de dados Union-Find"""

    def __init__(self, list):
        self.parent = {}
        for x in list:
            self.parent[x] = x

    def union(self, x, y):
        """x sempre vai ser o pai de y"""
        self.parent[y] = x

    def find(self, x):
        return x if self.parent[x] == x else self.find(self.parent[x])

    def detach(self, x):
        self.parent[x] = x

    def add(self, x):
        self.parent[x] = x