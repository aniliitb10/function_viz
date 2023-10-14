import argparse

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

    def write(self, filepath: str):
        extension = self._get_valid_extension(filepath)
        self.graph.write(f"{filepath}", format=extension)

    @staticmethod
    def _get_valid_extension(filepath: str) -> str:
        if '.' not in filepath:
            raise ValueError(f"[{filepath}] doesn't have file extension")

        extension = filepath.split('.')[-1]
        if not extension.isalpha():
            raise ValueError(f"Extension [{extension}] in file [{filepath}] is not a valid extension")

        return extension


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--source", help="Source file")
    arg_parser.add_argument("-o", "--output", help="output file name, default extension is 'png'")
    arg_parser.add_argument("-n", "--name", help="graph name", default='my graph')
    parsed_args = arg_parser.parse_args()

    output: str = parsed_args.output
    file_format = output.split('.')[-1] if '.' in output else 'png'
    filepath = output if '.' in output else f'{output}.{file_format}'
    Graph(filepath=parsed_args.source, name=parsed_args.name).write(filepath)
    print(f'Output is at: {filepath}')


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        argv.extend(["-s", r"./resource/example1.txt", "-o", "./resource/example1.svg", "-n", "sample wiring"])

    main()
