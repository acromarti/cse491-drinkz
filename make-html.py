# -*- coding: iso-8859-1 -*-
#! /user/bin/env python

import os
from drinkz import db
from drinkz import recipes

#fill the database

db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
 
db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

 r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
 db.add_recipe(r)
 
 r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
 db.add_recipe(r)
 
 r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
 db.add_recipe(r)
 
 
 try:
   
   os.mkdir('html')
   
except:
  pass

recipes_html = """<p><a href="recipes.html">Recipes</a>"""
liquor_types_html = """<p><a href="liquor-types.html">Liquor Types</a>"""
index_html = """<p><a href="index.html">Index</a>"""
inventory_html = """<p><a href="inventory.html">Inventory</a>"""



#Index.html

fp = open('html/index.html', 'w')
links = "CSE491 Draankz\n" + liquor_types_html + inventory_html + recipes_html
print >> fp, links

fp.close()


#Recipers.html


fp = open('html/recipes.html', w)
display_recipes = db.get_all_recipes()
recipe_str = "Recipes\n<ol>"

for r in display_recipes:
  if(r.need_ingredients() == []):
    response = "Have all the ingredients"
    
  else:
    response = "Missing some ingredients"
    
  recipe_str += "<li>" + r.name + ": " + response + "</li>\n"
  
recipe_str += "</ol>"
links = index_html + liquor_types_html + inventory_html
recipe_str += links
print >> fp, recipe_str
  
fp.close()
  
  
  
  #liquor-types.html

fp = open('html/liquor-types.html', w)
liquors_str = "Liquor Types\n<ol>"

for mfg, liquor in db.get_liquor_inventory():
    liquors += "<li>" + mfg + ", " + liquor + "</li>"
    
liquors += "</ol>"
    
links = index_html + recipes_html + inventory_html
liquors_str += links
print >> fp, recipe_str
  
  fp.close()
  
  
  
#Inventory.html

fp = open('html/inventory.html', w)
inventory_str = "Inventory\n<ol>"

for liquor in db.get_liquor_inventory():
    mfg = liquor[0]
    l = liquors[1]
    amount = db.get_liquor_amount(mfg,l)
    inventory_str += "<li>" + mfg + ", " + l + ": " + str(amount) + " ml</li>\n"
    
inventory_str += "</ol>"
    
links = index_html + recipes_html + liquor_html
inventory_str += links
print >> fp, inventory_str
  
  fp.close()
  
  
  
  
  
  
  