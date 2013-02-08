import drinkz.db

drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '22 oz')

drinkz.db.add_bottle_type('Jack Daniels', 'Old No. 7', 'whiskey')
drinkz.db.add_to_inventory('Jack Daniels', 'Old No. 7', '2000 ml')
drinkz.db.add_to_inventory('Jack Daniels', 'Old No. 7', '50 oz')

different_list = set()

print 'Manufacturer\tLiquor'
print '------------\t------'
for mfg, liquor in drinkz.db.get_liquor_inventory():

    if (mfg, liquor) in different_list:
	continue

    amount = drinkz.db.get_liquor_amount(mfg, liquor)

    print '%s\t%s\t%s' % (mfg,liquor,amount)

    different_list.add((mfg, liquor))
  
