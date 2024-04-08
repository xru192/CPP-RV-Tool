#!/usr/bin/env python
import _thread
import os
import sys
import json

import subprocess
import pprint
import logging

_logger = logging.getLogger(__name__)

_loggingEnvLevel_old = 'WCOMPILER_OUTPUT'
_loggingEnvLevel_new = 'WCOMPILER_OUTPUT_LEVEL'
_loggingDestination = 'WCOMPILER_OUTPUT_FILE'

_validLogLevels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']


def logWcompilerConfig(name):
    destination = os.getenv(_loggingDestination)

    if destination:
        logging.basicConfig(filename=destination, level=logging.WARNING, format='%(levelname)s:%(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(message)s')

    retval = logging.getLogger(name)

    # ignore old setting
    level = os.getenv(_loggingEnvLevel_new)
    if level is None:
        level='INFO'
    if level:
        level = level.upper()
        if not level in _validLogLevels:
            logging.error('"%s" is not a valid value for %s or %s. Valid values are %s',
                          level, _loggingEnvLevel_old, _loggingEnvLevel_new, _validLogLevels)
            sys.exit(1)
        else:
            retval.setLevel(getattr(logging, level))

    # Adjust the format if debugging
    if retval.getEffectiveLevel() == logging.DEBUG:
        formatter = logging.Formatter(
            '%(levelname)s::%(module)s.%(funcName)s() at %(filename)s:%(lineno)d ::%(message)s')
        for h in logging.getLogger().handlers:
            h.setFormatter(formatter)

    return retval


_logger = logWcompilerConfig(__name__)


def getDefaultCompiler(language):
    if language == 'C':
        return 'wacc'
    else:
        return 'wacxx'


def addWCCExport(language, command):
    if 'cmake ' in command:
        split = command.split('cmake')
        if len(split) == 2:
            split[0] = split[0] + 'cmake '
            # split[1]='-DCMAKE_C_COMPILER_ID=Clang -DCMAKE_AR=$(which war) '+split[1]
            split[1] = '-DCMAKE_C_COMPILER_ID=Clang  ' + split[1]
            command = ''.join(split)
    if 'cxx' in language or 'CXX' in language:
        return 'export CC=clang;export CXX=wacxx; ' + command
    else:
        return 'export CC=wacc;export CXX=clang++; ' + command


def print_msg(input, r, s):
    while r is None:
        line = input.readline()
        if len(line) > 0:
            try:
                _logger.info("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            except Exception as e:
                _logger.info("Wcompiler: %s ", str(line.strip()))
        r = s.poll()


def executeCommand(command, mop):
    buildAspect(os.getcwd(), mop)
    _logger.info("Wcompiler Executing:\n" + command + "\nin: " + os.getcwd())
    try:
        s = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=os.getcwd(), shell=True)
        r = s.poll()
        _thread.start_new_thread(print_msg, (s.stdout, r, s))
        _thread.start_new_thread(print_msg, (s.stderr, r, s))
        s.wait()
        while r is None:
            line = s.stdout.readline()
            if len(line) > 0:
                _logger.info("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            line = s.stderr.readline()
            if len(line) > 0:
                _logger.info("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            r = s.poll()
        return s
    except OSError:
        _logger.error("Wcompiler Failed to execute: %s", pprint.pformat(command))
        raise


def executeCommand(command, root, mop, compileMode, print_flag, compile_language):
    os.putenv("compileMode", compileMode)
    if print_flag:
        os.putenv("print", "1")
    compileStage = os.getenv("compile_stage")
    if compileStage == 'make':
        buildAspect(root, mop, compile_language)
    _logger.info("Wcompiler Executing:\n" + command + "\nin: " + os.getcwd())
    try:
        s = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        r = s.poll()
        _thread.start_new_thread(print_msg, (s.stdout, r, s))
        _thread.start_new_thread(print_msg, (s.stderr, r, s))
        s.wait()
        while r is None:
            line = s.stdout.readline()
            if len(line) > 0:
                _logger.info("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            line = s.stderr.readline()
            if len(line) > 0:
                _logger.error("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            r = s.poll()
        return s
    except OSError:
        _logger.error("Wcompiler Failed to execute: %s", pprint.pformat(command))
        raise


def buildAspect(root, mop, compile_language):
    old_dir = os.getcwd()
    os.chdir(root)

    file_name_prefix = mop.split('/')[-1].split('.')[0]
    aspect_dir = root + os.sep + file_name_prefix + "aspect"
    if not os.path.exists(aspect_dir):
        os.mkdir(aspect_dir)
        os.chdir(aspect_dir)
    else:
        _logger.info("%s aspect lib directory has already exists!", pprint.pformat(aspect_dir))
        _logger.info(" Regenerated aspect lib now!")
        os.chdir(aspect_dir)
        # os.system("rm -rf *")
    if 'cxx' in compile_language or 'CXX' in compile_language:
        xModel = ' -x c++ '
    else:
        xModel = ' -x c '
    rvm_file_name = file_name_prefix + ".rvm"
    file = open("install.sh", "w")
    file.write("#!/bin/bash\n")
    file.write("cmop -v -d . " + mop + "\n")
    file.write("rv-monitor -c -p " + rvm_file_name + "\n")
    file.write(f"clang++  -O3  -fPIC -c  *.cc\n")
    file.write("clang -r -o libaspect.a *.o\n")
    file.write("echo \"The aspect library  have been generated.\"\n")

    file.close()
    # os.system("clang  -fPIC -shared  *.c -o libaspect.so")
    os.system("chmod +x install.sh")

    try:
        s = subprocess.Popen("./install.sh", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        r = s.poll()
        _thread.start_new_thread(print_msg, (s.stdout, r, s))
        _thread.start_new_thread(print_msg, (s.stderr, r, s))
        s.wait()
        while r is None:
            line = s.stdout.readline()
            if len(line) > 0:
                _logger.info("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            line = s.stderr.readline()
            if len(line) > 0:
                _logger.info("Wcompiler: %s ", str(line.strip(), 'utf-8'))
            r = s.poll()
    except OSError:
        _logger.error("Wcompiler Failed to execute: %s", pprint.pformat("./install.sh"))
        raise
    # os.system("./install.sh")
    aspect_lib = aspect_dir
    aspect_ah = aspect_dir + os.sep + file_name_prefix + "MonitorAspect.ah"
    os.putenv("aspect_ah", aspect_ah)
    os.putenv("aspect_lib", aspect_lib)
    os.putenv('root_dir', root)
    os.chdir(old_dir)


def checkAndFixConfig():
    os.environ['LLVM_COMPILER'] = 'clang'


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, filename='t.log')
    _logger.error('abc')
