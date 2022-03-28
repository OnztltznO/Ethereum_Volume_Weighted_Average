
import requests
from datetime import datetime
import time

import math
import random
import ast
import hmac
import functools
import operator
import statistics
import sys
import os

import numpy as np

import bybit

import http.client 

from datetime import datetime

from pprint import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient import discovery

import socket
#import smtpLib, ssl 
import email.mime.multipart 
#import MIMEMultipart
import imaplib
import email
from email.header import decode_header
import traceback 
from imaplib import IMAP4_SSL

import pandas as pd

import ta as ta


def EMA_signal(closes):
  ser = pd.Series(closes, copy=False)
#  print(ser)

#  df =  dropna(ser)

  technicals_trend = ta.trend.EMAIndicator(ser)
 # trend = ta.trend()
#  print(trend)
  
  EMA21 = ta.trend.ema_indicator(close=ser, window=21, fillna=True)
#  print(EMA21.iloc[-1])

  EMA9 = ta.trend.ema_indicator(close=ser, window=9, fillna=True)
#  print(EMA9.iloc[-1])

  return EMA9.iloc[-1],EMA21.iloc[-1]


  


class HistoricalPrice(object):

    def __init__(self, host, symbol, interval, timestamp, limit, client):

        self.host = host
        self.symbol = symbol
        self.interval = interval
        self.timestamp = timestamp - (48 * 3600)
        self.limit = limit 
        self.client = client

        self.url = '{}/v2/public/kline/list'.format(self.host)


    def api_historical_response(self):
      #  r = self.client.LinearKline.LinearKline_get(symbol="BTCUSDT", interval=self.interval, limit=None, **{'from':int(self.timestamp)}).result() #IS A TYPE TUPLE FOR SOME REASON
        r = self.client.Kline.Kline_get(symbol=self.symbol, interval=self.interval, **{'from':self.timestamp}).result()
    
        for entries in r:
            self.results = entries['result']
#            print(entries)
            return self.results

    def volume(self):

        volumes = []

        for result in self.results:
            volumes.append(float(result['volume']))

            
        return volumes
        

    def price_close(self):

        closes = []


        for result in self.results:
            closes.append(float(result['close']))

        return closes

    def price_open(self):
        opens = [] 

        for result in self.results:
            opens.append(float(result['open']))

        return opens

    def price_high(self):
        highs = []

        for result in self.results:
            highs.append(float(result['high']))

        return highs

    def price_low(self):
        lows = []

        for result in self.results:
            lows.append(float(result['low']))

        return lows

    def candles(self):
        candlez = []

        for result in self.results:
            candlez.append((float(result['open']),float(result['close']),float(result['high']),float(result['low']),float(result['volume'])))

        # 0 = open, 1 = close, 2 = high, 3 = low, 4 = volume 

        return candlez


class LivePrice(object):

    def __init__(self, host, param_str, symbol, interval, timestamp):
        self.host = host
         
        self.symbol = symbol
        
        self.url = "{}/v2/public/tickers".format(self.host)




    def price_response(self):
        r = requests.get(self.url)                  #TODO: Insert URL for response
        response = r.text
        response_dict = ast.literal_eval(response)

        return (response_dict)

    def price_dict(self):
        self.response_dict = self.price_response()
        dict_result = list(self.response_dict["result"])

   #     return dict_result

        for result in dict_result:
            if result['symbol'] == self.symbol:
                price = result['last_price']


        return float(price)



class timeStamp(object):

    def __init__(self, client):
        self.client = client
        
    def api_time_request(self):
        r = self.client.Common.Common_get().result()[0]
        time = float(r['time_now'])

 #       print('API TIME: ' + str(r))
        return int(time)

    



def get_signature(api_secret,params):
    '''Encryption Signature'''

    _val = '&'.join([str(k)+"="+str(v) for k, v in sorted(params.items()) if (k != 'sign') and (v is not None)])
    # print(_val)
    return str(hmac.new(bytes(api_secret, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())

class ExecuteOrder(object):

    def __init__(self,client,symbol,side,size,price,take_profit,stop_loss):

        self.client = client
        self.symbol = symbol
        self.side = side
 #       print(int(price))
  #      print(float(size))
        self.size = size #int(round(int(price) * float(size),0))
        self.price = int(round(price,0))
   #     print(self.size)

        self.take_profit = int(round(take_profit,0))

   #     print(int(self.take_profit))
    #    print(int(self.size))
     #   print(int(self.price))
        self.stop_loss = stop_loss

            
 
        

    def order(self):

     #   client_order = client.Order.Order_newV2(side=self.side,symbol=self.symbol,order_type="Limit",qty=int(self.size),price=int(self.price),time_in_force="ImmediateOrCancel",
     #                                           take_profit=int(self.take_profit),stop_loss=self.stop_loss,order_link_id=None).result()

        client_order = client.Order.Order_newV2(side=self.side,symbol=self.symbol,order_type="Limit",qty=int(self.size),price=int(self.price),time_in_force="FillOrKill", stop_loss=self.stop_loss,order_link_id=None).result()

      #  print(client.Order.Order_new(side=self.side,symbol=self.symbol,order_type="Limit",qty=self.size,price=self.price,time_in_force="PostOnly", take_profit=(self.take_profit),stop_loss=self.stop_loss).result())

  #      client_order = client.LinearOrder.LinearOrder_new(side=self.side,symbol=self.symbol,order_type="Market",qty=self.size,price=self.price,time_in_force="FillOrKill",reduce_only=False,take_profit=int(self.take_profit),stop_loss=self.stop_loss,close_on_trigger=False).result()
  #      client_order = client.LinearConditional.LinearConditional_new(stop_px=self.stop_px, side=self.side,symbol=self.symbol,order_type="Limit",qty=self.size,base_price=self.base_price, price=self.price,time_in_force="PostOnly",reduce_only=False,take_profit=int(self.take_profit),stop_loss=self.stop_loss,close_on_trigger=False).result())
  #      print(client_order)


        return (client_order)
     #   for entries in client_order:
     #       results = entries['result']
     #       order_id = results['order_id']
     #       return order_id

      #  print(type(client_order))
     #   result = client_order['result']
     #   print("ORDER RESULT: " + str(result))
     #   order_id = result['order_id']
        
        
      #  return client_order

   
 

        


class Position(object):

    def __init__(self,host,param_str,symbol):

        self.client = client
        self.host = host
        self.params = param_str
        self.symbol = symbol

        self.url = '{}/v2/private/position/list?{}'.format(self.host,self.params)
        

    def wrapper_position(self):
        previous = []
        
        try:
            r = self.client.Positions.Positions_myPosition().result()
            for entries in r:
                results = entries['result']
                for result in results:
                    if result['symbol'] == self.symbol:
                        return float(result['position_value'])
        except Exception as e:
            print("Main program position error: " + str(e))
                
         
        


    def HTTP_connect_position(self):
        '''NOT IN USE'''        
        print("position host: " + str(self.host))
        print("position params: " + str(self.params))
        r = requests.get(self.url)
        response = r.text
        try:
           response_dict = ast.literal_eval(response)
           dict_result = response_dict['result']
           for result in dict_result.values():
               if result == self.symbol:
                  position_value = dict_result['position_value']
 
           if int(position_value) > 0:
                return True
           else:
                return False
 
        except Exception:
            server_time = int(response[143:156])
            recv_window = int(response[170:174])

            x = server_time - recv_window
            y = server_time + 1000

            print("Timestamp must be greater than this: " + str(server_time - recv_window))
            print("Timestamp must be less than this: " + str(server_time + 1000))

            midpoint = int((y+x)/2)

            print("MIDPOINT: " + str(midpoint))
            

       #     if server_time - recv_window <= timestamp < server_time + 1000:
        #            return timestamp

            
            
            return response

class Wallet(object):

    def __init__(self,client,host,param_str,symbol):

        self.client = client
        self.host = host
        self.params = param_str
        self.symbol = symbol

        self.url = '{}/v2/private/wallet/balance?{}'.format(self.host,self.params)

 

    def HTTP_connect_wallet(self):
        '''NOT IN USE'''
        r = requests.get(self.url)                   
        response = r.text
        try:
           response_dict = ast.literal_eval(response)
           dict_result = response_dict['result']
           for result in dict_result.keys():
                if result == self.symbol[0:3]:
                    balance = dict_result[result]['available_balance']
                
                
     #      print(response) 
           return balance
        except Exception:
            return response

    def wrapper_wallet(self):
        new_wallet = client.Wallet.Wallet_getBalance(coin="ETH").result()

        try:
            for new in new_wallet:
                result = new['result']
                ETH = result['ETH']
                available_balance = ETH['available_balance']
                return float(available_balance)
        except Exception:
            self.wrapper_wallet()
        
    #    return "done" 
        
         
 

def LB(SMA,closes):
    '''Lower Bollinger Band'''
    return SMA - (statistics.stdev(closes)*2)

def UB(SMA,closes):
    '''Upper Bollinger Band'''
    return SMA + (statistics.stdev(closes) * 2)


def SMA(closes):
    '''20 Day Simple Moving Average Calculation'''

    return sum(closes) / len(closes)

def EMA(closes, exponential_averages):
    '''Exponential moving averages over a period of time'''

    multiplier = (2/(len(closes) + 1))

    previous_day = SMA(closes)

    if len(exponential_averages) == 0:
        previous_day = SMA(closes)
    else:
        previous_day = exponential_averages[-1]

    EMA_calculation = ((closes[-1] - previous_day) * multiplier) + previous_day

    if len(exponential_averages) < 1 or exponential_averages[-1] != EMA_calculation:
        exponential_averages.append(EMA_calculation)

   # print((closes[-1] - previous_day) * multiplier + previous_day)
   # print((1 - multiplier) * previous_day + multiplier * closes[-1] )
   # print(closes[-1] * multiplier + previous_day * (1 - multiplier))

  #  print(str(len(closes)) + " EMA: " + str(EMA_calculation))

    return EMA_calculation

   # return (1 - multiplier) * previous_day + multiplier * closes[-1] 

    #return closes[-1] * multiplier + previous_day * (1 - multiplier)



def short_entry_candle(candles,downwards_candle):

    if candles[1] < candles[0]:     #bearish candle
        #print('short entry candle reached')
        if len(downwards_candle) == 0 or candles[3] != downwards_candle[-1]:
            downwards_candle.append(candles[3])
        return True
    else:
        return False 


def long_entry_candle(candles,upwards_candle):

    if candles[1] > candles[0]:       # bullish candle
        #print('long entry candle reached')
        if len(upwards_candle) == 0 or candles[2] != upwards_candle[-1]:
            upwards_candle.append(candles[2])
        return True
        
    else:
        return False



def MACD(closes, MACD_crosses, EMA12, EMA26):

    
    MAC_D = EMA(closes[-9:-1],EMA12) - EMA(closes[-22:-1],EMA26) # 11 and 25

  #  print(len(closes[-12:-1]))
  #  print(len(closes[-26:-1]))

  #  print("EMA26: " + str(EMA26))
  #  print("EMA12: " + str(EMA12))

    if MAC_D not in MACD_crosses:
        MACD_crosses.append(MAC_D)
        MACD_crosses = MACD_crosses[-3:-1]
      #  print(MACD_crosses)
      #  print("EMA 12: " + str(EMA12[-1]))
      #  print("EMA 26: " + str(EMA26[-1]))

def live_api_time():
    
    api_time = client.Common.Common_getTime().result()[0]
    for time in api_time:
        if time == "time_now":
            api_time = float(api_time["time_now"])+ 160800 #-(1*6000)
            return(api_time)


def time_period(client):

    #May 1 - August 1st Consolidation 
  

    today = datetime.today()   
    
    #january 10 - February 10 

    start_date = datetime(2019, 4, 23) #YY / MM / DD           Check file to see if theres an existing datetime and entry for latest EMA
  
    print(start_date)
    start =  int(start_date.timestamp())   #+ 170200 - 9390)# * 1000)) #date in millisecond timestamp
    print(start)


    end_date = datetime(2021, 10, 22)

    time_stamp = timeStamp(client)
  #  api_time = time_stamp.api_time_request() + 137000

    end = int(end_date.timestamp())# + 137000)

    print(end)
#    end.append(api_time)

    return start, end
 
    

def entry(sheet, api_time, row, price, side):


#  sheet.get(3)

  row.append(row[-1] + 1) 


  date = datetime.fromtimestamp(api_time)

  #Get corresponding cell

#  cell = sheet.cell(row[-1],1).value #row, column
  sheet.update_cell(row[-1],1, "Side: " + str(side))
  sheet.update_cell(row[-1],2, "Price: " + str(price))
#  sheet.update_cell(row[-1],8, "MACD: " + str(MACD_crosses[-1]))
 
  sheet.update_cell(row[-1],15, "Datetime: " + str(datetime.utcnow()))


#  sheet.update_cell(row[-1],13, "Balance: " + str(balance))


def stoploss(sheet,start,row,stop_loss,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction):

#  date = datetime.fromtimestamp(start)

  if first_reduction == False:
      sheet.update_cell(row[-1],9, str(stop_loss))
  #    sheet.update_cell(row[-1],13, str(balance))
 
  elif first_reduction == True and second_reduction == False:
      sheet.update_cell(row[-1],10, str(stop_loss))
  #    sheet.update_cell(row[-1],13, str(balance))
 

  elif second_reduction == True and third_reduction == False: 
      sheet.update_cell(row[-1],11, str(stop_loss))
   #   sheet.update_cell(row[-1],13, str(balance))
 

  elif third_reduction == True and fourth_reduction == False:
      sheet.update_cell(row[-1],12, str(stop_loss))
   #   sheet.update_cell(row[-1],13, str(balance))
 

  elif fourth_reduction == True and fifth_reduction == False:
      sheet.update_cell(row[-1],13, str(stop_loss))
    #  sheet.update_cell(row[-1],13, str(balance)) 

  elif fifth_reduction == True:
    sheet.update_cell(row[-1], 14, str(stop_loss))
 

def takeprofit(sheet, start, row, take_profit, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction):

 # date = datetime.fromtimestamp(start)   

  if first_reduction == False:
      sheet.update_cell(row[-1],3, str(take_profit))
  #    sheet.update_cell(row[-1],13, str(balance))
  elif first_reduction == True and second_reduction == False:
      sheet.update_cell(row[-1],4, str(take_profit))
 #     sheet.update_cell(row[-1],13, str(balance))
  elif second_reduction == True and third_reduction == False:
      sheet.update_cell(row[-1],5, str(take_profit))
 #     sheet.update_cell(row[-1],13, str(balance))     
  elif third_reduction == True and fourth_reduction == False:
      sheet.update_cell(row[-1],6, str(take_profit))
  #    sheet.update_cell(row[-1],13, str(balance)) 

  elif fourth_reduction == True and fifth_reduction == False:
    sheet.update_cell(row[-1],7, str(take_profit))
  #  sheet.update_cell(row[-1],13, str(balance)) 

  elif fifth_reduction == True:
    sheet.update_cell(row[-1],8, str(take_profit))


def taker_order(price,quantity,balance):

    return ((quantity/price) * 1.075)

def maker_order(price,quantity,balance):

    return ((quantity/price) * 1.025)


def stop_timer(early_close, host, symbol, interval, api_time, limit, client):

  while True:
    time_stamp = timeStamp(client)
    api_time = time_stamp.api_time_request() - 6000
    historical_price = HistoricalPrice(host, symbol, interval, api_time, limit, client)
    api_historical_response = historical_price.api_historical_response()
    closes = historical_price.price_close()
    if early_close != closes[-2]:
      break 


def volume_weighted_average_price(vwap_vc,vwap_volumes):



    return (sum(vwap_vc)) / sum(vwap_volumes)






def trade(host, param_str, symbol, interval, timestamp, params, limit, client, api_time, api_key, signature, sheet, api_secret):
    """The Actual Strategy """

    #TODO:
    #Fix Break Even entries
    #Bring 
    #Test?

#    print(sheet.get('A25'))

    #5.9% TP
    #2% SL
    #30 Min Time Frame 

 #   print(sheet.get('A1'))


 




    #Backtesting objects
    row = [1]
    sent_requests = 0
 
    minute = 60 * 30
    start, end = time_period(client)
    sent_requests = 0


    

    #Strategy objects


    
    
    break_even = []

    
    short_cross = False
    long_cross = False

    first_reduction = False
    second_reduction = False
    third_reduction = False
    fourth_reduction = False
    fifth_reduction = False 

    long_position = 0
    short_position = 0

    historical_price = HistoricalPrice(host, symbol, interval, api_time, limit, client)
    api_historical_response = historical_price.api_historical_response()
    closes = historical_price.price_close()
     

    EMA9, EMA21 = EMA_signal(closes)

    print("EMA9: " + str(EMA9))
    print("EMA21: " + str(EMA21))

    print("NAIVE DATETIME: " + str(datetime.utcnow()))

    vwap_vc = []
    vwap_volumes = []    
    vwaps = []

    #48 candles a day
    #Could we take the current utc time and determine how many candles should be included in the vwap calculation? 
    #First VWAP of the day is 7:30 Toronto Time 

    #NOTES
    #Adapt the stop_loss and take_profit functions for google sheets
    #Troubleshoot by testing first with calculated VWAP, if that fails adapt to tradingview VWAP 

    long_reentry = False
    short_reentry = False 


    position = False
    long_position = False
    short_position = True  

    trade_check = False 

  #  time_stamp = timeStamp(client)
  #  api_time = time_stamp.api_time_request() - 6000
  #  historical_price = HistoricalPrice(host, symbol, interval, api_time, limit, client)
  #  api_historical_response = historical_price.api_historical_response()
  #  closes = historical_price.price_close()
  #  candles = historical_price.candles()
  #  MA55 = SMA(closes[-56:-1])

    while True:
      if datetime.utcnow().hour == 00 and datetime.utcnow().minute == 30 and trade_check == False:
        break 

 
    #Potential VWAP issue at re-entry trigger. Veers off path 

    while True:
        try:
          
          if datetime.now().minute == 00 or datetime.now().minute == 30:
            time.sleep(2)
    #        print(trade_check)

            

            if trade_check == False:

              if datetime.utcnow().hour == 00 and datetime.utcnow().minute == 30 and trade_check == False:
                 print("UTC RESET.")
                 vwap_vc[:] = []
                 vwap_volumes[:] = [] 
                 vwaps[:] = []

              trade_check = True

            
              time_stamp = timeStamp(client)
              api_time = time_stamp.api_time_request() - 6000
              historical_price = HistoricalPrice(host, symbol, interval, api_time, limit, client)
              api_historical_response = historical_price.api_historical_response()
              closes = historical_price.price_close()
              candles = historical_price.candles()
              opens = historical_price.price_open()
              volume = historical_price.volume()
              MA55 = SMA(closes[-56:-1])
              highs = historical_price.price_high()
              lows = historical_price.price_low()
              

              if len(vwap_vc) == 0 or closes[-1] != vwap_vc[-1]:
                vwap_vc.append(((candles[-2][1] + candles[-2][2] + candles[-2][3]) /3) * candles[-2][4])

              if len(vwap_volumes) == 0 or volume[-1] != vwap_volumes[-1]:
                vwap_volumes.append(candles[-2][4])

              if len(vwap_vc) > 0 and len(vwap_volumes) > 0: 
                vwap = volume_weighted_average_price(vwap_vc, vwap_volumes)
              #  vwap = round(vwap,2)
                vwaps.append(vwap)
              #  print("vwap volumes: " + str(vwap_volumes))
              #  print("vwap vcs: " + str(vwap_vc))              
              #  print("latest close: " + str(candles[-1][1]))
                print("MA 55: " + str(MA55))
                print("latest close: " + str(closes[-2]))
                print("VWAP: " + str(vwaps[-1])) 

                if long_position == True and position == False and opens[-1] < MA55 and vwaps[-1] > MA55 and long_reentry == False: 
                  print("long position re-entry trigger")
                  long_reentry = True
              #  elif long_position == True and position == False and vwaps[-1] < MA55 and long_reentry == True: 
              #    long_reentry = False

                if short_position == True and position == False and opens[-1] > MA55 and vwaps[-1] < MA55 and short_reentry == False: 
                  print("short position re-entry trigger")
                  short_reentry = True
               # elif short_position == True and position == False and vwaps[-1] > MA55 and short_reentry == True:
               #   short_reentry = False 

                


                if vwaps[-1] > MA55 and candles[-2][1] > vwaps[-1] and position == False and long_position == False and long_reentry == False:  # long position 
                  print("long position hit")
                  short_position = False

                  short_reentry = False 

                  first_reduction = False
                  second_reduction = False
                  third_reduction = False
                  fourth_reduction = False
                  fifth_reduction = False

                  price = candles[-1][1]

                  side = "Buy"

                  first_tsl = round(price * 1.02,0)
                  second_tsl = round(price * 1.03,0)

                  first_tsl_move = round(price * 1.0025,0)
                  second_tsl_move = round(price * 1.01,0)
                  third_tsl_move = round(price * 1.015,0)

                  take_profit_1 = round(price * 1.04,0)
                  take_profit_2 = round(price * 1.06,0)
                  take_profit_3 = round(price * 1.08,0)
                  take_profit_4 = round(price * 1.1,0)

                  stop_loss = round(price - (price * 0.02),0)

                  position = True 
                  long_position = True 

                  entry(sheet, api_time, row, price, side)
                  sent_requests += 3



                elif vwaps[-1] < MA55 and candles[-2][1] < vwaps[-1] and position == False and short_position == False and short_reentry == False: # short position
                  print("short position hit")
                  long_position = False 

                  long_reentry = False 

                  first_reduction = False
                  second_reduction = False
                  third_reduction = False
                  fourth_reduction = False
                  fifth_reduction = False

                  price = candles[-1][1]

                  side = "Sell"

                  first_tsl = round(price - (price * 0.02),0)
                  second_tsl = round(price - (price * 0.03),0)
   
                  first_tsl_move = round(price - (price * 0.0025),0)
                  second_tsl_move = round(price - (price * 0.01),0)
                  third_tsl_move = round(price - (price * 0.015),0)

                  take_profit_1 = round(price - (price * 0.04),0)
                  take_profit_2 = round(price - (price * 0.06),0)
                  take_profit_3 = round(price - (price * 0.08),0)
                  take_profit_4 = round(price - (price * 0.1),0)

                  stop_loss = round(price * 1.02,0)

                  position = True 
                  short_position = True 

                  entry(sheet, api_time, row, price, side)
                  sent_requests += 3

                elif vwaps[-1] < MA55 and candles[-2][1] < vwaps[-1] and position == False and short_position == True and short_reentry == True:
                    print("short position re-entry")
                    long_position = False 

                    first_reduction = False
                    second_reduction = False
                    third_reduction = False
                    fourth_reduction = False
                    fifth_reduction = False

                    price = candles[-1][1]

                    side = "Sell"

                    first_tsl = round(price - (price * 0.02),0)
                    second_tsl = round(price - (price * 0.03),0)
     
                    first_tsl_move = round(price - (price * 0.0025),0)
                    second_tsl_move = round(price - (price * 0.01),0)
                    third_tsl_move = round(price - (price * 0.015),0)

                    take_profit_1 = round(price - (price * 0.04),0)
                    take_profit_2 = round(price - (price * 0.06),0)
                    take_profit_3 = round(price - (price * 0.08),0)
                    take_profit_4 = round(price - (price * 0.1),0)

                    stop_loss = round(price * 1.02,0)

                    position = True 
                    short_position = True 

                    entry(sheet, api_time, row, price, side)
                    sent_requests += 3

                elif vwaps[-1] > MA55 and candles[-2][1] > vwaps[-1] and position == False and long_position == True and long_reentry == True:
                        print('long position re-entry')
                        short_position = False

                        first_reduction = False
                        second_reduction = False
                        third_reduction = False
                        fourth_reduction = False
                        fifth_reduction = False

                        price = candles[-1][1]

                        side = "Buy"

                        first_tsl = round(price * 1.02,0)
                        second_tsl = round(price * 1.03,0)

                        first_tsl_move = round(price * 1.0025,0)
                        second_tsl_move = round(price * 1.01,0)
                        third_tsl_move = round(price * 1.015,0)

                        take_profit_1 = round(price * 1.04,0)
                        take_profit_2 = round(price * 1.06,0)
                        take_profit_3 = round(price * 1.08,0)
                        take_profit_4 = round(price * 1.1,0)

                        stop_loss = round(price - (price * 0.02),0)

                        position = True 
                        long_position = True 

                        entry(sheet, api_time, row, price, side)
                        sent_requests += 3
          

          elif datetime.now().minute == 10 or datetime.now().minute == 40:
            trade_check = False 

          
          

          if position == True: 
            time_stamp = timeStamp(client)
            api_time = time_stamp.api_time_request() - 6000
            historical_price = HistoricalPrice(host, symbol, interval, api_time, limit, client)
            api_historical_response = historical_price.api_historical_response()
 
            if side == "Buy":
              if first_reduction == False and (historical_price.price_low()[-1] <= stop_loss or historical_price.price_close()[-1] <= stop_loss):
                  stoploss(sheet,start,row,stop_loss,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                  sent_requests += 1
                  print("Buy Stop Loss hit")
                  position = False 
   
              if historical_price.price_high()[-1] >= first_tsl or historical_price.price_close()[-1] >= first_tsl:
                  if first_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, first_tsl, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      first_reduction = True 
                      print("Buy first TSL hit")
                      print("New SL: " + str(first_tsl_move))

              if historical_price.price_high()[-1] >= second_tsl or historical_price.price_close()[-1] >= second_tsl:
                  if second_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, second_tsl, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      second_reduction = True 
                      print("Buy second TSL hit")
                      print("New SL: " + str(second_tsl_move))


              if historical_price.price_high()[-1] >= take_profit_1 or historical_price.price_close()[-1] >= take_profit_1:
                  if third_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_1, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      third_reduction = True 
                      print("Buy TP1 hit")
                      print("New SL: " + str(third_tsl_move))


              if historical_price.price_high()[-1] >= take_profit_2 or historical_price.price_close()[-1] >= take_profit_2:
                  if fourth_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_2, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      fourth_reduction = True
                      print("Buy TP2 hit") 
                      print("New SL: " + str(take_profit_1))

              if historical_price.price_high()[-1] >= take_profit_3 or historical_price.price_close()[-1] >= take_profit_3:
                  if fifth_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_3, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      fifth_reduction = True 
                      print("Buy TP3 hit")
                      print("New SL: " + str(take_profit_2))


              if historical_price.price_high()[-1] >= take_profit_4 or historical_price.price_close()[-1] >= take_profit_4:
                  if fifth_reduction == True:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_4, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      position = False 
                      print("Buy TP4 hit")
                      print("New SL: " + str(take_profit_3))


              if first_reduction == True and (historical_price.price_low()[-1] <= first_tsl_move or historical_price.price_close()[-1] <= first_tsl_move):
                stoploss(sheet,start,row,first_tsl_move,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False
                print("Buy first tsl move hit")
                long_reentry = False

              if second_reduction == True and (historical_price.price_low()[-1] <= second_tsl_move or historical_price.price_close()[-1] <= second_tsl_move):
                stoploss(sheet,start,row,second_tsl_move,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False  
                print("Buy second tsl move hit")
                long_reentry = False

              if third_reduction == True and (historical_price.price_low()[-1] <= third_tsl_move or historical_price.price_close()[-1] <= third_tsl_move):
                stoploss(sheet,start,row,third_tsl_move,first_reduction,second_reduction, third_reduction, fourth_reduction. fifth_reduction)
                sent_requests += 1
                position = False 
                print("Buy third tsl move hit")
                long_reentry = False

              if fourth_reduction == True and (historical_price.price_low()[-1] <= take_profit_1 or historical_price.price_close()[-1] <= take_profit_1):
                stoploss(sheet,start,row,take_profit_1,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False 
                print("Buy SL TP1 hit")
                long_reentry = False

              if fifth_reduction == True and (historical_price.price_low()[-1] <= take_profit_2 or historical_price.price_close()[-1] <= take_profit_2):
                stoploss(sheet,start,row,take_profit_2,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False 
                print("Buy SL TP2 hit")
                long_reentry = False

              if candles[-1][0] <= MA55 and position == True:
                stoploss(sheet,start,row,"Moving Average Close " + str(historical_price.price_close()[-1]),first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False
                print("Buy Moving Average Close hit " + str(historical_price.price_close()[-1])) 
                long_reentry = True 

            elif side == "Sell":
              if first_reduction == False and (historical_price.price_high()[-1] >= stop_loss or historical_price.price_close()[-1] >= stop_loss):
                  stoploss(sheet,start,row,stop_loss,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                  sent_requests += 1
                  print("Sell Stop Loss hit")
                  position = False 
   
              if historical_price.price_low()[-1] <= first_tsl or historical_price.price_close()[-1] <= first_tsl:
                  if first_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, first_tsl, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      first_reduction = True
                      print("Sell first TSL hit") 
                      print("New SL: " + str(first_tsl_move))

              if historical_price.price_low()[-1] <= second_tsl or historical_price.price_close()[-1] <= second_tsl:
                  if second_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, second_tsl, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      second_reduction = True 
                      print("Sell second TSL hit")
                      print("New SL: " + str(second_tsl_move))

              if historical_price.price_low()[-1] <= take_profit_1:
                  if third_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_1, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      third_reduction = True 
                      print("Sell TP1 hit")
                      print("New SL: " + str(third_tsl_move))

              if historical_price.price_low()[-1] <= take_profit_2 or historical_price.price_close()[-1] <= take_profit_2:
                  if fourth_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_2, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      fourth_reduction = True 
                      print("Sell TP2 hit")
                      print("New SL: " + str(take_profit_1))

              if historical_price.price_low()[-1] <= take_profit_3 or historical_price.price_close()[-1] <= take_profit_3:
                  if fifth_reduction == False:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_3, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      fifth_reduction = True
                      print("Sell TP3 hit") 
                      print("New SL: " + str(take_profit_2))

              if historical_price.price_low()[-1] <= take_profit_4 or historical_price.price_close()[-1] <= take_profit_4:
                  if fifth_reduction == True:
                      sent_requests += 1
                      takeprofit(sheet, start, row, take_profit_4, first_reduction, second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                      position = False 
                      print("Sell TP4 hit")
                      print("New SL: " + str(take_profit_3))

              if first_reduction == True and (historical_price.price_high()[-1] >= first_tsl_move or historical_price.price_close()[-1] >= first_tsl_move):
                stoploss(sheet,start,row,first_tsl_move,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False
                print("Sell first tsl move hit")
                short_reentry = False

              if second_reduction == True and (historical_price.price_high()[-1] >= second_tsl_move or historical_price.price_close()[-1] >= second_tsl_move):
                stoploss(sheet,start,row,second_tsl_move,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False
                print("Sell second tsl move hit")  
                short_reentry = False

              if third_reduction == True and (historical_price.price_high()[-1] >= third_tsl_move or historical_price.price_close()[-1] >= third_tsl_move):
                stoploss(sheet,start,row,third_tsl_move,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False 
                print("Sell third tsl move hit")
                short_reentry = False

              if fourth_reduction == True and (historical_price.price_high()[-1] >= take_profit_1 or historical_price.price_close()[-1] >= take_profit_1):
                stoploss(sheet,start,row,take_profit_1,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False 
                print("Sell SL TP1 hit")
                short_reentry = False 


              if fifth_reduction == True and (historical_price.price_high()[-1] >= take_profit_2 or historical_price.price_close()[-1] >= take_profit_2):
                stoploss(sheet,start,row,take_profit_2,first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False 
                print("Sell SL TP2 hit")
                short_reentry = False 


              if candles[-1][0] >= MA55 and position == True:
                stoploss(sheet,start,row,"Moving Average Close " + str(historical_price.price_close()[-1]),first_reduction,second_reduction, third_reduction, fourth_reduction, fifth_reduction)
                sent_requests += 1
                position = False 
                print("Sell Moving Average Close hit") 
                short_reentry = True 

        except Exception as e:
          print("Error: " + str(e))
          time.sleep(100) 




    
   # closes = historical_price.price_close()
   # print("CLOSES: " + str(closes))
   # print(len(closes))
   # time.sleep(60)

   # zero_cross = MACD(closes, MACD_crosses)
   # print(MACD_crosses)
    
#    print(len(closes))
#    volume = historical_price.volume()
#    volume_sma = SMA(volume[-20:-1])
#    print(type(volume[-1]))

#    low = historical_price.price_low()
#    high = historical_price.price_high()
#    print("Low: " + str(low))
#    print("High: " + str(high))


#    simple_moving_average = SMA(closes[-20:-1])
#    upper_band = UB(simple_moving_average,closes[-21:-1])
#    lower_band = LB(simple_moving_average,closes[-21:-1])

 #   print("Upper Band: " + str(upper_band))
 #   print("Lower Band: " + str(lower_band))

 #   print("Latest Close: " + str(closes[-1]))

  #  positions = Position(host,param_str,symbol)
  #  position = positions.wrapper_position()
  #  live_price = LivePrice(host, param_str, symbol, interval, timestamp)
   # print("POSITION: " + str(position))
    

 #   wallet = Wallet(client,host,param_str,symbol)
 #   size = wallet.wrapper_wallet()
 #   print("Balance: " + str(size))# * live_price.price_dict()))

  #  live_price = LivePrice(host, param_str, symbol, interval, timestamp)
  #  price = live_price.price_dict()
  #  print(price)


  #Record entry, stop loss, take profit, and date/time in google sheets
  #














if __name__ == "__main__":

  #GOOGLE SHEETS 
  scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets'] #authorization For Drive


  credentials = ServiceAccountCredentials.from_json_keyfile_name("Bybit_Bitcoin_1_Minute_Data-517ea6748c2b.json",scope)     #JSON FILE WITH Credentials

  client = gspread.authorize(credentials)   

  sheet = client.open("VWAP + SMA55 Live").worksheet('Dec Live Test')#SHEET

#  data = sheet.get_all_records() 

  # TODO: Change code below to process the `response` dict:
# pprint(data)
  timestamp =  int(time.time()*1000) + 4000000 - 310000 #+5000
  timestamp = int(time.time()*1000) + 2500
  api_domain = {"live": "MSSbffFG1IWPkA1SZq", "test": "b1PEl6WF2IldIg4nGb"} #Ontario IP: "JOY4FE04n78T30XJ0r"}
  secret = {"live": "wT32i3s7DXz7bv0gPILdh0ESQpTxoTVpZ8za", "test": "ka1afUc2iAPe4FR0KP7KtqHKYfWLm8216lQm"} #"h7UObGL1FcTYtezWuNH9qolfY32uSAVaShlC"}
  url_domain = {"live": "https://api.bybit.com", "test": "https://api-testnet.bybit.com"}

  domain = "live"
  api_key = api_domain[domain]
  host = url_domain[domain]
  api_secret = secret[domain]
  client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)   
  limit = '5'
  symbols = ["BTCUSD","ETHUSD","EOSUSD","XPRUSD","BTCUSDT"]
  symbol = "ETHUSD"
  leverage = "1"
  interval = "30"          #timeframe
  time_stamp = timeStamp(client)
  api_time = time_stamp.api_time_request() - 6000   #3 Min = + 137000       15 min = - 6000
  print("API TIME: " + str(api_time)) 
  print("TIMESTAMP: " + str(timestamp))
  client.Positions.Positions_saveLeverage(symbol=symbol, leverage="1").result()
  params = {}
  params['api_key'] = api_domain[domain]
  params['leverage'] = leverage
  params['symbol'] = symbol
  params['timestamp'] = timestamp
  signature = get_signature(api_secret,params)
  param_str = "api_key={}&leverage={}&symbol={}&timestamp={}&sign={}".format(api_key, leverage, symbol, timestamp, signature)  # Parameter required for HTTP requests
  trade(host, param_str, symbol, interval, timestamp, params, limit, client, api_time, api_key, signature, sheet, api_secret)






#Necessary Alerts:
# Alert when EMA 9 is greater or less than EMA 21
# Alert when EMA 21 is greater or less than MA 55








