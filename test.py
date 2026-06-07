import pandas as pd
import re

from pathlib import Path


import sqlite3
from dotenv import load_dotenv
print(123)

load_dotenv()

dt = pd.DataFrame(columns = ["Vlan", 'Interface', 'MAC', 'Name', 'data','time'])
diki = {}
pattern = re.compile(r'[\(\'\),]')
p = Path('.')
for x in p.glob('*.txt'):
	with open (x, "r") as file:
		print (x)
		time = re.search(r'_\d\d\-\d\d',str(x))
		time = str(time[0])[1:]
		for f in file:
			if f != "\n":
				s = list((filter (lambda n: n != ' ' and n !='', pattern.split(f.strip()))))

				s.append(time)
				if s[2] in diki.keys():
					tmpS = diki[s[2]][-1].split()
					if len(tmpS) <= 16 and s[2] not in tmpS:
						diki[s[2]][-1] +=  " " + s[4]
					"""
					elif s[5] not in tmps :
						diki[s[2]][-2] +=  " " + s[5]
					"""
				else:
					diki[s[2]] = [s[0],s[1], s[3],s[5], s[4]]
				
dt = pd.DataFrame.from_dict(diki,orient="index",columns=["Vlan", 'Interface', 'Name', 'time','data'])

#print(dt)

num = len(dt['Vlan'])
con = sqlite3.connect("Mac.db")

cursor = con.cursor()

cursor.execute("PRAGMA synchronous = OFF;")
cursor.execute("PRAGMA journal_mode = WAL;")
#Выделение оперативки
cursor.execute("PRAGMA cache_size =-500000;")
cursor.execute("PRAGMA locking_mode = EXCLUSIVE;")
cursor.execute('''
			CREATE TABLE IF NOT EXISTS mac_addresses(
			   mac VARCHAR(8) PRIMARY KEY,
			   vlan VARCHAR(50),
			   interface VARCHAR(20),
			   name VARCHAR(200),
			   data DATE,
			   time VARCHAR(5)
			   )
			   ''')

record = dt.reset_index().values.tolist()
query = "INSERT OR REPLACE INTO mac_addresses(mac,vlan,interface,name,data,time) VALUES (?,?, ?,?, ?, ?)"
cursor.executemany(query,record)

con.commit()
con.close()