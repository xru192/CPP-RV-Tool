import argparse
import re

def is_match(pattern, string):
    match = re.match(pattern, string)
    return match is not None and match.end() == len(string)


class MOPFile :
    def __init__(self, file):
        self.file = file
        self.specname = ""
        self.params = []
        self.includes = []
        self.events = []
        if self.check_file():
            self.parse_file()
            self.header_fileout = f"{self.specname}_dispatcher.h"
            self.source_fileout = f"{self.specname}_dispatcher.cpp"
            self.class_name = f"{self.specname}_dispatcher"
        else:
            print(f"File: {file} not formatted correctly")
            exit(1)

    def check_file(self):
        try:
            with open(self.file, 'r') as f:
                lines = f.readlines()

            in_header = False
            for line in lines:
                line = line.strip()
                if in_header:
                    if len(line) == 0 or line.startswith("#include"):
                        continue
                    if not is_match(r'.*\(.*\).*', line):
                        return False
                    in_header = False

            return True
        except FileNotFoundError as e:
            print(f"File {self.file} not found")
            exit(1)

    def parse_file(self):
        try:
            with open(self.file, 'r') as f:
                lines = f.readlines()

            in_header = True
            for line in lines:
                line = line.strip()
                if in_header:
                    if line.startswith("#include"):
                        self.includes.append(line)
                    elif len(line) > 0:
                        # parse spec name and parameters
                        in_header = False
                        self.specname = line[:line.find('(')].strip()
                        param_string = line[line.find('(')+1:line.find(')')]
                        parts = param_string.split(',')
                        for part in parts:
                            self.params.append(part.strip())
                else:
                    if line.startswith('event'):
                        parts = line.split()
                        event_name = parts[1]
                        event_params = ""

                        param_string = line[line.find('(')+1:line.find(')')].strip()
                        if not param_string.startswith('void '):
                            event_params = param_string
                        self.events.append((event_name, event_params))
                    
        except Exception as e:
            print("Exception occured: ", e)


def generate_header(mop : MOPFile, file_out):
    file_out.write('// This is a generated dispatcher for non-parametric monitoring\n\n')
    file_out.write('#pragma once\n\n')
    file_out.write(f'#include "{mop.specname}_monitor.h"\n')
    for include in mop.includes:
        file_out.write(f'{include}\n')
    file_out.write('\n')
    file_out.write(f'class {mop.class_name}\n')
    file_out.write('{\n')
    file_out.write('private:\n')
    file_out.write(f'\t{mop.specname}_Monitor monitor {{}};\n\n')
    file_out.write('public:\n')
    for event_name, event_params in mop.events:
        file_out.write(f'\tvoid receive_{event_name}({event_params});\n')
    file_out.write('};\n')

def generate_source(mop : MOPFile, file_out):
    file_out.write('// This is a generated dispatcher for non-parametric monitoring\n\n')
    file_out.write(f'#include "{mop.header_fileout}"\n\n')
    for event in mop.events:
        event_name = event[0]
        event_params = event[1]
        file_out.write(f'void {mop.class_name}::receive_{event_name}({event_params})\n')
        file_out.write('{\n')
        file_out.write(f'\tmonitor.__RVC_{mop.specname}_{event_name}();\n')
        file_out.write('}\n\n')

def generate_header_parametric(mop : MOPFile, file_out):
    pass

def generate_source_parametric(mop : MOPFile, file_out):
    pass


def print_mop(mop : MOPFile):
    print(mop.file)
    print(mop.specname)
    print(mop.params)
    print(mop.includes)
    print(mop.events)

def main():
    parser = argparse.ArgumentParser(description='Generate dispatcher from .mop file.')

    parser.add_argument('filename', type=str, help='Input file name')
    parser.add_argument('-p', '--parametric', action='store_true', help='Use parametric monitoring')

    args = parser.parse_args()

    # Access the parsed arguments
    filename = args.filename
    do_parametric = args.parametric

    mop = MOPFile(filename)
    # print_mop(mop)

    if do_parametric:
        try:
            with open(mop.source_fileout, 'w') as f:
                generate_source_parametric(mop, f)
            with open(mop.header_fileout, 'w') as f:
                generate_header_parametric(mop, f)
        except Exception as e:
            print("Something went wrong generating parametric dispatcher")
            exit(1)
    else:
        try:
            with open(mop.source_fileout, 'w') as f:
                generate_source(mop, f)
            with open(mop.header_fileout, 'w') as f:
                generate_header(mop, f)
        except Exception as e:
            print("Something went wrong generating dispatcher")
            exit(1)


if __name__ == '__main__':
    main()