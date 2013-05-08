import sys
import os
import urllib
import db
import recipes
from drinkz import app
#sys.path.insert(0, 'bin/') #allow _mypath to be loaded


def db_Init():    
    db._reset_db()

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



def test_generated_page():
  
  db_Init()
  
  theApp = app.SimpleApp()
  
  environ = {}
  environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO', lastname='BAR')) 
  environ['PATH_INFO'] = '/recipes.html'

  d = {}

  def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

  #results = app_obj(environ, my_start_response)
  
  results = theApp.__call__(environ, my_start_response)
    
  text = "".join(results)

  assert text.find("scotch on the rocks") != 1, text
  assert text.find("vodka martini") != 1, text
  assert text.find("vomit inducing martini") != 1, text
  
  