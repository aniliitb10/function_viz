from typing import List

import pydot

from method import Method


class Line:
    """
    A class to parse a line, either containing a single method or multiple methods separated by ','
    """

    def __init__(self, each_line: str):
        each_line = each_line.strip()
        self.methods: List[Method] = [Method(m) for m in each_line.split(',')]

    def add_to_graph(self, graph: pydot.Graph):
        for method in self.methods:
            method.add_to_graph(graph)

    def __repr__(self):
        return ','.join(str(m) for m in self.methods)


class LineGroup:
    """
    A class to represent a group of lines (practically a list of line.Line)
    """
    def __init__(self, line_list: List[str]):
        for line in line_list:
            if not line:
                raise ValueError(f'Empty line is not expected in LineGroup')
        self.lines: List[Line] = [Line(each_line) for each_line in line_list]

    def add_to_graph(self, graph: pydot.Graph):
        # adding lines individually:
        for line in self.lines:
            line.add_to_graph(graph)

        # adding connection between following lines
        lines_count: int = len(self.lines)
        for line_index in range(0, lines_count - 1):
            for caller in self.lines[line_index].methods:
                for callee in self.lines[line_index + 1].methods:
                    graph.add_edge(pydot.Edge(caller.id, callee.id))

    def __repr__(self):
        group = '\n'.join(str(line) for line in self.lines)
        return f'\n{group}\n'


def main():
    print(Line("com.example.Person#get_first_name, com.example.Person#get_second_name").methods)
    print(Line("com.example.Person#get_first_name").methods)


if __name__ == '__main__':
    main()
