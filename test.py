import re

from pathlib import Path

import sqlite3

print(123)

def fileDB (x, time):
	with open (x, "r") as file:
		for f in file:
			if f != "\n":
				s = list((filter (lambda n: n != ' ' and n !='' and n!="(" and n!=")", pattern.split(f.strip()))))

				s.append(time)
				if s[2] in diki.keys():
					
					tmpS = diki[s[2]][-1].split()
					if s[4] not in tmpS:
						"""print(f)
						print(s)
						print(tmpS)
						print (2, s[4])
						print()"""
						tmpS.append(s[4])
						tmpS = sorted(tmpS, reverse=True)[:10]
						diki[s[2]][-1] = " ".join(tmpS)
					if s[1] not in diki[s[2]][1].split():
						diki[s[2]][1] = diki[s[2]][1] + " " + s[1]
					
					"""
					elif s[5] not in tmps :
						diki[s[2]][-2] +=  " " + s[5]
					"""
				else:
					diki[s[2]] = [s[0],s[1], s[3],s[5], s[4]]

		return diki
def mac_db():
	con = sqlite3.connect("Mac.db")

	cursor = con.cursor()

	cursor.execute("PRAGMA synchronous = OFF;")
	cursor.execute("PRAGMA journal_mode = WAL;")
	#Выделение оперативки
	cursor.execute("PRAGMA cache_size =-500000;")
	cursor.execute("PRAGMA locking_mode = EXCLUSIVE;")

	diki = {}
	pattern = re.compile(r"\('([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)'\)\s*(.*)")
	p = Path('.')

	cursor.execute("""CREATE TABLE IF NOT EXISTS names(
					name VARCHAR(20) UNIQUE)""")

	cursor.execute('''
				CREATE TABLE IF NOT EXISTS mac_addresses(
				   mac VARCHAR(8) PRIMARY KEY,
				   vlan VARCHAR(50),
				   interface VARCHAR(20),
				   name VARCHAR(200),
				   time VARCHAR(5),
				   data VARCHAR(100)
				   )
				   ''')

	cursor.execute("SELECT name FROM names")
	names = {row[0] for row in cursor.fetchall()}
	for x in p.glob('*.txt'):

		if str(x) in names:
			print(x)
			continue
		else:
			print (23242, x)
			time = re.search(r'_\d\d\-\d\d',str(x))
			time = str(time[0])[1:]
			diki = fileDB(x, time)

			cursor.execute("INSERT INTO names(name) VALUES (?)", (str(x),))
		
	if diki:

		macs = list(diki.keys())
		for i in range(0, len(macs), 900):
			part_macs = ",".join('?'* len(macs[i:i+900]))
			
			cursor.execute(f"SELECT mac, interface, data FROM mac_addresses WHERE mac IN ({part_macs})", macs[i:i+900])
			
			for row in cursor.fetchall():
				db_mac, db_interface, db_data = row
				
				all_dates = list(set(diki[db_mac][-1].split() + db_data.split()))
				diki[db_mac][-1] = " ".join(sorted(all_dates, reverse=True)[:10])
				
				all_ints = list(set(diki[db_mac][1].split() + db_interface.split()))
				diki[db_mac][1] = " ".join(all_ints)

	record = [[mac, vals[0], vals[1], vals[2], vals[3], vals[4]] for mac, vals in diki.items()]
	query = "INSERT OR REPLACE INTO mac_addresses(mac,vlan,interface,name,time, data) VALUES (?,?, ?,?, ?, ?)"
	cursor.executemany(query,record)

	con.commit()
	con.close()
	
mac_db()
