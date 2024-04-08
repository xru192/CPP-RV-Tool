#!/usr/bin/env python
import json
import os

from wac.utils.utils import *
from wac.aspectlib.project import *

_logger = logWcompilerConfig(__name__)


# This class compiles a single file into bitcode,
# and generates the type information of all the functions into a single Json file.
# It assumes that FunctionTypeExtractor is in the same folder of clang and the folder in the PATH environment

class SingleFileCompiler(object):
    full_file_name = None
    project_config = None
    mop_file_path=None
    print_flag=False
    language='C'
    compile_args=[]
    # default_compile_command_file_name = "compile_commands.json"
    def __init__(self, mop_file,print_flag,lang,compile_args):
        if not mop_file:
            _logger.error('Argument mop_file must be declared in single_file compiler!')
            exit(-1)
        if not lang:
            self.language='C'
        else:
            self.language='CXX'
        if not os.path.isabs(mop_file):
            self.mop_file_path=os.getcwd()+os.sep+mop_file
        else:
            self.mop_file_path=mop_file
        self.print_flag=print_flag
        self.compile_args=compile_args
        if os.path.isabs(mop_file):
            self.full_file_name = mop_file
        else:
            self.full_file_name = os.getcwd() + os.sep + mop_file

    def compile(self):
        compileMode="sf"
        os.environ["compile_stage"] = 'make'
        folder_name = os.path.dirname(self.full_file_name)
        base_name = os.path.basename(self.full_file_name)
        file_name_with_prefix = os.path.splitext(base_name)[0]

        #old_dir = os.curdir
        #os.chdir(folder_name)
        #target_name = file_name_with_prefix+'.o'
        self.compile_args.insert(0,getDefaultCompiler(self.language))
        #compile_command = "{0} -c -fmcdc -g {1} -o {2}".format(getDefaultCompiler(), base_name, target_name)
        #compile_command = "{0} -c -g {1} -o {2}".format(getDefaultCompiler(), base_name, target_name)
        compile_command=" ".join(self.compile_args)
        #print(compile_command)
        executeCommand(compile_command,os.getcwd(),self.mop_file_path,compileMode,self.print_flag,self.language)






