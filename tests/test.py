#!/usr/bin/env python

import os
import os.path
import tempfile
import subprocess
import time
import signal
import re
import sys
import shutil
import decode_out as dec
import csv
import abc

#file_locations = os.path.expanduser(os.getcwd())
file_locations = '.'
#logisim_location = os.path.join(os.getcwd(),"logisim.jar")
logisim_location = "logisim.jar"


class TestCase():
  """
      Runs specified circuit file and compares output against the provided reference trace file.
  """

  def __init__(self, circfile, expected):
    self.circfile  = circfile
    self.expected = expected

  def __call__(self, typ):
    oformat = dec.get_test_format(typ)
    if not oformat:
        print "CANNOT format test type called [{}]".format(typ)
        return (False, "Error in the test")

    try:
        if not isinstance(self.expected, list):
            # it is a file so parse it
            self.expected = [x for x in ReferenceFileParser(oformat, self.expected).outputs()]
        else:
            [oformat.validate(x) for x in self.expected]
    except dec.OutputFormatException as e:
        print "Error in formatting of expected output (check test.py if this is a test you wrote):"
        print "\t", e
        return (False, "Error in the test")

    output = tempfile.TemporaryFile(mode='r+')
    command = ["java","-jar",logisim_location,"-tty","table", self.circfile]
    proc = subprocess.Popen(command,
                            stdin=open(os.devnull),
                            stdout=subprocess.PIPE)
    try:
      debug_buffer = [] 
      passed = compare_unbounded(proc.stdout,self.expected, oformat, debug_buffer)
    except dec.OutputFormatException as e:
        print "Error in formatting of Logisim output (check {}):".format(self.circfile)
        print "\t", e
        return (False, "Error in the test")
    finally:
      if os.name != 'nt':
        os.kill(proc.pid,signal.SIGTERM)
    if passed:
      return (True, "Matched expected output")
    else:
      print "Format is student then expected"
      wtr = csv.writer(sys.stdout, delimiter='\t')
      oformat.header(wtr)
      for row in debug_buffer:
        wtr.writerow(['{0:x}'.format(b) for b in row[0]])
        wtr.writerow(['{0:x}'.format(b) for b in row[1]])

      return (False, "Did not match expected output (check {}, also check test.py if this is a test you wrote)".format(self.circfile))

def compare_unbounded(student_out, expected, oformat, debug):
  parser = OutputProvider(oformat)
  for i in range(0, len(expected)):
    line1 = student_out.readline()
    values_student_parsed = parser.parse_line(line1.rstrip())

    debug.append((values_student_parsed, expected[i]))

    if values_student_parsed != expected[i]:
      return False

  return True

def run_tests(tests):
  # actual submission testing code
  print "Testing files..."
  tests_passed = 0
  tests_failed = 0

  for description,test,typ in tests:
    test_passed, reason = test(typ)
    if test_passed:
      print "\tPASSED test: %s" % description
      tests_passed += 1
    else:
      print "\tFAILED test: %s (%s)" % (description, reason)
      tests_failed += 1
  
  print "Passed %d/%d tests" % (tests_passed, (tests_passed + tests_failed))

class OutputProvider(object):
    def __init__(self, format):
        self.format = format

    @abc.abstractmethod
    def outputs(self):
        pass
    
    def parse_line(self, line):
        value_strs = line.split('\t')   
        values_bin = [''.join(v.split(' ')) for v in value_strs] 
        try:
            values = [int(v, 2) for v in values_bin]
        except ValueError as e:
            if values_bin == ['']:
                raise dec.OutputFormatException("you have a non-integer in this list: {}. If this is logisim output, are you sure you have a circ file for this test?".format(values_bin))
            else :
                raise dec.OutputFormatException("you have a non-integer in this list: {}".format(values_bin))
        self.format.validate(values)
        return values

class ReferenceFileParser(OutputProvider):
    def __init__(self, format, filename=None):
        self.f = filename
        super(ReferenceFileParser, self).__init__(format)

    def outputs(self):
        assert self.f is not None, "cannot use outputs if no filename given"
        with open(self.f, 'r') as inp:
            for line in inp.readlines():
                values = self.parse_line(line)
                yield values 

p1_tests = [
  ("ALU add (with overflow) test, with output in python",
        TestCase(os.path.join(file_locations,'alu-add.circ'),
                 [[0, 0, 0, 0x7659035D],
                  [1, 1, 0, 0x87A08D79],
                  [2, 1, 0, 0x80000000],
                  [3, 0, 1, 0x00000000],
                  [4, 0, 0, 0x00000000],
                  [5, 0, 0, 0x00000227],
                  [6, 1, 0, 0x70000203],
                  [7, 0, 0, 0xFFFFFEFF],
                  [8, 0, 1, 0x00000000],
                  [9, 0, 1, 0x00000000],
                  [10, 0, 1, 0x00000000],
                  [11, 0, 1, 0x00000000],
                  [12, 0, 1, 0x00000000],
                  [13, 0, 1, 0x00000000],
                  [14, 0, 1, 0x00000000],
                  [15, 0, 1, 0x00000000]]), "alu"),
  ("ALU arithmetic right shift test",
        TestCase(os.path.join(file_locations,'alu-sra.circ'),
                [[0, 0, 0, 0xF7AB6FBB],
                 [1, 0, 0, 0xFFFFFC00],
                 [2, 0, 0, 0x00000000],
                 [3, 0, 0, 0xFEEDF00D],
                 [4, 0, 1, 0x00000000],
                 [5, 0, 1, 0x00000000],
                 [6, 0, 1, 0x00000000],
                 [7, 0, 1, 0x00000000],
                  [8, 0, 1, 0x00000000],
                  [9, 0, 1, 0x00000000],
                  [10, 0, 1, 0x00000000],
                  [11, 0, 1, 0x00000000],
                  [12, 0, 1, 0x00000000],
                  [13, 0, 1, 0x00000000],
                  [14, 0, 1, 0x00000000],
                  [15, 0, 1, 0x00000000]]), "alu"),
  ("RegFile read/write test",
        TestCase(os.path.join(file_locations,'regfile-read_write.circ'),
                [[0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [2, 0x0, 0x0, 0x0, 0x0, 0x0, 0xBAD00DAD, 0xBAD00DAD],
                 [3, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [5, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10101010],
                 [6, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10101010, 0x0],
                 [7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]]), "regfile"),
  ("RegFile $zero test",
        TestCase(os.path.join(file_locations,'regfile-zero.circ'),
                [[0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [3, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [5, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]]), "regfile"),
  ("RegFile debug outputs test",
        TestCase(os.path.join(file_locations,'regfile-debug_outputs.circ'),
                [[0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [2, 0xBAD00DAD, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [3, 0xBAD00DAD, 0xFEEDF00D, 0x0, 0x0, 0x0, 0x0, 0x0],
                 [4, 0xBAD00DAD, 0xFEEDF00D, 0x12345678, 0x0, 0x0, 0x0, 0x0],
                 [5, 0xBAD00DAD, 0xFEEDF00D, 0x12345678, 0x10101010, 0x0, 0x0, 0x0],
                 [6, 0xBAD00DAD, 0xFEEDF00D, 0x12345678, 0x10101010, 0xDADADADA, 0x0, 0x0],
                 [7, 0xBAD00DAD, 0xFEEDF00D, 0xBABABABA, 0x10101010, 0xDADADADA, 0x0, 0x0]]), "regfile")
]

# Single-cycle (sc) tests
p2sc_tests = [
  ("CPU starter test",
          TestCase(os.path.join(file_locations,'CPU-starter_kit_test.circ'),
                  [[0, 0, 0, 0x0, 0x0, 0, 0x0, 0x20100001],
                   [1, 0, 0, 0x0, 0x0, 1, 0x4, 0x20110002],
                   [1, 2, 0, 0x0, 0x0, 2, 0x8, 0x02119020],
                   [1, 2, 3, 0x0, 0x0, 3, 0xC, 0x00000000],
                   [1, 2, 3, 0x0, 0x0, 4, 0x10, 0x00000000]
                   ]), "cpu"),
  
  ("adding test",
          TestCase(os.path.join(file_locations,'test_adding.circ'),
                  [[0,0,0,0],
                   [1,0,0,0],
                   [1,2,0,0],
                   [1,2,3,0],
                   [5,2,3,0],
                   [0XFFFFFFFF,2,3,0],
                   [0XFFFFFFFF,2,0xFFFFFFFB,0],
                   [0xFFFFFFFD,2,0xFFFFFFFB,0],
                   [0xFFFFFFFD,0xFFFFFFFD,0xFFFFFFFB,0],
                   [0xFFFFFFFD,0xFFFFFFF8,0xFFFFFFFB,0],
                   [0xFFFFFFF5,0xFFFFFFF8,0xFFFFFFFB,0],
                   [0xFFFFFFF5,0xFFFFFFF8,0xFFFFFFED,0],
                   [0xFFFFFFE5,0xFFFFFFF8,0xFFFFFFED,0]
                   ]), "cpu-end"),
  
  ("bitwise test",
          TestCase(os.path.join(file_locations,'test_bitwise.circ'),
                  [[0,0,0,0],
                   [0,1,0,0],
                   [0,1,1,0],
                   [0,1,0,0]
                   ]), "cpu-end"),
  
  ("comparison test",
          TestCase(os.path.join(file_locations,'test_comparison.circ'),
                  [[0,0,0,0],
                   [1,0,0,0],
                   [1,0xFFFFFFFE,0,0],
                   [1,0xFFFFFFFE,1,0],
                   [1,0xFFFFFFFE,0,0],
                   [1,0xFFFFFFFE,1,0],
                   [1,0xFFFFFFFE,0,0],
                   [1,0xFFFFFFFE,1,0],
                   [1,0xFFFFFFFE,0,0],
                   [1,0xFFFFFFFE,1,0],
                   [1,0xFFFFFFFE,0,0],
                   [1,0xFFFFFFFE,1,0],
                   [1,0xFFFFFFFE,0,0]
                   ]), "cpu-end"),
  
  ("shift test",
          TestCase(os.path.join(file_locations,'test_shift.circ'),
                  [[0,0,0,0],
                   [1638400,0,0,0],
                   [1640210,0,0,0],
                   [1640210,820105,0,0],
                   [1640210,820105,6407,0],
                   [6560768,820105,6407,0],
                   [6560768,102512,6407,0],
                   [6560768,102512,0xFFFF0000,0],
                   [6560768,102512,0xFFFFFF00,0]
                   ]), "cpu-end"),
    
  ("lw/sw test",
          TestCase(os.path.join(file_locations,'test_lw_sw.circ'),
                  [[0,0,0,0],
                   [8196,0,0,0],
                   [8196,5,0,0],
                   [8196,5,5,0],
                   [8196,5,10,0]
                   ]), "cpu-end"),
    
  ("branch test",
          TestCase(os.path.join(file_locations,'test_branch.circ'),
                  [[0,0,0,0],
                   [1,0,0,0],
                   [1,1,0,0],
                   [2,1,0,0],
                   [2,2,0,0]
                   ]), "cpu-end"),
  
  
  ("jump test",
          TestCase(os.path.join(file_locations,'test_jump.circ'),
                  [[0,0,0,0,0,0],
                   [0,0,0,0,0,1],
                   [5,0,0,0,0,2],
                   [5,0,0,40,0,3],
                   [5,11,0,40,0,4],
                   [5,11,0,40,0,5],
                   [5,16,0,40,0,6],
                   [5,16,0,40,0,7],
                   [5,21,0,40,0,8],
                   [5,21,0,12,0,9],
                   [5,26,0,12,0,10],
                   [5,26,0,12,0,11],
                   [5,26,0,12,0,12],
                   [5,0,0,12,0,13],
                   [0,0,0,12,0,14]
                   ]), "cpu-lite"),
  
  ("multiply test",
          TestCase(os.path.join(file_locations,'mult_test.circ'),
                  [[0,0,0,0],
                   [50,0,0,0],
                   [50,200,0,0],
                   [50,200,10000,0],
                   [50,200,500000,0],
                   [50,200,100000000,0],
                   [50,4,100000000,0],
                   [50,4,0xA817C800,0],
                   [0xFFFFFFEC,4,0xA817C800,0],
                   [0xFFFFFFEC,0xFFFFFFFF,0xA817C800,0],
                   [0xFFFFFFEC,0xFFFFFFFF,0xFFFFFFB0,0]
                   ]), "cpu-end"),
  
  ("func test",
          TestCase(os.path.join(file_locations,'func_test.circ'),
                  [[0,0,0,0],
                   [36,0,0,0],
                   [36,16,0,0]
                   ]), "cpu-end")
]

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " (p1|p2sc)")
    sys.exit(-1)
  if sys.argv[1] == 'p1':
    run_tests(p1_tests)
  elif sys.argv[1] == 'p2sc':
    run_tests(p2sc_tests)
  else:
    print("Usage: " + sys.argv[0] + " (p1|p2)")
    sys.exit(-1)
