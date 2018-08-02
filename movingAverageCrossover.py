# -*- coding: utf-8 -*-

import pandas as pd
from random import randint
import numpy as np
import pickle
import dataSetup #queries quandl data and saves it locally in case data does not exist
import os
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

class movingAverageCrossover:
    def __init__(self,start='2003-05-31',end='2018-05-31',days=[20,80],plotDuration=5,eqName='HINDALCO'):
        self.eqList=pickle.load(open(os.getcwd()+'/data/equityList.pickle','rb'))
        self.eqName=eqName
        self.start=start
        self.end=end
        self.plotDuration=plotDuration
        self.workingDir=os.getcwd()
        if self.verification(days):
            self.shortDays=min(days)
            self.longDays=max(days)
            if self.loadDF():
                print(self.df.head())
                self.eqList.append(self.eqName)
                self.df["Date"]=pd.to_datetime(self.df["Date"])
                self._generateMovingAverage()
                self._crossoverDates()
                self._generatePlot()
                pickle.dump(self.eqList,open(os.getcwd()+'/data/equityList.pickle','wb'))
    def verification(self,days):
        if len(days)==2:
            if days[0]<=0 or days[1] <=0:
                print("Days for moving average have to be positive.")
                return 0
            else:
                return 1
        else:
            return 0
    
    def loadDF(self):
        if not os.path.isfile(self.workingDir+'/data/'+self.eqName.lower()+'.csv'):
            if dataSetup.customAdd(self.eqName,self.start,self.end,self.workingDir):
                self.df=pd.read_csv(self.workingDir+'/data/'+self.eqName.lower()+'.csv')
                return 1
            else:
                print("Invalid Equity Symbol")
                print("Rename symbol and re-run program")
                return 0
        else:
            self.df=pd.read_csv(self.workingDir+'/data/'+self.eqName+'.csv')
            return 1
        
    def _generateMovingAverage(self):
        self.df['SMA-'+str(self.shortDays)]= np.round(self.df['Close'].rolling(window=self.shortDays).mean(),2)
        self.df['SMA-'+str(self.longDays)]= np.round(self.df['Close'].rolling(window=self.longDays).mean(),2)

    def _crossoverDates(self):
        diff = self.df['SMA-'+str(self.shortDays)] < self.df['SMA-'+str(self.longDays)]
        diff_forward = diff.shift(1)
        crossing = np.where(abs(diff - diff_forward) == 1)[0]
        self.df.iloc[crossing]["Date"].to_csv(os.getcwd()+'/data/MAC_DATES_'+self.eqName+'_'+str(self.shortDays)+'_'+str(self.longDays)+'.csv')
    
    def _generatePlot(self):
        self.plotEnd=datetime.strptime(self.end,'%Y-%m-%d')
        self.plotStart=self.plotEnd-relativedelta(years=self.plotDuration)
        self.df=self.df[(self.df['Date'] >= self.plotStart) & (self.df['Date'] <= self.plotEnd)]
        self.df=self.df[['Date','Close','SMA-'+str(self.shortDays),'SMA-'+str(self.longDays)]]
        self.df.plot(x="Date",y=['Close','SMA-'+str(self.shortDays),'SMA-'+str(self.longDays)],grid=True,figsize=(14, 7))
        plt.xlabel('Dates')
        plt.ylabel('Share price')
        plt.title('Moving Average Crossover For '+self.eqName.upper())
        plt.savefig(os.getcwd()+'/figures/MAC_'+self.eqName+'_'+str(self.shortDays)+'_'+str(self.longDays)+'.png')
        plt.show()
        
def test(no="one"):
    eqList=pickle.load(open(os.getcwd()+'/data/equityList.pickle','rb'))
    n=len(eqList)-1
    if no=="one":
        movingAverageCrossover(eqName=eqList[randint(0,n)])
    elif no=="all":
        for i in range(n+1):
            movingAverageCrossover(eqName=eqList[i])
            
if __name__=='__main__':
    test("all")