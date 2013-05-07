# -*- coding: utf-8 -*-
"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

from . import recipes


def data_reader(fp):

	reader = csv.reader(fp)
	x = []
	
	for line in reader:
        	if not line or not line[0].strip() or len(line) == 0 or line[0].startswith('#'):
            		continue
		   
        	yield line
        	
def recipe_reader(fp):

	reader = csv.reader(fp)
	x = []
	
	for line in reader:
        	if not line or not line[0].strip() or len(line) == 0 or line[0].startswith('#'):
            		continue
		recipe = line
		   
        	yield recipe


def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)

    x = []
    n = 0
    for line in new_reader:
	try:
	    (mfg, name, typ) = line
	except ValueError:
	    print 'Badly formatted line: %s' % line
	    continue
	  
	n += 1
	db.add_bottle_type(mfg, name, typ)

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0
    for line in new_reader:
	try:
	    (mfg, name, amount) = line
	except ValueError:
	    print 'Badly formatted line: %s' % line
	    continue
	  
	n += 1
	db.add_to_inventory(mfg, name, amount)

    return n
    
def load_recipes(fp):

    new_reader = recipe_reader(fp)
    
    n = 0

    while(1):
        try:
            for(recipe) in new_reader: #each line represents a recipe
                name = recipe[0] 
                
                i = 1
                ingredients = []
                while(i<len(recipe)): # iterate the ingredients
                    ingName = recipe[i]
                    ingAmt = recipe[i+1]
                    tempTup = (ingName, ingAmt)# put name and amt in tup
                    ingredients.append(tempTup)# then put into list of ingredients
                    i+=2
                r = recipes.Recipe(name, ingredients)# add recipe to db
                db.add_recipe(r)
                n = 1
                
            new_reader.next()
        except StopIteration:
            break
    #print db.get_all_recipe_names()
    return n



