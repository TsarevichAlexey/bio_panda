import pandas as pd
import re

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String


import sqlite3
from dotenv import load_dotenv
print(123)

# def sql(dt:pd.DataFrame, bd) :
load_dotenv()

"""
db_url = "sqlite:///./bd"

class Base(DeclarativeBase):
	pass

class MacBase (Base):
	__tablename__ == "Mac"

	id:Mapped[str] = mapped_column(String(12))
	vlan:Mapped[str] = mapped_column(String(50))
	interface:Mapped[str] = mapped_column(String(50))
	name:Mapped[str] = mapped_column(String(200))
	data:Mapped[str] = mapped_column(String(100))
	time: Mapped[str] = mapped_column(String(50))

"""

"""engine = create_engine(db_url, echo=False)

Session = sessionmaker(engine)

with Session as session:
	"""
dt = pd.DataFrame(columns = ["Vlan", 'Interface', 'MAC', 'Name', 'data','time'])
#dt.set_index('id')
p = Path('.')
for x in p.glob('*.txt'):
	with open (x, "r+") as file:
		time = re.search(r'_\d\d\-\d\d',str(x))
		time = str(time[0])[1:]
		print(time)
		for f in file:
			#print(f)
			if f != "\n":
				#dt.insert(f, None, None, None)
				#print(list(filter (lambda n: n is not '', re.split("[()',\s]",f))))
				s = pd.Series (list(filter (lambda n: n != '', re.split("[(''),]\s",f))), index = ["Vlan", 'Interface', 'MAC', 'Name', 'data'])
				s['time'] = time
				if s['MAC'] in dt["MAC"].values:
					#print (1, s)
					#print(dt[dt['MAC'] == s["MAC"]].index[0].tolist())
					numD = dt[dt['MAC'] == s["MAC"]].index[0]#.tolist()
					#print(numD)
					if len(dt.loc[ numD, 'data'].split()) <= 10:
						dtS = dt.loc[ numD, 'data']
						sd = s["data"]
						dt.loc[numD, 'data'] = f"{dtS}{sd}"
						# print(dtS)
				else:
					#print (2, s)
					#dt['fio'].str.split(pat=r"[()',\s]",regex=True, expand=True)

					#print(0,dt)
					

					dt = pd.concat([dt, s.to_frame().T],ignore_index = True)
				#print (dt)

dt=dt.set_index("MAC")
print(dt)

# dt.to_csv(r'test.csv')
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
query = "INSERT INTO mac_addresses(mac,vlan,interface,name,data,time) VALUES (?,?, ?,?, ?, ?)"
cursor.executemany(query,record)

con.commit()
con.close()