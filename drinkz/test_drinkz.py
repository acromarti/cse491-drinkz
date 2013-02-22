# -*- coding: utf-8 -*-
"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from . import db, load_bulk_data
from cStringIO import StringIO
import imp

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n


def test_bulk_load_inventory_2():

	#handles comment out lines

	db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

	data = "#Johnnie Walker,Black Label,1000 ml"
	fp = StringIO(data)                 # make this look like a file handle
    	n = load_bulk_data.load_inventory(fp)

	assert n == 0, n


def test_bulk_load_inventory_3():

	#handles whitespace lines

	db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

	data = "        "
	fp = StringIO(data)                 # make this look like a file handle
    	n = load_bulk_data.load_inventory(fp)

	assert n == 0, n


def test_bulk_load_inventory_4():

	#handles good file

	db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

	fp = open('test-data/inventory-data-1.txt')
    	n = load_bulk_data.load_inventory(fp)

	assert n == 1, n

def test_bulk_load_inventory_5():

	#handles whitespace lines and commented out lines

	db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

	fp = open('test-data/inventory-data-2.txt')
    	n = load_bulk_data.load_inventory(fp)

	assert n == 1, n

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    print amount
    assert amount == '1000.0', amount

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == '1000.0', amount


def test_get_liquor_amount_3():

    #handles test when the amount input is oz

    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == '29573.5', amount


def test_get_liquor_amount_4():

    #this test handles when the amount input is oz

    db._reset_db()    

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label, 1000 oz"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == '29573.5', amount

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data) # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n


def test_bulk_load_bottle_types_2():
   
   # this test return n as 0 which makes the data not present in the bottle
   # bottle type data base which makes x == 0
   #handles commented out lines
  
    db._reset_db()
    

    data = "#Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data) # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)
    x = db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
    assert x == 0, x
    assert n == 0, n

def test_bulk_load_bottle_types_3():

    #handles whitespace lines
    # this test return n as 0 which makes the data not present in the bottle
   # bottle type data base which makes x == 0
    db._reset_db()

    data = "         "
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    x = db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
    assert x == 0, x
    assert n == 0, n

def test_bulk_load_bottle_types_4():

    #handles loading good bottle type file
    db._reset_db()

    fp = open('test-data/bottle-types-data-1.txt')
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n


def test_bulk_load_bottle_types_5():

    #handles files with commented lines and whitespace lines
    # this test return n as 1 because in the text file the first two lines are skipped 
    # and the last line is readable which makes n and x == 1
    db._reset_db()

    fp = open('test-data/bottle-types-data-2.txt')
    n = load_bulk_data.load_bottle_types(fp)
    x = db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
    assert x == 1, x
    assert n == 1, n
    
def test_bulk_load_bottle_types_6():

    #handles files with commented lines and whitespace lines
    # this test return n as 1 because in the text file the last line is readable 
    # and the first line is skipped which is the name of the bottle type that is checked
    # si x == 0
    db._reset_db()

    fp = open('test-data/bottle-types-data-3.txt')
    n = load_bulk_data.load_bottle_types(fp)
    x = db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
    assert x == 0, x
    assert n == 1, n


def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x
    
    
    
def test_get_liquor_amount_gallon():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1 gallon"
    fp = StringIO(data) # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    
    print amount
    
    assert amount == '3785.41', amount
    
    
def test_uniqify_inventory():
    """
Ensure that get_liquor_inventory doesn't return duplicates.
"""
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '500 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '25 ml')

    uniq = set()
    for mfg, liquor in db.get_liquor_inventory():
        assert (mfg, liquor) not in uniq, "dup: %s, %s" % (mfg, liquor)
        uniq.add((mfg, liquor))

    assert len(uniq) == 1, "should only be one mfg/liquor in inventory"
    
    
    
def test_script_load_liquor_inventory():
    db._reset_db()

    scriptpath = 'bin/load-liquor-inventory.py'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt',
                             'test-data/inventory-data-4.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    print amount
    assert amount == '1234.0'
