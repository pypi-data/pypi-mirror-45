#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
# external libraries
import pandas as pd
import numpy as np

def recordIDX(IDX,buildmodel,csv,cellornuc,IDX_dist):
	IDX = IDX+1
	print('## recordIDX.py')
	UI = pd.read_csv(csv)
	setpaths = UI['set location']

	if cellornuc == 'ch1':
		ledgername = UI['ch1'][0] + '_registry.csv'
		picklename =  UI['ch1'][0] + '_boundary_coordinate_stack.pickle'
	else: 
		ledgername =  UI['ch2'][0] + '_registry.csv'
		picklename =  UI['ch2'][0] + '_boundary_coordinate_stack.pickle'

	for setpath in setpaths:
		obj_ledger = pd.read_csv(os.path.join(setpath,ledgername))
		pkl = pd.read_pickle(os.path.join(setpath,picklename)).values
		pkl = pkl.flatten()
		setlength = len(pkl)
		obj_ledger['IDX']=pd.Series(IDX[0:setlength]) #write
		obj_ledger['Fitness']=pd.Series(IDX_dist[0:setlength])
		IDX = np.delete(IDX,range(setlength)) #remove
		IDX_dist = np.delete(IDX_dist,range(setlength))
		obj_ledger.to_csv(os.path.join(setpath,ledgername), index=False)

