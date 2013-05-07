#! /usr/bin/env python
from wsgiref.simple_server import make_server
import simplejson
from Cookie import SimpleCookie
from drinkz import db
from drinkz import recipes
import urlparse
import uuid
import jinja2

usernames = {}

# this sets up jinja2 to load templates from the 'templates' directory
loader = jinja2.FileSystemLoader('./drinkz/templates')
env = jinja2.Environment(loader=loader)

dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/liquidRecv' : 'liquidRecv',
    '/rpc'  : 'dispatch_rpc', 
    '/recipe.html' : 'recipers',
    '/liquor_types.html' : 'liquorTypes',
    '/inventory.html' : 'inventory',
    '/calculate_liquid' : 'calculateLiquid',  
    '/adding_to_liquor_types' : 'adding_to_liquor_types',
    '/adding_to_inventory' : 'adding_to_inventory', 
    '/adding_to_recipes' : 'adding_to_recipes',
    '/liquor_types_Rev' : 'liquor_types_Rev',
    '/inventory_Rev' : 'inventory_Rev',
    '/recipe_Rev' : 'recipe_Rev',
    '/login_1' : 'login1',
    '/login1_process' : 'login1_process',
    '/logout' : 'logout',
    '/status' : 'status'   
}


def load_db_file(self, file_name):
        db.load_db(file_name)


html_headers = [('Content-type', 'text/html')]


###############################################################################################################################################SHORTCUTS


html_headers = [('Content-type', 'text/html')]
recipes_html = """<p><a href="recipes.html">Recipes</a>"""
liquor_types_html = """<p><a href="liquor-types.html">Liquor Types</a>"""
index_html = """<p><a href="index.html">Index</a>"""
inventory_html = """<p><a href="inventory.html">Inventory</a>"""
calculate_liquid_html = """<p><a href="calculate_liquid">Calculate Liquid</a>"""

add_liquor_types = """<p><a href='adding_to_liquor_types'>Add A Liquor Type</a></p>"""
add_inventory = """<p><a href='adding_to_inventory'>Add To Inventory</a></p>"""
add_reciepes = """<p><a href='adding_to_recipes'>Add To Recipes</a></p>"""

logout = """<p><a href='/logout'>Logging Out</a></p>"""



##################################################################################################################################################HIS STUFF

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None) 

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
        
    def load_db_file(self, file_name):
        db.load_db(file_name)
            
    
    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]
        
   

    
    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)
        
#######################################################################################################################################################################LOGGING STUFF

    def login1(self, environ, start_response):
	#start_response('200 OK', list(html_headers))

        #title = 'login'
        #template = env.get_template('login1.html')
        #return str(template.render(locals()))
        
        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        if name1:
            return self.index(environ,start_response)
        else:
            start_response('200 OK', list(html_headers))
            title = 'login'
            #loader = jinja2.FileSystemLoader('../drinkz/templates')
            #env = jinja2.Environment(loader=loader)
            template = env.get_template('login1.html')
            return str(template.render(locals()))



    def login1_process(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        content_type = 'text/html'

        # authentication would go here -- is this a valid username/password,
        # for example?

        k = str(uuid.uuid4())
        usernames[k] = name

        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(('Set-Cookie', 'name1=%s' % k))

        start_response('302 Found', headers)
        return ["Redirect to /status..."]
        
        
        

    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key

                if key in usernames:
                    del usernames[key]
                    print 'DELETING'

        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /status..."]
        
        
        
    def status(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
                
        title = 'login status'
        #env = jinja2.Environment(loader=loader)
        template = env.get_template('status.html')
        return str(template.render(locals()))


        
        
############################################################################################################################################################My STUFF   

    def index(self, environ, start_response): #generates the index tabs
	name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        if name1 == '':
	    return self.login1(environ,start_response)
	    #print "right here"
            
        start_response('200 OK', list(html_headers))
        
        template = env.get_template("index.html")

        title = "index"
        return str(template.render(locals()))
        
        
    def recipers(self, environ, start_response):

	start_response('200 OK', list(html_headers))
        
        template = env.get_template("recipe.html")

        title = "recipe"
        return str(template.render(locals()))
        
    def liquorTypes(self, environ, start_response):
        
        start_response("200 OK", list(html_headers))

        title = "liquor types"

        liquor_types = [ (m, l, t) for (m, l, t) in db._bottle_types_db ]
        
        template = env.get_template("liquor_types.html")
        return str(template.render(locals()))
        
    def inventory(self, environ, start_response):
      
        start_response("200 OK", list(html_headers))

        title = "inventory"
        
        
        inventory = [ (m, l, db.get_liquor_amount(m, l)) \
                      for (m, l) in db.get_liquor_inventory() ]
        
        template = env.get_template("inventory.html")
        return str(template.render(locals()))
        
      
    def calculateLiquid(self, environ, start_response):
	content_type = 'text/html'
        data = open('./drinkz/calculate_liquid.html').read()

        start_response('200 OK', list(html_headers))
        return [data]
        
    def liquidRecv(self, environ, start_response):
	
	
	
        return [data]	
	    
        
        
        
        
        
        
        
 ######################################################################################################################################################JASON_RPC


    def rpc_convert_units_to_ml(self,amount):        
	return str(db.convert_to_ml(amount))   
	
    def rpc_get_recipe_names(self):        
	recipeList = db.get_all_recipe_names()        
	nameList = list()        
	for recipe in recipeList:            
	    nameList.append(recipe)        
	return nameList 
	
    def rpc_get_liqour_inventory(self):        
	liqourInvList = list()        
	for (m,l) in db.get_liquor_inventory():
            liqourInvList.append((m,l))
        return liqourInvList
        
    def rpc_add_liquor(self, mfg, liquor, typ):
	n = False
	result = db._check_bottle_type_exists(mfg, liquor)
	if result == False:
	    db._bottle_types_db.add((mfg, liquor, typ))
	    n = True
	   
	return n
	
    def rpc_add_inventory(self, mfg, liquor, amount):
	n = False;
	result = db.check_inventory(mfg, liquor)
	if result == False:
	    db.add_to_inventory(mfg, liquor, amount)
	    n = True
	return n
	
    def rpc_add_recipe(self, name, ing):

        db.add_recipe(recipes.Recipe(name, ing))
    
       	
    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
        
        
        
    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

####################################################################################################################################ADDING FUNCTIONS

    def adding_to_liquor_types(self, environ, start_response):
        data = adding_to_liquorForm()
        start_response('200 OK', list(html_headers))
        return [data]

    def adding_to_inventory(self, environ, start_response):
        data = adding_to_inventoryForm()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def adding_to_recipes(self, environ, start_response):
        data = adding_to_recipeForm()
        start_response('200 OK', list(html_headers))
        return [data]

    def recipe_Rev(self, environ, start_response):
        formdata = environ["QUERY_STRING"]
        results = urlparse.parse_qs(formdata)
        
        recipeName = results['recipeName'][0]
        ingredients = results['ingredients'][0].split(',')
        Ingredients = []
        
        i=0
        while i < len(ingredients):
	    Ingredients.append((ingredients[i], ingredients[i+1]))
	    i += 2
	    
	db.add_recipe(recipes.Recipe(recipeName, Ingredients))
            
        data = "Added recipe to database"
        data += "<p><a href = '/'>Index</a></p>"
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    def liquor_types_Rev(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liq = results['liquor'][0]
        typ = results['typ'][0]

        db.add_bottle_type(mfg,liq,typ)
        
        #print db._bottle_types_db

        data = "Added liquor type to database"
        data += "<p><a href = '/'>Index</a></p>"

        start_response('200 OK', list(html_headers))
        return [data]

    def inventory_Rev(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liq = results['liquor'][0]
        amt = results['amount'][0]
        
        #print amt
        data = ""
    
        bottleTypExists = db._check_bottle_type_exists(mfg, liq)
        
        if bottleTypExists == True:
	    db.add_to_inventory(mfg, liq, amt)
	    data += "Added Liquor to Inventory"
	else:
	    data = "Could not add bottle to inventory, Liquor bottle type could not be found"

        data += "<p><a href='/'>Index</a></p>"
        
        start_response('200 OK', list(html_headers))
        return [data]




#####################################################################################################################################################HTML STUFF

def form():
    return """    
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

 


def adding_to_inventoryForm():
    return """
<html>
<head>
<title>Adding An Inventory</title>
<style type='text/css'>
h1 {color:green;}
body {font-size: 20px;}
</style>
<h1>Adding to Inventory!!!!</h1>
<style type='text/css'>
h2 {color:red;}
body {font-size: 20px;}
</style>
<h2>lets get started!!!</h2><ul>

<form action='inventory_Rev'>
Manufacturer: <input type='text' name='mfg'>
<br><br>
Liquor: <input type='text' name='liquor'>
<br><br>
Amount: <input type='text' name='amount'>
<br><br>
<input type='submit'>
</form>
<p><a href='/'>Index</a></p>
"""



def adding_to_recipeForm():
    return """
<html>
<head>
<title>Adding An Recipe</title>
<style type='text/css'>
h1 {color:green;}
body {font-size: 20px;}
</style>
<h1>Adding to Recipe!!!!</h1>
<style type='text/css'>
h2 {color:red;}
body {font-size: 20px;}
</style>
<h2>The more the merrier!!!</h2><ul>
<form action='recipe_Rev'>
Enter recipe name: <input type='text' name='recipeName' size'30'><br />
Enter ingredients*: <input type='text' name='ingredients' size'100'><br />
<br><br>
*Add recipe ingredients in the following format: ingredient, amount, ingredient, amount, etc.<br/>
(e.g. "unflavored vodka,6 oz,vermouth,1.5 oz" )<br/><br/>
<input type='submit'>
</form>
</body>
</html>"""

###############################################################################Main

if __name__ == '__main__':

    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()




    

