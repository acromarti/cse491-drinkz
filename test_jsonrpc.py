import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded;
#jonesd52

import os
import ast
from drinkz import db
from drinkz import recipes
from drinkz import app
import urllib
import simplejson
from StringIO import StringIO

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
    
    db.add_bottle_type('Freedom Walker', 'blue label', 'unblended scotch')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
    db.add_recipe(r)
 
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
    db.add_recipe(r)
 
    r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
    db.add_recipe(r)



def call_rpc():
    db_Init()    
    theApp = app.SimpleApp()    
    environ = {}    
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'        

    d = dict(method='hello', params=[] ,id=1)    
    encoded = simplejson.dumps(d)    
    environ['wsgi.input'] = StringIO(encoded)    
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=d):        
	d['status'] = s
        d['headers'] = h

    results = theApp.__call__(environ,my_start_response)    
    text = "".join(results)        

    assert text.find("world") != -1, text


def test_rpc_convert_ml_to_ml():        
    db_Init()    
    theApp = app.SimpleApp()    
    environ = {}    
    environ['REQUEST_METHOD'] = 'POST'    
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='convert_units_to_ml', params=['100 ml'] ,id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded)    
    environ['CONTENT_LENGTH'] = 1000        

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    
    results = theApp.__call__(environ,my_start_response)
    text = "".join(results)
        
    assert text.find("100.0") != -1, text


def test_rpc_convert_gallon_to_ml():        
    db_Init()
    theApp = app.SimpleApp()
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='convert_units_to_ml', params=['40 gallon'] ,id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h     

    results = theApp.__call__(environ,my_start_response)
    text = "".join(results)    
    assert text.find("151416.4") != -1, text


def test_rpc_convert_oz_to_ml():
    db_Init()
    theApp = app.SimpleApp()
    environ = {}
    environ['REQUEST_METHOD'] = 'POST' 
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='convert_units_to_ml', params=['40 oz'] ,id=1)
    encoded = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h     
    results = theApp.__call__(environ,my_start_response)
    text = "".join(results)
    assert text.find("1182.94") != -1, text


def test_rpc_convert_liters_to_ml():
    db_Init()
    theApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'  

    d = dict(method='convert_units_to_ml', params=['40 liter'] ,id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000
   
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h      
    results = theApp.__call__(environ,my_start_response)
    text = "".join(results)

    assert text.find("40000.0") != -1, text


def test_rpc_get_recipe_names():    
    db_Init()
    theApp = app.SimpleApp()
    environ = {} 
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='get_recipe_names', params=[] ,id=1)
    encoded = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000    

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h      
    results = theApp.__call__(environ,my_start_response)
    text = "".join(results)   
    assert text.find("scotch on the rocks") != -1, text    
    assert text.find("vodka martini") != -1, text
    assert text.find("vomit inducing martini") != -1, text

def test_rpc_get_liqour_inventory():   
    db_Init()
    theApp = app.SimpleApp()
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='get_liqour_inventory', params=[] ,id=1)
    encoded = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h      
    results = theApp.__call__(environ,my_start_response)
    text = "".join(results)

    assert text.find("Johnnie Walker\", \"black label") != -1, text
    assert text.find("Uncle Herman's\", \"moonshine") != -1, text
    
def test_rpc_add_liqour():   
    db_Init()
    theApp = app.SimpleApp()
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='add_liquor', params=['Brother David', 'shinemoon', 'volka'] ,id=1)
    encoded = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h      
    results = theApp.__call__(environ,my_start_response)
 
    assert True, results
    
def test_rpc_add_inventory():   
    db_Init()
    theApp = app.SimpleApp()
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='add_inventory', params=['Freedom Walker', 'blue label', '100 ml'] ,id=1)
    encoded = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h      
    results = theApp.__call__(environ,my_start_response)
    
    assert  True, results
    
def test_rpc_add_recipe():   
    db_Init()
    theApp = app.SimpleApp()
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    name = "vongola pure"
    ing =  [('blended water','20 oz')]
    
    d = dict(method='add_recipe', params=[name, ing] ,id=1)
    encoded = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h      
    results = theApp.__call__(environ,my_start_response)
    
    assert  True, results