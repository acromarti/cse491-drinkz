# -*- coding: utf-8 -*-
"""
Database functionality for drinkz information.
"""

# The reason I chose to implent a set was because usinset will take less code than a dictonary.  I can just pull
# the ingredients using recipe.ingredients

from recipes import Recipe

import os

from cPickle import dump, load

import sqlite3

import base64

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
_recipes_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set([])
    _inventory_db = {}
    _recipes_db = {}
    
    
def save_db(filename):
 
	mySQL = sqlite3.connect(filename)
	c = mySQL.cursor()
	
	# Clear any existing tables
	c.execute('drop table if exists bottleTyp_Table')
	c.execute('drop table if exists inventory_Table')
	c.execute('''drop table if exists recipes''')
	
	c.execute('CREATE TABLE bottleTyp_Table (mfg text, liq text, typ text)')
	c.execute('CREATE TABLE inventory_Table (mfg text, liq text, amounts text)')
	c.execute('CREATE TABLE recipe_Table (name, ing)')
	
	for line in _bottle_types_db:
	  
	   (mfg,liq,typ) = line
	  
	   c.execute('INSERT INTO bottleTyp_Table (mfg, liq, typ) VALUES (?, ?, ?)', (mfg, liq, typ))
	
	for line in get_liquor_inventory():
	  
	   (mfg,l) = line  
           amount = get_liquor_amount(mfg,l)
	   c.execute('INSERT INTO inventory_Table (mfg, liq, amounts) VALUES (?, ?, ?)', (mfg, l, amount))
	  
	show_all_recipes = get_all_recipes()
	for recipe in show_all_recipes:
	  
	    name = recipe.name
	    templist = recipe.ingredients
	    finallist = buffer(myListToStr(templist))
	    c.execute("INSERT INTO recipe_Table VALUES (?,?)",(name,finallist))
	    
	#this commits the changes and closes the connection
	
	c.execute('SELECT * FROM recipe_Table')
	bottleTyp_list = c.fetchall()
	
	#c.execute('SELECT * FROM inventory_Table')
	#inventory_list = c.fetchall()
	
	print "IN THE SAVE FUNCTION, BOTTLE TYP IS.......", bottleTyp_list
	#print "IN THE SAVE FUNCTION, Inventory  IS.......", inventory_list
	
	mySQL.commit()
	mySQL.close()
	
def load_db(filename):
  
	mySQL = sqlite3.connect(filename)
	c = mySQL.cursor()
  
	c.execute('SELECT * FROM bottleTyp_Table')
	bottleTyp_list = c.fetchall()
	print "IN THE LOAD FUNCTION, BOTTLE TYP IS.......", bottleTyp_list
	
	for line in bottleTyp_list:
	    
	   m,l,t = line
	   add_bottle_type(m, l, t)
	
	c.execute('SELECT * FROM inventory_Table')
	inventory_list = c.fetchall()
	print "IN THE LOAD FUNCTION, Inventory  IS.......", inventory_list
		
	for inv_list in inventory_list:
	  
	   m,l,a = inv_list
	   
	   amount = convert_to_ml(a)
	   
	   add_to_inventory(m,l,amount)
	   
	c.execute("Select * FROM recipe_Table")
	rows = c.fetchall()
	#print rows
	for row in rows:
	    name,ing = row
	    #print name
	    #print str(ing)
	    my_list2 = strToMyList(str(ing))
	    r = Recipe(name,my_list2)
	    add_recipe(r)
	  
	#c.execute('SELECT * FROM recipe_Table')
	#print c.fetchall
	mySQL.commit()
	mySQL.close()
    

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
  
class IdenticalRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))


def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
	print "THIS IS DOES NOT EXIST!!!....", mfg, liquor
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    key = (mfg, liquor)
    _inventory_db[key] = amount
    print "This is the key", key
    print "THis is the something", _inventory_db[key]

def check_inventory(mfg, liquor):
    return ((mfg, liquor) in _inventory_db)

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
   
    if (mfg, liquor) in _inventory_db:
      
      #return _inventory_db.get((mfg, liquor), 0.0)
    
      amounts = _inventory_db[(mfg, liquor)]
    
    return amounts

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l


def convert_to_ml(amount):
  
  #Converts to ml no matter the unit
  
    answer = 0;

    if("ml") in amount:
	amount = amount.strip('ml')
	answer = float(amount)
	
    elif ("oz") in amount:
	amount = amount.strip('oz')
	answer = float(amount) * 29.5735
	
	
    elif("gallon") in amount:
	 amount = amount.strip('gallon')
	 answer = float(amount) * 3785.41
	 
    elif("liter") in amount:
	  amount = amount.strip('liter')
	  answer = float(amount) * 1000
    else:
	  answer = 0
	
    return answer
    
    
    
def check_inventory_for_type(typ):
  # Checks the inventory to see if the type exists
  #and return the whole amount of the type
    
    matching_ml = []
    
    for (m, l, t) in _bottle_types_db:
        if t == generic_type:
            amount = _inventory_db.get((m, l), 0.0)
            matching_ml.append((m, l, amount))

    return matching_ml
    
def add_recipe(r):  
    if r.name not in _recipes_db:
        _recipes_db[r.name]=r
    else:
        raise IdenticalRecipeName()
      
def _check_recipe_exists(name):
    if name not in _recipes_db:
	return False
    return True
    
def get_recipe(name):
    if name not in _recipes_db:
	    return None
    return _recipes_db.get(name)        


def get_all_recipe_names():
    return _recipes_db.keys()
    
def get_all_inventory_names():
    return _inventory_db.keys()
    

def get_all_recipes():
    return _recipes_db.values()
    
    
def myListToStr(myList):
    """This method takes a list of (int, str) tuples and converts them to a string"""

    strList = ""
    for item in myList:
        name, amount = item #split the tuple

        strList += "{}:{};".format(name, amount) #append the tuple in "num:name" format with a " " delimiter
    return strList[:-1] #remove the final space (unneeded)

def strToMyList(myStr):
    """This method takes a string in the format "int:str int:str int:str..."
and converts it to a list of (str, str) tuples"""

    myList = []
    for tup in myStr.split(";"): #for each converted tuple
        name, amount = tup.split(":") #split the tuple

        myList.append((name, amount))

    return myList

