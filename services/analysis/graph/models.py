from dataclasses import dataclass, field

@dataclass(frozen=True)
class Node:
    id: str
    type: str
    label: str

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    type: str
    file: str
    line: int | None = None

@dataclass
class DependencyGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    unresolved: list[Edge] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)
