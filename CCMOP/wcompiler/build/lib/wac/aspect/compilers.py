from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import hashlib
import json
import string
from shutil import copyfile

import chardet as chardet

from .popenwrapper import Popen
from .arglistfilter import ArgumentListFilter

from .logconfig import logConfig

# Internal logger
_logger = logConfig(__name__)


def wcompile(mode):
    """ The workhorse, called from wllvm , wllvm++ ,war.
    """
    rc = 1
    legible_argstring = ' '.join(list(sys.argv)[1:])
    # for diffing with gclang
    _logger.info('Entering CC [%s]', legible_argstring)
    try:
        cmd = list(sys.argv)
        cmd = cmd[1:]
        #print(' '.join(cmd))
        builder = getBuilder(cmd, mode)
        flag = False
        if mode == "war":
            builder.addARLink()
        else:
            if compileStage != 'generate_make':
                af = builder.getBitcodeArglistFilter()
                if af.isEmitToObject:
                    if len(af.inputFiles) != 0:
                        if af.inputFiles[0].endswith('_instrumentation.i'):
                            return 0
                        else:
                            if not af.inputFiles[0].startswith('/usr/') and (
                                    af.inputFiles[0].endswith('.c') or af.inputFiles[0].endswith('.cpp') or
                                    af.inputFiles[0].endswith('.cc') \
                                    or af.inputFiles[0].endswith('.cxx') or af.inputFiles[0].endswith('.c++')):
                                addHeader(af)
                                flag = True
                                builder.addIncludeArg()
                                if builder.insert:
                                    updateCommand(builder, af)
                                callInsert(builder, af)

                    # we attach the linked libs
                    if af.outputFilename is not None and len(af.outputFilename) > 0:
                        outputFileName = af.outputFilename[-2:]
                        if not outputFileName == ".o" and builder.insert:
                            builder.addLinkArg()
                            #print(' '.join(builder.cmd))
        #print(' '.join(builder.cmd))
        rc = buildObject(builder)
        if flag:
            dropHeaders(af)
        if rc != 0:
            if flag:
                dropHeaders(af)
            # _logger.error('buildObject failed with %s', rc)
            sys.exit(-1)

    except Exception as e:
        _logger.warning('%s: exception case: %s', mode, str(e))

    _logger.debug('Calling %s returned %d', list(sys.argv), rc)
    return rc


# Environmental variable for path to aspect ah file
aspectAh = os.getenv('aspect_ah')
# Environmental variable for path to lib of ah
aspectLib = os.getenv('aspect_lib')
# root dir of project
rootDir = os.getenv('root_dir')
# mode of compile -sf or -proj
compileMode = os.getenv('compileMode')
compileStage = os.getenv('compile_stage')
print_flag = os.getenv("print")
# Environmental variable for path to compiler tools (clang/llvm-link etc..)
llvmCompilerPathEnv = 'LLVM_COMPILER_PATH'

fullSelfPath = os.path.realpath(__file__)
prefix = os.path.dirname(fullSelfPath)
driverDir = prefix

generateConfigFile = False


# Same as an ArgumentListFilter, but DO NOT change the name of the output filename when
# building the bitcode file so that we don't clobber the object file.
class ClangBitcodeArgumentListFilter(ArgumentListFilter):
    def __init__(self, arglist):
        localCallbacks = {'-o': (1, ClangBitcodeArgumentListFilter.outputFileCallback)}
        # super(ClangBitcodeArgumentListFilter, self).__init__(arglist, exactMatches=localCallbacks)
        super().__init__(arglist, exactMatches=localCallbacks)

    def outputFileCallback(self, flag, filename):
        self.outputFilename = filename


def writeToCompile(builder, af):
    cmd = list(builder.getCommand())
    for arg in cmd:
        if arg.startswith('-pedantic-errors'):
            index = cmd.index('-pedantic-errors')
            cmd[index] = '-pedantic'
        if arg.startswith('-Werror'):
            arg_index = cmd.index(arg)
            cmd[arg_index] = '-Wall'
        if arg.startswith('-MT'):
            global generateConfigFile
            generateConfigFile = True
    cmd.insert(0, "-Wno-empty-translation-unit")
    cmd.insert(0, "-Wno-int-conversion")
    single_file_cmd = cmd
    # builder.cmd = cmd
    compile_command = []
    for srcFile in af.inputFiles:
        objCompiler = builder.getCompiler()
        for file in af.inputFiles:
            if file != srcFile:
                single_file_cmd.remove(file)
        objCompiler.extend(single_file_cmd)
        single_command = {'arguments': objCompiler,
                          'directory': os.getcwd(),
                          'file': srcFile}
        compile_command.append(single_command)

    if rootDir is not None:
        output_file = rootDir + os.sep + "compile_commands.json"
    else:
        output_file = "compile_commands.json"
    with open(output_file, "w") as f:
        json.dump(compile_command, f)
        f.flush()
        f.close()


def callInsert(builder, af):
    # command = [f'aspectcc']
    if aspectAh is not None:
        # command.extend([f'--aspectpath={aspectAh}'])
        # if compileMode == "proj":
        #     writeToCompile(builder, af)
        print_flag = os.getenv("print")
        cmd = builder.getCommand()
        knit_lib_dir = os.getenv("ASPECT_LIB")
        if knit_lib_dir is None:
            _logger.error('ASPECT_LIB is not declared in enviroment!')
            _logger.error('Please export ASPECT_LIB=<The dir of libKnitC.so.>')
            sys.exit(-1)
        else:
            knit_lb = knit_lib_dir + "/libKnitC.so"
        new_cmd = ['-Xclang', '-load', '-Xclang', f'{knit_lb}', '-Xclang', '-add-plugin', '-Xclang', 'KnitC', '-Xclang',
                   '-plugin-arg-KnitC', '-Xclang', f'-aspectpath={aspectAh}']
        if print_flag is not None:
            new_cmd.extend(['-Xclang', '-plugin-arg-KnitC', '-Xclang', '-print'])
        new_cmd.extend(cmd)
        builder.cmd = new_cmd

    # if file[0] != '/':
    #     command.append(os.getcwd() + '/' + file)
    # else:
    #     command.append(file)
    # print((' ').join(command))
    # proc = Popen(command)
    # rc = proc.wait()
    # if rc != 0:
    #     _logger.error('callInsert failed with %s', command)
    #     sys.exit(-1)
    # command=command[0:-1]
    else:
        _logger.error('the path of ah file does not set')
        print("insert failed!")
        builder.insert = False


def updateCommand(builder, af):
    cmd = builder.getCommand()
    for arg in cmd:
        if arg.startswith('-Werror'):
            arg_index = cmd.index(arg)
            cmd[arg_index] = '-W'
        if arg.startswith('-pedantic-errors'):
            arg_index = cmd.index(arg)
            cmd[arg_index] = '-pedantic'
        if arg.startswith('-static'):
            arg_index = cmd.index(arg)
            cmd[arg_index] = '-w'

    cmd.insert(0, "-Wno-empty-translation-unit")
    cmd.insert(0, "-Wno-strict-prototypes")
    # cmd.insert(0, "-Wno-shadow")
    # cmd.insert(0, "-Wno-uninitialized")
    # cmd.insert(0, "-Wno-int-conversion")
    # cmd.insert(0, "-Wno-language-extension-token")
    # cmd.insert(0, "-Wno-declaration-after-statement")
    builder.cmd = cmd


class BuilderBase:
    def __init__(self, cmd, mode, prefixPath=None):
        self.af = None  # memoize the arglist filter
        self.cmd = cmd
        self.mode = mode
        self.insert = True

        # Used as prefix path for compiler
        if prefixPath:
            self.prefixPath = prefixPath
            # Ensure prefixPath has trailing slash
            if self.prefixPath[-1] != os.path.sep:
                self.prefixPath = self.prefixPath + os.path.sep
            # Check prefix path exists
            if not os.path.exists(self.prefixPath):
                errorMsg = 'Path to compiler "%s" does not exist'
                _logger.error(errorMsg, self.prefixPath)
                raise Exception(errorMsg)

        else:
            self.prefixPath = ''

    def getCommand(self):
        if self.af is not None:
            # need to remove things like "-dead_strip"
            forbidden = self.af.forbiddenArgs
            if forbidden:
                for baddy in forbidden:
                    self.cmd.remove(baddy)
        return self.cmd


class ClangBuilder(BuilderBase):

    def getCompiler(self):
        if self.mode == "wllvm++":
            env, prog = 'LLVM_CXX_NAME', 'clang++'
        elif self.mode == "wllvm":
            env, prog = 'LLVM_CC_NAME', 'clang'
        elif self.mode == "war":
            env, prog = 'LLVM_ar_NAME', 'llvm-ar'
        else:
            raise Exception(f'Unknown mode {self.mode}')
        return [f'{self.prefixPath}{os.getenv(env) or prog}']

    def addIncludeArg(self):
        if aspectLib is not None:
            self.cmd.insert(0, "-Wno-int-conversion")
            self.cmd.insert(0, "-I" + aspectLib)
        else:
            errorMsg = 'Path of the ASPECT_LIB does not set'
            _logger.error(errorMsg)
            exit(-1)

    def addLinkArg(self):
        if aspectLib is not None:
            # self.cmd.insert(0, "-Wl,-rpath=" + aspectLib)
            self.cmd.insert(len(self.cmd), "-L" + aspectLib)
            self.cmd.insert(len(self.cmd), '-laspect')
            if self.mode == "wllvm":
                self.cmd.insert(len(self.cmd), '-lstdc++')
            for arg in self.cmd:
                if arg.startswith('-static'):
                    arg_index = self.cmd.index(arg)
                    self.cmd[arg_index] = '-w'
        else:
            errorMsg = 'Path of the ASPECT_LIB does not set'
            _logger.error(errorMsg)
            exit(-1)
    def addARLink(self):
        if aspectLib is not None:
            self.cmd.insert(len(self.cmd),aspectLib+os.sep+'libaspect.a')
        else:
            errorMsg = 'Path of the ASPECT_LIB does not set'
            _logger.error(errorMsg)
            exit(-1)

    def getBitcodeArglistFilter(self):
        if self.af is None:
            self.af = ClangBitcodeArgumentListFilter(self.cmd)
        return self.af


def getBuilder(cmd, mode):
    compilerEnv = 'LLVM_COMPILER'
    cstring = os.getenv(compilerEnv)
    if cstring is None:
        cstring='clang'
    pathPrefix = os.getenv(llvmCompilerPathEnv)  # Optional

    _logger.debug('WLLVM compiler using %s', cstring)
    if pathPrefix:
        _logger.debug('WLLVM compiler path prefix "%s"', pathPrefix)
    if cstring == 'clang':
        return ClangBuilder(cmd, mode, pathPrefix)
    if cstring is None:
        errorMsg = ' No compiler set. Please set environment variable %s'
        _logger.critical(errorMsg, compilerEnv)
        raise Exception(errorMsg)
    errorMsg = '%s = %s : Invalid compiler type'
    _logger.critical(errorMsg, compilerEnv, str(cstring))
    raise Exception(errorMsg)


def buildObject(builder):
    objCompiler = builder.getCompiler()
    objCompiler.extend(builder.getCommand())
    #print(objCompiler)
    proc = Popen(objCompiler)
    rc = proc.wait()
    _logger.debug('buildObject rc = %d', rc)
    return rc


def addHeader(af):
    header = '#include"'
    if aspectAh is None:
        _logger.error('please export aspect_ah!')
        exit(-1)
    with open(aspectAh, 'r') as aspectFile:
        content = aspectFile.read()
        aspectName = content.split('aspect')[1].split('{')[0].strip(' ')
    header = header + "__RVC_" + aspectName + '_Monitor.h"\n'
    contents = ['#include""\n', 'source']
    for file in af.inputFiles:
        with open(file, 'rb') as enf:
            text = enf.read()
            encod = chardet.detect(text)
            endcodForfile = encod['encoding']
            # if endcodForfile is not None:
            #     if endcodForfile.find('indows') != -1:
            #         endcodForfile = 'utf-8'
        try:
            with open(file, 'r', encoding=endcodForfile) as f:
                content = f.readlines()
                if content[0].find(header) == -1:
                    contents[0] = header
                    if content[0].startswith('\n'):
                        contents[1] = "".join(content[1:])
                    else:
                        contents[1] = "".join(content)
                    with open(file, 'w', encoding=endcodForfile) as wf:
                        source = "".join(contents)
                        wf.write(source)
        except Exception as e:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.readlines()
                if content[0].find(header) == -1:
                    contents[0] = header
                    if content[0].startswith('\n'):
                        contents[1] = "".join(content[1:])
                    else:
                        contents[1] = "".join(content)
                    with open(file, 'w', encoding='utf-8') as wf:
                        source = "".join(contents)
                        wf.write(source)


def dropHeaders(af):
    header = '#include"'
    if aspectAh is None:
        _logger.error('please export aspect_ah!')
        exit(-1)
        return
    with open(aspectAh, 'r') as aspectFile:
        content = aspectFile.read()
        aspectName = content.split('aspect')[1].split('{')[0].strip(' ')
    header = header + "__RVC_" + aspectName + '_Monitor.h"\n'
    contents = ['\n', 'source']
    for file in af.inputFiles:
        with open(file, 'rb') as enf:
            text = enf.read()
            encod = chardet.detect(text)
            endcodForfile = encod['encoding']
            # if endcodForfile is not None:
            #     if  endcodForfile.find('indows') != -1:
            #         endcodForfile = 'utf-8'
            try:
                with open(file, 'r', encoding=endcodForfile) as f:
                    content = f.readlines()
                    if content[0].find(header) != -1:
                        contents[1] = "".join(content[1:])
                        with open(file, 'w', encoding=endcodForfile) as wf:
                            wf.write("".join(contents))
            except Exception as e:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.readlines()
                    if content[0].find(header) != -1:
                        contents[1] = "".join(content[1:])
                        with open(file, 'w', encoding='utf-8') as wf:
                            wf.write("".join(contents))
