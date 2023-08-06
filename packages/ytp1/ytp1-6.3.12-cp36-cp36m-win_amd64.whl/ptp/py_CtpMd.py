
#!/usr/bin/env python3
# encoding:utf-8
import cProfile
import pstats
import io
import os
import time,datetime  
import configparser 
import sys  
from   ptp           import py_ApiStructure
from   ptp           import py_base


from ptp                import CythonLib
from ptp.CythonLib      import printString
from ptp.CythonLib      import printNumber

import cfg.ptp_env                 as myEnv
import cfg.ptp_can_change_env      as myDEnv #需要动态实时变化的

from   ptp.MdApi import MdApiWrapper  
 
class py_CtpMd(MdApiWrapper):

  def __init__(self, server 
                   , broker_id, investor_id, password                   
                   , i_queue_list=[] 
                   , pszFlowPath="", bIsUsingUdp=False, bIsMulticast=False):
                   
    try:
      
      #Profiler
      if myEnv.Profiler == 1:
        self.Profiler = cProfile.Profile()
        self.Profiler.enable()
        
      str_date_time              = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")
      self.pid_file              = "log/PID_MD.%s.%s.log"%(os.getpid(),str_date_time)
      
      l_pid_file = open(self.pid_file, "w", encoding="utf-8")
      l_pid_file.write(str(os.getpid()))
      l_pid_file.close()
      
      #调用情况
      self.m_started   = 0
      self.req_call    = {}    
      
      #基本信息
      self.broker_id   = broker_id
      self.investor_id = investor_id
      self.password    = password
      self.md_servers  = server
      
      self.pszFlowPath = pszFlowPath        
      self.bIsUsingUdp = bIsUsingUdp
      self.bIsMulticast= bIsMulticast  
      
      #进程间通信
      self.m_md_queue_list = i_queue_list 
      self.m_md_sum        = 0
      
      
      #Algos
      self.PTP_Algos = CythonLib.CPTPAlgos()     
      
      #基础配置
      self.config = configparser.ConfigParser()
      self.config.read("cfg/ptp.ini",encoding="utf-8")
      
      #0：实盘行情 1：行情回测
      self.Md_Rule        = int(self.config.get("TRADE_MODE", "Md_Rule"))
      self.Md_Gap         = float(self.config.get("TRADE_MODE", "Md_Gap"))  
      self.Md_Trading_Day = self.config.get("TRADE_MODE", "Md_Trading_Day") 
      
      nRetVal = self.Init_Base()
      if nRetVal != 0:
        myEnv.logger.error("py_CtpMd Init_Base failed.")
        sys.exit(1)
      
      if self.Md_Rule == 0:
        l_found=0
        for the_server in server:
          info_list = the_server.split(":")
          ip = info_list[1][2:]
          port = int(info_list[2])
          if not py_base.check_service(ip,port):
            print(the_server + " is closed")
          else:
            print(the_server + " is OK!")
            l_found=1
        if l_found == 0:
          print("There is no active MD server")
          sys.exit(1)           

        #初始化运行环境,只有调用后,接口才开始发起前置的连接请求。
        super(py_CtpMd, self).Init_Net() 
        
        self.SubscribeMarketData(myDEnv.my_instrument_id)
      
      #启动完成
      self.m_started = 1
      
      myEnv.logger.info("行情启动完毕(broker_id:%s,investor_id:%s,server:%s)"%(broker_id,investor_id,server))
    except Exception as err:
        myEnv.logger.error("py_CtpMd init failed.", exc_info=True)          
         
    
  def __del__(self):    
    if myEnv.Profiler == 1:
      self.Profiler.disable() 
      
      s = io.StringIO() 
      ps = pstats.Stats(self.Profiler, stream=s).sort_stats("cumulative") 
      ps.print_stats() 
      pr_file = open("log/Profiler_MD.%s.log"%os.getpid(), "w", encoding="utf-8")
      pr_file.write(s.getvalue())
      pr_file.close() 
      
      if os.path.exists(self.pid_file):
        os.remove(self.pid_file)

          
  """
  当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
  #OnFrontConnected初始化成功后会被回调
  #这时这里自动登录
  """
  def OnFrontConnected(self): 
    self.__Connected = 1
    
    user_login = py_ApiStructure.ReqUserLoginField(BrokerID=self.broker_id,
                                                   UserID=self.investor_id,
                                                   Password=self.password
                                                  )
    self.ReqUserLogin(user_login)        
    
  def  OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
    #交易日
    l_TradingDay=pRspUserLogin.TradingDay.decode(encoding="gb18030", errors="ignore")
    #登录成功时间
    l_LoginTime=pRspUserLogin.LoginTime.decode(encoding="gb18030", errors="ignore")
    #经纪公司代码
    l_BrokerID=pRspUserLogin.BrokerID.decode(encoding="gb18030", errors="ignore")
    #用户代码
    l_UserID=pRspUserLogin.UserID.decode(encoding="gb18030", errors="ignore")
    #交易系统名称
    l_SystemName=pRspUserLogin.SystemName.decode(encoding="gb18030", errors="ignore")
    #前置编号
    l_FrontID=pRspUserLogin.FrontID
    #会话编号
    l_SessionID=pRspUserLogin.SessionID
    #最大报单引用
    l_MaxOrderRef=pRspUserLogin.MaxOrderRef.decode(encoding="gb18030", errors="ignore")
    #上期所时间
    l_SHFETime=pRspUserLogin.SHFETime.decode(encoding="gb18030", errors="ignore")
    #大商所时间
    l_DCETime=pRspUserLogin.DCETime.decode(encoding="gb18030", errors="ignore")
    #郑商所时间
    l_CZCETime=pRspUserLogin.CZCETime.decode(encoding="gb18030", errors="ignore")
    #中金所时间
    l_FFEXTime=pRspUserLogin.FFEXTime.decode(encoding="gb18030", errors="ignore")
    #能源中心时间
    l_INETime=pRspUserLogin.INETime.decode(encoding="gb18030", errors="ignore")
    #错误代码
    l_ErrorID=pRspInfo.ErrorID
    if l_ErrorID == 0:
      self.Logined = 1
      
    #错误信息
    l_ErrorMsg=pRspInfo.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    #申请编号
    l_nRequestID = nRequestID
    #是否为最后一个包
    l_bIsLast = bIsLast

      

  def Join(self) -> int:
    """
    等待接口线程结束运行
    @return 线程退出代码
    :return:
    """
    
    return super(py_CtpMd, self).Join()        
    
  def GetTradingDay(self) -> str:
    """
    获取当前交易日
    @retrun 获取到的交易日
    @remark 只有登录成功后,才能得到正确的交易日
    :return:
    """
    day = super(py_CtpMd, self).GetTradingDay()
    return day.decode(encoding="gb18030", errors="ignore")

  def RegisterNameServer(self, pszNsAddress: str):
    """
    注册名字服务器网络地址
    @param pszNsAddress：名字服务器网络地址。
    @remark 网络地址的格式为：“protocol:# ipaddress:port”，如：”tcp:# 127.0.0.1:12001”。
    @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”12001”代表服务器端口号。 
    设置名字服务器网络地址。RegisterNameServer 优先于 RegisterFront 。
    调用前需要先使用 RegisterFensUserInfo 设置登录模式。
    """
    super(py_CtpMd, self).RegisterNameServer(pszNsAddress.encode())

  def RegisterFensUserInfo(self, pFensUserInfo):
    """
    注册名字服务器用户信息
    @param pFensUserInfo：用户信息。
    """
    super(py_CtpMd, self).RegisterFensUserInfo(pFensUserInfo)

  def SubscribeMarketData(self, pInstrumentID: list) -> int:
    """
     订阅行情。
    char *ppInstrumentID[]

    订阅行情，对应响应 OnRspSubMarketData；订阅成功后，推送OnRtnDepthMarketData
    
    0，代表成功。
    -1，表示网络连接失败；
    -2，表示未处理请求超过许可数；
    -3，表示每秒发送请求数超过许可数。

    """
    ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]
    return super(py_CtpMd, self).SubscribeMarketData(ids)

  def UnSubscribeMarketData(self, pInstrumentID: list) -> int:
    """
    退订行情。
    @param ppInstrumentID 合约ID
    :return: int
    """
    ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]

    return super(py_CtpMd, self).UnSubscribeMarketData(ids)

  def SubscribeForQuoteRsp(self, pInstrumentID: list) -> int:
    """
    订阅询价。
    订阅询价，对应响应OnRspSubForQuoteRsp；订阅成功后推送OnRtnForQuoteRsp。
    """
    ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]

    return super(py_CtpMd, self).SubscribeForQuoteRsp(ids)

  def UnSubscribeForQuoteRsp(self, pInstrumentID: list) -> int:
    """
    退订询价。
    :param pInstrumentID: 合约ID list
    :return: int
    """
    ids = [bytes(item, encoding="utf-8") for item in pInstrumentID]

    return super(py_CtpMd, self).UnSubscribeForQuoteRsp(ids)

  """
  当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
  @param nReason 错误原因
          0x1001 网络读失败
          0x1002 网络写失败
          0x2001 接收心跳超时
          0x2002 发送心跳失败
          0x2003 收到错误报文
  """
  def  OnFrontDisconnected(self, nReason):
    print(nReason) 
      
  """
  心跳超时警告。当长时间未收到报文时，该方法被调用。
  @param nTimeLapse 距离上次接收报文的时间
  """
  def  OnHeartBeatWarning(self, nTimeLapse):
    print(nTimeLapse)




  def ReqUserLogin(self, pReqUserLogin):
    '''
    ///用户登录请求
    '''

    """CThostFtdcReqUserLoginField

    l_CThostFtdcReqUserLoginField=py_ApiStructure.ReqUserLoginField(
         TradingDay                    ='?' # ///交易日
        ,BrokerID                      ='?' # ///经纪公司代码
        ,UserID                        ='?' # ///用户代码
        ,Password                      ='?' # ///密码
        ,UserProductInfo               ='?' # ///用户端产品信息
        ,InterfaceProductInfo          ='?' # ///接口端产品信息
        ,ProtocolInfo                  ='?' # ///协议信息
        ,MacAddress                    ='?' # ///Mac地址
        ,OneTimePassword               ='?' # ///动态密码
        ,ClientIPAddress               ='?' # ///终端IP地址
        ,LoginRemark                   ='?' # ///登录备注
        )

    #"""

    self.req_call['UserLogin'] = 0
    if self.Md_Rule == 0:
      return super(py_CtpMd, self).ReqUserLogin(pReqUserLogin,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqUserLogin(pReqUserLogin,self.Inc_RequestID() )


  def ReqUserLogout(self, pUserLogout):
    '''
    ///登出请求
    '''

    """CThostFtdcUserLogoutField

    l_CThostFtdcUserLogoutField=py_ApiStructure.UserLogoutField(
         BrokerID                      ='?' # ///经纪公司代码
        ,UserID                        ='?' # ///用户代码
        )

    #"""

    self.req_call['UserLogout'] = 0
    if self.Md_Rule == 0:
      return super(py_CtpMd, self).ReqUserLogout(pUserLogout,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqUserLogout(pUserLogout,self.Inc_RequestID() )


  def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
    '''
    ///登出请求响应
    '''


    if bIsLast == True:
      self.req_call['UserLogout'] = 1


    self.PTP_Algos.DumpRspDict("T_UserLogout",pUserLogout)

    l_dict={}

    """CThostFtdcUserLogoutField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pUserLogout.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pUserLogout.UserID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspError(self, pRspInfo, nRequestID, bIsLast):
    '''
    ///错误应答
    '''


    if bIsLast == True:
      self.req_call['Error'] = 1


    self.PTP_Algos.DumpRspDict("T_RspInfo",pRspInfo)

    l_dict={}

    """CThostFtdcRspInfoField

    # ///错误代码
    l_dict["ErrorID"]                   = pRspInfo.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspInfo.ErrorMsg.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
    '''
    ///订阅行情应答
    '''


    if bIsLast == True:
      self.req_call['SubMarketData'] = 1


    self.PTP_Algos.DumpRspDict("T_SpecificInstrument",pSpecificInstrument)

    l_dict={}

    """CThostFtdcSpecificInstrumentField

    # ///合约代码
    l_dict["InstrumentID"]              = pSpecificInstrument.InstrumentID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
    '''
    ///取消订阅行情应答
    '''


    if bIsLast == True:
      self.req_call['UnSubMarketData'] = 1


    self.PTP_Algos.DumpRspDict("T_SpecificInstrument",pSpecificInstrument)

    l_dict={}

    """CThostFtdcSpecificInstrumentField

    # ///合约代码
    l_dict["InstrumentID"]              = pSpecificInstrument.InstrumentID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspSubForQuoteRsp(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
    '''
    ///订阅询价应答
    '''


    if bIsLast == True:
      self.req_call['SubForQuoteRsp'] = 1


    self.PTP_Algos.DumpRspDict("T_SpecificInstrument",pSpecificInstrument)

    l_dict={}

    """CThostFtdcSpecificInstrumentField

    # ///合约代码
    l_dict["InstrumentID"]              = pSpecificInstrument.InstrumentID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspUnSubForQuoteRsp(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
    '''
    ///取消订阅询价应答
    '''


    if bIsLast == True:
      self.req_call['UnSubForQuoteRsp'] = 1


    self.PTP_Algos.DumpRspDict("T_SpecificInstrument",pSpecificInstrument)

    l_dict={}

    """CThostFtdcSpecificInstrumentField

    # ///合约代码
    l_dict["InstrumentID"]              = pSpecificInstrument.InstrumentID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnDepthMarketData(self, pDepthMarketData):
    '''
    ///深度行情通知
    '''


    self.PTP_Algos.DumpRspDict("T_DepthMarketData",pDepthMarketData)

    l_dict={}

    #"""CThostFtdcDepthMarketDataField

    # ///交易日
    l_dict["TradingDay"]                = pDepthMarketData.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pDepthMarketData.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pDepthMarketData.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pDepthMarketData.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///最新价
    l_dict["LastPrice"]                 = pDepthMarketData.LastPrice
    # ///上次结算价
    l_dict["PreSettlementPrice"]        = pDepthMarketData.PreSettlementPrice
    # ///昨收盘
    l_dict["PreClosePrice"]             = pDepthMarketData.PreClosePrice
    # ///昨持仓量
    l_dict["PreOpenInterest"]           = pDepthMarketData.PreOpenInterest
    # ///今开盘
    l_dict["OpenPrice"]                 = pDepthMarketData.OpenPrice
    # ///最高价
    l_dict["HighestPrice"]              = pDepthMarketData.HighestPrice
    # ///最低价
    l_dict["LowestPrice"]               = pDepthMarketData.LowestPrice
    # ///数量
    l_dict["Volume"]                    = pDepthMarketData.Volume
    # ///成交金额
    l_dict["Turnover"]                  = pDepthMarketData.Turnover
    # ///持仓量
    l_dict["OpenInterest"]              = pDepthMarketData.OpenInterest
    # ///今收盘
    l_dict["ClosePrice"]                = pDepthMarketData.ClosePrice
    # ///本次结算价
    l_dict["SettlementPrice"]           = pDepthMarketData.SettlementPrice
    # ///涨停板价
    l_dict["UpperLimitPrice"]           = pDepthMarketData.UpperLimitPrice
    # ///跌停板价
    l_dict["LowerLimitPrice"]           = pDepthMarketData.LowerLimitPrice
    # ///昨虚实度
    l_dict["PreDelta"]                  = pDepthMarketData.PreDelta
    # ///今虚实度
    l_dict["CurrDelta"]                 = pDepthMarketData.CurrDelta
    # ///最后修改时间
    l_dict["UpdateTime"]                = pDepthMarketData.UpdateTime.decode(encoding="gb18030", errors="ignore")

    # ///最后修改毫秒
    l_dict["UpdateMillisec"]            = pDepthMarketData.UpdateMillisec
    # ///申买价一
    l_dict["BidPrice1"]                 = pDepthMarketData.BidPrice1
    # ///申买量一
    l_dict["BidVolume1"]                = pDepthMarketData.BidVolume1
    # ///申卖价一
    l_dict["AskPrice1"]                 = pDepthMarketData.AskPrice1
    # ///申卖量一
    l_dict["AskVolume1"]                = pDepthMarketData.AskVolume1
    # ///申买价二
    l_dict["BidPrice2"]                 = pDepthMarketData.BidPrice2
    # ///申买量二
    l_dict["BidVolume2"]                = pDepthMarketData.BidVolume2
    # ///申卖价二
    l_dict["AskPrice2"]                 = pDepthMarketData.AskPrice2
    # ///申卖量二
    l_dict["AskVolume2"]                = pDepthMarketData.AskVolume2
    # ///申买价三
    l_dict["BidPrice3"]                 = pDepthMarketData.BidPrice3
    # ///申买量三
    l_dict["BidVolume3"]                = pDepthMarketData.BidVolume3
    # ///申卖价三
    l_dict["AskPrice3"]                 = pDepthMarketData.AskPrice3
    # ///申卖量三
    l_dict["AskVolume3"]                = pDepthMarketData.AskVolume3
    # ///申买价四
    l_dict["BidPrice4"]                 = pDepthMarketData.BidPrice4
    # ///申买量四
    l_dict["BidVolume4"]                = pDepthMarketData.BidVolume4
    # ///申卖价四
    l_dict["AskPrice4"]                 = pDepthMarketData.AskPrice4
    # ///申卖量四
    l_dict["AskVolume4"]                = pDepthMarketData.AskVolume4
    # ///申买价五
    l_dict["BidPrice5"]                 = pDepthMarketData.BidPrice5
    # ///申买量五
    l_dict["BidVolume5"]                = pDepthMarketData.BidVolume5
    # ///申卖价五
    l_dict["AskPrice5"]                 = pDepthMarketData.AskPrice5
    # ///申卖量五
    l_dict["AskVolume5"]                = pDepthMarketData.AskVolume5
    # ///当日均价
    l_dict["AveragePrice"]              = pDepthMarketData.AveragePrice
    # ///业务日期
    l_dict["ActionDay"]                 = pDepthMarketData.ActionDay.decode(encoding="gb18030", errors="ignore")

    #"""

    for md_queue in self.m_md_queue_list:
      md_queue.put(l_dict)
      
    self.m_md_sum = self.m_md_sum + 1

  def OnRtnForQuoteRsp(self, pForQuoteRsp):
    '''
    ///询价通知
    '''


    self.PTP_Algos.DumpRspDict("T_ForQuoteRsp",pForQuoteRsp)

    l_dict={}

    """CThostFtdcForQuoteRspField

    # ///交易日
    l_dict["TradingDay"]                = pForQuoteRsp.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pForQuoteRsp.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///询价编号
    l_dict["ForQuoteSysID"]             = pForQuoteRsp.ForQuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///询价时间
    l_dict["ForQuoteTime"]              = pForQuoteRsp.ForQuoteTime.decode(encoding="gb18030", errors="ignore")
    # ///业务日期
    l_dict["ActionDay"]                 = pForQuoteRsp.ActionDay.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pForQuoteRsp.ExchangeID.decode(encoding="gb18030", errors="ignore")

    #"""
