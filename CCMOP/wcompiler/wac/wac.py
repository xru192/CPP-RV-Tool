#!/usr/bin/env python

import argparse
import sys
import os

from wac.project_compiler.project_compiler import *
from wac.project_compiler.single_file_compiler import *
from wac.utils.utils import *

_logger = logWcompilerConfig(__name__)


# Currently, I suggest that this script should be run in the virtual python environment of IDE. You can install it by:
#   pip3 install -e .
# please check the following:
#   1) clang, clang++.

# For the usage of wac, there are following typical scenarios (all the file names are suggested to be absolute):

# 1) If you just want to compile  (all of the following will generate <project_name>_config.json):
#    a) for a project:       wac  -proj <project_build_json_file>
#    b) for single file:     wac  [-cxx] -mop <mop_file>


# For logging configuration, we have following three environment variables:
# 1) WCOMPILER_OUTPUT_LEVEL, which can be 'ERROR', 'WARNING', 'INFO', or 'DEBUG', and default one is WARNING
# 2) WCOMPILER_OUTPUT_FILE, i.e., the logging file, which is disabled if empty or not exists
# You can control the logging in different details and output styles. DEBUG is the most detailed.


def clearFolder(folder):
    old_folder = os.curdir
    os.system('rm -f {0}/*.bc'.format(folder))
    os.system('rm -f {0}/*.o'.format(folder))
    os.system('find {0} -name "*_instrument*"  | xargs rm -f'.format(folder))
    os.chdir(old_folder)
#find ./ -name "*_instrument*"  | xargs rm -f
# mkdir build
# cd build
# export CXX=clang++
# cmake ..

mop_arg_list=['--cxx','-cxx','--mop-file','-mop','--project-build-json-file', '-proj','--print','-print','-h','--help']
def main():
    mop_args=[]
    compile_args=[]
    for arg in sys.argv[1:]:
        if arg.split('=')[0] in mop_arg_list or arg.endswith('.mop') or arg.endswith('.json'):
            mop_args.append(arg)
        else:
            compile_args.append(arg)

    # print("".join(compile_args))
    parser = argparse.ArgumentParser()
    # singfile compile
    #parser.add_argument('--single-file-compile', default=False, action='store_true', help='Compile a single file')
    parser.add_argument('--cxx','-cxx',default=False, action='store_true', help='Set the compiler to cpp(Default C).')
    parser.add_argument('--mop-file', '-mop', action='store', type=str, help='The path of mop file.')


    # project compile
    #parser.add_argument('--project-compile', default=False, action='store_true', help='Compile a project')
    parser.add_argument('--project-build-json-file', '-proj', action='store', type=str,
                        help='The Project Json config file.')

    # common arguments
    parser.add_argument('--print','-print',default=False,action='store_true',help='Output the instrumented file.')
    # # input file path of mop file or path of aspect directory
    # parser.add_argument('--mop-file', '-mop', action='store', type=str, help='The path of mop file.')
    # parser.add_argument('--cxx','-cxx',default=False, action='store_true', help='Output the instrumented file.')
    # parser.add_argument('--aspect-directory-', '-aspect', action='store', type=str,
    #                     help='The directory path of aspect.')

    args = parser.parse_args(mop_args)

    # Compile the project
    if  args.project_build_json_file:
    #if args.project_compile and args.project_build_json_file:
        pc = ProjectCompiler(args.project_build_json_file,args.print)
        clearFolder(pc.project_root_dir)
        pc.compile()
        exit(0)

    # Compile the project
    if  args.mop_file:
    #if args.project_compile and args.project_build_json_file:
        sf = SingleFileCompiler(args.mop_file,args.print,args.cxx,compile_args)
        clearFolder(os.path.dirname(sf.full_file_name))
        sf.compile()
        exit(0)


if __name__ == '__main__':
    sys.exit(main())
