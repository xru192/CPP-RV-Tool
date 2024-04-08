import logging
import collections
import os
import re
import sys

# Internal logger
_logger = logging.getLogger(__name__)


class ArgumentListFilter:
    def __init__(self, inputList, exactMatches={}, patternMatches={}):
        defaultArgExactMatches = {
            '-o' : (1, ArgumentListFilter.outputFileCallback),
            '/dev/null' : (0, ArgumentListFilter.inputFileCallback),
            '-Wl,-dead_strip' :  (0, ArgumentListFilter.warningLinkUnaryCallback),
            '-dead_strip' :  (0, ArgumentListFilter.warningLinkUnaryCallback),
            '-E': (0, ArgumentListFilter.preProcessCallback),
        }


        defaultArgPatterns = {
            r'^.+\.(c|cc|cpp|C|cxx|i|s|S|bc)$' : (0, ArgumentListFilter.inputFileCallback),
            r'^.+\.([fF](|[0-9][0-9]|or|OR|pp|PP))$' : (0, ArgumentListFilter.inputFileCallback),
            r'^.+\.(o|lo|So|so|po|a|dylib)$' : (0, ArgumentListFilter.objectFileCallback),
            r'^.+\.dylib(\.\d)+$' : (0, ArgumentListFilter.objectFileCallback),
            r'^.+\.(So|so)(\.\d)+$' : (0, ArgumentListFilter.objectFileCallback)
        }

        self.inputList = inputList
        self.inputFiles = []
        self.objectFiles = []
        self.outputFilename = None
        self.compileArgs = []
        self.linkArgs = []
        self.forbiddenArgs = []
        self.isEmitToObject=True

        argExactMatches = dict(defaultArgExactMatches)
        argExactMatches.update(exactMatches)
        argPatterns = dict(defaultArgPatterns)
        argPatterns.update(patternMatches)

        self._inputArgs = collections.deque(inputList)
        while (self._inputArgs):
            currentItem = self._inputArgs.popleft()
            _logger.debug('Trying to match item %s', currentItem)
            if currentItem in argExactMatches:
                (arity, handler) = argExactMatches[currentItem]
                flagArgs = self._shiftArgs(arity)
                handler(self, currentItem, *flagArgs)
            else:
                for pattern, (arity, handler) in argPatterns.items():
                    if re.match(pattern, currentItem):
                        flagArgs = self._shiftArgs(arity)
                        handler(self, currentItem, *flagArgs)
                        if pattern == '^-Wl,.+$':
                            while len(self._inputArgs) > 0 and re.match('.*lib.+.so.*', self._inputArgs[0]):
                                handler(self, self._inputArgs[0])
                                self._inputArgs.popleft()
                        break

    def _shiftArgs(self, nargs):
        ret = []
        while nargs > 0:
            a = self._inputArgs.popleft()
            ret.append(a)
            nargs = nargs - 1
        return ret

    def preProcessCallback(self,flag):
        self.isEmitToObject=False
    def inputFileCallback(self, infile):
        _logger.debug('Input file: %s', infile)
        self.inputFiles.append(infile)
        if re.search('\\.(s|S)$', infile):
            self.isAssembly = True

    def outputFileCallback(self, flag, filename):
        _logger.debug('outputFileCallback: %s %s', flag, filename)
        self.outputFilename = filename

    def objectFileCallback(self, objfile):
        _logger.debug('objectFileCallback: %s', objfile)
        self.objectFiles.append(objfile)


    def warningLinkUnaryCallback(self, flag):
        _logger.debug('warningLinkUnaryCallback: %s', flag)
        _logger.warning('The flag "%s" cannot be used with this tool; we are ignoring it', flag)
        self.forbiddenArgs.append(flag)

    def getOutputFilename(self):
        if self.outputFilename is not None:
            return self.outputFilename
        if self.isCompileOnly:
            (_, base) = os.path.split(self.inputFiles[0])
            (root, _) = os.path.splitext(base)
            return f'{root}.o'
        return 'a.out'


