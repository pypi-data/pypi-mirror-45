# encoding:utf-8
# distutils: language=c++
from cpython cimport PyObject
from libc.stdlib cimport malloc, free
from libc.string cimport const_char
from libcpp cimport bool as cbool
 
# from libcpp.memory cimport shared_ptr,make_shared
import ctypes
import configparser

from imp import reload
import time
from   datetime import datetime
import pymysql
import sys
import collections
import traceback

import cfg.ptp_env                as myEnv
import cfg.ptp_can_change_env     as myDEnv

from ptp       import py_ApiStructure

def  toString(val):
  if isinstance(val,bytes):
    myVal = bytes.decode(val,encoding="gb18030", errors="ignore")
  elif isinstance(val,(int,float)):
    myVal = str(val)
  else:
    myVal = val

  return myVal  
  
  
def  toString2(val):
  if isinstance(val,bytes):
    myVal = "'" + bytes.decode(val,encoding="gb18030", errors="ignore")  + "'" 
  elif isinstance(val,str):
    myVal = "'" + val + "'"
  else:
    myVal =  str(val)

  return myVal  
  
def  myDecode(val):
  if isinstance(val,bytes):
    myVal = bytes.decode(val,encoding="gb18030", errors="ignore")  
  else:
    myVal = val

  return myVal  

def nvl(p1, p2):
  if p1 is None:
    return p2
  else:
    return p1
    
def  printString(fileName, key, val, dwTimes=1):
    config = configparser.ConfigParser()
    config.read("cfg/ptp.ini",encoding="utf-8")

    if isinstance(val,bytes):
        myVal = bytes.decode(val,encoding="gb18030", errors="ignore")
    elif isinstance(val,(int,float)):
        myVal = str(val)
    else:
        myVal = val
    try:
        detail = config.get("PYTHON_SWITCH", "detail")
        debug  = config.get("PYTHON_SWITCH", "debug")
    except Exception as err:
        print(err)
        
    if debug == "1":
        with open("log/py2c_"+ fileName + ".log", "a+") as f:
            f.write(str(dwTimes) + ":" + key + "=" + myVal + "\n")
    if detail == "1":
        with open("log/py2c_all.log", "a+") as f:
            f.write(str(dwTimes) + ":" + key + "=" + myVal + "\n")

def  printNumber(fileName, key, val, dwTimes=1):
    config = configparser.ConfigParser()
    config.read("ptp.ini",encoding="utf-8")
    try:
        detail = config.get("PYTHON_SWITCH", "detail")
        debug = config.get("PYTHON_SWITCH", "debug")
    except Exception as err:
        print(err)

    if debug == "1":
        with open("log/py2c_"+ fileName + ".log", "a+") as f:
            f.write(str(dwTimes) + ":" + key + "=" + str(val) + "\n")
    if detail == "1":
        with open("log/py2c_all.log", "a+") as f:
            f.write(str(dwTimes) + ":" + key + "=" + str(val) + "\n") 

 
def testPerform(i):
  sum = 0
  for it in range(i):
    sum = sum + it * 2 - it * 1.2 / 3
  return sum

def  dump_py2c(fileName, logInfo, dwTimes=1):
  config = configparser.ConfigParser()
  config.read("ptp.ini",encoding="utf-8")
  
  try:
    detail = config.get("PYTHON_SWITCH", "detail")
    debug  = config.get("PYTHON_SWITCH", "debug")
  except Exception as err:
    print(err)

  if debug == "1":
    with open("log/py2c_"+ fileName + ".log", "a+") as f:
      f.write(str(dwTimes) + ":" + logInfo + "\n")
  if detail == "1":
    with open("log/py2c_all.log", "a+") as f:
      f.write(str(dwTimes) + ":" + logInfo + "\n")  
      

def  dump_c2py(fileName, logInfo, dwTimes=1):
  config = configparser.ConfigParser()
  config.read("ptp.ini",encoding="utf-8")
  
  try:
    detail = config.get("PYTHON_SWITCH", "detail")
    debug  = config.get("PYTHON_SWITCH", "debug")
  except Exception as err:
    print(err)

  if debug == "1":
    with open("log/c2py_"+ fileName + ".log", "a+") as f:
      f.write(str(dwTimes) + ":" + logInfo + "\n")
  if detail == "1":
    with open("log/c2py_all.log", "a+") as f:
      f.write(str(dwTimes) + ":" + logInfo + "\n") 


def connectDB():
    dbConnect = None

    try:
      config= configparser.ConfigParser()
      config.read("cfg/ptp.ini",encoding="utf-8")
      PTP_DB_TYPE   = config.get("CLOUD", "PTP_DB_TYPE")
      PTP_DB_SERVER = config.get("CLOUD", "PTP_DB_SERVER")
      PTP_DB_USER   = config.get("CLOUD", "PTP_DB_USER")
      PTP_DB_PWD    = config.get("CLOUD", "PTP_DB_PWD")
      PTP_DB_NAME   = config.get("CLOUD", "PTP_DB_NAME")
      PTP_DB_PORT   = int(config.get("CLOUD", "PTP_DB_PORT"))
    except Exception as err:
      myEnv.logger.error('get db config', exc_info=True) 
      PTP_DB_TYPE   = None
      PTP_DB_SERVER = None
      PTP_DB_USER   = None
      PTP_DB_PWD    = None
      PTP_DB_NAME   = None
      PTP_DB_PORT   = None

    PTP_DB_TYPE   = nvl(PTP_DB_TYPE  ,"mysql"       )
    #PTP_DB_SERVER = nvl(PTP_DB_SERVER,"103.235.232.142")
    PTP_DB_SERVER = nvl(PTP_DB_SERVER,"127.0.0.1"   )
    PTP_DB_USER   = nvl(PTP_DB_USER  ,"sim_test"    )
    PTP_DB_PWD    = nvl(PTP_DB_PWD   ,"SimTest@2019")
    PTP_DB_NAME   = nvl(PTP_DB_NAME  ,"sim_test"    )
    PTP_DB_PORT   = nvl(PTP_DB_PORT  ,3306          )

    dbConnect = pymysql.Connect(host=PTP_DB_SERVER , user=PTP_DB_USER
                                  , passwd=PTP_DB_PWD, db  =PTP_DB_NAME
                                  , charset="utf8"   , port=PTP_DB_PORT)
    return dbConnect      

def ExecuteQuery(i_strSQL):
    results = ()
    try:
      myDB = connectDB()
      mycursor = myDB.cursor()      
    
      if len(i_strSQL) == 0:
          return results;

      if type(mycursor) != pymysql.cursors.Cursor:
          return results


      mycursor.execute(i_strSQL)
      # 获取所有记录列表
      results = mycursor.fetchall()

    except Exception as err:
        myEnv.logger.error('ExecuteQuery', exc_info=True)

    return results;
    
class MathFunction(object):
    def __init__(self, name, operator):
        self.name = name
        self.operator = operator

    def __call__(self, *operands):
        return self.operator(*operands)
        
class CPTPAlgos(object):     
  
  def __init__(self):
    try:  
      myEnv.logger.info('CPTPAlgos.init ...')
      
      """
      'OnRspQryInstrument', 
      'OnRspOrderInsert', 
      'OnRspQryOrder', 
      'OnRspQryInvestorPosition', 
      'OnRspQrySettlementInfo', 
      'OnRtnOrder', 
      'OnRtnInstrumentStatus'
      ReqOrderInsert
      """ 
      self.update_factor_date = datetime.now()
      #全局属性
      self.global_dict          = collections.OrderedDict()
      
      #合约属性
      self.instrument_attr_dict = collections.OrderedDict()
      #记录报单，用于模拟时行情驱动自动成交的报单簿
      self.instrument_req_order_dict = collections.OrderedDict()
      #记录报单回报，用于撤单
      self.instrument_rtn_order_dict = collections.OrderedDict()
      #记录仓位回报，用于平仓
      self.instrument_position_dict = collections.OrderedDict() 
      #记录资金信息 
      self.TradingAccount = {} 
      
      self.instrumentStatus = collections.OrderedDict() 
      
      self.__RequestID = 0 #记录调用次数
      self.__id        = 1 #用于重演行情
      
      myEnv.logger.info("get config for Algos")

      self.config= configparser.ConfigParser()
      self.config.read("cfg/ptp.ini",encoding="utf-8")
 
      self.upload      = int(self.config.get("CLOUD", "upload"))
      self.cloud_debug = int(self.config.get("CLOUD", "debug"))
      self.array_size  = int(self.config.get("CLOUD", "array_size"))
      self.c_cython    = int(self.config.get("COMMUNICATION_SWITCH", "c_cython"))
      self.cython_c    = int(self.config.get("COMMUNICATION_SWITCH", "cython_c"))
                 
      myEnv.logger.info('CPTPAlgos.init end.')
    except Exception as err:
      myEnv.logger.error('CPTPAlgos.init', exc_info=True) 
      self.upload      = 1
      self.cloud_debug = 1
      self.array_size  = 10
      self.c_cython    = 1
      self.cython_c    = 1

  def Inc_RequestID(self):
    self.__RequestID = self.__RequestID + 1
    return self.__RequestID
      
  def get_InstrumentAttr(self, instrumentID):
    l_dict={}

    if not instrumentID is None :
      l_dict= self.instrument_attr_dict.get(instrumentID)

    return l_dict      
  
  """
  这个某个合约的一个属性
  """
  def set_InstrumentAttr(self, instrumentID, key, val):
    try:
      l_dict={}

      if not instrumentID is None and not key is None and not val is None:
        l_dict= self.instrument_attr_dict.get(instrumentID)
        if l_dict is None:
          l_dict = self.InitFactor()
          self.instrument_attr_dict[instrumentID] = l_dict  
        
        l_dict[key] = val
      
    except Exception as err:
        myEnv.logger.error('set_InstrumentAttr', exc_info=True)
        
  """
  'OnRspQryInstrument', 
  'OnRspOrderInsert', 
  'OnRspQryOrder', 
  'OnRspQryInvestorPosition', 
  'OnRspQrySettlementInfo', 
  'OnRtnOrder', 
  'OnRtnInstrumentStatus'
  ReqOrderInsert
  OnRspQryTradingAccount
  """ 
   
  def push_OnRspQryTradingAccount(self, table_name, TradingAccount):          
    l_dict = TradingAccount.to_dict()
    self.TradingAccount.update(l_dict)
    
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)    
    
  def push_OnRspQryInstrument(self, table_name, Instrument):          
    l_dict = Instrument.to_dict()
    self.push_InstrumentAttr(l_dict["InstrumentID"], l_dict)
    
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)    
    
  def push_OnRspOrderInsert(self, table_name, OrderInsert):
    l_dict = OrderInsert.to_dict()
    l_order_list= self.instrument_rtn_order_dict.get(l_dict['InstrumentID'])
         
    if l_order_list is None:
      l_order_list=[l_dict]
      self.instrument_rtn_order_dict[l_dict['InstrumentID']]=l_order_list
    else:
      l_order_list.append(l_dict) 
      
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)      
      
  def push_Order(self, table_name, Order):
    l_dict = Order.to_dict()
    
    if l_dict["OrderStatus"] not in ['a']:
      l_order_list= self.instrument_rtn_order_dict.get(l_dict["InstrumentID"])
      if l_order_list is None:
        l_order_list=[l_dict]
        self.instrument_rtn_order_dict[l_dict["InstrumentID"]]=l_order_list;
      else: 
        found=False
        for it_order in l_order_list:
          if it_order["OrderSysID"] == l_dict["OrderSysID"] and it_order["ExchangeID"] == l_dict["ExchangeID"]:
            found=True 
            it_order.update(l_dict)
            
        if found == False:
          l_order_list.append(l_dict)
          
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)          
  
  def push_OnRspQryOrder(self, table_name, Order):
    self.push_Order(table_name, Order) 
  
  def push_OnRspQryInvestorPosition(self, table_name, InvestorPosition):   
    l_dict = InvestorPosition.to_dict()
    l_position_list= self.instrument_position_dict.get(l_dict["InstrumentID"])
    if l_position_list is None:
      l_position_list=[l_dict]
      self.instrument_position_dict[l_dict["InstrumentID"]]=l_position_list
    else: 
      found=False
      for it_pos in l_position_list: 
        if it_pos["InstrumentID"] == l_dict["InstrumentID"] and it_pos["PosiDirection"] == l_dict["PosiDirection"]:
          found=True
          it_pos.update(l_dict) 
          
      if found == False:
        l_position_list.append(l_dict) 
      
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)
    
  def push_OnRspQrySettlementInfo(self, table_name, SettlementInfo):   
    l_dict = SettlementInfo.to_dict()
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)
      
    if self.upload == 1:
      self.dict2DB(table_name, l_dict)
    
  def push_OnRtnOrder(self, table_name, Order):
    self.push_Order(table_name, Order) 
    
  def push_OnRtnInstrumentStatus(self, table_name, InstrumentStatus):
    l_dict = InstrumentStatus.to_dict()
    
    self.set_InstrumentAttr(l_dict["InstrumentID"], "InstrumentStatus", l_dict["InstrumentStatus"])
    self.set_InstrumentAttr(l_dict["InstrumentID"], "TradingSegmentSN", l_dict["TradingSegmentSN"])
    self.set_InstrumentAttr(l_dict["InstrumentID"], "EnterTime", l_dict["EnterTime"])
    self.set_InstrumentAttr(l_dict["InstrumentID"], "EnterReason", l_dict["EnterReason"])
    
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)
    
  def push_ReqOrderInsert(self, table_name, OrderInsert):
    l_dict = OrderInsert.to_dict()
    l_order_list= self.instrument_rtn_order_dict.get(l_dict['InstrumentID'])
    if l_order_list is None:
      l_order_list=[l_dict]
      self.instrument_req_order_dict[l_dict["InstrumentID"]]=l_order_list
    else:
      l_order_list.append(l_dict) 
    
    if self.cython_c == 1:
      self.dump_req(table_name, l_dict)
      
  """
  把合约的整个属性push进来
  """
  def push_InstrumentAttr(self, instrumentID, attr_dict):
    try:
      l_dict={}

      if isinstance(attr_dict, dict) and isinstance(instrumentID, str):
        l_dict= self.instrument_attr_dict.get(instrumentID)
        if l_dict is None:
          l_dict = self.InitFactor()
          self.instrument_attr_dict[instrumentID] = l_dict  
        
        l_dict.update(attr_dict)
      
    except Exception as err:
        myEnv.logger.error('push_InstrumentAttr', exc_info=True) 
          
  def get_global_Attr(self, key):

    if not key is None :
      val= self.global_dict.get(key)

    return val
      
  def set_global_Attr(self, key, val):
    l_dict={}

    if not key is None and not val is None: 
      self.global_dict[key] = val 
      
       
  def push_global_Attr(self, key, val):
    l_dict={}

    if not key is None and not val is None: 
      self.global_dict[key] = val       
       

  def get_Order_list(self, instrumentID):
    l_list=[]
    if not instrumentID is None :
        l_list= self.instrument_rtn_order_dict.get(instrumentID)

    return l_list 


  def get_Position(self, instrumentID):
    l_list=[]

    if not instrumentID is None :
        l_list= self.instrument_position_dict.get(instrumentID)

    return l_list

  def get_ReqOrderList(self, instrumentID):
    l_list=[]

    if not instrumentID is None :
        l_list= self.instrument_req_order_dict.get(instrumentID)

    return l_list 

  def InitFactor(self):
      factor={}

      for name in myDEnv.Init_Factor_Zero:
        factor[name] = 0
    
      #行情的最新时间
      factor["UpdateTime"]           = "01:01:01"
    
      #报单的 book
      factor["bid_order_book"]  = {}
      factor["ask_order_book"]  = {}
      #成交 book
      factor["trade_book"]      = {}

      return factor                
    
  def statMD(self,factor, pMD):
    #####################
    #管理价格和Vol的BOOK 
      
    #最新价
    old_val = factor["LastPrice"]
    new_val = pMD["LastPrice"]

    ##############
    #价格的统计业务
    if new_val > old_val:
    #上涨
      #本次
      factor["LastPrice_Cur_Up"] = factor["LastPrice_Cur_Up"] + 1
      #累计
      factor["LastPrice_Acc_Up"] = factor["LastPrice_Acc_Up"] + 1
      #本次下单后上涨次数
      factor["order_acc_up"]     = factor["order_acc_up"] + 1

      #调整其它方向
      factor["LastPrice_Cur_Keep"] = 0
      factor["LastPrice_Cur_Down"] = 0
      #factor["order_acc_up"]      = 0
      #factor["order_acc_keep"]    = 0

    elif old_val == new_val:
    #保持
      #本次
      factor["LastPrice_Cur_Keep"] = factor["LastPrice_Cur_Keep"] + 1
      #累计
      factor["LastPrice_Acc_Keep"] = factor["LastPrice_Acc_Keep"] + 1
      #本次下单后保持次数
      factor["order_acc_keep"]   = factor["order_acc_keep"] + 1

      #调整其它方向
      #factor["order_acc_up"]       = 0
      #factor["order_acc_down"]     = 0
      factor["LastPrice_Cur_Down"] = 0
      factor["LastPrice_Cur_Up"]   = 0

    else:
    #下跌
      #本次
      factor["LastPrice_Cur_Down"] = factor["LastPrice_Cur_Down"] + 1
      #累计
      factor["LastPrice_Acc_Down"] = factor["LastPrice_Acc_Down"] + 1
      #本次下单后下跌次数
      factor["order_acc_down"]   = factor["order_acc_down"] + 1

      #调整其它方向
      #factor["order_acc_keep"]     = 0
      #factor["order_acc_down"]     = 0
      factor["LastPrice_Cur_Keep"] = 0
      factor["LastPrice_Cur_Up"]   = 0
    ##############   
    #数量 
    factor["vol_diff"]          = pMD["Volume"] - factor["Volume"]
    factor["order_TradeVolume"] = factor["order_TradeVolume"] + factor["vol_diff"] 

    l_LastPrice=pMD["LastPrice"]
    l_trade_order_book = factor["trade_book"]
    try:
      l_trade_order_book[l_LastPrice] = l_trade_order_book[l_LastPrice] + factor["vol_diff"]
    except Exception as err:
      l_trade_order_book[l_LastPrice] = factor["vol_diff"]
    factor["trade_book"] = l_trade_order_book   
     
    #申买价一
    if pMD["BidPrice1"] >= 1.79e+308:
        l_BidPrice1 = 0
    else:
        l_BidPrice1=pMD["BidPrice1"]
    factor["BidPrice1"]            = l_BidPrice1

    ############################
    #申买量一
    if pMD["BidVolume1"] >= 1.79e+308:
        l_BidVolume1 = 0
    else:
        l_BidVolume1=pMD["BidVolume1"]
    factor["BidVolume1"]            = l_BidVolume1

    factor["BidVolume"]       = factor["BidVolume"] + l_BidVolume1
    factor["order_BidVolume"] = factor["order_BidVolume"] + l_BidVolume1

    l_bid_order_book = factor["bid_order_book"]
    try:
        l_bid_order_book[l_BidPrice1] = l_bid_order_book[l_BidPrice1] + l_BidVolume1
    except Exception as err:
        l_bid_order_book[l_BidPrice1] = l_BidVolume1
    factor["bid_order_book"] = l_bid_order_book
    ############################

    #申卖价一
    if pMD["AskPrice1"] >= 1.79e+308:
        l_AskPrice1 = 0
    else:
        l_AskPrice1=pMD["AskPrice1"]
    factor["AskPrice1"]            = l_AskPrice1

    #####################################
    #申卖量一
    if pMD["AskVolume1"] >= 1.79e+308:
        l_AskVolume1 = 0
    else:
        l_AskVolume1=pMD["AskVolume1"]
    factor["AskVolume1"]            = l_AskVolume1

    factor["AskVolume"]       = factor["AskVolume"] + l_AskVolume1
    factor["order_AskVolume"] = factor["order_AskVolume"] + l_AskVolume1

    l_ask_order_book = factor["ask_order_book"]
    try:
      l_ask_order_book[l_AskPrice1] = l_ask_order_book[l_AskPrice1] + l_AskVolume1
    except Exception as err:
      l_ask_order_book[l_AskPrice1] = l_AskVolume1
    factor["ask_order_book"] = l_ask_order_book      
    
    
  def SimNow(self,InvestorID, InstrumentID, LastPrice, Volume):
    if InvestorID   is None or InstrumentID is None or LastPrice    is None or Volume < 1:
       return

    try:
      l_list= self.instrument_req_order_dict.get(InstrumentID)
      if l_list is None:
        return

      bTraded=0
      for it_order in l_list: 
        if it_order["Direction"] == '0' and LastPrice <= it_order["LimitPrice"]   and not it_order["OrderStatus"] in ('0','5'):
          #买单成交
          bTraded=1
          it_order["OrderStatus"] = '0'
          printNumber("SimNow",InstrumentID+".buyPrice:",it_order["LimitPrice"])
          printNumber("SimNow",InstrumentID+".TradePrice:",LastPrice)

        elif it_order["Direction"] == '1' and LastPrice >= it_order["LimitPrice"] and not it_order["OrderStatus"] in ('0','5'):
          #卖单成交
          bTraded=1
          it_order["OrderStatus"] = '0'
          printNumber("SimNow",InstrumentID+".sellPrice:",it_order["LimitPrice"])
          printNumber("SimNow",InstrumentID+".TradePrice:",LastPrice)

        #通过更改报单状态来实现，然后将成交入库
        if bTraded==1:
          the_SQL  ="""
                    INSERT INTO T_SimNow_AutoTrade(InvestorID,InstrumentID,Express,Direction,CombOffsetFlag,Order_Time,Order_Price,Order_MDPrice,Trade_Price,Trade_Volume)
                                            VALUES(%s        ,%s          ,%s     ,%s       ,%s            ,%s        ,%s         ,%s           ,%s         ,%s)
                    """
          the_data =[(InvestorID, InstrumentID, it_order["Express"], it_order["Direction"], it_order["CombOffsetFlag"],it_order["OrderTime"]
                     ,it_order["LimitPrice"],it_order["MD_Last_Price"],LastPrice, Volume)]
          self.SQL2DB(the_SQL,the_data)

    except Exception as err:
        myEnv.logger.error('__cinit__', exc_info=True)

  def connectDB(self):
    dbConnect = None

    try:
      PTP_DB_TYPE   = self.config.get("CLOUD", "PTP_DB_TYPE")
      PTP_DB_SERVER = self.config.get("CLOUD", "PTP_DB_SERVER")
      PTP_DB_USER   = self.config.get("CLOUD", "PTP_DB_USER")
      PTP_DB_PWD    = self.config.get("CLOUD", "PTP_DB_PWD")
      PTP_DB_NAME   = self.config.get("CLOUD", "PTP_DB_NAME")
      PTP_DB_PORT   = int(self.config.get("CLOUD", "PTP_DB_PORT"))
    except Exception as err:
      PTP_DB_TYPE   = None
      PTP_DB_SERVER = None
      PTP_DB_USER   = None
      PTP_DB_PWD    = None
      PTP_DB_NAME   = None
      PTP_DB_PORT   = None

    PTP_DB_TYPE   = nvl(PTP_DB_TYPE  ,"mysql"       )
    #PTP_DB_SERVER = nvl(PTP_DB_SERVER,"103.235.232.142")
    PTP_DB_SERVER = nvl(PTP_DB_SERVER,"127.0.0.1"   )
    PTP_DB_USER   = nvl(PTP_DB_USER  ,"sim_test"    )
    PTP_DB_PWD    = nvl(PTP_DB_PWD   ,"SimTest@2019")
    PTP_DB_NAME   = nvl(PTP_DB_NAME  ,"sim_test"    )
    PTP_DB_PORT   = nvl(PTP_DB_PORT  ,3306          )

    dbConnect = pymysql.Connect(host=PTP_DB_SERVER , user=PTP_DB_USER
                                  , passwd=PTP_DB_PWD, db  =PTP_DB_NAME
                                  , charset="utf8"   , port=PTP_DB_PORT)
    return dbConnect

  def dumpRspDict(self, table_name, val_dict):  
    l_dict = val_dict.to_dict()
    if self.c_cython == 1:
      self.dump_rsp(table_name, l_dict)
      
    if self.upload == 1:
      self.dict2DB(table_name, l_dict)
  
  def DumpReqDict(self, table_name, val_dict):
    l_dict = val_dict.to_dict()
    if self.c_cython == 1:
      self.dump_req(table_name, l_dict)
      
    if self.upload == 1:
      self.dict2DB(table_name, l_dict)
  

  def dump_req(self, table_name, val_dict):
    inx = 0
    col_names = ""
    vals = ""
    for (k,v) in val_dict.items():
      if inx == 0:
        col_names = col_names + k
        vals      = vals      + toString2(v)
      else:
        col_names = col_names + ',' + k
        vals      = vals      + ',' + toString2(v)  

      inx = inx + 1
      
    dump_py2c(table_name, '\n' + col_names + '\n' + vals , self.Inc_RequestID()) 
    
  def dump_rsp(self, table_name, val_dict):
    inx = 0
    col_names = ""
    vals = ""
    for (k,v) in val_dict.items():
      if inx == 0:
        col_names = col_names + k
        vals      = vals      + toString2(v)
      else:
        col_names = col_names + ',' + k
        vals      = vals      + ',' + toString2(v)  

      inx = inx + 1
      
    dump_c2py(table_name, '\n' + col_names + '\n' + vals , self.Inc_RequestID()) 
    
  def dict2DB(self, table_name, val_dict):
    try:
      print(val_dict)
      
      l_val_list = [ ]

      inx = 0
      col_names = ""
      bind_name = ""
      for (k,v) in val_dict.items():
        if inx == 0:
          col_names = col_names + k
          bind_name = bind_name + '%s'
        else:
          col_names = col_names + ',' + k
          bind_name = bind_name + ',' +'%s'
        l_val_list.append(v)

        inx = inx + 1
        
      l_sql = 'INSERT INTO ' + table_name + '(' + col_names + ')VALUES(' + bind_name + ')'
      
      l_rows=[tuple(l_val_list)]
      self.SQL2DB(l_sql, l_rows)
      
      print('ok')
      print(l_sql)
      print(l_rows)
    except Exception as err:
        myEnv.logger.error('dict2DB', exc_info=True)
    
  def SQL2DB(self, szSQL, listVal):
    ###########
    tryTimes = 0 

    while True:
      #再次执行
      try:
        #首次执行
        try:
          tryTimes = tryTimes + 1

          if self.upload == 1:
            if self.cloud_debug== 1:
              myEnv.logger.debug(szSQL)
              myEnv.logger.debug(str(listVal))

            myDB     = self.connectDB()
            mycursor = myDB.cursor()
            l_retVal = mycursor.executemany(szSQL, listVal)
            myDB.commit()
            
          break;
        except Exception as err1:
          myEnv.logger.error('excute sql faild in SQL2DB' + szSQL, exc_info=True)
          print(err1)
          print(listVal)

          #retCode = err1.args[0]
          #if retCode == 2013:
          myDB     = self.connectDB()
          mycursor = myDB.cursor()
          l_retVal = mycursor.executemany(szSQL, listVal) 
          myDB.commit()
          break;
      except Exception as err2:
        myEnv.logger.error('re excute sql faild in SQL2DB' + szSQL, exc_info=True)
        print(err2)
        print(listVal) 

      if tryTimes >= 5:
          break

  def ExecuteQuery(self,i_strSQL):
    myDB = self.connectDB()
    mycursor = myDB.cursor()
    results = ()
    try:
      if len(i_strSQL) == 0:
          return results;

      if type(mycursor) != pymysql.cursors.Cursor:
          return results


      mycursor.execute(i_strSQL)
      # 获取所有记录列表
      results = mycursor.fetchall()

    except Exception as err:
        myEnv.logger.error('ExecuteQuery', exc_info=True)

    return results;
               
 
  #报单后，统计哪些因子和下单时刻的差异
  def restOrderFactor(self,instrument):
    try:
      dwTime  = self.Inc_RequestID()

      funName = "%s.%s" % ('MdApiWrapper', 'restOrderFactor')
      #printString("MD_call_stack","call->",funName,dwTime)

      factor = self.instrument_attr_dict.get(instrument)
      if factor is None:
        factor = self.InitFactor()
      else:
        #发生报单后，累计下跌
        factor["order_acc_down"]    = 0

        ##发生报单后，累计上涨
        factor["order_acc_up"]      = 0

        ##发生报单后，累计保持
        factor["order_acc_keep"]    = 0

        ##发生报单后，累计买量
        factor["order_BidVolume"]   = 0

        ##发生报单后，累计卖量
        factor["order_AskVolume"]   = 0

        ##发生报单后，累计成交量
        factor["order_TradeVolume"] = 0
       
        ##发生报单后，LastPrice
        factor["order_price"] = 0

      self.instrument_attr_dict[instrument] = factor

    except Exception as err:
         myEnv.logger.error('restOrderFactor', exc_info=True)
           
  """
  symbol="DCE.m1901", direction="BUY", offset="OPEN", volume=5
  #返回 [ (opt,exchange_id, instrumentID,price,volum)
         ,(opt,exchange_id, instrumentID,price,volum)
         ] 
  """
  def push_md2trade(self, i_InvestorID, i_InstrumentID, dict_new_md): 
    l_ret_opt = []
    try:
      if isinstance(i_InvestorID, str) and isinstance(i_InstrumentID, str) and isinstance(dict_new_md, dict):
  
        l_dict_InstrumentAttr = self.get_InstrumentAttr(i_InstrumentID)
        l_ExchageID           = l_dict_InstrumentAttr["ExchangeID"]
        
        #做些行情统计的事情
        self.statMD(l_dict_InstrumentAttr, dict_new_md)       
 
        dict_new_md["ExchangeID"] = l_ExchageID #行情中这个信息是缺失的
        l_dict_InstrumentAttr.update(dict_new_md) #merge dict_new_md into l_dict_InstrumentAttr
        
        #间隔 10 秒推送 tushare 因子
        l_cur_dt = datetime.now()
        if myDEnv.Real_Fresh_Factor ==1 and (l_cur_dt - self.update_factor_date).seconds > myDEnv.update_factor_period: 
          self.updateFactor() 
          self.update_factor_date = l_cur_dt 
          
        #######################
        #指令匹配 
        reload(myDEnv)	  
        try:
          factor=myDEnv.AI_Strategy[i_InvestorID][i_InstrumentID]
        except Exception as err:
          myEnv.logger.warning('There is no strategy for(' + i_InvestorID + '.' + i_InstrumentID + ')')
          return l_ret_opt;

        l_buy_open_price   = -1
        l_buy_open_express = None
        l_retVal = -1 
        ###########################
        #买策略
        l_buy_open_express = factor["buy_open_express"]
        (retCode, l_buy_open_flag) = self.Calc_Express(i_InstrumentID, l_buy_open_express);
        if retCode == 0 and l_buy_open_flag   == True: 
          l_buy_open_price_express = factor["buy_open_price"]
          (retCode, l_buy_open_price) = self.Calc_Express(i_InstrumentID, l_buy_open_price_express);
          if retCode == 0:
            l_buy_open_vol = factor["buy_open_vol"] 

            l_ret_opt.append(("buy_open", l_ExchageID, l_buy_open_price, l_buy_open_vol))

            """ 
            #下买单
            p_buy_open = py_ApiStructure.InputOrderField(
                    BrokerID=self.broker_id,
                    InvestorID=i_InvestorID,
                    ExchangeID=l_ExchageID,
                    InstrumentID=i_InstrumentID,
                    UserID=i_InvestorID,
                    OrderPriceType='2',
                    Direction='0',
                    CombOffsetFlag='0',  # ///开仓
                    CombHedgeFlag='1',
                    LimitPrice=l_buy_open_price,
                    VolumeTotalOriginal=l_buy_open_vol,
                    TimeCondition='3',
                    VolumeCondition='1',
                    MinVolume=1,
                    ContingentCondition='1',
                    StopPrice=0,
                    ForceCloseReason='0',
                    IsAutoSuspend=0
                )
            l_retVal = self.ReqOrderInsert(p_buy_open, l_buy_open_express + ':' + l_buy_open_price_express, i_MD_LastPrice)
            """
            
        ###########################
        #卖策略
        l_sell_open_express = factor["sell_open_express"]
        (retCode, l_sell_open_flag) = self.Calc_Express(i_InstrumentID, l_sell_open_express);
        if retCode == 0 and l_sell_open_flag == True: 
           l_sell_open_price_express = factor["sell_open_price"]
           (retCode, l_sell_open_price) = self.Calc_Express(i_InstrumentID, l_sell_open_price_express);
           if retCode == 0:
              l_sell_open_vol = factor["sell_open_vol"]
              
              l_ret_opt.append(("sell_open", l_ExchageID, l_sell_open_price, l_sell_open_vol))
              """
              #下卖单 
              p_sell_Open = py_ApiStructure.InputOrderField(
                      BrokerID=self.broker_id,
                      InvestorID=i_InvestorID,
                      ExchangeID=l_ExchageID,
                      InstrumentID=i_InstrumentID,
                      UserID=i_InvestorID,
                      OrderPriceType='2',
                      Direction='1',
                      CombOffsetFlag='0',  # ///开仓
                      CombHedgeFlag='1',
                      LimitPrice=l_sell_open_price,
                      VolumeTotalOriginal=l_sell_open_vol,
                      TimeCondition='3',
                      VolumeCondition='1',
                      MinVolume=1,
                      ContingentCondition='1',
                      StopPrice=0,
                      ForceCloseReason='0',
                      IsAutoSuspend=0
                  )
              l_retVal = self.ReqOrderInsert(p_sell_Open, l_sell_open_express + ':' + l_sell_open_price_express, i_MD_LastPrice)
              """
        ###########################
        #平仓策略
        l_order_list    = self.get_Order_list(i_InstrumentID)
        l_position_list = self.get_Position  (i_InstrumentID)
 
        if not l_position_list is None and len(l_position_list) > 0:
          l_close_express = factor["buy_close_express"]
          (retCode, l_buy_close_flag) = self.Calc_Express(i_InstrumentID, l_close_express);
          if retCode == 0 and l_buy_close_flag == True: 
            l_close_price_express = factor["buy_close_price"]
            (retCode, l_Calc_Price) = self.Calc_Express(i_InstrumentID, l_close_price_express);
            if retCode == 0: 
              l_Volume = factor["buy_close_vol"]
              l_ret_opt.append(("buy_close", l_ExchageID, l_Calc_Price, l_Volume))
           
              #self.buy_close(i_InvestorID,i_InstrumentID,l_Calc_Price,l_Volume,i_MD_LastPrice,l_ExchageID)               

          l_close_express = factor["sell_close_express"]
          (retCode, l_sell_close_flag) = self.Calc_Express(i_InstrumentID, l_close_express);
          if retCode == 0 and l_sell_close_flag == True:
             return l_ret_opt;
          elif l_sell_close_flag == True:
           l_close_price_express = factor["sell_close_price"]
           (retCode, l_Calc_Price) = self.Calc_Express(i_InstrumentID, l_close_price_express);
           if retCode == 0: 
             l_Volume = factor["sell_close_vol"]
             l_ret_opt.append(("sell_close", l_ExchageID, l_Calc_Price, l_Volume))
           #self.sell_close(i_InvestorID,i_InstrumentID,l_Calc_Price,l_Volume,i_MD_LastPrice,l_ExchageID)               
        
    except Exception as err:
      myEnv.logger.error('push_md2trade', exc_info=True)
      
    return l_ret_opt
   
  #返回-1：缺少计算因子
  #返回-2：合约没有查询到
  def Calc_Express(self,instrument, strExpress, i_otherFactor={}):
    exe_Result = 0
    calc_Val = 0
    try:
      dictInputVal = self.instrument_attr_dict.get(instrument)
      if not dictInputVal is None:
        calc_Val = eval(strExpress, dictInputVal)
      else:
        exe_Result = -2

    except Exception as err:
      exe_Result = -1
      myEnv.logger.error('Calc_Express', exc_info=True)

    return (exe_Result, calc_Val)    

  def Factor2String(self, instrument):
    strRet=instrument + ':{'
    factor = self.instrument_attr_dict[instrument]
    try:
      if not instrument is None and not factor is None:
        for (k,v) in self.instrument_attr_dict.items():
          strRet = strRet + toString(k) + toString(v)

    except Exception as err:
      myEnv.logger.error('Factor2String', exc_info=True)

    strRet=strRet + '}'

    return strRet  
            
  def updateFactor(self):
    try:
     l_sql = "select id,InstrumentID,factor_name,factor_val from t_factor t where t.id>%s order by id asc"%(self.__id)
     l_factor_list = self.ExecuteQuery(l_sql);
     myEnv.logger.debug('set dynamic factor cnt:' + str(len(l_factor_list)))
     for it_factor in l_factor_list:
       try:
        myEnv.logger.debug('set dynamic factor' + it_factor[1] + ':' + it_factor[2] + ':' + str(it_factor[3]) )
        
        l_InstrumentID=it_factor[1]
        if l_InstrumentID == 'all':
          self.set_global_Attr(it_factor[2],it_factor[3])
        else:
          factor = self.instrument_attr_dict.get(l_InstrumentID)
          if factor is None:
            factor = self.InitFactor()
          self.instrument_attr_dict[l_InstrumentID] = factor
          factor[it_factor[2]] = it_factor[3]
        
        #下一次从这个新的位置开始读取因子
        self.__id=it_factor[0]
       except Exception as err:
        myEnv.logger.error('set dynamic factor failed' + ':' + it_factor[1] + ':' + it_factor[2], exc_info=True)
    except Exception as err:
        myEnv.logger.error('updateFactor failed', exc_info=True)
 
  
  def ReqQryInstrument(self,pQryInstrument,reqID):
    l_sql   = "select * from t_Instrument t where t.InstrumentID='%s' limit 1"%(pQryInstrument.InstrumentID.decode(encoding="gb18030", errors="ignore"))
    results = self.ExecuteQuery(l_sql); 
     
    retVal = []
    for it_res in results:
      retVal.append(py_ApiStructure.InstrumentField(InstrumentID= it_res[1],
                ExchangeID=it_res[2],
                InstrumentName=it_res[3],
                ExchangeInstID=it_res[4],
                ProductID=it_res[5],
                ProductClass=it_res[6],
                DeliveryYear=it_res[7],
                DeliveryMonth=it_res[8],
                MaxMarketOrderVolume=it_res[9],
                MinMarketOrderVolume=it_res[10],
                MaxLimitOrderVolume=it_res[11],
                MinLimitOrderVolume=it_res[12],
                VolumeMultiple=it_res[13],
                PriceTick=it_res[14],
                CreateDate=it_res[15],
                OpenDate=it_res[16],
                ExpireDate=it_res[17],
                StartDelivDate=it_res[18],
                EndDelivDate=it_res[19],
                InstLifePhase=it_res[20],
                IsTrading=it_res[21],
                PositionType=it_res[22],
                PositionDateType=it_res[23],
                LongMarginRatio=it_res[24],
                ShortMarginRatio=it_res[25],
                MaxMarginSideAlgorithm=it_res[26],
                UnderlyingInstrID=it_res[27],
                StrikePrice=it_res[28],
                OptionsType=it_res[29],
                UnderlyingMultiple=it_res[30],
                CombinationType=it_res[31]))
    return retVal
    