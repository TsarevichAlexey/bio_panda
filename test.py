import pandas as pd
import re

print(123)

dt = pd.DataFrame(columns = ["Name", 'Interface', 'MAC', 'data', 'time'])
with open ("2026-06-04_16-00-00.txt", "r+") as file:
	for f in file:
		#dt.insert(f, None, None, None)
		#print(list(filter (lambda n: n is not '', re.split("[()',\s]",f))))
		s = pd.Series (list(filter (lambda n: n is not '', re.split("[()',\s]",f))), index = ["Name", 'Interface', 'MAC', 'data', 'time'])
		
		#s.dropna()
		#dt['fio'].str.split(pat=r"[()',\s]",regex=True, expand=True)

		print(0,dt)
		dt = pd.concat([dt, s.to_frame().T], ignore_index = True)
		print (s)
		print(dt)
		#break
	    #f.replace()
