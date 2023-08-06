import exceptions
import logging
import os
import re
import subprocess
import sys
import unittest

CRAM = 1
JUNIT = 2
NOSE = 3

class ParseException(exceptions.Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

class SubunitWriter(object):

    def __init__(self, label):
        self.count = 0
        # A label that makes it easier to identify failing
        # test(s).
        self.dir = label

    def bad(self):
        self.count = self.count + 1
        s = self._getteststr()
        return os.linesep.join(['test %s' % s  , 'failure %s' % s]) 

    def good(self):
        self.count = self.count + 1
        s = self._getteststr()
        return os.linesep.join(['test %s' % s  , 'success %s' % s]) 

    def preamble(self, reallyrun):
        return ''

    def _getteststr(self):
        return 'test-%s %d' % (self.dir, self.count)

class TapWriter(object):

    def bad(self):
        return 'not ok'

    def good(self):
        return 'ok'

    def preamble(self, reallyrun):
        return '1..%d' % reallyrun

class CramSummaryParser(object):

    def _getsummary(self, lines):
        # Summary is on last line of output.
        summary = lines[-1]
        return summary

    def _getresult(self, summary):
        '''
        >>> CramSummaryParser()._getresult('# Ran 1001 tests, 333 skipped, 227 failed.')
        (441, 227, 333, 0)
        '''
        match = re.match('\D+(\d+)\D+(\d+)\D+(\d+)\D+', summary)
        total = int(match.group(1))
        skipped = int(match.group(2))
        failed = int(match.group(3))
        success = total - skipped - failed
        return success, failed, skipped, 0

    def getresult(self, lines):
        summary = self._getsummary(lines)
        return self._getresult(summary)

class JUnitSummaryParser(object):

    def _getsummary(self, lines):
        # Junit output has an additional blank line after the summary line.
        summary = lines[-2]
        return summary

    def _getresult(self, summary):
        '''
        >>> JUnitSummaryParser()._getresult('Tests run: 7,  Failures: 1,  Errors: 2')
        (4, 1, 0, 2)
        >>> JUnitSummaryParser()._getresult('Tests run: 700,  Failures: 101, \
                >>> Errors: 229')
        (370, 101, 0, 229)
        >>> JUnitSummaryParser()._getresult('OK (7891 tests)')
        (7891, 0, 0, 0)
        '''
        if summary.startswith('OK'):
            match = re.match('\D+(\d+)', summary)
            total = int(match.group(1))
            failed = error = 0
        else:
            # Junit result line ends in a nummber, in contrast to cram output
            # which has additional text after the last number.
            match = re.match('\D+(\d+)\D+(\d+)\D+(\d+)', summary)
            total = int(match.group(1))
            failed = int(match.group(2))
            error = int(match.group(3))
        success = total - failed - error
        # Skipped is not a test outcome in Junit.
        return success, failed, 0, error

    def getresult(self, lines):
        summary = self._getsummary(lines)
        return self._getresult(summary)

class NoseSummaryParser(object):
    '''
    Nose parser is different because output is spread over three lines, so we're
    not talking about a single summary line here.
    '''

    def _getresult(self, summary):
        success = total - skipped - failed
        return success, failed, skipped, 0

    def getresult(self, lines):
        success = failed = skipped = error = 0
        summary = lines[-3]
        matchtotal = re.match('Ran (\d+)\D+', summary)
        total = int(matchtotal.group(1))
        resultline = lines[-1]
        if resultline.startswith('OK'):
            success = total

        # Nose doesn't show the number of failed tests when there are errors, it
        # just ends up displaying the errors.
        elif resultline.startswith('FAILED (errors='):
            matchresult = re.match('\D+(\d+)\D+', resultline)
            error = int(matchresult.group(1))
            success = total - error
        elif resultline.startswith('FAILED (failures='):
            matchresult = re.match('\D+(\d+)\D+', resultline)
            failed = int(matchresult.group(1))
            success = total - failed
        else:
            raise ParseException('Cannot handle result line "%s"' % resultline)

        # Skipped is not a test outcome in Nose tests.
        return success, failed, skipped, error

def _convert(writer, instream, outstream, sourcetype=CRAM):
    '''
    Parse the summary string of cram- and Junit test and put out test results. 
    
    TODO: 
     * Parse more than the summary. Failing tests can be found in the 'Failed
      ...' lines. To find the names of all tests, so you can show the name of
      successful tests, too, you have to run cram in verbose mode.
    '''
    parsermap = {CRAM: CramSummaryParser,
            JUNIT: JUnitSummaryParser,
            NOSE: NoseSummaryParser}
    summaryparser = parsermap.get(sourcetype)()
    lines = instream.readlines()
    success, failed, skipped, error = summaryparser.getresult(lines)
    total = success + failed + skipped + error 
    p = writer.preamble(total)
    if p:
        outstream.write(p)
        outstream.write(os.linesep)
    outputmethod = (
            writer.good, # success.
            writer.bad, # failed.
            writer.good, # skipped.
            writer.bad) # error.
    testcount = 0
    for index, count in enumerate((success, failed, skipped, error)):
        method = outputmethod[index]
        for c in range(0, count):
            outstream.write(method())
            outstream.write(os.linesep)
            testcount += 1

def cram2subunit(instream, outstream, label):
    return _convert(SubunitWriter(label), instream, outstream)

def cram2tap(instream, outstream):
    return _convert(TapWriter(), instream, outstream)

def junit2tap(instream, outstream):
    return _convert(TapWriter(), instream, outstream, sourcetype=JUNIT)

def nose2tap(instream, outstream):
    return _convert(TapWriter(), instream, outstream, sourcetype=NOSE)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
