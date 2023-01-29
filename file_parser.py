from typing import List, Tuple

from line import LineGroup


class FileParser:
    """
    To parse a file having methods. Let's say following is the series of calls:
    Person#details calls Person#to_string which calls both Person#get_first_name and Person#get_second_name

    (Following is another series of calls)
    Person#get_first_name then calls Utils#title_case

    For above-mentioned series of calls, following is the format of calls to specify in the source file

    com.example.Person#details
    com.example.Person#to_string
    com.example.Person#get_first_name, com.example.Person#get_second_name

    com.example.Person#get_first_name
    com.string.Utils#title_case
    """
    def __init__(self, file_path: str):
        self.string_lines = self.file_lines(file_path)
        self.indices: List[Tuple[int, int]] = self.find_groups(self.string_lines)
        self.line_groups: List[LineGroup] = [LineGroup(self.string_lines[begin:end + 1]) for begin, end in self.indices]
        print(f'parsed file: {file_path}')

    @staticmethod
    def find_groups(lines: List[str]) -> List[Tuple[int, int]]:
        def find_groups_impl(all_lines: List[str], begin_index: int, existing_list: List[Tuple[int, int]]):
            # finding begin index
            for i in range(begin_index, len(all_lines)):
                if all_lines[i]:
                    begin_index = i
                    break

            # finding end_index
            end_index = len(all_lines) - 1
            for i in range(begin_index + 1, len(all_lines)):
                if not all_lines[i]:
                    end_index = i - 1  # end-index points to a valid line
                    break

            if begin_index < end_index:
                existing_list.append((begin_index, end_index))
                find_groups_impl(all_lines, end_index + 1, existing_list)

            if begin_index == end_index:
                raise ValueError(f'A line group can not contain just one line, as it is for: {all_lines[begin_index]}')

            # else the loop will break anyway

        indices_list: List[Tuple[int, int]] = []
        find_groups_impl(all_lines=lines, begin_index=0, existing_list=indices_list)
        return indices_list

    @staticmethod
    def file_lines(file_path: str) -> List[str]:
        with open(file_path) as file_handler:
            lines = file_handler.readlines()

        lines = [line.strip() for line in lines]

        # some pre-processing
        # first line must not be empty
        begin_index, end_index = 0, 0  # default values
        for i in range(0, len(lines)):
            if lines[i]:
                begin_index = i
                break

        # last line must not be empty
        for i in range(len(lines) - 1, 0, -1):
            if lines[i]:
                end_index = i
                break

        if begin_index >= end_index:
            raise ValueError(f'There must be at least 2 non-empty lines')

        # this can still contain consecutive empty lines in the middle, but that will be handled while making LineGroups
        return lines[begin_index:end_index + 1]
