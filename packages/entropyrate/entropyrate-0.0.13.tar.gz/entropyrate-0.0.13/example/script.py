import entropyrate.entropyrate as e
import pandas as pd
df=pd.read_csv('test.dat',header=None,sep=" ")
s=e.sequence(df,NUMERIC=False,alphabet=['A','T','G','C'])
s.ent()
print(s.data.entropy)
