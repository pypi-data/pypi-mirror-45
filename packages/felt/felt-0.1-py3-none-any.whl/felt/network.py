""""""

from collections import defaultdict
from dataclasses import dataclass
from .routing import shortest_path
from .movement import Movement
from typing import Hashable, Mapping
import math

__all__ = ['Network', 'Node', 'Way', 'Path']

class HasAttr:
    def __getattr__(self, name):
        try:
            return self._attr[name]
        except KeyError:
            raise AttributeError(name)
    
        
@dataclass
class Node(HasAttr):
    name: Hashable
    x: float
    y: float
    _attr: Mapping

    def __init__(self, name, x, y, **attr):
        self.name = name
        self.x = x
        self.y = y
        self._attr = attr
        self._network = None

class Path:
    def __init__(self, nodes):
        self._nodes = nodes
        self._network = None

    def __repr__(self):
        return f'Path({self._nodes})'

    def __iter__(self):
        return iter(self._nodes)

    def __eq__(self, other):
        if not isinstance(other, Path):
            return False
        return list(self) == list(other)

    def nodes(self):
        return [ self._network._nodes[node] for node in self._nodes ]

    def length(self):
        length = 0
        for a, b in zip(self.nodes()[:-1], self.nodes()[1:]):
            length += math.hypot(a.x - b.x, a.y - b.y)
        return length


class Way(HasAttr, Path):

    def __init__(self, nodes, **attr):
        self._nodes = nodes
        self._attr = attr
        self._network = None
    
    def __repr__(self):
        return f'Way({self._nodes}, {self._attr})'

class Link(HasAttr, Path):

    def __init__(self, a, b, **attr):
        self.a = a
        self.b = b
        self._nodes = [a, b]
        self._attr = attr
        self._network = None

    def __repr__(self):
        return f'Link({self.a}, {self.b}, {self._attr})'

class Network:
    
    def __init__(self, nodes, ways):

        self._nodes = {}
        for node in nodes:
            node._network = self
            self._nodes[node.name] = node

        self._ways = []
        for way in ways:
            way._network = self
            for node in way.nodes():
                if node.name not in self._nodes:
                    raise ValueError(f'Node {node.name} in way but not in nodes')
            self._ways.append(way)

    def links(self):
        for way in self._ways:
            oneway = getattr(way, 'oneway', 0)
            if oneway > 0:
                oriented = [way.nodes()]
            elif oneway < 0:
                oriented = [way.nodes()[::-1]]
            else:
                oriented = [way.nodes(), way.nodes()[::-1]]
            for oriented_way in oriented:
                for a, b in zip(oriented_way[:-1], oriented_way[1:]):
                    link = Link(a.name, b.name, **way._attr)
                    link._network = self
                    yield link

    def nodes(self):
        yield from self._nodes.values()

    def graph(self):
        return Graph(self.nodes(), self.links())

    def shortest_path(self, source, sink):
        path = Path(self.graph().shortest_path(source, sink))
        path._network = self
        return path

                    
class Graph:

    def __init__(self, nodes, links):
        
        self._nodes = {}
        for node in nodes:
            self._nodes[node.name] = node
        
        self._links = defaultdict(dict)
        for link in links:
            self._links[link.a][link.b] = link
        self._links = dict(self._links)

    @property
    def links(self):
        return self._links

    def neighbors(self, node):
        assert node in self._nodes
        if node not in self._links:
            return []
        return [self._nodes[node] for node in self._links[node].keys()]

    def nodes(self):
        yield from self._nodes.values()

    def shortest_path(self, source, sink):
        return shortest_path(self, source, sink)

    
