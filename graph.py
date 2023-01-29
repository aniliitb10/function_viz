from typing import Optional

import pydot

from file_parser import FileParser


class Graph:
    def __init__(self, *, filepath: str, name="my_graph", graph_type="digraph", strict=True):
        self.filepath: str = filepath
        self.file: FileParser = FileParser(filepath)
        self.name: str = name
        self.graph_type: str = graph_type
        self.is_strict: bool = strict
        self.graph = pydot.Dot(self.name, graph_type=self.graph_type, strict=self.is_strict)

        for line_group in self.file.line_groups:
            line_group.add_to_graph(self.graph)

    def write(self, *, file_format: str = "svg", filepath: Optional[str] = None):
        self.graph.write(f"{filepath or self.filepath}.{file_format}", format=file_format)


if __name__ == '__main__':
    Graph(filepath=r'./resource/example1.txt').write()
