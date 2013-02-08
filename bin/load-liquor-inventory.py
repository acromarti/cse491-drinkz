#! /usr/bin/env python
import sys
import _mypath

from drinkz.load_bulk_data import load_bottle_types, load_inventory

def main(args):
   if len(args) != 2:
      print >>sys.stderr, 'Usage: %s file_to_load.csv'
      return -1

   filename = args[1]

   fp = open(filename)
   try:
      n = load_bottle_types(fp)
   finally:
      fp.close()

   fp = open(filename)
   try:
      o = load_inventory(fp)
   finally:
      fp.close()

   print 'Loaded %d bottle types.' % n
   print 'Loaded inventory', % o
   return 0
    
# run the 'main()' function if this script is run from the command line;
# this will not execute if the file is imported.
#
# pass in command line arguments verbatim, as a list.

if __name__ == '__main__':
   exit_code = main(sys.argv)
   sys.exit(exit_code)
