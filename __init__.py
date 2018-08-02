# -*- coding: utf-8 -*-
__author__="Priyesh Srivastava"
__version__="1.0.0"
#This will allow you to use the project as a module
__all__=["customAdd",
         "MAC",
         "setupEnvironment",
         "drawDown",
         "portfolioGenerate"]

import portfolio
import drawdown
import movingAverageCrossover
import dataSetup
import os

def customAdd(name,start='2003-05-31',end='2018-05-31',workingDir=os.getcwd()):
    dataSetup.customAdd(name,start='2003-05-31',end='2018-05-31',workingDir=os.getcwd())

def MAC():
    return movingAverageCrossover.movingAverageCrossover()
 
def setupEnvironment():
    return dataSetup.setupEnvironment()

def drawDown():
    return drawdown.Drawdown()

def portfolioGenerate():
    return portfolio.Portfolio()