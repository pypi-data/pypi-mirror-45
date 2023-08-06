# encoding:utf-8
# distutils: language=c++ 

from cpython       cimport PyObject
from libc.stdlib   cimport malloc, free
from libcpp.memory cimport shared_ptr,make_shared
from libc.string   cimport const_char
from libcpp        cimport bool as cbool

import ctypes
import configparser
import time 
import sys  

from imp      import reload
from datetime import datetime
from ptp      import py_ApiStructure

from ptp                import CythonLib
from ptp.CythonLib      import printString
from ptp.CythonLib      import printNumber
 
import cfg.ptp_env            as myEnv
import cfg.ptp_can_change_env as myDEnv

from .cython2c.ThostFtdcUserApiStruct cimport *
from .cython2c.cMdApi cimport CMdSpi, CMdApi, CreateFtdcMdApi

cdef class MdApiWrapper:
  cdef CMdApi *_api
  cdef CMdSpi *_spi

  def __cinit__(self):
    try:

      funName = "%s.%s" % ("MdApiWrapper", "__cinit__")

      printString("MdApicall_stack","call->",funName)

      self._api = NULL
      self._spi = NULL
      
      self.PTP_Algos = CythonLib.CPTPAlgos()

      self.__id = 0  
  
      printString("MdApicall_stack","call-<",funName)
        
    except Exception as err:
        myEnv.logger.error("MdApiWrapper.__cinit__", exc_info=True)

  def Inc_RequestID(self):
    self.RequestID = self.RequestID + 1
    return self.RequestID
      
  def Create(self, const_char *pszFlowPath, cbool bIsUsingUdp, cbool bIsMulticast):
    try:
      printString("MdApicall_stack","call->","CThostFtdcMdApi.Create")

      self._api = CreateFtdcMdApi(pszFlowPath, bIsUsingUdp, bIsMulticast)
      if not self._api:
          raise MemoryError()

      printString("MdApicall_stack","call-<","CThostFtdcMdApi.Create")

    except Exception as err:
      myEnv.logger.error("Create", exc_info=True)

  def Init(self):
    try:
      printString("MdApicall_stack","call->","MdApiWrapper.Init")

      logDes="step 1(of 4 step)"
      myEnv.logger.info(logDes)
      self.Create(self.pszFlowPath.encode(), self.bIsUsingUdp, self.bIsMulticast)
      if self._api is not NULL:
        self._spi = new CMdSpi(<PyObject *> self)

        if self._spi is not NULL:

          logDes="step 2(of 4 step)"
          self._api.RegisterSpi(self._spi)

          logDes="step 3(of 4 step)"
          #SSL前置格式：ssl://192.168.0.1:41205
          #TCP前置格式：tcp://192.168.0.1:41205
          #此处注册多个前置，连接的时候会随机选择一个
          #pUserMdApi->RegisterFront(“tcp://192.168.0.1:41213”);
          #pUserMdApi->RegisterFront(“tcp://192.168.0.2:41213”);
          for server in self.md_servers:
            #server = "tcp://" + self.md_server + ":" + str(self.md_port)
            myEnv.logger.info("regist " + server)
            self.RegisterFront(server.encode())

          time.sleep(1)

          logDes="step 4(of 4 step)"
          #OnFrontConnected初始化成功后会被回调
          self._api.Init()
        else:
          myEnv.logger.error("new CMdSpi")
          raise MemoryError()
      else:
         myEnv.logger.error("Create")

      myEnv.logger.info(logDes)
      time.sleep(1)

      printString("MdApicall_stack","call-<","MdApiWrapper.Init")

    except Exception as err:
      myEnv.logger.error("MdServer.Init", exc_info=True)


  
  def __dealloc__(self):
    try:
      printString("MdApicall_stack","call->","MdApiWrapper.__dealloc__")

      self.Release()

      printString("MdApicall_stack","call-<","MdApiWrapper.__dealloc__")

    except Exception as err:
      myEnv.logger.error("__dealloc__", exc_info=True)

  @staticmethod
  def GetApiVersion():
    result  = ""
    try:

      printString("MdApicall_stack","call->","MdApiWrapper.GetApiVersion")

      result = CMdApi.GetApiVersion()

      printString("MdApicall_stack","call-<","MdApiWrapper.GetApiVersion")

    except Exception as err:
      myEnv.logger.error("GetApiVersion", exc_info=True)

    return result

  def Release(self):
    try:

      printString("MdApicall_stack","call->","MdApiWrapper.Release")

      if self._api is not NULL:
        self._api.RegisterSpi(NULL)
        self._api.Release()
        self._api = NULL
        self._spi = NULL

      printString("MdApicall_stack","call-<","MdApiWrapper.Release")

    except Exception as err:
      myEnv.logger.error("Release", exc_info=True)


  """
  "name"
  "open"
  "pre_close"
  "price"
  "high"
  "low"
  "bid"
  "ask"
  "volume"
  "amount"
  "b1_v"
  "b1_p"
  "b2_v"
  "b2_p"
  "b3_v"
  "b3_p"
  "b4_v"
  "b4_p"
  "b5_v"
  "b5_p"
  "a1_v"
  "a1_p"
  "a2_v"
  "a2_p"
  "a3_v"
  "a3_p"
  "a4_v"
  "a4_p"
  "a5_v"
  "a5_p"
  "date"
  "time"
  "code"
  """

  def Join(self, l_day="", i_InstrumentIDs=[]):

    cdef int result
    try: 
      
      printString("MdApicall_stack","call->","MdApiWrapper.Join")
      if self._spi is not NULL:
        if self.Md_Rule == 1:
          #行情重演
          if len(self.Md_Trading_Day) >0 and len(myDEnv.my_instrument_id) > 0:
            print("begin to replay MD.");
            l_InstrumentID = str(myDEnv.my_instrument_id).replace('[','')
            l_InstrumentID = l_InstrumentID.replace(']', '')
              
              l_sql = "select * from t_depthmarketdata t where t.TradingDay = '" + self.Md_Trading_Day + "' and t.InstrumentID in (" + l_InstrumentID + ") order by id asc"
              print(l_sql)
              l_MDs = CythonLib.ExecuteQuery(l_sql);
              print("begin to replay MD:" + l_InstrumentID + ",md count:" + str(len(l_MDs)));
              for l_md in l_MDs:
                print(l_md)
                time.sleep(self.Md_Gap)
                l_pMd = py_ApiStructure.DepthMarketDataField(TradingDay=l_md[1] ,
                              InstrumentID=        l_md[2] ,
                              ExchangeID=          l_md[3] ,
                              ExchangeInstID=      l_md[4] ,
                              LastPrice=           l_md[5] ,
                              PreSettlementPrice=  l_md[6] ,
                              PreClosePrice=       l_md[7] ,
                              PreOpenInterest=     l_md[8] ,
                              OpenPrice=           l_md[9] ,
                              HighestPrice=        l_md[10],
                              LowestPrice=         l_md[11],
                              Volume=              l_md[12],
                              Turnover=            l_md[13],
                              OpenInterest=        l_md[14],
                              ClosePrice=          l_md[15],
                              SettlementPrice=     l_md[16],
                              UpperLimitPrice=     l_md[17],
                              LowerLimitPrice=     l_md[18],
                              PreDelta=            l_md[19],
                              CurrDelta=           l_md[20],
                              UpdateTime=          l_md[21],
                              UpdateMillisec=      l_md[22],
                              BidPrice1=           l_md[23],
                              BidVolume1=          l_md[24],
                              AskPrice1=           l_md[25],
                              AskVolume1=          l_md[26],
                              BidPrice2=           l_md[27],
                              BidVolume2=          l_md[28],
                              AskPrice2=           l_md[29],
                              AskVolume2=          l_md[30],
                              BidPrice3=           l_md[31],
                              BidVolume3=          l_md[32],
                              AskPrice3=           l_md[33],
                              AskVolume3=          l_md[34],
                              BidPrice4=           l_md[35],
                              BidVolume4=          l_md[36],
                              AskPrice4=           l_md[37],
                              AskVolume4=          l_md[38],
                              BidPrice5=           l_md[39],
                              BidVolume5=          l_md[40],
                              AskPrice5=           l_md[41],
                              AskVolume5=          l_md[42],
                              AveragePrice=        l_md[43],
                              ActionDay=           l_md[44]
                        ) 
                self.OnRtnDepthMarketData(l_pMd)
              print("replay MD:" + l_InstrumentID + " End.");
            print("replay MD End.");

            printString("MdApicall_stack","call-<","MdApiWrapper.Join") 
            return 0

        with nogil:
          result = self._api.Join()
    except Exception as err:
      myEnv.logger.error("Join", exc_info=True)

    return result


  
  def GetTradingDay(self):
    cdef const_char *result
    try:
      printString("MdApicall_stack","call->","MdApiWrapper.GetTradingDay")

      if self._spi is not NULL:
        with nogil:
          result = self._api.GetTradingDay()
        printString("MdApicall_stack","call-<","MdApiWrapper.GetTradingDay")

    except Exception as err:
        myEnv.logger.error("GetTradingDay", exc_info=True)

    return result

  def RegisterFront(self, char *pszFrontAddress):

    try:

      printString("MdApicall_stack","call->","MdApiWrapper.RegisterFront")
      printString("RegisterFront","pszFrontAddress",pszFrontAddress);

      if self._api is not NULL:
        self._api.RegisterFront(pszFrontAddress)

      printString("MdApicall_stack","call-<","MdApiWrapper.RegisterFront")

    except Exception as err:
      myEnv.logger.error("RegisterFront", exc_info=True)

  def RegisterNameServer(self, char *pszNsAddress):
    try:

      printString("MdApicall_stack","call->","MdApiWrapper.RegisterNameServer")
      printString("RegisterNameServer","pszNsAddress",pszNsAddress);

      if self._api is not NULL:
        self._api.RegisterNameServer(pszNsAddress)

      printString("MdApicall_stack","call-<","MdApiWrapper.RegisterNameServer")

    except Exception as err:
      myEnv.logger.error("RegisterNameServer", exc_info=True)

  def RegisterFensUserInfo(self, pFensUserInfo):
    cdef size_t address
    try:
      printString("MdApicall_stack","call-<","MdApiWrapper.RegisterFensUserInfo")

      printString("RegisterFensUserInfo","BrokerID",pFensUserInfo.BrokerID);
      printString("RegisterFensUserInfo","UserID",pFensUserInfo.UserID);
      printString("RegisterFensUserInfo","LoginMode",pFensUserInfo.LoginMode);

      if self._api is not NULL:
        address = ctypes.addressof(pFensUserInfo)
        self._api.RegisterFensUserInfo(<CThostFtdcFensUserInfoField *> address)

      printString("MdApicall_stack","call-<","MdApiWrapper.RegisterFensUserInfo")
    except Exception as err:
      myEnv.logger.error("RegisterFensUserInfo", exc_info=True)

  def SubscribeMarketData(self, pInstrumentID):
    cdef Py_ssize_t count
    cdef int result
    cdef char **InstrumentIDs

    try:
      printString("MdApicall_stack","call->","CThostFtdcMdApi.SubscribeMarketData")
      """
       订阅行情。
      @param ppInstrumentID 合约ID
      @param nCount 要订阅/退订行情的合约个数
      """

      if self._spi is not NULL:
        count = len(pInstrumentID)
        InstrumentIDs = <char **> malloc(sizeof(char*) * count)

        try:
          for i from 0 <= i < count:
            InstrumentIDs[i] = pInstrumentID[i]
            printString("SubscribeMarketData","pInstrumentID",pInstrumentID[i]);
          with nogil:
            result = self._api.SubscribeMarketData(InstrumentIDs, <int>count)
        finally:
            free(InstrumentIDs)

        printString("MdApicall_stack","call-<","CThostFtdcMdApi.SubscribeMarketData")
    except Exception as err:
        myEnv.logger.error("SubscribeMarketData", exc_info=True)

    return result

  def UnSubscribeMarketData(self, pInstrumentID):
    cdef Py_ssize_t count
    cdef int result
    cdef char **InstrumentIDs
    try:
      printString("MdApicall_stack","call->","CThostFtdcMdApi.UnSubscribeMarketData")
      """
      退订行情。
      @param ppInstrumentID 合约ID
      @param nCount 要订阅/退订行情的合约个数
      :return:
      """

      if self._spi is not NULL:
        count = len(pInstrumentID)
        InstrumentIDs = <char **> malloc(sizeof(char*) * count)

        try:
          for i from 0 <= i < count:
            InstrumentIDs[i] = pInstrumentID[i]
            printString("UnSubscribeMarketData","pInstrumentID",pInstrumentID[i]);
          with nogil:
            result = self._api.UnSubscribeMarketData(InstrumentIDs, <int>count)
        finally:
            free(InstrumentIDs)
        printString("MdApicall_stack","call->","CThostFtdcMdApi.UnSubscribeMarketData")
    except Exception as err:
        myEnv.logger.error("UnSubscribeMarketData", exc_info=True)

    return result

  def SubscribeForQuoteRsp(self, pInstrumentID):
    cdef Py_ssize_t count
    cdef int result
    cdef char **InstrumentIDs

    try:
      printString("MdApicall_stack","call-<","CThostFtdcMdApi.SubscribeForQuoteRsp")
      """
      订阅询价。
      :param pInstrumentID: 合约ID list
      :return:
      """

      if self._spi is not NULL:

        count = len(pInstrumentID)
        InstrumentIDs = <char **> malloc(sizeof(char*) * count)

        try:
          for i from 0 <= i < count:
            InstrumentIDs[i] = pInstrumentID[i]
            printString("SubscribeForQuoteRsp","pInstrumentID",pInstrumentID[i]);
          with nogil:
            result = self._api.SubscribeForQuoteRsp(InstrumentIDs, <int>count)
        finally:
            free(InstrumentIDs)
      printString("MdApicall_stack","call-<","CThostFtdcMdApi.SubscribeForQuoteRsp")
    except Exception as err:
        myEnv.logger.error("SubscribeForQuoteRsp", exc_info=True)

    return result

  def UnSubscribeForQuoteRsp(self, pInstrumentID):
    cdef Py_ssize_t count
    cdef int result
    cdef char **InstrumentIDs

    try:
      printString("MdApicall_stack","call->","CThostFtdcMdApi.UnSubscribeForQuoteRsp")
      """
      退订询价。
      :param pInstrumentID: 合约ID list
      :return:
      """

      if self._spi is not NULL:

        count = len(pInstrumentID)
        InstrumentIDs = <char **> malloc(sizeof(char*) * count)
        try:
          for i from 0 <= i < count:
            InstrumentIDs[i] = pInstrumentID[i]
            printString("UnSubscribeForQuoteRsp","pInstrumentID",pInstrumentID[i]);
          with nogil:
            result = self._api.UnSubscribeForQuoteRsp(InstrumentIDs, <int>count)
        finally:
          free(InstrumentIDs)
        printString("MdApicall_stack","call-<","CThostFtdcMdApi.UnSubscribeForQuoteRsp")
    except Exception as err:
        myEnv.logger.error("UnSubscribeForQuoteRsp", exc_info=True)

    return result

  #用户登录请求
  def  ReqUserLogin(self, pReqUserLoginField, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("MdApicall_stack","call->",funName,dwTime)

      if self.Md_Rule == 0:
        if self._spi is not NULL:
          address = ctypes.addressof(pReqUserLoginField)
          with nogil:
            result = self._api.ReqUserLogin(<CThostFtdcReqUserLoginField *> address, nRequestID)

      self.PTP_Algos.DumpReqDict("ReqUserLogin",pReqUserLoginField)

      printString("MdApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqUserLogin', exc_info=True)

    return result


  #登出请求
  def  ReqUserLogout(self, pUserLogout, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("MdApicall_stack","call->",funName,dwTime)

      if self.Md_Rule == 0:
        if self._spi is not NULL:
          address = ctypes.addressof(pUserLogout)
          with nogil:
            result = self._api.ReqUserLogout(<CThostFtdcUserLogoutField *> address, nRequestID)

      self.PTP_Algos.DumpReqDict("ReqUserLogout",pUserLogout)

      printString("MdApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqUserLogout', exc_info=True)

    return result


"""
当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
"""
cdef extern int   MdSpi_OnFrontConnected(self) except -1:

  try:
      self.OnFrontConnected()
  except Exception as err:
      myEnv.logger.error('OnFrontConnected', exc_info=True)

  return 0


"""
当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
///@param nReason 错误原因
///        0x1001 网络读失败
///        0x1002 网络写失败
///        0x2001 接收心跳超时
///        0x2002 发送心跳失败
///        0x2003 收到错误报文
"""
cdef extern int   MdSpi_OnFrontDisconnected(self
    , int nReason) except -1:

  try:
      self.OnFrontDisconnected(nReason)
  except Exception as err:
      myEnv.logger.error('OnFrontDisconnected', exc_info=True)

  return 0


"""
心跳超时警告。当长时间未收到报文时，该方法被调用。
///@param nTimeLapse 距离上次接收报文的时间
"""
cdef extern int   MdSpi_OnHeartBeatWarning(self
    , int nTimeLapse) except -1:

  try:
      self.OnHeartBeatWarning(nTimeLapse)
  except Exception as err:
      myEnv.logger.error('OnHeartBeatWarning', exc_info=True)

  return 0


"""
登录请求响应
"""
cdef extern int   MdSpi_OnRspUserLogin(self
    , CThostFtdcRspUserLoginField *pRspUserLogin
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRspUserLogin != NULL:
      self.PTP_Algos.dumpRspDict("OnRspUserLogin",None if pRspUserLogin is NULL else py_ApiStructure.RspUserLoginField.from_address(<size_t> pRspUserLogin))
      self.OnRspUserLogin(None if pRspUserLogin is NULL else py_ApiStructure.RspUserLoginField.from_address(<size_t> pRspUserLogin)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspUserLogin', exc_info=True)

  return 0


"""
登出请求响应
"""
cdef extern int   MdSpi_OnRspUserLogout(self
    , CThostFtdcUserLogoutField *pUserLogout
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pUserLogout != NULL:
      self.PTP_Algos.dumpRspDict("OnRspUserLogout",None if pUserLogout is NULL else py_ApiStructure.UserLogoutField.from_address(<size_t> pUserLogout))
      self.OnRspUserLogout(None if pUserLogout is NULL else py_ApiStructure.UserLogoutField.from_address(<size_t> pUserLogout)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspUserLogout', exc_info=True)

  return 0


"""
错误应答
"""
cdef extern int   MdSpi_OnRspError(self
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRspInfo != NULL:
      self.PTP_Algos.dumpRspDict("OnRspError",None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
      self.OnRspError(None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspError', exc_info=True)

  return 0


"""
订阅行情应答
"""
cdef extern int   MdSpi_OnRspSubMarketData(self
    , CThostFtdcSpecificInstrumentField *pSpecificInstrument
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSpecificInstrument != NULL:
      self.PTP_Algos.dumpRspDict("OnRspSubMarketData",None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument))
      self.OnRspSubMarketData(None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspSubMarketData', exc_info=True)

  return 0


"""
取消订阅行情应答
"""
cdef extern int   MdSpi_OnRspUnSubMarketData(self
    , CThostFtdcSpecificInstrumentField *pSpecificInstrument
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSpecificInstrument != NULL:
      self.PTP_Algos.dumpRspDict("OnRspUnSubMarketData",None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument))
      self.OnRspUnSubMarketData(None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspUnSubMarketData', exc_info=True)

  return 0


"""
订阅询价应答
"""
cdef extern int   MdSpi_OnRspSubForQuoteRsp(self
    , CThostFtdcSpecificInstrumentField *pSpecificInstrument
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSpecificInstrument != NULL:
      self.PTP_Algos.dumpRspDict("OnRspSubForQuoteRsp",None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument))
      self.OnRspSubForQuoteRsp(None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspSubForQuoteRsp', exc_info=True)

  return 0


"""
取消订阅询价应答
"""
cdef extern int   MdSpi_OnRspUnSubForQuoteRsp(self
    , CThostFtdcSpecificInstrumentField *pSpecificInstrument
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSpecificInstrument != NULL:
      self.PTP_Algos.dumpRspDict("OnRspUnSubForQuoteRsp",None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument))
      self.OnRspUnSubForQuoteRsp(None if pSpecificInstrument is NULL else py_ApiStructure.SpecificInstrumentField.from_address(<size_t> pSpecificInstrument)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspUnSubForQuoteRsp', exc_info=True)

  return 0


"""
深度行情通知
"""
cdef extern int   MdSpi_OnRtnDepthMarketData(self
    , CThostFtdcDepthMarketDataField *pDepthMarketData) except -1:

  try:
    if pDepthMarketData != NULL and self.Md_Rule == 0:
      self.PTP_Algos.dumpRspDict("OnRtnDepthMarketData",None if pDepthMarketData is NULL else py_ApiStructure.DepthMarketDataField.from_address(<size_t> pDepthMarketData))
      self.OnRtnDepthMarketData(None if pDepthMarketData is NULL else py_ApiStructure.DepthMarketDataField.from_address(<size_t> pDepthMarketData))
  except Exception as err:
      myEnv.logger.error('OnRtnDepthMarketData', exc_info=True)

  return 0


"""
询价通知
"""
cdef extern int   MdSpi_OnRtnForQuoteRsp(self
    , CThostFtdcForQuoteRspField *pForQuoteRsp) except -1:

  try:
    if pForQuoteRsp != NULL:
      self.PTP_Algos.dumpRspDict("OnRtnForQuoteRsp",None if pForQuoteRsp is NULL else py_ApiStructure.ForQuoteRspField.from_address(<size_t> pForQuoteRsp))
      self.OnRtnForQuoteRsp(None if pForQuoteRsp is NULL else py_ApiStructure.ForQuoteRspField.from_address(<size_t> pForQuoteRsp))
  except Exception as err:
      myEnv.logger.error('OnRtnForQuoteRsp', exc_info=True)

  return 0

