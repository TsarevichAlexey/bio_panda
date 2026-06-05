import pandas as pd
import re

import sqlite3
from pathlib import Path
#print(123)

def sql (table, bd):
	pass

#dt.set_index('id')
def index_MAC(x:str, dt:pd.DataFrame) -> pd.DataFrame:
	# print (x)
	with open (x, "r+") as file:
		# print(dt)
		for f in file:
			if f != "\n":
				#dt.insert(f, None, None, None)
				#print(list(filter (lambda n: n is not '', re.split("[()',\s]",f))))
				s = pd.Series (list(filter (lambda n: n != '', re.split("[()',\s]",f))), index = ["id","Name", 'Interface', 'MAC', 'data', 'time'])
				
				if s['MAC'] in dt["MAC"].values:
					#print (1, s)
					#print(dt[dt['MAC'] == s["MAC"]].index[0].tolist())
					numD = dt[dt['MAC'] == s["MAC"]].index[0].tolist()
					# print (dt.loc[ numD, 'data'])
					# print (dt)
					if type(dt.loc[ numD, 'data']) == "<class 'pandas.core.series.Series'>":
						if len(dt.loc[ numD, 'data'].str.split()) <= 10:
							dtS = dt.loc[ numD, 'data'].str
							sd = s["data"]
							dt.loc[numD, 'data'].str = f"{dtS}\n{sd}"
							# print(dtS)
							return dt
						else:
							dtS = dt.loc[ numD, 'data']
							sd = s["data"]
							dt.loc[numD, 'data'] = f"{dtS}\n{sd}"
							# print(dtS)
							return dt
				else:
					#print (2, s)
					s = s.drop(labels=["id"])
					#dt['fio'].str.split(pat=r"[()',\s]",regex=True, expand=True)

					#print(0,dt)
					

					dt = pd.concat([dt, s.to_frame().T],ignore_index = True)
					return dt
				#print (dt)

dt = pd.DataFrame(columns = ["Name", 'Interface', 'MAC', 'data', 'time'])

p = Path('.')
for x in p.glob('*.txt'):
	dt =pd.concat([dt,index_MAC(x, dt)], axis=0)
dt=dt.set_index("MAC")
print(dt)
			#break
			#f.replace()
