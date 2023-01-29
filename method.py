import pydot


class Method:
    """
    A class which represents a function, either caller or a callee
    e.g. com.example.Person#to_string
    """

    def __init__(self, description: str):
        description = description.strip()
        full_class, self.name = description.split('#')
        full_class_pieces = full_class.split('.')
        self.package: str = '.'.join(full_class_pieces[:-1])
        self.class_name = full_class_pieces[-1]

    @property
    def id(self):
        return f"{self.package}.{self.class_name}#{self.name}"

    def _get_tool_tip(self):
        return f'class: {self.class_name}, package: {self.package}'

    def _generate_class_node(self) -> pydot.Node:
        return pydot.Node(name=f"{self.package}.{self.class_name}", label=self.class_name, shape='rectangle')

    def _generate_method_node(self) -> pydot.Node:
        return pydot.Node(name=self.id, label=self.name, shape='ellipse', tooltip=self._get_tool_tip())

    def add_to_graph(self, graph: pydot.Graph):
        class_node: pydot.Node = self._generate_class_node()
        method_node: pydot.Node = self._generate_method_node()

        # Now adding both nodes and an edge from class_node to method_node
        graph.add_node(class_node)
        graph.add_node(method_node)
        graph.add_edge(pydot.Edge(class_node.get_name(), method_node.get_name(), color='blue', style='dashed'))

    def __repr__(self):
        return f'package:{self.package}, class:{self.class_name}, method:{self.name}'

    def __str__(self):
        return self.__repr__()
