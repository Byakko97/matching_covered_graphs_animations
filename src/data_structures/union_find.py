from typing import TypeVar

T = TypeVar('T')


class UnionFind:
    """Implementação lenta da estrutura de dados Union-Find"""

    def __init__(self, list: list[T]):
        self.parent = {}
        for x in list:
            self.parent[x] = x

    def union(self, x: T, y: T) -> None:
        """x sempre vai ser o pai de y"""
        self.parent[y] = x

    def find(self, x: T) -> T:
        return x if self.parent[x] == x else self.find(self.parent[x])

    def detach(self, x: T) -> None:
        self.parent[x] = x

    def add(self, x: T) -> None:
        self.parent[x] = x
