#!/usr/bin/env python

import os
import sys
import json

from wac.utils.utils import *
from wac.aspectlib.project import *

_logger = logWcompilerConfig(__name__)


# This class compiles a project into bitcode,
# and generates the type information of all the functions into a single Json file.
# It assumes that FunctionTypeExtractor is in the same folder of clang and the folder in the PATH environment

class ProjectCompiler(object):
    project_name = None  # project name
    project_root_dir = None  # project's root directory
    project_build_subdir = None
    project_compile_cmd = None
    project_config = None
    mop_file_path = None
    project_generate_make = None
    project_compile_make = None
    print_flag = False
    compile_lanuage = None;
    json_root=None
    # exe_or_lib_name = None  # for extract-bc
    # compile_method = None  # cmake, make, etc.
    # compile_commands = None  # compile command for the project
    # output_info_file = None  # file name for type information
    # project_build_dir = None  # build dir constructed during compiling
    # compile_libs_str = None  # linked libs for compiling (to be automatically extracted)
    # function_json_file = None  # function Json file for DSE
    # bitcode_file_name = None  # bitcode file name

    def __init__(self, project_info_file, print_flag):

        # Parse project_info.json
        if not os.path.isabs(project_info_file):
            project_info_file = os.getcwd() + os.sep + os.path.basename(project_info_file)
        self.print_flag = print_flag
        with open(project_info_file, "r") as f:
            project_info = json.load(f)
        self.json_root=os.path.dirname(project_info_file)
        self.project_name = project_info["project_name"]
        self.project_root_dir = project_info["project_root_dir"]
        if not os.path.isabs(self.project_root_dir):
            self.project_root_dir=self.json_root+os.sep+project_info["project_root_dir"]
        self.project_build_subdir = project_info["project_build_subdir"]
        self.project_compile_cmd = project_info["project_compile_cmd"]
        self.mop_file_path = project_info["mop_file"]
        if not os.path.isabs(self.mop_file_path):
            self.mop_file_path = self.json_root + os.sep + project_info["mop_file"]
        self.compile_lanuage = project_info["compile_language"]
        self.splitCmd()
        if not self.mop_file_path:
            _logger.error('mop_file attribute must be declared in configure json!')
            exit(-1)

    def compile(self):
        compileMode = "proj"
        old_dir = os.curdir
        os.chdir(self.project_root_dir)
        build_dir = self.project_root_dir
        if len(self.project_build_subdir) > 0:
            build_dir = self.project_root_dir + os.sep + self.project_build_subdir
            if os.path.exists(build_dir):
                _logger.error("The build directory already exists!")
                os.system("rm -rf " + build_dir)
            os.mkdir(self.project_build_subdir)
            os.chdir(build_dir)
        if self.project_generate_make is not None:
            os.putenv("compile_stage", 'generate_make')
            executeCommand(addWCCExport(self.compile_lanuage, self.project_generate_make), self.project_root_dir,
                           self.mop_file_path, compileMode, self.print_flag, self.compile_lanuage)
            if self.project_compile_make is not None:
                os.environ["compile_stage"] = 'make'
                executeCommand(self.project_compile_make, self.project_root_dir, self.mop_file_path,
                               compileMode, self.print_flag,self.compile_lanuage)
        else:
            if self.project_compile_make is not None:
                os.environ["compile_stage"] = 'make'
                executeCommand(addWCCExport(self.compile_lanuage, self.project_compile_make), self.project_root_dir,
                               self.mop_file_path,
                               compileMode, self.print_flag, self.compile_lanuage)

    def splitCmd(self):
        single_cmd = self.project_compile_cmd.split(';')
        if single_cmd[0].find("make clean") !=-1:
            self.project_compile_make = self.project_compile_cmd
            return;
        if 'make' in single_cmd[-1]:
            if len(single_cmd) == 1:
                if 'cmake' in single_cmd[0] or 'config' in single_cmd[0]:
                    self.project_generate_make = single_cmd[0]
                else:
                    self.project_compile_make = single_cmd[0]
            else:
                self.project_generate_make = (';').join(single_cmd[0:-1])
                self.project_compile_make = single_cmd[-1]



