#!/usr/bin/python

#This script reads the TIME and PDCSAP FLUX from series of Kepler .fits files,
#converts fluxes to magnitudes, subtract a linear fit from the magnitude data and 
#extract a file containing 'phase - binned data points' based on user input.
#Works on Python 2.x (c)bulash

from __future__ import print_function

print("-"*len("K E P L C B I N"))
print("K E P L C B I N", "\n", "-"*len("K E P L C B I N"), sep="")

# remove folders and files from previous run...
import glob
dlist = (glob.glob("*"))
for item in dlist:
    if item == 'binlc.dat':
        deg = 2
        while deg == 2:
            yes = {'yes','y', 'ye', ''}
            no = {'no','n'}
            asw = raw_input('\033[93m' + "'binlc.dat' file from the previous run will be deleted. Continue? (y/n): " + '\033[0m').lower()
            if asw in yes:
                import os
                os.remove("binlc.dat")
                deg = 3
            elif asw in no:
                print("\033[91mEXIT...\033[00m")
                print()
                quit()
            else:
                pass


#Input T0 and P
def askto():
    global toin
    print()
    toin = raw_input('\033[93m' + "Enter the time of minimum: " + '\033[0m')
    try: #convert to float True
        float(toin)
    except: # convert to float False
        print("\033[91mPlease enter a valid number!...\033[00m")
        askto()
askto()

toinf = float(toin)

def askper():
    global per
    print()
    per = raw_input('\033[93m' + "Enter the period: " + '\033[0m')
    try:
        float(per)
    except:
        print()
        print("\033[91mPlease enter a valid number!...\033[00m")
        askper()
askper()

perf = float(per)

print()
print("\033[92m...PROCESSING...\033[00m")
print()

# extract time-pdcsap data from fits files and remove pdc with nan
import glob
fitlist = (glob.glob("*.fits"))
from astropy.io import fits
import pandas as pd
import numpy as np
tpmdata = pd.DataFrame(columns=['TIME', 'PHASE', 'MAGREGMAG'])
for i in fitlist:
    data = fits.getdata(i, ext=1)
    data2 = pd.DataFrame(np.array(data).byteswap().newbyteorder())
    tpdata = pd.DataFrame(data2, columns=['TIME','PDCSAP_FLUX'])
    tpdata2 = tpdata.dropna()
    logtemp = np.log10(tpdata2.loc[:,'PDCSAP_FLUX']) * -2.5
    tpdata3 = pd.concat([tpdata2,logtemp], axis=1)
    tpdata3.columns = ['TIME','PDCSAP_FLUX', 'PDCSAP_MAG']

# Fit using regression model to eliminate linear variations....
    from sklearn.linear_model import LinearRegression
    X = tpdata3.TIME
    Y = tpdata3.PDCSAP_MAG
    regmodel = LinearRegression().fit(X.values.reshape(-1,1), Y)
    Y_pred = regmodel.intercept_ + regmodel.coef_ * X
    magdif = tpdata3.loc[:,'PDCSAP_MAG'] - Y_pred
    tpdata4 = pd.concat([tpdata3,magdif], axis=1)
    tpdata4.columns = ['TIME','PDCSAP_FLUX', 'PDCSAP_MAG', 'MAGREGMAG']

### Binned point extraction based on the phase calculated from T0 and P
#Extract T - phase- mag to a file
    tpdata5 = ((tpdata4.loc[:,'TIME'] - toinf) / perf)
    tpdata6 = tpdata5.round(0)
    tpdata7 = tpdata5 - tpdata6
    tpdata8 = pd.concat([tpdata4,tpdata7,tpdata7], axis=1)
    tpdata8.columns = ['TIME','PDCSAP_FLUX', 'PDCSAP_MAG', 'MAGREGMAG', 'PRE_PHASE', 'PHASE']
    tpdata8['PHASE']= np.where((tpdata8['PRE_PHASE'])<0, tpdata8['PRE_PHASE'] + 1.0, tpdata8['PRE_PHASE'])
    tpdata9 = tpdata8[['TIME', 'PHASE', 'MAGREGMAG']]
    tpmdata = tpmdata.append(tpdata9)
#sort on phase
tpmdata = tpmdata.drop(['TIME'], axis=1)
tpmdata = tpmdata.sort_values(by='PHASE')
print("Processed fits files contain", len(tpmdata.index), "data points.")



#tpmdata.to_csv(r'alldata.dat')
#tpmdata.to_csv('alldata.dat', header=False, index=False, sep='\t')
#print(tpmdata)


print()
def askbin():
    global norinp
    norinp = raw_input('\033[93m' + "Number of bins in output file: " + '\033[0m')
    print()
    try:
        int(norinp)
    except:
        print("\033[91mPlease enter a valid number!...\033[00m")
        askbin()
askbin()

def askstd():
    global stdinp
    stdinp = raw_input('\033[93m' + "Enter the amount of dispersion (coefficient of sigma): " + '\033[0m')
    print()
    try:
        int(stdinp)
    except:
        try:
            float(stdinp)
        except:
            print("\033[91mPlease enter a valid number!...\033[00m")
            askstd()
askstd()

# Extract binned data according to input values

print()
print("\033[92m...PROCESSING...\033[00m")
print()

stdinf = float(stdinp)
norin = int(norinp)
nordv = 1 / float(norinp)
#print(norin, nordv)
for norcon in range(1,int(norin)+1):
    tpmdata2 = pd.DataFrame(columns=['PHASE', 'MAGREGMAG'])
    tpmdata2 = tpmdata[(tpmdata.PHASE > ((norcon - 1) * nordv)) & (tpmdata.PHASE <= (norcon * nordv))]
    stadev = tpmdata2['MAGREGMAG'].std()
    magmean = tpmdata2['MAGREGMAG'].mean()
    tpmdata2 = tpmdata2[(tpmdata2.MAGREGMAG  > magmean - (stdinf *stadev)) & (tpmdata2.MAGREGMAG < magmean + (stdinf * stadev))]
    magmean2 = tpmdata2['MAGREGMAG'].mean()
    phmean  = tpmdata2['PHASE'].mean()
    norlc = open('binlc.dat', 'a+')
    norlc.write(str(phmean) + " " + str(magmean2) + "\n")
    norlc.close()
print("\033[94mBinned light curve data are written to\033[00m \033[93m'binlc.dat'\033[00m \033[94mfile. The columns are:\033[00m", "[PHASE] and [MAG-REGMAG]")
print()
