# -*- coding: utf-8 -*-


import pandas as pd
import dataSetup
import numpy as np
import os
import pickle
from scipy.stats import norm
import matplotlib.pyplot as plt
np.warnings.filterwarnings('ignore')
#All PnL calculations can be performed with close,open,high,low prices
#Therefore we need to create a single date indexed DataFrame that can be used for all calculations


#This class has is not extensible for number of equities without adding
#lot sizes in same order
class Portfolio:
    def __init__(self,analysisType="Close",
                 eqList=["HINDALCO","BAJAJFINSV","ITC","TITAN","TECHM"],
                 portfolioSize=5000000,
                 confidenceLevel=0.9,
                 rollingSize=1260):
        self.analysisType=analysisType.title()
        self.eqList=list(set(eqList))
        self.portfolioSize=portfolioSize
        self.lotSizes=self.generateLotSizes()
        self.confidenceLevel=confidenceLevel
        self.rollingSize=rollingSize
        self.workingDir=os.getcwd()
        
        if self.verifyToProceed():
            if self.combinePrice():
                self.dailyPNL()
                self.var()
                self.donotPlot=False
                self.donotReturn=False
                self.existingList=pickle.load(open(self.workingDir+'/data/equityList.pickle',"rb"))
                self.existingList+=self.eqList
                self.existingList=list(set(self.existingList))
                pickle.dump(self.existingList,open(self.workingDir+'/data/equityList.pickle',"wb"))
            else:
                self.donotPlot=True
                self.donotReturn=True
                self.existingList=pickle.load(open(self.workingDir+'/data/equityList.pickle',"rb"))
                self.existingList+=self.eqList
                self.existingList=list(set(self.existingList))
                pickle.dump(self.existingList,open(self.workingDir+'/data/equityList.pickle',"wb"))
        else:
            self.donotPlot=True
            self.donotReturn=True
    def generateLotSizes(self):
        df=pd.read_csv(os.getcwd()+'/data/LotSizes.csv')
        df.set_index("Symbol",inplace=True)
        lots=[]
        for i in self.eqList:
            if i in df.index:
                lots.append(df.loc[i]["LotSizes"])
        return lots
    
    def verifyToProceed(self):
        if len(self.eqList)!=len(self.lotSizes):
            print("Sorry not all the tickers you gave as input are valid")
            return 0
        elif self.analysisType not in ["Open","Close","High","Low"]:
            print('Invalid analysis type.choose one from ["Open","Close","High","Low"]')
            return 0
        elif self.portfolioSize<=0:
            print('Enter valid portfolio size')
            return 0
        else:
            return 1
            
    def combinePrice(self):
        individualCloses={}
        index=-1
        for i in self.eqList:
            index+=1
            if not os.path.isfile(self.workingDir+'/data/'+i.lower()+'.csv'):
                if not dataSetup.customAdd(i.upper()):
                    self.eqList.pop(index)
                    return 0
            individualCloses[i]=pd.read_csv(os.getcwd()+'/data/'+i.lower()+".csv")[["Date",self.analysisType]]
            individualCloses[i].columns=["Date",i.upper()]
            individualCloses[i]["Date"]=pd.to_datetime(individualCloses[i]["Date"])
            individualCloses[i].set_index("Date",inplace=True)
        self.df=pd.concat([individualCloses[i] for i in individualCloses.keys()],axis=1,sort=True).dropna()
        self.df=self.df[[i.upper() for i in self.eqList]]
        return 1
    def dailyPNL(self):
        #1.Firstly we will need to calculate stock weights    
        #formula= Individual Lot Size/ Sum of all Lot Sizes
        #Lot sizes will be an initially set value because 
        #no reliable source of historic lot sizes has been found
        stockWeights=np.array(self.lotSizes)/np.sum(self.lotSizes,axis=0)
        #Now we need to multiply it by our first day's close prices to see unit cost
        unitCost=np.sum(self.df.iloc[0].mul(stockWeights,axis=0),axis=0)
        #Now we need to scale this to portfolioSize
        sizeMultiplier=self.portfolioSize/unitCost
        #we need to find no. of shares per equity
        sharesPerEquity=np.round(sizeMultiplier*stockWeights,decimals=0)
        self.df["PortfolioVal"]=np.sum(self.df.mul(sharesPerEquity,axis=1),axis=1)
        self.df["PnL"]=self.df["PortfolioVal"]-self.df["PortfolioVal"].shift(1)
        self.df["PnL"]=self.df["PnL"].fillna(value=0)
    
    def varCovar(self,value, confidence,mean,volatility):
        alpha = norm.ppf(1-confidence, mean,volatility)
        return value - value*(alpha + 1)
    
    def var(self):
        returns=self.df["PortfolioVal"].pct_change().fillna(value=0)
        returns=np.round(returns,decimals=2)
        self.df["VAR"]=self.varCovar(self.portfolioSize,
          self.confidenceLevel,returns.rolling(self.rollingSize).mean(),
          returns.rolling(self.rollingSize).std())
        self.df["VAR"]=np.round(self.df["VAR"],decimals=2)
    
    def plotPNL(self):
        if not self.donotPlot:
            plt.plot(self.df.index,self.df["PnL"])
            plt.xlabel('Dates')
            plt.ylabel('PnL')
            plt.figtext(1.0,1.0,'Portfolio Size:'+str(self.portfolioSize))
            plt.title('PROFIT AND LOSS CURVE FOR THE STRATEGY')
            plt.show()
            plt.savefig('{}/figures/pnl_{}.png'.format(os.getcwd(),self.portfolioSize))

    def plotVar(self):
        if not self.donotPlot:
            self.df["VAR"].plot(figsize=(10,5),grid=True)
            plt.ylabel("Value at Risk")
    
    def getDataFrame(self):
        if not self.donotReturn:
            return self.df
        else:
            return None

#    lotSizes=[3500,1575,125,1200,750]  #order is "HINDALCO","ITC","BAJAJFINSV","TECHM","TITAN"

def test():
    portfolio1=Portfolio()
    df=portfolio1.getDataFrame()
    if df is not None:
        print(df[["PortfolioVal","PnL","VAR"]].dropna().head())
    portfolio1.plotPNL()
    portfolio1.plotVar()

if __name__=="__main__":
    test()
    
    
