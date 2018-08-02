# -*- coding: utf-8 -*-


import os
import config
import pickle
import quandl
from quandl.errors.quandl_error import NotFoundError 


quandl.ApiConfig.api_key=config.key


def customAdd(name,start='2003-05-31',end='2018-05-31',workingDir=os.getcwd()):
    try:
        df=quandl.get('NSE/'+name,start_date=start,end_date=end)
        df.to_csv(workingDir+'/data/'+name.lower()+'.csv')
        return 1
    except NotFoundError:
        print("Symbol Does not Exist")
        return 0
        
        
"""
This function is used to check if the following files exist in the script folder or not
so that over repeat runs, the program does not unnecessarily burden quandl servers,
also adds significant speed to program and having a local copy allows to work without internet
"""
class setupEnvironment:
    def __init__(self,workingDir=os.getcwd(),startDate='2003-05-31',endDate='2018-05-31',eqList=["HINDALCO","BAJAJFINSV","ITC","TITAN","TECHM"]):
        self.workingDir=workingDir
        self.startDate=startDate
        self.endDate=endDate
        self.eqList=eqList
    def _individualData(self,name):
        if not os.path.isfile(self.workingDir+'/data/'+name.lower()+'.csv'):
            df=quandl.get('NSE/'+name,start_date=self.start,end_date=self.end)
            df.to_csv(self.workingDir+'/data/'+name.lower()+'.csv')
    def _writeFile(self):
        pickle.dump(self.eqList,open(os.getcwd()+'/data/equityList.pickle','wb'))
    def checkExistingFiles(self):
        if not os.path.exists(self.workingDir+'/data'):
            os.makedirs(self.workingDir+'/data')
        if not os.path.exists(self.workingDir+'/figures'):
            os.makedirs(self.workingDir+'/figures')
        for i in self.eqList:
            self._individualData(i)
        self._writeFile()
def main():
    workingDir=input("Full path of the directory where the data needs to be stored:")
    startDate=input("starting date for analysis timeframe:")
    endDate=input("ending date for analysis timeframe:")
    n=int(input("number of equities:"))
    eqList=[]
    for i in range(n):
        temp=input("Equity symbol:")
        eqList.append(temp.upper())
    env=setupEnvironment(workingDir,startDate,endDate,eqList)
    env.checkExistingFiles()
    
if __name__ !='__main__':
    env=setupEnvironment()
    env.checkExistingFiles()
else:
    #main()
    customAdd('BANKNIFTY')