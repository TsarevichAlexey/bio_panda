import re 
import sqlite3 

from test import *

if (input("Update db (y/n)?").lower) == 'y' :
	mac_db()
pattern = re.compile(r"^[0-9a-z]{1,12}$")
mac = re.fullmatch(pattern, str(input()))
if mac:
	con = sqlite3.connect("Mac.db")


	cursor = con.cursor()

	cursor.execute("SELECT * FROM mac_addresses WHERE mac LIKE '%(?)%';", mac)
	macs = cursor.fetchall()
	if len(macs) !=0:
		print(macs)
	else:
		print ("Nothing was found")
		
else:
	print("Incorrect mac")

