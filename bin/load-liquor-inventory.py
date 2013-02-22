#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import _mypath

from drinkz.load_bulk_data import load_inventory, load_bottle_types


def main(args):
   if len(args) != 3:
      print >>sys.stderr, 'Usage: %s file_to_load.csv'
      return -1
   
   types = args[1]
   amount = args[2]
   
   fp = open(types)
   
   try:
      n = load_bottle_types(fp)
   finally:
      fp.close()

   fp = open(amount)
   try:
      o = load_inventory(fp)
   finally:
      fp.close()

   #print 'Loaded %d bottle types.' % n
   #print 'Loaded %d amounts', % o
   return 0
    
# run the 'main()' function if this script is run from the command line;
# this will not execute if the file is imported.
#
# pass in command line arguments verbatim, as a list.

if __name__ == '__main__':
   exit_code = main(sys.argv)
   sys.exit(exit_code)


if __name__ == '__main__':
   exit_code = main(sys.argv)
   sys.exit(exit_code)

def test1():

  	scriptpath = 'bin/load-liquor-inventory'

  	module = imp.load_source('lli', scriptpath)

  	exit_code = module.main([scriptpath, 'test-data/test2.txt'])

        assert exit_code == 0, 'non zero exit code %s' % exit_code

def test2():

  	scriptpath = 'bin/load-liquor-inventory'

	module = imp.load_source('lli', scriptpath)

  	exit_code = module.main([scriptpath, 'test-data/test1.txt'])

  	assert exit_code == 0, 'non zero exit code %s' % exit_code

test1
test2