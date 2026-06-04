import pandas as pd
import re

from pathlib import Path
print(123)

dt = pd.DataFrame(columns = ["Name", 'Interface', 'MAC', 'data', 'time'])
#dt.set_index('id')
p = Path('.')
for x in p.glob('*.txt'):
	print (1)
	with open (x, "r+") as file:
		for f in file:
			#dt.insert(f, None, None, None)
			#print(list(filter (lambda n: n is not '', re.split("[()',\s]",f))))
			s = pd.Series (list(filter (lambda n: n is not '', re.split("[()',\s]",f))), index = ["id","Name", 'Interface', 'MAC', 'data', 'time'])
			
			s = s.drop(labels=["id"])
			#dt['fio'].str.split(pat=r"[()',\s]",regex=True, expand=True)

			#print(0,dt)

			dt = pd.concat([dt, s.to_frame().T],ignore_index = True)
			#print (dt)

print(dt)
dt.set_index("MAC")
print(dt)
			#break
			#f.replace()
