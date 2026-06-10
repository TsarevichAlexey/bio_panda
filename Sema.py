import re 
import sqlite3 

from test import *

if (input("Update db (y/n)? ").lower) == 'y' :
	mac_db()
pattern = re.compile(r"^[0-9a-z]{1,12}$")
mac = input("Enter mac: ")
if re.fullmatch(pattern, mac):
	con = sqlite3.connect("Mac.db")


	cursor = con.cursor()

	cursor.execute("SELECT * FROM mac_addresses WHERE mac LIKE '%' || (?) || '%';", (mac,))
	macs = cursor.fetchall()
	if len(macs) !=0:
		for row in macs:
			print(*row, sep=" | ")
	else:
		print ("Nothing was found")

	con.close()
		
else:
	print("Incorrect mac")

