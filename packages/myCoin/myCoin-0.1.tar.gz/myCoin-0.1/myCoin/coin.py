# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:17:28 2019

@author: edalr
"""
    
class Coin():
    '''Parent class with coin attributes accross all crypto currencies'''
    def __init__(self, coin_name, coin_symbol):
        '''Set coin name and symbol'''
        self.name = coin_name
        self.symbol = coin_symbol
        self.price = 0
        self.circulating = 0
        self.fixed_supply = False
        self.mineable = False
    def inputCoinData(self, price, circulating_supply):
        '''Set the coin circulating supply and price
        
        >>> c = Coin("Ethereum", "ETH")
        >>> c.inputCoinData(25, 4)
        >>> c.price
        25
        '''
        self.price = price
        self.circulating = circulating_supply 



class edwin_coin(Coin):
    '''A specific subclass of Coin above'''
    def __init__(self):
         '''Initialize coin and set currency symbol'''
         Coin.__init__(self, "EdwinCoin", "EDC")
         self.mc = 0
    def getMarketCap(self):
        '''Calculate Market Cap price based on circulating supply and price'''
        self.mc = self.price*self.circulating
    def setMineable(self):
        '''Define boolean if coin is mineable'''
        self.mineable = True
    def setFixedSupply(self):
        '''Define boolean if coin is mineable'''
        self.fixed_supply = True

        








        
        

