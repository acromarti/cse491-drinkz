class Convert():
  
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
	
      return str(answer)