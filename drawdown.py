# -*- coding: utf-8 -*-



import matplotlib.pyplot as plt
import portfolio
import os
from matplotlib.ticker import FuncFormatter



class Drawdown:
    def __init__(self):
        self.fulldf=portfolio.Portfolio()
        self.portfolio=self.fulldf.getDataFrame()[["PortfolioVal","PnL"]]
        self.calculateDrawdown()
        
    def calculateDrawdown(self):
        self.portfolio["Drawdowns"]=self.portfolio["PortfolioVal"].pct_change()
        self.portfolio["Drawdowns"][self.portfolio["Drawdowns"]>0]=0
        self.portfolio["Drawdowns"]*=100
        self.portfolio.fillna(value=0,inplace=True)        
        print(self.portfolio.head())
        max_daily_drawdown=self.portfolio["Drawdowns"].min()*-1
        print("{}%".format(max_daily_drawdown))
    
    def plotDrawdown(self,plotColor="blue",transparency=0.5,figSize=(12,7)):
        
        self.ax = plt.gca()
        self.setPlotProperties(plotColor,transparency,figSize)
        self.setupXaxis()
        self.setupYaxis()
        self.setTitle()
        self.plotActual()
        
        plt.setp(self.ax.get_xticklabels(),
                 visible=True,
                 rotation=0,
                 ha='center')
        plt.savefig(os.getcwd()+'/figures/underwaterPlot.png')
        plt.show()
    
    def plotActual(self):
        self.portfolio["Drawdowns"].plot(ax=self.ax,
                      grid=True,
                      lw=1,
                      kind='area',
                      color=self.plotColor,
                      alpha=self.transparency,
                      figsize=self.figSize)
        
    def setPlotProperties(self,plotColor,transparency,figSize):
        self.plotColor=plotColor
        self.transparency=transparency
        self.figSize=figSize
    
    def formatPerc(self,x, pos):
        return '%.0f%%' % x
    
    def setupYaxis(self):
        self.ax.set_ylabel('Drawdown',fontsize=14)
        self.ax.yaxis.set_label_position("right")
        self.ax.yaxis.tick_right()
        self.ax.yaxis.set_major_formatter(FuncFormatter(self.formatPerc))
        
    def setupXaxis(self):
        self.ax.set_xlabel('Date',fontsize=14)
        self.ax.xaxis.set_label_position("top")
        self.ax.xaxis.tick_top()
    def setTitle(self):
        self.ax.set_title('Portfolio Drawdown (%)',
                          fontweight='bold',
                          y=1.15,
                          fontsize=20)
def test(parameters=["red",0.3,(10,6)]):
    drawdown=Drawdown()
    drawdown.plotDrawdown(parameters[0],parameters[1],parameters[2])

if __name__=='__main__':
    test()