# -*- coding: iso-8859-1 -*-
import db

class Recipe():
  
  
    def __init__(self, name, ingredients):

	  self.name = name
	  self.ingredients = ingredients
	  
    def need_ingredients(self):
      
	  notFound = []
	  
	  for typ, amount in self.ingredients:
	      
	    
	      ingNeeded = db.convert_to_ml(amount)
	      print type(ingNeeded)
	      
	      #print ingNeeded
	      
	      ingInInventory = db.check_inventory_for_type(typ)
	      print type(ingInInventory)
	      
	      print typ, amount, ingInInventory, ingNeeded
	      
	      if float(ingInInventory) <= float(ingNeeded):
		      ingMissing = float(ingNeeded) - float(ingInInventory)
		      missingTup = (typ, ingMissing)
		      notFound.append(missingTup)
		  
	      else:
		  continue
	
	  return notFound