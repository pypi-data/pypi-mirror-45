import pandas as pd
import numpy as np
import subprocess
import tempfile
import os
import sys


def getEntropy(row):
    '''
        calculates entropy
        write row to tempfile
        and executes binary
    '''
    tmp=tempfile.NamedTemporaryFile()
    module_folder = os.path.dirname(sys.modules['entropyrate'].__file__)
    binary = module_folder + '/bin/entropy'
    config = module_folder + '/bin/entropy.cfg'
    command = binary + ' -c ' + config + ' -d 2000000 -f ' + tmp.name
    row.to_csv(tmp.name,sep=" ",index=None,header=None)

    return np.array(subprocess.check_output(command,shell=True).split())[0]

def toint(x,ARRAY=['A','T','G','C']):
    '''
        entropy calculation  requires 
        numeric input. So we transform
        dataframe to map alphabets to integers
    '''
    return pd.Series(np.argwhere(np.array(ARRAY)==x.values[0])[0][0])

class sequence(object):

    def __init__(self,data,NUMERIC=True,alphabet=None):
        self.data=data
        self.NUMERIC=NUMERIC
        self.alphabet=alphabet


    def ent(self):
        '''
        entropy calculation  requires 
        numeric input. So we transform
        dataframe to map alphabets to integers
        '''
        
        self.data=self.data.transform(lambda x: toint(x,ARRAY=self.alphabet))

        self.data['entropy']=self.data.apply(getEntropy,axis=1)
        
        return

