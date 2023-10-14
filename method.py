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

    def _generate_method_node(self) -> pydot.Node:
        single_name = f'<{self.name}<BR /><FONT POINT-SIZE="10">class:{self.class_name}</FONT>>'
        return pydot.Node(name=self.id, label=single_name, shape='ellipse', tooltip=self._get_tool_tip())

    def add_to_graph(self, graph: pydot.Graph):
        method_node: pydot.Node = self._generate_method_node()

        graph.add_node(method_node)

    def __repr__(self):
        return f'package:{self.package}, class:{self.class_name}, method:{self.name}'

    def __str__(self):
        return self.__repr__()
