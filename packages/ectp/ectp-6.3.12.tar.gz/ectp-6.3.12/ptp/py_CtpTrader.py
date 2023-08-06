
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

from   ptp.TraderApi import TraderApiWrapper  
 
class py_CtpTrader(TraderApiWrapper):

  def __init__(self, server
                   , broker_id
                   , investor_id
                   , password
                   , i_md_queue
                   , pszFlowPath=""):
                   
    try:   
    
      #Profiler
      if myEnv.Profiler == 1:
        self.Profiler = cProfile.Profile()
        self.Profiler.enable()
      
      str_date_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")
      self.pid_file = "log/PID_Trader.%s.%s.log"%(os.getpid(),str_date_time)
      
      l_pid_file = open(self.pid_file, "w", encoding="utf-8")
      l_pid_file.write(str(os.getpid()))
      l_pid_file.close()
      
      
      self.PTP_Algos = CythonLib.CPTPAlgos() 
      
      #调用情况
      self.m_started      = 0
      self.req_call       = {}      
      
      #基本信息 
      self.broker_id      = broker_id
      self.investor_id    = investor_id
      self.password       = password
      self.trader_server  = server
      self.pszFlowPath    = pszFlowPath
      self.PrivateSubscribeTopic = myEnv.PrivateSubscribeTopic
      self.PublicSubscribeTopic  = myEnv.PublicSubscribeTopic
      
      #进程间通信
      self.md_queue              = i_md_queue
      self.m_md_sum              = 0
      
      #基础配置
      self.config = configparser.ConfigParser()
      self.config.read("cfg/ptp.ini",encoding="utf-8")
      
      #0：实盘撮合成交 1：PTP撮合成交(价格合适就成交，全量成交) 
      self.Trader_Rule      = int(self.config.get("TRADE_MODE", "Trader_Rule")) 
      
      
      nRetVal = self.Init_Base()
      if nRetVal != 0:
        myEnv.logger.error("py_CtpTrader Init_Base failed.")
        sys.exit(1)
            
      #"""
      #0:实盘， 1：模拟撮合
      #准备基础数据                  
      if self.Trader_Rule == 0: 
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
          print("There is no active Trader server")
          sys.exit(1)

        super(py_CtpTrader, self).Init_Net()  # C++的RegisterSpi和Init都封装在父类的Init中        
        
      #get 基础数据(Order)
      l_pQryOrder = py_ApiStructure.QryOrderField(BrokerID   = self.broker_id,
                                                  InvestorID = self.investor_id
                                                 )
      l_retVal = -1
      while l_retVal != 0:
         time.sleep(1)
         myEnv.logger.info("ready to ReqQryOrder...")
         l_retVal = self.ReqQryOrder(pQryOrder=l_pQryOrder)


      #get 基础数据(Position)
      l_pQryPos = py_ApiStructure.QryInvestorPositionField(BrokerID   = self.broker_id,
                                                           InvestorID = self.investor_id
                                                          )
      l_retVal = -1
      while l_retVal != 0:
         time.sleep(1)
         myEnv.logger.info("ready to ReqQryInvestorPosition...")
         l_retVal = self.ReqQryInvestorPosition(pQryInvestorPosition=l_pQryPos)
              
      #get 基础数据(资金)
      pQryTradingAccount = py_ApiStructure.QryTradingAccountField(BrokerID   = self.broker_id,
                                                                  InvestorID = self.investor_id,
                                                                  CurrencyID = "CNY",
                                                                  BizType    = "1"
                                                                 )
      l_retVal = -1
      while l_retVal != 0:
         time.sleep(1)
         myEnv.logger.info("ready to ReqQryTradingAccount...")
         l_retVal = self.ReqQryTradingAccount(pQryTradingAccount)
         
              
      #get 基础数据(instrument)
      l_dict = {}
      for  it_instrumentid in myDEnv.my_instrument_id:
        InstrumentField = py_ApiStructure.QryInstrumentField(InstrumentID=it_instrumentid) #InstrumentID=it_instrumentid
        l_retVal = -1
        while True:
          time.sleep(1)
          myEnv.logger.info("ready to ReqQryInstrument...")
          l_retVal = self.ReqQryInstrument(pQryInstrument=InstrumentField)

          if l_retVal == 0:
            l_dict = self.get_InstrumentAttr(it_instrumentid)
            if not l_dict is None and len(l_dict)>0: 
              break
      
      #启动完成
      self.m_started = 1
      
      myEnv.logger.info("交易启动完毕(broker_id:%s,investor_id:%s,server:%s)"%(broker_id,investor_id,server))
    except Exception as err:
        myEnv.logger.error("py_CtpTrader init failed.", exc_info=True)

        
  def __del__(self):    
    if myEnv.Profiler == 1:
      self.Profiler.disable() 
      
      s = io.StringIO() 
      ps = pstats.Stats(self.Profiler, stream=s).sort_stats("cumulative") 
      ps.print_stats() 
      pr_file = open("log/Profiler_Trader.%s.log"%os.getpid(), "w", encoding="utf-8")
      pr_file.write(s.getvalue())
      pr_file.close()        
      
      if os.path.exists(self.pid_file):
        os.remove(self.pid_file)
                
  def Release(self):
    super(py_CtpTrader, self).Release()
      
  def Join(self):
    while True:
        #print(time.localtime( time.time() ))  
        time.sleep(1)
    return super(py_CtpTrader, self).Join()
      
  def GetTradingDay(self):
    """
    获取当前交易日
    @retrun 获取到的交易日
    @remark 只有登录成功后,才能得到正确的交易日
    """
    day = super(py_CtpTrader, self).GetTradingDay()
    if day is None:
      return None;
    else:
      return day.decode(encoding="gb18030", errors="ignore")
      
  def OnRspError(self, pRspInfo, nRequestID, bIsLast):
    """
    :param info:
    :return:
    """
    if pRspInfo is None:
      return ;
      
    if pRspInfo.ErrorID != 0:
        print("RequestID=%s ErrorID=%d, ErrorMsg=%s",
              nRequestID, pRspInfo.ErrorID, pRspInfo.ErrorMsg.decode(encoding="gb18030", errors="ignore"))
    return pRspInfo.ErrorID != 0         

  def RegisterNameServer(self, pszNsAddress):
    """
    注册名字服务器网络地址
    @param pszNsAddress：名字服务器网络地址。
    @remark 网络地址的格式为：“protocol:
    ipaddress:port”，如：”tcp:
    127.0.0.1:12001”。
    @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”12001”代表服务器端口号。
    @remark RegisterNameServer优先于RegisterFront
    """
    super(py_CtpTrader, self).RegisterNameServer(pszNsAddress.encode())

  def RegisterFensUserInfo(self, pFensUserInfo):
    """
    注册名字服务器用户信息
    @param pFensUserInfo：用户信息。
    """
    super(py_CtpTrader, self).RegisterFensUserInfo(pFensUserInfo)

  def SubscribePrivateTopic(self, nResumeType: int):
    """
    订阅私有流。
    @param nResumeType 私有流重传方式
            THOST_TERT_RESTART:0,从本交易日开始重传
            THOST_TERT_RESUME:1,从上次收到的续传
            THOST_TERT_QUICK:2,只传送登录后私有流的内容

    @remark 该方法要在Init方法前调用。若不调用则不会收到私有流的数据。
    """
    super(py_CtpTrader, self).SubscribePrivateTopic(nResumeType)

  def SubscribePublicTopic(self, nResumeType: int):
    """
    订阅公共流。
    @param nResumeType 公共流重传方式
            THOST_TERT_RESTART:0,从本交易日开始重传
            THOST_TERT_RESUME:1,从上次收到的续传
            THOST_TERT_QUICK:2只传送登录后公共流的内容
    @remark 该方法要在Init方法前调用。若不调用则不会收到公共流的数据。
    """
    super(py_CtpTrader, self).SubscribePublicTopic(nResumeType) 

 ###################################################
  def OnHeartBeatWarning(self, nTimeLapse):
    """心跳超时警告。当长时间未收到报文时，该方法被调用。
    @param nTimeLapse 距离上次接收报文的时间
    """
    print("on OnHeartBeatWarning time: ", nTimeLapse)

  # 当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
  # @param nReason 错误原因
  #        0x1001 网络读失败
  #        0x1002 网络写失败
  #        0x2001 接收心跳超时
  #        0x2002 发送心跳失败
  #        0x2003 收到错误报文 
  def OnFrontDisconnected(self, nReason):
    print("on FrontDisConnected disconnected", nReason)

  def OnFrontConnected(self):

    #连接回调后自动登录，所以不需要单独调用登录接口
    req = py_ApiStructure.ReqUserLoginField(BrokerID=self.broker_id,
                                         UserID=self.investor_id,
                                         Password=self.password)
    self.ReqUserLogin(req)

  def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):

    if bIsLast == True:
      self.req_call["UserLogin"] = 1
    
    if pRspInfo.ErrorID != 0:
      print("登录CTP柜台失败. Server return error_id=%s msg:%s",
            pRspInfo.ErrorID, pRspInfo.ErrorMsg.decode(encoding="gb18030", errors="ignore"))
    else:
      #登陆成功自动确认结算结果
      print("py_CtpTrader Server user login successfully")
      req = py_ApiStructure.SettlementInfoConfirmField(BrokerID = self.broker_id,InvestorID=self.investor_id)
      self.ReqSettlementInfoConfirm(req)

  def ReqAuthenticate(self, pReqAuthenticate):
    '''
    ///客户端认证请求
    '''

    """CThostFtdcReqAuthenticateField

    l_CThostFtdcReqAuthenticateField=py_ApiStructure.ReqAuthenticateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,UserID                        ='?' # ///用户代码
        ,UserProductInfo               ='?' # ///用户端产品信息
        ,AuthCode                      ='?' # ///认证码
        )

    #"""

    self.req_call['Authenticate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqAuthenticate(pReqAuthenticate,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqAuthenticate(pReqAuthenticate,self.Inc_RequestID() )


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
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqUserLogin(pReqUserLogin,self.Inc_RequestID() )
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
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqUserLogout(pUserLogout,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqUserLogout(pUserLogout,self.Inc_RequestID() )


  def ReqUserPasswordUpdate(self, pUserPasswordUpdate):
    '''
    ///用户口令更新请求
    '''

    """CThostFtdcUserPasswordUpdateField

    l_CThostFtdcUserPasswordUpdateField=py_ApiStructure.UserPasswordUpdateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,UserID                        ='?' # ///用户代码
        ,OldPassword                   ='?' # ///原来的口令
        ,NewPassword                   ='?' # ///新的口令
        )

    #"""

    self.req_call['UserPasswordUpdate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqUserPasswordUpdate(pUserPasswordUpdate,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqUserPasswordUpdate(pUserPasswordUpdate,self.Inc_RequestID() )


  def ReqTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate):
    '''
    ///资金账户口令更新请求
    '''

    """CThostFtdcTradingAccountPasswordUpdateField

    l_CThostFtdcTradingAccountPasswordUpdateField=py_ApiStructure.TradingAccountPasswordUpdateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,AccountID                     ='?' # ///投资者帐号
        ,OldPassword                   ='?' # ///原来的口令
        ,NewPassword                   ='?' # ///新的口令
        ,CurrencyID                    ='?' # ///币种代码
        )

    #"""

    self.req_call['TradingAccountPasswordUpdate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqTradingAccountPasswordUpdate(pTradingAccountPasswordUpdate,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqTradingAccountPasswordUpdate(pTradingAccountPasswordUpdate,self.Inc_RequestID() )


  def ReqUserLogin2(self, pReqUserLogin):
    '''
    ///登录请求2
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

    self.req_call['UserLogin2'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqUserLogin2(pReqUserLogin,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqUserLogin2(pReqUserLogin,self.Inc_RequestID() )


  def ReqUserPasswordUpdate2(self, pUserPasswordUpdate):
    '''
    ///用户口令更新请求2
    '''

    """CThostFtdcUserPasswordUpdateField

    l_CThostFtdcUserPasswordUpdateField=py_ApiStructure.UserPasswordUpdateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,UserID                        ='?' # ///用户代码
        ,OldPassword                   ='?' # ///原来的口令
        ,NewPassword                   ='?' # ///新的口令
        )

    #"""

    self.req_call['UserPasswordUpdate2'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqUserPasswordUpdate2(pUserPasswordUpdate,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqUserPasswordUpdate2(pUserPasswordUpdate,self.Inc_RequestID() )


  def ReqOrderInsert(self, pInputOrder,express="",md_LastPrice=0):
    '''
    ///报单录入请求
    '''

    """CThostFtdcInputOrderField

    l_CThostFtdcInputOrderField=py_ApiStructure.InputOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,OrderRef                      ='?' # ///报单引用
        ,UserID                        ='?' # ///用户代码
        ,OrderPriceType                ='?' # ///报单价格条件
        ,Direction                     ='?' # ///买卖方向
        ,CombOffsetFlag                ='?' # ///组合开平标志
        ,CombHedgeFlag                 ='?' # ///组合投机套保标志
        ,LimitPrice                    ='?' # ///价格
        ,VolumeTotalOriginal           ='?' # ///数量
        ,TimeCondition                 ='?' # ///有效期类型
        ,GTDDate                       ='?' # ///GTD日期
        ,VolumeCondition               ='?' # ///成交量类型
        ,MinVolume                     ='?' # ///最小成交量
        ,ContingentCondition           ='?' # ///触发条件
        ,StopPrice                     ='?' # ///止损价
        ,ForceCloseReason              ='?' # ///强平原因
        ,IsAutoSuspend                 ='?' # ///自动挂起标志
        ,BusinessUnit                  ='?' # ///业务单元
        ,RequestID                     ='?' # ///请求编号
        ,UserForceClose                ='?' # ///用户强评标志
        ,IsSwapOrder                   ='?' # ///互换单标志
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,AccountID                     ='?' # ///资金账号
        ,CurrencyID                    ='?' # ///币种代码
        ,ClientID                      ='?' # ///交易编码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['OrderInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqOrderInsert(pInputOrder,self.Inc_RequestID() ,express,md_LastPrice)
    else:
      return self.PTP_Algos.ReqOrderInsert(pInputOrder,self.Inc_RequestID() ,express,md_LastPrice)


  def ReqParkedOrderInsert(self, pParkedOrder):
    '''
    ///预埋单录入请求
    '''

    """CThostFtdcParkedOrderField

    l_CThostFtdcParkedOrderField=py_ApiStructure.ParkedOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,OrderRef                      ='?' # ///报单引用
        ,UserID                        ='?' # ///用户代码
        ,OrderPriceType                ='?' # ///报单价格条件
        ,Direction                     ='?' # ///买卖方向
        ,CombOffsetFlag                ='?' # ///组合开平标志
        ,CombHedgeFlag                 ='?' # ///组合投机套保标志
        ,LimitPrice                    ='?' # ///价格
        ,VolumeTotalOriginal           ='?' # ///数量
        ,TimeCondition                 ='?' # ///有效期类型
        ,GTDDate                       ='?' # ///GTD日期
        ,VolumeCondition               ='?' # ///成交量类型
        ,MinVolume                     ='?' # ///最小成交量
        ,ContingentCondition           ='?' # ///触发条件
        ,StopPrice                     ='?' # ///止损价
        ,ForceCloseReason              ='?' # ///强平原因
        ,IsAutoSuspend                 ='?' # ///自动挂起标志
        ,BusinessUnit                  ='?' # ///业务单元
        ,RequestID                     ='?' # ///请求编号
        ,UserForceClose                ='?' # ///用户强评标志
        ,ExchangeID                    ='?' # ///交易所代码
        ,ParkedOrderID                 ='?' # ///预埋报单编号
        ,UserType                      ='?' # ///用户类型
        ,Status                        ='?' # ///预埋单状态
        ,ErrorID                       ='?' # ///错误代码
        ,ErrorMsg                      ='?' # ///错误信息
        ,IsSwapOrder                   ='?' # ///互换单标志
        ,AccountID                     ='?' # ///资金账号
        ,CurrencyID                    ='?' # ///币种代码
        ,ClientID                      ='?' # ///交易编码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['ParkedOrderInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqParkedOrderInsert(pParkedOrder,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqParkedOrderInsert(pParkedOrder,self.Inc_RequestID() )


  def ReqParkedOrderAction(self, pParkedOrderAction):
    '''
    ///预埋撤单录入请求
    '''

    """CThostFtdcParkedOrderActionField

    l_CThostFtdcParkedOrderActionField=py_ApiStructure.ParkedOrderActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,OrderActionRef                ='?' # ///报单操作引用
        ,OrderRef                      ='?' # ///报单引用
        ,RequestID                     ='?' # ///请求编号
        ,FrontID                       ='?' # ///前置编号
        ,SessionID                     ='?' # ///会话编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,OrderSysID                    ='?' # ///报单编号
        ,ActionFlag                    ='?' # ///操作标志
        ,LimitPrice                    ='?' # ///价格
        ,VolumeChange                  ='?' # ///数量变化
        ,UserID                        ='?' # ///用户代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ParkedOrderActionID           ='?' # ///预埋撤单单编号
        ,UserType                      ='?' # ///用户类型
        ,Status                        ='?' # ///预埋撤单状态
        ,ErrorID                       ='?' # ///错误代码
        ,ErrorMsg                      ='?' # ///错误信息
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['ParkedOrderAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqParkedOrderAction(pParkedOrderAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqParkedOrderAction(pParkedOrderAction,self.Inc_RequestID() )


  def ReqOrderAction(self, pInputOrderAction):
    '''
    ///报单操作请求
    '''

    """CThostFtdcInputOrderActionField

    l_CThostFtdcInputOrderActionField=py_ApiStructure.InputOrderActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,OrderActionRef                ='?' # ///报单操作引用
        ,OrderRef                      ='?' # ///报单引用
        ,RequestID                     ='?' # ///请求编号
        ,FrontID                       ='?' # ///前置编号
        ,SessionID                     ='?' # ///会话编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,OrderSysID                    ='?' # ///报单编号
        ,ActionFlag                    ='?' # ///操作标志
        ,LimitPrice                    ='?' # ///价格
        ,VolumeChange                  ='?' # ///数量变化
        ,UserID                        ='?' # ///用户代码
        ,InstrumentID                  ='?' # ///合约代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['OrderAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqOrderAction(pInputOrderAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqOrderAction(pInputOrderAction,self.Inc_RequestID() )


  def ReqQueryMaxOrderVolume(self, pQueryMaxOrderVolume):
    '''
    ///查询最大报单数量请求
    '''

    """CThostFtdcQueryMaxOrderVolumeField

    l_CThostFtdcQueryMaxOrderVolumeField=py_ApiStructure.QueryMaxOrderVolumeField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,Direction                     ='?' # ///买卖方向
        ,OffsetFlag                    ='?' # ///开平标志
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,MaxVolume                     ='?' # ///最大允许报单数量
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QueryMaxOrderVolume'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQueryMaxOrderVolume(pQueryMaxOrderVolume,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQueryMaxOrderVolume(pQueryMaxOrderVolume,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQueryMaxOrderVolume(it_ret_val, None, nRequestID, True)
      return 0


  def ReqSettlementInfoConfirm(self, pSettlementInfoConfirm):
    '''
    ///投资者结算结果确认
    '''

    """CThostFtdcSettlementInfoConfirmField

    l_CThostFtdcSettlementInfoConfirmField=py_ApiStructure.SettlementInfoConfirmField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ConfirmDate                   ='?' # ///确认日期
        ,ConfirmTime                   ='?' # ///确认时间
        ,SettlementID                  ='?' # ///结算编号
        ,AccountID                     ='?' # ///投资者帐号
        ,CurrencyID                    ='?' # ///币种代码
        )

    #"""

    self.req_call['SettlementInfoConfirm'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqSettlementInfoConfirm(pSettlementInfoConfirm,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqSettlementInfoConfirm(pSettlementInfoConfirm,self.Inc_RequestID() )


  def ReqRemoveParkedOrder(self, pRemoveParkedOrder):
    '''
    ///请求删除预埋单
    '''

    """CThostFtdcRemoveParkedOrderField

    l_CThostFtdcRemoveParkedOrderField=py_ApiStructure.RemoveParkedOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ParkedOrderID                 ='?' # ///预埋报单编号
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['RemoveParkedOrder'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqRemoveParkedOrder(pRemoveParkedOrder,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqRemoveParkedOrder(pRemoveParkedOrder,self.Inc_RequestID() )


  def ReqRemoveParkedOrderAction(self, pRemoveParkedOrderAction):
    '''
    ///请求删除预埋撤单
    '''

    """CThostFtdcRemoveParkedOrderActionField

    l_CThostFtdcRemoveParkedOrderActionField=py_ApiStructure.RemoveParkedOrderActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ParkedOrderActionID           ='?' # ///预埋撤单编号
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['RemoveParkedOrderAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqRemoveParkedOrderAction(pRemoveParkedOrderAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqRemoveParkedOrderAction(pRemoveParkedOrderAction,self.Inc_RequestID() )


  def ReqExecOrderInsert(self, pInputExecOrder):
    '''
    ///执行宣告录入请求
    '''

    """CThostFtdcInputExecOrderField

    l_CThostFtdcInputExecOrderField=py_ApiStructure.InputExecOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExecOrderRef                  ='?' # ///执行宣告引用
        ,UserID                        ='?' # ///用户代码
        ,Volume                        ='?' # ///数量
        ,RequestID                     ='?' # ///请求编号
        ,BusinessUnit                  ='?' # ///业务单元
        ,OffsetFlag                    ='?' # ///开平标志
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,ActionType                    ='?' # ///执行类型
        ,PosiDirection                 ='?' # ///保留头寸申请的持仓方向
        ,ReservePositionFlag           ='?' # ///期权行权后是否保留期货头寸的标记,该字段已废弃
        ,CloseFlag                     ='?' # ///期权行权后生成的头寸是否自动平仓
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,AccountID                     ='?' # ///资金账号
        ,CurrencyID                    ='?' # ///币种代码
        ,ClientID                      ='?' # ///交易编码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['ExecOrderInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqExecOrderInsert(pInputExecOrder,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqExecOrderInsert(pInputExecOrder,self.Inc_RequestID() )


  def ReqExecOrderAction(self, pInputExecOrderAction):
    '''
    ///执行宣告操作请求
    '''

    """CThostFtdcInputExecOrderActionField

    l_CThostFtdcInputExecOrderActionField=py_ApiStructure.InputExecOrderActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ExecOrderActionRef            ='?' # ///执行宣告操作引用
        ,ExecOrderRef                  ='?' # ///执行宣告引用
        ,RequestID                     ='?' # ///请求编号
        ,FrontID                       ='?' # ///前置编号
        ,SessionID                     ='?' # ///会话编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,ExecOrderSysID                ='?' # ///执行宣告操作编号
        ,ActionFlag                    ='?' # ///操作标志
        ,UserID                        ='?' # ///用户代码
        ,InstrumentID                  ='?' # ///合约代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['ExecOrderAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqExecOrderAction(pInputExecOrderAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqExecOrderAction(pInputExecOrderAction,self.Inc_RequestID() )


  def ReqForQuoteInsert(self, pInputForQuote):
    '''
    ///询价录入请求
    '''

    """CThostFtdcInputForQuoteField

    l_CThostFtdcInputForQuoteField=py_ApiStructure.InputForQuoteField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ForQuoteRef                   ='?' # ///询价引用
        ,UserID                        ='?' # ///用户代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['ForQuoteInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqForQuoteInsert(pInputForQuote,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqForQuoteInsert(pInputForQuote,self.Inc_RequestID() )


  def ReqQuoteInsert(self, pInputQuote):
    '''
    ///报价录入请求
    '''

    """CThostFtdcInputQuoteField

    l_CThostFtdcInputQuoteField=py_ApiStructure.InputQuoteField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,QuoteRef                      ='?' # ///报价引用
        ,UserID                        ='?' # ///用户代码
        ,AskPrice                      ='?' # ///卖价格
        ,BidPrice                      ='?' # ///买价格
        ,AskVolume                     ='?' # ///卖数量
        ,BidVolume                     ='?' # ///买数量
        ,RequestID                     ='?' # ///请求编号
        ,BusinessUnit                  ='?' # ///业务单元
        ,AskOffsetFlag                 ='?' # ///卖开平标志
        ,BidOffsetFlag                 ='?' # ///买开平标志
        ,AskHedgeFlag                  ='?' # ///卖投机套保标志
        ,BidHedgeFlag                  ='?' # ///买投机套保标志
        ,AskOrderRef                   ='?' # ///衍生卖报单引用
        ,BidOrderRef                   ='?' # ///衍生买报单引用
        ,ForQuoteSysID                 ='?' # ///应价编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,ClientID                      ='?' # ///交易编码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['QuoteInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQuoteInsert(pInputQuote,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqQuoteInsert(pInputQuote,self.Inc_RequestID() )


  def ReqQuoteAction(self, pInputQuoteAction):
    '''
    ///报价操作请求
    '''

    """CThostFtdcInputQuoteActionField

    l_CThostFtdcInputQuoteActionField=py_ApiStructure.InputQuoteActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,QuoteActionRef                ='?' # ///报价操作引用
        ,QuoteRef                      ='?' # ///报价引用
        ,RequestID                     ='?' # ///请求编号
        ,FrontID                       ='?' # ///前置编号
        ,SessionID                     ='?' # ///会话编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,QuoteSysID                    ='?' # ///报价操作编号
        ,ActionFlag                    ='?' # ///操作标志
        ,UserID                        ='?' # ///用户代码
        ,InstrumentID                  ='?' # ///合约代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,ClientID                      ='?' # ///交易编码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['QuoteAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQuoteAction(pInputQuoteAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqQuoteAction(pInputQuoteAction,self.Inc_RequestID() )


  def ReqBatchOrderAction(self, pInputBatchOrderAction):
    '''
    ///批量报单操作请求
    '''

    """CThostFtdcInputBatchOrderActionField

    l_CThostFtdcInputBatchOrderActionField=py_ApiStructure.InputBatchOrderActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,OrderActionRef                ='?' # ///报单操作引用
        ,RequestID                     ='?' # ///请求编号
        ,FrontID                       ='?' # ///前置编号
        ,SessionID                     ='?' # ///会话编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,UserID                        ='?' # ///用户代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['BatchOrderAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqBatchOrderAction(pInputBatchOrderAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqBatchOrderAction(pInputBatchOrderAction,self.Inc_RequestID() )


  def ReqOptionSelfCloseInsert(self, pInputOptionSelfClose):
    '''
    ///期权自对冲录入请求
    '''

    """CThostFtdcInputOptionSelfCloseField

    l_CThostFtdcInputOptionSelfCloseField=py_ApiStructure.InputOptionSelfCloseField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,OptionSelfCloseRef            ='?' # ///期权自对冲引用
        ,UserID                        ='?' # ///用户代码
        ,Volume                        ='?' # ///数量
        ,RequestID                     ='?' # ///请求编号
        ,BusinessUnit                  ='?' # ///业务单元
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,OptSelfCloseFlag              ='?' # ///期权行权的头寸是否自对冲
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,AccountID                     ='?' # ///资金账号
        ,CurrencyID                    ='?' # ///币种代码
        ,ClientID                      ='?' # ///交易编码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['OptionSelfCloseInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqOptionSelfCloseInsert(pInputOptionSelfClose,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqOptionSelfCloseInsert(pInputOptionSelfClose,self.Inc_RequestID() )


  def ReqOptionSelfCloseAction(self, pInputOptionSelfCloseAction):
    '''
    ///期权自对冲操作请求
    '''

    """CThostFtdcInputOptionSelfCloseActionField

    l_CThostFtdcInputOptionSelfCloseActionField=py_ApiStructure.InputOptionSelfCloseActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,OptionSelfCloseActionRef      ='?' # ///期权自对冲操作引用
        ,OptionSelfCloseRef            ='?' # ///期权自对冲引用
        ,RequestID                     ='?' # ///请求编号
        ,FrontID                       ='?' # ///前置编号
        ,SessionID                     ='?' # ///会话编号
        ,ExchangeID                    ='?' # ///交易所代码
        ,OptionSelfCloseSysID          ='?' # ///期权自对冲操作编号
        ,ActionFlag                    ='?' # ///操作标志
        ,UserID                        ='?' # ///用户代码
        ,InstrumentID                  ='?' # ///合约代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        )

    #"""

    self.req_call['OptionSelfCloseAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqOptionSelfCloseAction(pInputOptionSelfCloseAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqOptionSelfCloseAction(pInputOptionSelfCloseAction,self.Inc_RequestID() )


  def ReqCombActionInsert(self, pInputCombAction):
    '''
    ///申请组合录入请求
    '''

    """CThostFtdcInputCombActionField

    l_CThostFtdcInputCombActionField=py_ApiStructure.InputCombActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,CombActionRef                 ='?' # ///组合引用
        ,UserID                        ='?' # ///用户代码
        ,Direction                     ='?' # ///买卖方向
        ,Volume                        ='?' # ///数量
        ,CombDirection                 ='?' # ///组合指令方向
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,ExchangeID                    ='?' # ///交易所代码
        ,IPAddress                     ='?' # ///IP地址
        ,MacAddress                    ='?' # ///Mac地址
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['CombActionInsert'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqCombActionInsert(pInputCombAction,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqCombActionInsert(pInputCombAction,self.Inc_RequestID() )


  def ReqQryOrder(self, pQryOrder):
    '''
    ///请求查询报单
    '''

    """CThostFtdcQryOrderField

    l_CThostFtdcQryOrderField=py_ApiStructure.QryOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,OrderSysID                    ='?' # ///报单编号
        ,InsertTimeStart               ='?' # ///开始时间
        ,InsertTimeEnd                 ='?' # ///结束时间
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryOrder'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryOrder(pQryOrder,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryOrder(pQryOrder,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryOrder(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryTrade(self, pQryTrade):
    '''
    ///请求查询成交
    '''

    """CThostFtdcQryTradeField

    l_CThostFtdcQryTradeField=py_ApiStructure.QryTradeField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,TradeID                       ='?' # ///成交编号
        ,TradeTimeStart                ='?' # ///开始时间
        ,TradeTimeEnd                  ='?' # ///结束时间
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryTrade'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryTrade(pQryTrade,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryTrade(pQryTrade,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryTrade(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInvestorPosition(self, pQryInvestorPosition):
    '''
    ///请求查询投资者持仓
    '''

    """CThostFtdcQryInvestorPositionField

    l_CThostFtdcQryInvestorPositionField=py_ApiStructure.QryInvestorPositionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInvestorPosition'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInvestorPosition(pQryInvestorPosition,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInvestorPosition(pQryInvestorPosition,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInvestorPosition(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryTradingAccount(self, pQryTradingAccount):
    '''
    ///请求查询资金账户
    '''

    """CThostFtdcQryTradingAccountField

    l_CThostFtdcQryTradingAccountField=py_ApiStructure.QryTradingAccountField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,CurrencyID                    ='?' # ///币种代码
        ,BizType                       ='?' # ///业务类型
        ,AccountID                     ='?' # ///投资者帐号
        )

    #"""

    self.req_call['QryTradingAccount'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryTradingAccount(pQryTradingAccount,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryTradingAccount(pQryTradingAccount,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryTradingAccount(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInvestor(self, pQryInvestor):
    '''
    ///请求查询投资者
    '''

    """CThostFtdcQryInvestorField

    l_CThostFtdcQryInvestorField=py_ApiStructure.QryInvestorField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        )

    #"""

    self.req_call['QryInvestor'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInvestor(pQryInvestor,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInvestor(pQryInvestor,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInvestor(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryTradingCode(self, pQryTradingCode):
    '''
    ///请求查询交易编码
    '''

    """CThostFtdcQryTradingCodeField

    l_CThostFtdcQryTradingCodeField=py_ApiStructure.QryTradingCodeField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,ClientID                      ='?' # ///客户代码
        ,ClientIDType                  ='?' # ///交易编码类型
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryTradingCode'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryTradingCode(pQryTradingCode,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryTradingCode(pQryTradingCode,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryTradingCode(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInstrumentMarginRate(self, pQryInstrumentMarginRate):
    '''
    ///请求查询合约保证金率
    '''

    """CThostFtdcQryInstrumentMarginRateField

    l_CThostFtdcQryInstrumentMarginRateField=py_ApiStructure.QryInstrumentMarginRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInstrumentMarginRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInstrumentMarginRate(pQryInstrumentMarginRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInstrumentMarginRate(pQryInstrumentMarginRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInstrumentMarginRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInstrumentCommissionRate(self, pQryInstrumentCommissionRate):
    '''
    ///请求查询合约手续费率
    '''

    """CThostFtdcQryInstrumentCommissionRateField

    l_CThostFtdcQryInstrumentCommissionRateField=py_ApiStructure.QryInstrumentCommissionRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInstrumentCommissionRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInstrumentCommissionRate(pQryInstrumentCommissionRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInstrumentCommissionRate(pQryInstrumentCommissionRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInstrumentCommissionRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryExchange(self, pQryExchange):
    '''
    ///请求查询交易所
    '''

    """CThostFtdcQryExchangeField

    l_CThostFtdcQryExchangeField=py_ApiStructure.QryExchangeField(
         ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryExchange'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryExchange(pQryExchange,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryExchange(pQryExchange,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryExchange(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryProduct(self, pQryProduct):
    '''
    ///请求查询产品
    '''

    """CThostFtdcQryProductField

    l_CThostFtdcQryProductField=py_ApiStructure.QryProductField(
         ProductID                     ='?' # ///产品代码
        ,ProductClass                  ='?' # ///产品类型
        ,ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryProduct'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryProduct(pQryProduct,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryProduct(pQryProduct,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryProduct(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInstrument(self, pQryInstrument):
    '''
    ///请求查询合约
    '''

    """CThostFtdcQryInstrumentField

    l_CThostFtdcQryInstrumentField=py_ApiStructure.QryInstrumentField(
         InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,ExchangeInstID                ='?' # ///合约在交易所的代码
        ,ProductID                     ='?' # ///产品代码
        )

    #"""

    self.req_call['QryInstrument'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInstrument(pQryInstrument,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInstrument(pQryInstrument,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInstrument(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryDepthMarketData(self, pQryDepthMarketData):
    '''
    ///请求查询行情
    '''

    """CThostFtdcQryDepthMarketDataField

    l_CThostFtdcQryDepthMarketDataField=py_ApiStructure.QryDepthMarketDataField(
         InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryDepthMarketData'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryDepthMarketData(pQryDepthMarketData,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryDepthMarketData(pQryDepthMarketData,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryDepthMarketData(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQrySettlementInfo(self, pQrySettlementInfo):
    '''
    ///请求查询投资者结算结果
    '''

    """CThostFtdcQrySettlementInfoField

    l_CThostFtdcQrySettlementInfoField=py_ApiStructure.QrySettlementInfoField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,TradingDay                    ='?' # ///交易日
        ,AccountID                     ='?' # ///投资者帐号
        ,CurrencyID                    ='?' # ///币种代码
        )

    #"""

    self.req_call['QrySettlementInfo'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQrySettlementInfo(pQrySettlementInfo,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQrySettlementInfo(pQrySettlementInfo,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQrySettlementInfo(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryTransferBank(self, pQryTransferBank):
    '''
    ///请求查询转帐银行
    '''

    """CThostFtdcQryTransferBankField

    l_CThostFtdcQryTransferBankField=py_ApiStructure.QryTransferBankField(
         BankID                        ='?' # ///银行代码
        ,BankBrchID                    ='?' # ///银行分中心代码
        )

    #"""

    self.req_call['QryTransferBank'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryTransferBank(pQryTransferBank,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryTransferBank(pQryTransferBank,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryTransferBank(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInvestorPositionDetail(self, pQryInvestorPositionDetail):
    '''
    ///请求查询投资者持仓明细
    '''

    """CThostFtdcQryInvestorPositionDetailField

    l_CThostFtdcQryInvestorPositionDetailField=py_ApiStructure.QryInvestorPositionDetailField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInvestorPositionDetail'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInvestorPositionDetail(pQryInvestorPositionDetail,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInvestorPositionDetail(pQryInvestorPositionDetail,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInvestorPositionDetail(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryNotice(self, pQryNotice):
    '''
    ///请求查询客户通知
    '''

    """CThostFtdcQryNoticeField

    l_CThostFtdcQryNoticeField=py_ApiStructure.QryNoticeField(
         BrokerID                      ='?' # ///经纪公司代码
        )

    #"""

    self.req_call['QryNotice'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryNotice(pQryNotice,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryNotice(pQryNotice,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryNotice(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQrySettlementInfoConfirm(self, pQrySettlementInfoConfirm):
    '''
    ///请求查询结算信息确认
    '''

    """CThostFtdcQrySettlementInfoConfirmField

    l_CThostFtdcQrySettlementInfoConfirmField=py_ApiStructure.QrySettlementInfoConfirmField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,AccountID                     ='?' # ///投资者帐号
        ,CurrencyID                    ='?' # ///币种代码
        )

    #"""

    self.req_call['QrySettlementInfoConfirm'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQrySettlementInfoConfirm(pQrySettlementInfoConfirm,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQrySettlementInfoConfirm(pQrySettlementInfoConfirm,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQrySettlementInfoConfirm(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInvestorPositionCombineDetail(self, pQryInvestorPositionCombineDetail):
    '''
    ///请求查询投资者持仓明细
    '''

    """CThostFtdcQryInvestorPositionCombineDetailField

    l_CThostFtdcQryInvestorPositionCombineDetailField=py_ApiStructure.QryInvestorPositionCombineDetailField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,CombInstrumentID              ='?' # ///组合持仓合约编码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInvestorPositionCombineDetail'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInvestorPositionCombineDetail(pQryInvestorPositionCombineDetail,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInvestorPositionCombineDetail(pQryInvestorPositionCombineDetail,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInvestorPositionCombineDetail(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryCFMMCTradingAccountKey(self, pQryCFMMCTradingAccountKey):
    '''
    ///请求查询保证金监管系统经纪公司资金账户密钥
    '''

    """CThostFtdcQryCFMMCTradingAccountKeyField

    l_CThostFtdcQryCFMMCTradingAccountKeyField=py_ApiStructure.QryCFMMCTradingAccountKeyField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        )

    #"""

    self.req_call['QryCFMMCTradingAccountKey'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryCFMMCTradingAccountKey(pQryCFMMCTradingAccountKey,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryCFMMCTradingAccountKey(pQryCFMMCTradingAccountKey,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryCFMMCTradingAccountKey(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryEWarrantOffset(self, pQryEWarrantOffset):
    '''
    ///请求查询仓单折抵信息
    '''

    """CThostFtdcQryEWarrantOffsetField

    l_CThostFtdcQryEWarrantOffsetField=py_ApiStructure.QryEWarrantOffsetField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InstrumentID                  ='?' # ///合约代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryEWarrantOffset'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryEWarrantOffset(pQryEWarrantOffset,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryEWarrantOffset(pQryEWarrantOffset,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryEWarrantOffset(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInvestorProductGroupMargin(self, pQryInvestorProductGroupMargin):
    '''
    ///请求查询投资者品种/跨品种保证金
    '''

    """CThostFtdcQryInvestorProductGroupMarginField

    l_CThostFtdcQryInvestorProductGroupMarginField=py_ApiStructure.QryInvestorProductGroupMarginField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,ProductGroupID                ='?' # ///品种/跨品种标示
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInvestorProductGroupMargin'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInvestorProductGroupMargin(pQryInvestorProductGroupMargin,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInvestorProductGroupMargin(pQryInvestorProductGroupMargin,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInvestorProductGroupMargin(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryExchangeMarginRate(self, pQryExchangeMarginRate):
    '''
    ///请求查询交易所保证金率
    '''

    """CThostFtdcQryExchangeMarginRateField

    l_CThostFtdcQryExchangeMarginRateField=py_ApiStructure.QryExchangeMarginRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InstrumentID                  ='?' # ///合约代码
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryExchangeMarginRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryExchangeMarginRate(pQryExchangeMarginRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryExchangeMarginRate(pQryExchangeMarginRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryExchangeMarginRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryExchangeMarginRateAdjust(self, pQryExchangeMarginRateAdjust):
    '''
    ///请求查询交易所调整保证金率
    '''

    """CThostFtdcQryExchangeMarginRateAdjustField

    l_CThostFtdcQryExchangeMarginRateAdjustField=py_ApiStructure.QryExchangeMarginRateAdjustField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InstrumentID                  ='?' # ///合约代码
        ,HedgeFlag                     ='?' # ///投机套保标志
        )

    #"""

    self.req_call['QryExchangeMarginRateAdjust'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryExchangeMarginRateAdjust(pQryExchangeMarginRateAdjust,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryExchangeMarginRateAdjust(pQryExchangeMarginRateAdjust,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryExchangeMarginRateAdjust(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryExchangeRate(self, pQryExchangeRate):
    '''
    ///请求查询汇率
    '''

    """CThostFtdcQryExchangeRateField

    l_CThostFtdcQryExchangeRateField=py_ApiStructure.QryExchangeRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,FromCurrencyID                ='?' # ///源币种
        ,ToCurrencyID                  ='?' # ///目标币种
        )

    #"""

    self.req_call['QryExchangeRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryExchangeRate(pQryExchangeRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryExchangeRate(pQryExchangeRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryExchangeRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQrySecAgentACIDMap(self, pQrySecAgentACIDMap):
    '''
    ///请求查询二级代理操作员银期权限
    '''

    """CThostFtdcQrySecAgentACIDMapField

    l_CThostFtdcQrySecAgentACIDMapField=py_ApiStructure.QrySecAgentACIDMapField(
         BrokerID                      ='?' # ///经纪公司代码
        ,UserID                        ='?' # ///用户代码
        ,AccountID                     ='?' # ///资金账户
        ,CurrencyID                    ='?' # ///币种
        )

    #"""

    self.req_call['QrySecAgentACIDMap'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQrySecAgentACIDMap(pQrySecAgentACIDMap,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQrySecAgentACIDMap(pQrySecAgentACIDMap,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQrySecAgentACIDMap(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryProductExchRate(self, pQryProductExchRate):
    '''
    ///请求查询产品报价汇率
    '''

    """CThostFtdcQryProductExchRateField

    l_CThostFtdcQryProductExchRateField=py_ApiStructure.QryProductExchRateField(
         ProductID                     ='?' # ///产品代码
        ,ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryProductExchRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryProductExchRate(pQryProductExchRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryProductExchRate(pQryProductExchRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryProductExchRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryProductGroup(self, pQryProductGroup):
    '''
    ///请求查询产品组
    '''

    """CThostFtdcQryProductGroupField

    l_CThostFtdcQryProductGroupField=py_ApiStructure.QryProductGroupField(
         ProductID                     ='?' # ///产品代码
        ,ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryProductGroup'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryProductGroup(pQryProductGroup,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryProductGroup(pQryProductGroup,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryProductGroup(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryMMInstrumentCommissionRate(self, pQryMMInstrumentCommissionRate):
    '''
    ///请求查询做市商合约手续费率
    '''

    """CThostFtdcQryMMInstrumentCommissionRateField

    l_CThostFtdcQryMMInstrumentCommissionRateField=py_ApiStructure.QryMMInstrumentCommissionRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        )

    #"""

    self.req_call['QryMMInstrumentCommissionRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryMMInstrumentCommissionRate(pQryMMInstrumentCommissionRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryMMInstrumentCommissionRate(pQryMMInstrumentCommissionRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryMMInstrumentCommissionRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryMMOptionInstrCommRate(self, pQryMMOptionInstrCommRate):
    '''
    ///请求查询做市商期权合约手续费
    '''

    """CThostFtdcQryMMOptionInstrCommRateField

    l_CThostFtdcQryMMOptionInstrCommRateField=py_ApiStructure.QryMMOptionInstrCommRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        )

    #"""

    self.req_call['QryMMOptionInstrCommRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryMMOptionInstrCommRate(pQryMMOptionInstrCommRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryMMOptionInstrCommRate(pQryMMOptionInstrCommRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryMMOptionInstrCommRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInstrumentOrderCommRate(self, pQryInstrumentOrderCommRate):
    '''
    ///请求查询报单手续费
    '''

    """CThostFtdcQryInstrumentOrderCommRateField

    l_CThostFtdcQryInstrumentOrderCommRateField=py_ApiStructure.QryInstrumentOrderCommRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        )

    #"""

    self.req_call['QryInstrumentOrderCommRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInstrumentOrderCommRate(pQryInstrumentOrderCommRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInstrumentOrderCommRate(pQryInstrumentOrderCommRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInstrumentOrderCommRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQrySecAgentTradingAccount(self, pQryTradingAccount):
    '''
    ///请求查询资金账户
    '''

    """CThostFtdcQryTradingAccountField

    l_CThostFtdcQryTradingAccountField=py_ApiStructure.QryTradingAccountField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,CurrencyID                    ='?' # ///币种代码
        ,BizType                       ='?' # ///业务类型
        ,AccountID                     ='?' # ///投资者帐号
        )

    #"""

    self.req_call['QrySecAgentTradingAccount'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQrySecAgentTradingAccount(pQryTradingAccount,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQrySecAgentTradingAccount(pQryTradingAccount,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQrySecAgentTradingAccount(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQrySecAgentCheckMode(self, pQrySecAgentCheckMode):
    '''
    ///请求查询二级代理商资金校验模式
    '''

    """CThostFtdcQrySecAgentCheckModeField

    l_CThostFtdcQrySecAgentCheckModeField=py_ApiStructure.QrySecAgentCheckModeField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        )

    #"""

    self.req_call['QrySecAgentCheckMode'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQrySecAgentCheckMode(pQrySecAgentCheckMode,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQrySecAgentCheckMode(pQrySecAgentCheckMode,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQrySecAgentCheckMode(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryOptionInstrTradeCost(self, pQryOptionInstrTradeCost):
    '''
    ///请求查询期权交易成本
    '''

    """CThostFtdcQryOptionInstrTradeCostField

    l_CThostFtdcQryOptionInstrTradeCostField=py_ApiStructure.QryOptionInstrTradeCostField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,HedgeFlag                     ='?' # ///投机套保标志
        ,InputPrice                    ='?' # ///期权合约报价
        ,UnderlyingPrice               ='?' # ///标的价格,填0则用昨结算价
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryOptionInstrTradeCost'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryOptionInstrTradeCost(pQryOptionInstrTradeCost,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryOptionInstrTradeCost(pQryOptionInstrTradeCost,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryOptionInstrTradeCost(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryOptionInstrCommRate(self, pQryOptionInstrCommRate):
    '''
    ///请求查询期权合约手续费
    '''

    """CThostFtdcQryOptionInstrCommRateField

    l_CThostFtdcQryOptionInstrCommRateField=py_ApiStructure.QryOptionInstrCommRateField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryOptionInstrCommRate'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryOptionInstrCommRate(pQryOptionInstrCommRate,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryOptionInstrCommRate(pQryOptionInstrCommRate,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryOptionInstrCommRate(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryExecOrder(self, pQryExecOrder):
    '''
    ///请求查询执行宣告
    '''

    """CThostFtdcQryExecOrderField

    l_CThostFtdcQryExecOrderField=py_ApiStructure.QryExecOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,ExecOrderSysID                ='?' # ///执行宣告编号
        ,InsertTimeStart               ='?' # ///开始时间
        ,InsertTimeEnd                 ='?' # ///结束时间
        )

    #"""

    self.req_call['QryExecOrder'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryExecOrder(pQryExecOrder,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryExecOrder(pQryExecOrder,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryExecOrder(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryForQuote(self, pQryForQuote):
    '''
    ///请求查询询价
    '''

    """CThostFtdcQryForQuoteField

    l_CThostFtdcQryForQuoteField=py_ApiStructure.QryForQuoteField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InsertTimeStart               ='?' # ///开始时间
        ,InsertTimeEnd                 ='?' # ///结束时间
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryForQuote'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryForQuote(pQryForQuote,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryForQuote(pQryForQuote,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryForQuote(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryQuote(self, pQryQuote):
    '''
    ///请求查询报价
    '''

    """CThostFtdcQryQuoteField

    l_CThostFtdcQryQuoteField=py_ApiStructure.QryQuoteField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,QuoteSysID                    ='?' # ///报价编号
        ,InsertTimeStart               ='?' # ///开始时间
        ,InsertTimeEnd                 ='?' # ///结束时间
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryQuote'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryQuote(pQryQuote,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryQuote(pQryQuote,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryQuote(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryOptionSelfClose(self, pQryOptionSelfClose):
    '''
    ///请求查询期权自对冲
    '''

    """CThostFtdcQryOptionSelfCloseField

    l_CThostFtdcQryOptionSelfCloseField=py_ApiStructure.QryOptionSelfCloseField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,OptionSelfCloseSysID          ='?' # ///期权自对冲编号
        ,InsertTimeStart               ='?' # ///开始时间
        ,InsertTimeEnd                 ='?' # ///结束时间
        )

    #"""

    self.req_call['QryOptionSelfClose'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryOptionSelfClose(pQryOptionSelfClose,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryOptionSelfClose(pQryOptionSelfClose,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryOptionSelfClose(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryInvestUnit(self, pQryInvestUnit):
    '''
    ///请求查询投资单元
    '''

    """CThostFtdcQryInvestUnitField

    l_CThostFtdcQryInvestUnitField=py_ApiStructure.QryInvestUnitField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryInvestUnit'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryInvestUnit(pQryInvestUnit,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryInvestUnit(pQryInvestUnit,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryInvestUnit(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryCombInstrumentGuard(self, pQryCombInstrumentGuard):
    '''
    ///请求查询组合合约安全系数
    '''

    """CThostFtdcQryCombInstrumentGuardField

    l_CThostFtdcQryCombInstrumentGuardField=py_ApiStructure.QryCombInstrumentGuardField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        )

    #"""

    self.req_call['QryCombInstrumentGuard'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryCombInstrumentGuard(pQryCombInstrumentGuard,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryCombInstrumentGuard(pQryCombInstrumentGuard,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryCombInstrumentGuard(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryCombAction(self, pQryCombAction):
    '''
    ///请求查询申请组合
    '''

    """CThostFtdcQryCombActionField

    l_CThostFtdcQryCombActionField=py_ApiStructure.QryCombActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryCombAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryCombAction(pQryCombAction,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryCombAction(pQryCombAction,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryCombAction(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryTransferSerial(self, pQryTransferSerial):
    '''
    ///请求查询转帐流水
    '''

    """CThostFtdcQryTransferSerialField

    l_CThostFtdcQryTransferSerialField=py_ApiStructure.QryTransferSerialField(
         BrokerID                      ='?' # ///经纪公司代码
        ,AccountID                     ='?' # ///投资者帐号
        ,BankID                        ='?' # ///银行编码
        ,CurrencyID                    ='?' # ///币种代码
        )

    #"""

    self.req_call['QryTransferSerial'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryTransferSerial(pQryTransferSerial,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryTransferSerial(pQryTransferSerial,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryTransferSerial(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryAccountregister(self, pQryAccountregister):
    '''
    ///请求查询银期签约关系
    '''

    """CThostFtdcQryAccountregisterField

    l_CThostFtdcQryAccountregisterField=py_ApiStructure.QryAccountregisterField(
         BrokerID                      ='?' # ///经纪公司代码
        ,AccountID                     ='?' # ///投资者帐号
        ,BankID                        ='?' # ///银行编码
        ,BankBranchID                  ='?' # ///银行分支机构编码
        ,CurrencyID                    ='?' # ///币种代码
        )

    #"""

    self.req_call['QryAccountregister'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryAccountregister(pQryAccountregister,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryAccountregister(pQryAccountregister,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryAccountregister(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryContractBank(self, pQryContractBank):
    '''
    ///请求查询签约银行
    '''

    """CThostFtdcQryContractBankField

    l_CThostFtdcQryContractBankField=py_ApiStructure.QryContractBankField(
         BrokerID                      ='?' # ///经纪公司代码
        ,BankID                        ='?' # ///银行代码
        ,BankBrchID                    ='?' # ///银行分中心代码
        )

    #"""

    self.req_call['QryContractBank'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryContractBank(pQryContractBank,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryContractBank(pQryContractBank,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryContractBank(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryParkedOrder(self, pQryParkedOrder):
    '''
    ///请求查询预埋单
    '''

    """CThostFtdcQryParkedOrderField

    l_CThostFtdcQryParkedOrderField=py_ApiStructure.QryParkedOrderField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryParkedOrder'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryParkedOrder(pQryParkedOrder,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryParkedOrder(pQryParkedOrder,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryParkedOrder(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryParkedOrderAction(self, pQryParkedOrderAction):
    '''
    ///请求查询预埋撤单
    '''

    """CThostFtdcQryParkedOrderActionField

    l_CThostFtdcQryParkedOrderActionField=py_ApiStructure.QryParkedOrderActionField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InstrumentID                  ='?' # ///合约代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryParkedOrderAction'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryParkedOrderAction(pQryParkedOrderAction,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryParkedOrderAction(pQryParkedOrderAction,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryParkedOrderAction(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryTradingNotice(self, pQryTradingNotice):
    '''
    ///请求查询交易通知
    '''

    """CThostFtdcQryTradingNoticeField

    l_CThostFtdcQryTradingNoticeField=py_ApiStructure.QryTradingNoticeField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QryTradingNotice'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryTradingNotice(pQryTradingNotice,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryTradingNotice(pQryTradingNotice,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryTradingNotice(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryBrokerTradingParams(self, pQryBrokerTradingParams):
    '''
    ///请求查询经纪公司交易参数
    '''

    """CThostFtdcQryBrokerTradingParamsField

    l_CThostFtdcQryBrokerTradingParamsField=py_ApiStructure.QryBrokerTradingParamsField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,CurrencyID                    ='?' # ///币种代码
        ,AccountID                     ='?' # ///投资者帐号
        )

    #"""

    self.req_call['QryBrokerTradingParams'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryBrokerTradingParams(pQryBrokerTradingParams,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryBrokerTradingParams(pQryBrokerTradingParams,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryBrokerTradingParams(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQryBrokerTradingAlgos(self, pQryBrokerTradingAlgos):
    '''
    ///请求查询经纪公司交易算法
    '''

    """CThostFtdcQryBrokerTradingAlgosField

    l_CThostFtdcQryBrokerTradingAlgosField=py_ApiStructure.QryBrokerTradingAlgosField(
         BrokerID                      ='?' # ///经纪公司代码
        ,ExchangeID                    ='?' # ///交易所代码
        ,InstrumentID                  ='?' # ///合约代码
        )

    #"""

    self.req_call['QryBrokerTradingAlgos'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQryBrokerTradingAlgos(pQryBrokerTradingAlgos,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQryBrokerTradingAlgos(pQryBrokerTradingAlgos,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQryBrokerTradingAlgos(it_ret_val, None, nRequestID, True)
      return 0


  def ReqQueryCFMMCTradingAccountToken(self, pQueryCFMMCTradingAccountToken):
    '''
    ///请求查询监控中心用户令牌
    '''

    """CThostFtdcQueryCFMMCTradingAccountTokenField

    l_CThostFtdcQueryCFMMCTradingAccountTokenField=py_ApiStructure.QueryCFMMCTradingAccountTokenField(
         BrokerID                      ='?' # ///经纪公司代码
        ,InvestorID                    ='?' # ///投资者代码
        ,InvestUnitID                  ='?' # ///投资单元代码
        )

    #"""

    self.req_call['QueryCFMMCTradingAccountToken'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQueryCFMMCTradingAccountToken(pQueryCFMMCTradingAccountToken,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQueryCFMMCTradingAccountToken(pQueryCFMMCTradingAccountToken,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQueryCFMMCTradingAccountToken(it_ret_val, None, nRequestID, True)
      return 0


  def ReqFromBankToFutureByFuture(self, pReqTransfer):
    '''
    ///期货发起银行资金转期货请求
    '''

    """CThostFtdcReqTransferField

    l_CThostFtdcReqTransferField=py_ApiStructure.ReqTransferField(
         TradeCode                     ='?' # ///业务功能码
        ,BankID                        ='?' # ///银行代码
        ,BankBranchID                  ='?' # ///银行分支机构代码
        ,BrokerID                      ='?' # ///期商代码
        ,BrokerBranchID                ='?' # ///期商分支机构代码
        ,TradeDate                     ='?' # ///交易日期
        ,TradeTime                     ='?' # ///交易时间
        ,BankSerial                    ='?' # ///银行流水号
        ,TradingDay                    ='?' # ///交易系统日期
        ,PlateSerial                   ='?' # ///银期平台消息流水号
        ,LastFragment                  ='?' # ///最后分片标志
        ,SessionID                     ='?' # ///会话号
        ,CustomerName                  ='?' # ///客户姓名
        ,IdCardType                    ='?' # ///证件类型
        ,IdentifiedCardNo              ='?' # ///证件号码
        ,CustType                      ='?' # ///客户类型
        ,BankAccount                   ='?' # ///银行帐号
        ,BankPassWord                  ='?' # ///银行密码
        ,AccountID                     ='?' # ///投资者帐号
        ,Password                      ='?' # ///期货密码
        ,InstallID                     ='?' # ///安装编号
        ,FutureSerial                  ='?' # ///期货公司流水号
        ,UserID                        ='?' # ///用户标识
        ,VerifyCertNoFlag              ='?' # ///验证客户证件号码标志
        ,CurrencyID                    ='?' # ///币种代码
        ,TradeAmount                   ='?' # ///转帐金额
        ,FutureFetchAmount             ='?' # ///期货可取金额
        ,FeePayFlag                    ='?' # ///费用支付标志
        ,CustFee                       ='?' # ///应收客户费用
        ,BrokerFee                     ='?' # ///应收期货公司费用
        ,Message                       ='?' # ///发送方给接收方的消息
        ,Digest                        ='?' # ///摘要
        ,BankAccType                   ='?' # ///银行帐号类型
        ,DeviceID                      ='?' # ///渠道标志
        ,BankSecuAccType               ='?' # ///期货单位帐号类型

        ,BrokerIDByBank                ='?' # ///期货公司银行编码
        ,BankSecuAcc                   ='?' # ///期货单位帐号
        ,BankPwdFlag                   ='?' # ///银行密码标志
        ,SecuPwdFlag                   ='?' # ///期货资金密码核对标志
        ,OperNo                        ='?' # ///交易柜员
        ,RequestID                     ='?' # ///请求编号
        ,TID                           ='?' # ///交易ID
        ,TransferStatus                ='?' # ///转账交易状态
        ,LongCustomerName              ='?' # ///长客户姓名
        )

    #"""

    self.req_call['FromBankToFutureByFuture'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqFromBankToFutureByFuture(pReqTransfer,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqFromBankToFutureByFuture(pReqTransfer,self.Inc_RequestID() )


  def ReqFromFutureToBankByFuture(self, pReqTransfer):
    '''
    ///期货发起期货资金转银行请求
    '''

    """CThostFtdcReqTransferField

    l_CThostFtdcReqTransferField=py_ApiStructure.ReqTransferField(
         TradeCode                     ='?' # ///业务功能码
        ,BankID                        ='?' # ///银行代码
        ,BankBranchID                  ='?' # ///银行分支机构代码
        ,BrokerID                      ='?' # ///期商代码
        ,BrokerBranchID                ='?' # ///期商分支机构代码
        ,TradeDate                     ='?' # ///交易日期
        ,TradeTime                     ='?' # ///交易时间
        ,BankSerial                    ='?' # ///银行流水号
        ,TradingDay                    ='?' # ///交易系统日期
        ,PlateSerial                   ='?' # ///银期平台消息流水号
        ,LastFragment                  ='?' # ///最后分片标志
        ,SessionID                     ='?' # ///会话号
        ,CustomerName                  ='?' # ///客户姓名
        ,IdCardType                    ='?' # ///证件类型
        ,IdentifiedCardNo              ='?' # ///证件号码
        ,CustType                      ='?' # ///客户类型
        ,BankAccount                   ='?' # ///银行帐号
        ,BankPassWord                  ='?' # ///银行密码
        ,AccountID                     ='?' # ///投资者帐号
        ,Password                      ='?' # ///期货密码
        ,InstallID                     ='?' # ///安装编号
        ,FutureSerial                  ='?' # ///期货公司流水号
        ,UserID                        ='?' # ///用户标识
        ,VerifyCertNoFlag              ='?' # ///验证客户证件号码标志
        ,CurrencyID                    ='?' # ///币种代码
        ,TradeAmount                   ='?' # ///转帐金额
        ,FutureFetchAmount             ='?' # ///期货可取金额
        ,FeePayFlag                    ='?' # ///费用支付标志
        ,CustFee                       ='?' # ///应收客户费用
        ,BrokerFee                     ='?' # ///应收期货公司费用
        ,Message                       ='?' # ///发送方给接收方的消息
        ,Digest                        ='?' # ///摘要
        ,BankAccType                   ='?' # ///银行帐号类型
        ,DeviceID                      ='?' # ///渠道标志
        ,BankSecuAccType               ='?' # ///期货单位帐号类型

        ,BrokerIDByBank                ='?' # ///期货公司银行编码
        ,BankSecuAcc                   ='?' # ///期货单位帐号
        ,BankPwdFlag                   ='?' # ///银行密码标志
        ,SecuPwdFlag                   ='?' # ///期货资金密码核对标志
        ,OperNo                        ='?' # ///交易柜员
        ,RequestID                     ='?' # ///请求编号
        ,TID                           ='?' # ///交易ID
        ,TransferStatus                ='?' # ///转账交易状态
        ,LongCustomerName              ='?' # ///长客户姓名
        )

    #"""

    self.req_call['FromFutureToBankByFuture'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqFromFutureToBankByFuture(pReqTransfer,self.Inc_RequestID() )
    else:
      return self.PTP_Algos.ReqFromFutureToBankByFuture(pReqTransfer,self.Inc_RequestID() )


  def ReqQueryBankAccountMoneyByFuture(self, pReqQueryAccount):
    '''
    ///期货发起查询银行余额请求
    '''

    """CThostFtdcReqQueryAccountField

    l_CThostFtdcReqQueryAccountField=py_ApiStructure.ReqQueryAccountField(
         TradeCode                     ='?' # ///业务功能码
        ,BankID                        ='?' # ///银行代码
        ,BankBranchID                  ='?' # ///银行分支机构代码
        ,BrokerID                      ='?' # ///期商代码
        ,BrokerBranchID                ='?' # ///期商分支机构代码
        ,TradeDate                     ='?' # ///交易日期
        ,TradeTime                     ='?' # ///交易时间
        ,BankSerial                    ='?' # ///银行流水号
        ,TradingDay                    ='?' # ///交易系统日期
        ,PlateSerial                   ='?' # ///银期平台消息流水号
        ,LastFragment                  ='?' # ///最后分片标志
        ,SessionID                     ='?' # ///会话号
        ,CustomerName                  ='?' # ///客户姓名
        ,IdCardType                    ='?' # ///证件类型
        ,IdentifiedCardNo              ='?' # ///证件号码
        ,CustType                      ='?' # ///客户类型
        ,BankAccount                   ='?' # ///银行帐号
        ,BankPassWord                  ='?' # ///银行密码
        ,AccountID                     ='?' # ///投资者帐号
        ,Password                      ='?' # ///期货密码
        ,FutureSerial                  ='?' # ///期货公司流水号
        ,InstallID                     ='?' # ///安装编号
        ,UserID                        ='?' # ///用户标识
        ,VerifyCertNoFlag              ='?' # ///验证客户证件号码标志
        ,CurrencyID                    ='?' # ///币种代码
        ,Digest                        ='?' # ///摘要
        ,BankAccType                   ='?' # ///银行帐号类型
        ,DeviceID                      ='?' # ///渠道标志
        ,BankSecuAccType               ='?' # ///期货单位帐号类型
        ,BrokerIDByBank                ='?' # ///期货公司银行编码
        ,BankSecuAcc                   ='?' # ///期货单位帐号
        ,BankPwdFlag                   ='?' # ///银行密码标志
        ,SecuPwdFlag                   ='?' # ///期货资金密码核对标志
        ,OperNo                        ='?' # ///交易柜员
        ,RequestID                     ='?' # ///请求编号

        ,TID                           ='?' # ///交易ID
        ,LongCustomerName              ='?' # ///长客户姓名
        )

    #"""

    self.req_call['QueryBankAccountMoneyByFuture'] = 0
    if self.Trader_Rule == 0:
      return super(py_CtpTrader, self).ReqQueryBankAccountMoneyByFuture(pReqQueryAccount,self.Inc_RequestID() )
    else:
      nRequestID = self.Inc_RequestID()
      ret_val_list   = self.PTP_Algos.ReqQueryBankAccountMoneyByFuture(pReqQueryAccount,nRequestID )
      for it_ret_val in ret_val_list:
        self.OnRspQueryBankAccountMoneyByFuture(it_ret_val, None, nRequestID, True)
      return 0


  def OnRspAuthenticate(self, pRspAuthenticateField, pRspInfo, nRequestID, bIsLast):
    '''
    ///客户端认证响应
    '''


    if bIsLast == True:
      self.req_call['Authenticate'] = 1


    self.PTP_Algos.DumpRspDict("T_RspAuthenticate",pRspAuthenticate)

    l_dict={}

    """CThostFtdcRspAuthenticateField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pRspAuthenticate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pRspAuthenticate.UserID.decode(encoding="gb18030", errors="ignore")
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pRspAuthenticate.UserProductInfo.decode(encoding="gb18030", errors="ignore")

    #"""

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

  def OnRspUserPasswordUpdate(self, pUserPasswordUpdate, pRspInfo, nRequestID, bIsLast):
    '''
    ///用户口令更新请求响应
    '''


    if bIsLast == True:
      self.req_call['UserPasswordUpdate'] = 1


    self.PTP_Algos.DumpRspDict("T_UserPasswordUpdate",pUserPasswordUpdate)

    l_dict={}

    """CThostFtdcUserPasswordUpdateField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pUserPasswordUpdate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pUserPasswordUpdate.UserID.decode(encoding="gb18030", errors="ignore")
    # ///原来的口令
    l_dict["OldPassword"]               = pUserPasswordUpdate.OldPassword.decode(encoding="gb18030", errors="ignore")
    # ///新的口令
    l_dict["NewPassword"]               = pUserPasswordUpdate.NewPassword.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate, pRspInfo, nRequestID, bIsLast):
    '''
    ///资金账户口令更新请求响应
    '''


    if bIsLast == True:
      self.req_call['TradingAccountPasswordUpdate'] = 1


    self.PTP_Algos.DumpRspDict("T_TradingAccountPasswordUpdate",pTradingAccountPasswordUpdate)

    l_dict={}

    """CThostFtdcTradingAccountPasswordUpdateField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTradingAccountPasswordUpdate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pTradingAccountPasswordUpdate.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///原来的口令
    l_dict["OldPassword"]               = pTradingAccountPasswordUpdate.OldPassword.decode(encoding="gb18030", errors="ignore")
    # ///新的口令
    l_dict["NewPassword"]               = pTradingAccountPasswordUpdate.NewPassword.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pTradingAccountPasswordUpdate.CurrencyID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///报单录入请求响应
    '''


    if bIsLast == True:
      self.req_call['OrderInsert'] = 1


    self.PTP_Algos.push_OnRspOrderInsert("T_InputOrder",pInputOrder)

    l_dict={}

    """CThostFtdcInputOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pInputOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pInputOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pInputOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pInputOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pInputOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pInputOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pInputOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pInputOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pInputOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pInputOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pInputOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pInputOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")
    # ///止损价
    l_dict["StopPrice"]                 = pInputOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pInputOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")

    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pInputOrder.IsAutoSuspend
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pInputOrder.RequestID
    # ///用户强评标志
    l_dict["UserForceClose"]            = pInputOrder.UserForceClose
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pInputOrder.IsSwapOrder
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInputOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pInputOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspParkedOrderInsert(self, pParkedOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///预埋单录入请求响应
    '''


    if bIsLast == True:
      self.req_call['ParkedOrderInsert'] = 1


    self.PTP_Algos.DumpRspDict("T_ParkedOrder",pParkedOrder)

    l_dict={}

    """CThostFtdcParkedOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pParkedOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pParkedOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pParkedOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pParkedOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pParkedOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pParkedOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pParkedOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pParkedOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pParkedOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pParkedOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pParkedOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pParkedOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pParkedOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pParkedOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pParkedOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pParkedOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")
    # ///止损价
    l_dict["StopPrice"]                 = pParkedOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pParkedOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")

    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pParkedOrder.IsAutoSuspend
    # ///业务单元
    l_dict["BusinessUnit"]              = pParkedOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pParkedOrder.RequestID
    # ///用户强评标志
    l_dict["UserForceClose"]            = pParkedOrder.UserForceClose
    # ///交易所代码
    l_dict["ExchangeID"]                = pParkedOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///预埋报单编号
    l_dict["ParkedOrderID"]             = pParkedOrder.ParkedOrderID.decode(encoding="gb18030", errors="ignore")
    # ///用户类型
    l_dict["UserType"]                  = pParkedOrder.UserType.decode(encoding="gb18030", errors="ignore")
    # ///预埋单状态
    l_dict["Status"]                    = pParkedOrder.Status.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pParkedOrder.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pParkedOrder.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pParkedOrder.IsSwapOrder
    # ///资金账号
    l_dict["AccountID"]                 = pParkedOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pParkedOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pParkedOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pParkedOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pParkedOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pParkedOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspParkedOrderAction(self, pParkedOrderAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///预埋撤单录入请求响应
    '''


    if bIsLast == True:
      self.req_call['ParkedOrderAction'] = 1


    self.PTP_Algos.DumpRspDict("T_ParkedOrderAction",pParkedOrderAction)

    l_dict={}

    """CThostFtdcParkedOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pParkedOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pParkedOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报单操作引用
    l_dict["OrderActionRef"]            = pParkedOrderAction.OrderActionRef
    # ///报单引用
    l_dict["OrderRef"]                  = pParkedOrderAction.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pParkedOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pParkedOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pParkedOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pParkedOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///报单编号
    l_dict["OrderSysID"]                = pParkedOrderAction.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pParkedOrderAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pParkedOrderAction.LimitPrice
    # ///数量变化
    l_dict["VolumeChange"]              = pParkedOrderAction.VolumeChange
    # ///用户代码
    l_dict["UserID"]                    = pParkedOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pParkedOrderAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///预埋撤单单编号
    l_dict["ParkedOrderActionID"]       = pParkedOrderAction.ParkedOrderActionID.decode(encoding="gb18030", errors="ignore")
    # ///用户类型
    l_dict["UserType"]                  = pParkedOrderAction.UserType.decode(encoding="gb18030", errors="ignore")
    # ///预埋撤单状态
    l_dict["Status"]                    = pParkedOrderAction.Status.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pParkedOrderAction.ErrorID

    # ///错误信息
    l_dict["ErrorMsg"]                  = pParkedOrderAction.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pParkedOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pParkedOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pParkedOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///报单操作请求响应
    '''


    if bIsLast == True:
      self.req_call['OrderAction'] = 1


    self.PTP_Algos.DumpRspDict("T_InputOrderAction",pInputOrderAction)

    l_dict={}

    """CThostFtdcInputOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报单操作引用
    l_dict["OrderActionRef"]            = pInputOrderAction.OrderActionRef
    # ///报单引用
    l_dict["OrderRef"]                  = pInputOrderAction.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pInputOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pInputOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pInputOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///报单编号
    l_dict["OrderSysID"]                = pInputOrderAction.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pInputOrderAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pInputOrderAction.LimitPrice
    # ///数量变化
    l_dict["VolumeChange"]              = pInputOrderAction.VolumeChange
    # ///用户代码
    l_dict["UserID"]                    = pInputOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputOrderAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQueryMaxOrderVolume(self, pQueryMaxOrderVolume, pRspInfo, nRequestID, bIsLast):
    '''
    ///查询最大报单数量响应
    '''


    if bIsLast == True:
      self.req_call['QueryMaxOrderVolume'] = 1


    self.PTP_Algos.DumpRspDict("T_QueryMaxOrderVolume",pQueryMaxOrderVolume)

    l_dict={}

    """CThostFtdcQueryMaxOrderVolumeField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pQueryMaxOrderVolume.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pQueryMaxOrderVolume.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pQueryMaxOrderVolume.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pQueryMaxOrderVolume.Direction.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pQueryMaxOrderVolume.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pQueryMaxOrderVolume.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///最大允许报单数量
    l_dict["MaxVolume"]                 = pQueryMaxOrderVolume.MaxVolume
    # ///交易所代码
    l_dict["ExchangeID"]                = pQueryMaxOrderVolume.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pQueryMaxOrderVolume.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
    '''
    ///投资者结算结果确认响应
    '''


    if bIsLast == True:
      self.req_call['SettlementInfoConfirm'] = 1


    self.PTP_Algos.DumpRspDict("T_SettlementInfoConfirm",pSettlementInfoConfirm)

    l_dict={}

    """CThostFtdcSettlementInfoConfirmField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pSettlementInfoConfirm.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pSettlementInfoConfirm.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///确认日期
    l_dict["ConfirmDate"]               = pSettlementInfoConfirm.ConfirmDate.decode(encoding="gb18030", errors="ignore")
    # ///确认时间
    l_dict["ConfirmTime"]               = pSettlementInfoConfirm.ConfirmTime.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pSettlementInfoConfirm.SettlementID
    # ///投资者帐号
    l_dict["AccountID"]                 = pSettlementInfoConfirm.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pSettlementInfoConfirm.CurrencyID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspRemoveParkedOrder(self, pRemoveParkedOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///删除预埋单响应
    '''


    if bIsLast == True:
      self.req_call['RemoveParkedOrder'] = 1


    self.PTP_Algos.DumpRspDict("T_RemoveParkedOrder",pRemoveParkedOrder)

    l_dict={}

    """CThostFtdcRemoveParkedOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pRemoveParkedOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pRemoveParkedOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///预埋报单编号
    l_dict["ParkedOrderID"]             = pRemoveParkedOrder.ParkedOrderID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pRemoveParkedOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspRemoveParkedOrderAction(self, pRemoveParkedOrderAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///删除预埋撤单响应
    '''


    if bIsLast == True:
      self.req_call['RemoveParkedOrderAction'] = 1


    self.PTP_Algos.DumpRspDict("T_RemoveParkedOrderAction",pRemoveParkedOrderAction)

    l_dict={}

    """CThostFtdcRemoveParkedOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pRemoveParkedOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pRemoveParkedOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///预埋撤单编号
    l_dict["ParkedOrderActionID"]       = pRemoveParkedOrderAction.ParkedOrderActionID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pRemoveParkedOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspExecOrderInsert(self, pInputExecOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///执行宣告录入请求响应
    '''


    if bIsLast == True:
      self.req_call['ExecOrderInsert'] = 1


    self.PTP_Algos.DumpRspDict("T_InputExecOrder",pInputExecOrder)

    l_dict={}

    """CThostFtdcInputExecOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputExecOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputExecOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputExecOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告引用
    l_dict["ExecOrderRef"]              = pInputExecOrder.ExecOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputExecOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInputExecOrder.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pInputExecOrder.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputExecOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pInputExecOrder.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInputExecOrder.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///执行类型
    l_dict["ActionType"]                = pInputExecOrder.ActionType.decode(encoding="gb18030", errors="ignore")
    # ///保留头寸申请的持仓方向
    l_dict["PosiDirection"]             = pInputExecOrder.PosiDirection.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后是否保留期货头寸的标记,该字段已废弃
    l_dict["ReservePositionFlag"]       = pInputExecOrder.ReservePositionFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后生成的头寸是否自动平仓
    l_dict["CloseFlag"]                 = pInputExecOrder.CloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputExecOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputExecOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInputExecOrder.AccountID.decode(encoding="gb18030", errors="ignore")

    # ///币种代码
    l_dict["CurrencyID"]                = pInputExecOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputExecOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputExecOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputExecOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspExecOrderAction(self, pInputExecOrderAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///执行宣告操作请求响应
    '''


    if bIsLast == True:
      self.req_call['ExecOrderAction'] = 1


    self.PTP_Algos.DumpRspDict("T_InputExecOrderAction",pInputExecOrderAction)

    l_dict={}

    """CThostFtdcInputExecOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputExecOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputExecOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告操作引用
    l_dict["ExecOrderActionRef"]        = pInputExecOrderAction.ExecOrderActionRef
    # ///执行宣告引用
    l_dict["ExecOrderRef"]              = pInputExecOrderAction.ExecOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pInputExecOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pInputExecOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pInputExecOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputExecOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告操作编号
    l_dict["ExecOrderSysID"]            = pInputExecOrderAction.ExecOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pInputExecOrderAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputExecOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputExecOrderAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputExecOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputExecOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputExecOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspForQuoteInsert(self, pInputForQuote, pRspInfo, nRequestID, bIsLast):
    '''
    ///询价录入请求响应
    '''


    if bIsLast == True:
      self.req_call['ForQuoteInsert'] = 1


    self.PTP_Algos.DumpRspDict("T_InputForQuote",pInputForQuote)

    l_dict={}

    """CThostFtdcInputForQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputForQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputForQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputForQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///询价引用
    l_dict["ForQuoteRef"]               = pInputForQuote.ForQuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputForQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputForQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputForQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputForQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputForQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQuoteInsert(self, pInputQuote, pRspInfo, nRequestID, bIsLast):
    '''
    ///报价录入请求响应
    '''


    if bIsLast == True:
      self.req_call['QuoteInsert'] = 1


    self.PTP_Algos.DumpRspDict("T_InputQuote",pInputQuote)

    l_dict={}

    """CThostFtdcInputQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报价引用
    l_dict["QuoteRef"]                  = pInputQuote.QuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///卖价格
    l_dict["AskPrice"]                  = pInputQuote.AskPrice
    # ///买价格
    l_dict["BidPrice"]                  = pInputQuote.BidPrice
    # ///卖数量
    l_dict["AskVolume"]                 = pInputQuote.AskVolume
    # ///买数量
    l_dict["BidVolume"]                 = pInputQuote.BidVolume
    # ///请求编号
    l_dict["RequestID"]                 = pInputQuote.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputQuote.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///卖开平标志
    l_dict["AskOffsetFlag"]             = pInputQuote.AskOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///买开平标志
    l_dict["BidOffsetFlag"]             = pInputQuote.BidOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///卖投机套保标志
    l_dict["AskHedgeFlag"]              = pInputQuote.AskHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///买投机套保标志
    l_dict["BidHedgeFlag"]              = pInputQuote.BidHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///衍生卖报单引用
    l_dict["AskOrderRef"]               = pInputQuote.AskOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///衍生买报单引用
    l_dict["BidOrderRef"]               = pInputQuote.BidOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///应价编号
    l_dict["ForQuoteSysID"]             = pInputQuote.ForQuoteSysID.decode(encoding="gb18030", errors="ignore")

    # ///交易所代码
    l_dict["ExchangeID"]                = pInputQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputQuote.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQuoteAction(self, pInputQuoteAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///报价操作请求响应
    '''


    if bIsLast == True:
      self.req_call['QuoteAction'] = 1


    self.PTP_Algos.DumpRspDict("T_InputQuoteAction",pInputQuoteAction)

    l_dict={}

    """CThostFtdcInputQuoteActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputQuoteAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputQuoteAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报价操作引用
    l_dict["QuoteActionRef"]            = pInputQuoteAction.QuoteActionRef
    # ///报价引用
    l_dict["QuoteRef"]                  = pInputQuoteAction.QuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pInputQuoteAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pInputQuoteAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pInputQuoteAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputQuoteAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///报价操作编号
    l_dict["QuoteSysID"]                = pInputQuoteAction.QuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pInputQuoteAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputQuoteAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputQuoteAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputQuoteAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputQuoteAction.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputQuoteAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputQuoteAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspBatchOrderAction(self, pInputBatchOrderAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///批量报单操作请求响应
    '''


    if bIsLast == True:
      self.req_call['BatchOrderAction'] = 1


    self.PTP_Algos.DumpRspDict("T_InputBatchOrderAction",pInputBatchOrderAction)

    l_dict={}

    """CThostFtdcInputBatchOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputBatchOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputBatchOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报单操作引用
    l_dict["OrderActionRef"]            = pInputBatchOrderAction.OrderActionRef
    # ///请求编号
    l_dict["RequestID"]                 = pInputBatchOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pInputBatchOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pInputBatchOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputBatchOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputBatchOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputBatchOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputBatchOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputBatchOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspOptionSelfCloseInsert(self, pInputOptionSelfClose, pRspInfo, nRequestID, bIsLast):
    '''
    ///期权自对冲录入请求响应
    '''


    if bIsLast == True:
      self.req_call['OptionSelfCloseInsert'] = 1


    self.PTP_Algos.DumpRspDict("T_InputOptionSelfClose",pInputOptionSelfClose)

    l_dict={}

    """CThostFtdcInputOptionSelfCloseField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputOptionSelfClose.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputOptionSelfClose.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputOptionSelfClose.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲引用
    l_dict["OptionSelfCloseRef"]        = pInputOptionSelfClose.OptionSelfCloseRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputOptionSelfClose.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInputOptionSelfClose.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pInputOptionSelfClose.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputOptionSelfClose.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInputOptionSelfClose.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权的头寸是否自对冲
    l_dict["OptSelfCloseFlag"]          = pInputOptionSelfClose.OptSelfCloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputOptionSelfClose.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputOptionSelfClose.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInputOptionSelfClose.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pInputOptionSelfClose.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputOptionSelfClose.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputOptionSelfClose.IPAddress.decode(encoding="gb18030", errors="ignore")

    # ///Mac地址
    l_dict["MacAddress"]                = pInputOptionSelfClose.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspOptionSelfCloseAction(self, pInputOptionSelfCloseAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///期权自对冲操作请求响应
    '''


    if bIsLast == True:
      self.req_call['OptionSelfCloseAction'] = 1


    self.PTP_Algos.DumpRspDict("T_InputOptionSelfCloseAction",pInputOptionSelfCloseAction)

    l_dict={}

    """CThostFtdcInputOptionSelfCloseActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputOptionSelfCloseAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputOptionSelfCloseAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲操作引用
    l_dict["OptionSelfCloseActionRef"]  = pInputOptionSelfCloseAction.OptionSelfCloseActionRef
    # ///期权自对冲引用
    l_dict["OptionSelfCloseRef"]        = pInputOptionSelfCloseAction.OptionSelfCloseRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pInputOptionSelfCloseAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pInputOptionSelfCloseAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pInputOptionSelfCloseAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputOptionSelfCloseAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲操作编号
    l_dict["OptionSelfCloseSysID"]      = pInputOptionSelfCloseAction.OptionSelfCloseSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pInputOptionSelfCloseAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputOptionSelfCloseAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputOptionSelfCloseAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputOptionSelfCloseAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputOptionSelfCloseAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputOptionSelfCloseAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspCombActionInsert(self, pInputCombAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///申请组合录入请求响应
    '''


    if bIsLast == True:
      self.req_call['CombActionInsert'] = 1


    self.PTP_Algos.DumpRspDict("T_InputCombAction",pInputCombAction)

    l_dict={}

    """CThostFtdcInputCombActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputCombAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputCombAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputCombAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///组合引用
    l_dict["CombActionRef"]             = pInputCombAction.CombActionRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputCombAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pInputCombAction.Direction.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInputCombAction.Volume
    # ///组合指令方向
    l_dict["CombDirection"]             = pInputCombAction.CombDirection.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInputCombAction.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputCombAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputCombAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputCombAction.MacAddress.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputCombAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryOrder(self, pOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询报单响应
    '''


    if bIsLast == True:
      self.req_call['QryOrder'] = 1


    self.PTP_Algos.push_OnRspQryOrder("T_Order",pOrder)

    l_dict={}

    """CThostFtdcOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")
    # ///止损价
    l_dict["StopPrice"]                 = pOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")
    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pOrder.IsAutoSuspend

    # ///业务单元
    l_dict["BusinessUnit"]              = pOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pOrder.RequestID
    # ///本地报单编号
    l_dict["OrderLocalID"]              = pOrder.OrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pOrder.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pOrder.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pOrder.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pOrder.InstallID
    # ///报单提交状态
    l_dict["OrderSubmitStatus"]         = pOrder.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pOrder.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pOrder.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pOrder.SettlementID
    # ///报单编号
    l_dict["OrderSysID"]                = pOrder.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单来源
    l_dict["OrderSource"]               = pOrder.OrderSource.decode(encoding="gb18030", errors="ignore")
    # ///报单状态
    l_dict["OrderStatus"]               = pOrder.OrderStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单类型
    l_dict["OrderType"]                 = pOrder.OrderType.decode(encoding="gb18030", errors="ignore")
    # ///今成交数量
    l_dict["VolumeTraded"]              = pOrder.VolumeTraded
    # ///剩余数量
    l_dict["VolumeTotal"]               = pOrder.VolumeTotal

    # ///报单日期
    l_dict["InsertDate"]                = pOrder.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///委托时间
    l_dict["InsertTime"]                = pOrder.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///激活时间
    l_dict["ActiveTime"]                = pOrder.ActiveTime.decode(encoding="gb18030", errors="ignore")
    # ///挂起时间
    l_dict["SuspendTime"]               = pOrder.SuspendTime.decode(encoding="gb18030", errors="ignore")
    # ///最后修改时间
    l_dict["UpdateTime"]                = pOrder.UpdateTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pOrder.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///最后修改交易所交易员代码
    l_dict["ActiveTraderID"]            = pOrder.ActiveTraderID.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pOrder.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pOrder.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pOrder.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pOrder.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pOrder.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pOrder.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///用户强评标志
    l_dict["UserForceClose"]            = pOrder.UserForceClose
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pOrder.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerOrderSeq"]            = pOrder.BrokerOrderSeq
    # ///相关报单
    l_dict["RelativeOrderSysID"]        = pOrder.RelativeOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///郑商所成交数量
    l_dict["ZCETotalTradedVolume"]      = pOrder.ZCETotalTradedVolume
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pOrder.IsSwapOrder
    # ///营业部编号
    l_dict["BranchID"]                  = pOrder.BranchID.decode(encoding="gb18030", errors="ignore")

    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询成交响应
    '''


    if bIsLast == True:
      self.req_call['QryTrade'] = 1


    self.PTP_Algos.DumpRspDict("T_Trade",pTrade)

    l_dict={}

    """CThostFtdcTradeField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTrade.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pTrade.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pTrade.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pTrade.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pTrade.UserID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pTrade.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///成交编号
    l_dict["TradeID"]                   = pTrade.TradeID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pTrade.Direction.decode(encoding="gb18030", errors="ignore")
    # ///报单编号
    l_dict["OrderSysID"]                = pTrade.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pTrade.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pTrade.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///交易角色
    l_dict["TradingRole"]               = pTrade.TradingRole.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pTrade.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pTrade.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pTrade.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["Price"]                     = pTrade.Price
    # ///数量
    l_dict["Volume"]                    = pTrade.Volume
    # ///成交时期
    l_dict["TradeDate"]                 = pTrade.TradeDate.decode(encoding="gb18030", errors="ignore")

    # ///成交时间
    l_dict["TradeTime"]                 = pTrade.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///成交类型
    l_dict["TradeType"]                 = pTrade.TradeType.decode(encoding="gb18030", errors="ignore")
    # ///成交价来源
    l_dict["PriceSource"]               = pTrade.PriceSource.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pTrade.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///本地报单编号
    l_dict["OrderLocalID"]              = pTrade.OrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pTrade.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///业务单元
    l_dict["BusinessUnit"]              = pTrade.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pTrade.SequenceNo
    # ///交易日
    l_dict["TradingDay"]                = pTrade.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pTrade.SettlementID
    # ///经纪公司报单编号
    l_dict["BrokerOrderSeq"]            = pTrade.BrokerOrderSeq
    # ///成交来源
    l_dict["TradeSource"]               = pTrade.TradeSource.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pTrade.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryInvestorPosition(self, pInvestorPosition, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资者持仓响应
    '''


    if bIsLast == True:
      self.req_call['QryInvestorPosition'] = 1


    self.PTP_Algos.push_OnRspQryInvestorPosition("T_InvestorPosition",pInvestorPosition)

    l_dict={}

    """CThostFtdcInvestorPositionField

    # ///合约代码
    l_dict["InstrumentID"]              = pInvestorPosition.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInvestorPosition.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInvestorPosition.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///持仓多空方向
    l_dict["PosiDirection"]             = pInvestorPosition.PosiDirection.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInvestorPosition.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///持仓日期
    l_dict["PositionDate"]              = pInvestorPosition.PositionDate.decode(encoding="gb18030", errors="ignore")
    # ///上日持仓
    l_dict["YdPosition"]                = pInvestorPosition.YdPosition
    # ///今日持仓
    l_dict["Position"]                  = pInvestorPosition.Position
    # ///多头冻结
    l_dict["LongFrozen"]                = pInvestorPosition.LongFrozen
    # ///空头冻结
    l_dict["ShortFrozen"]               = pInvestorPosition.ShortFrozen
    # ///开仓冻结金额
    l_dict["LongFrozenAmount"]          = pInvestorPosition.LongFrozenAmount
    # ///开仓冻结金额
    l_dict["ShortFrozenAmount"]         = pInvestorPosition.ShortFrozenAmount
    # ///开仓量
    l_dict["OpenVolume"]                = pInvestorPosition.OpenVolume
    # ///平仓量
    l_dict["CloseVolume"]               = pInvestorPosition.CloseVolume
    # ///开仓金额
    l_dict["OpenAmount"]                = pInvestorPosition.OpenAmount
    # ///平仓金额
    l_dict["CloseAmount"]               = pInvestorPosition.CloseAmount
    # ///持仓成本
    l_dict["PositionCost"]              = pInvestorPosition.PositionCost
    # ///上次占用的保证金
    l_dict["PreMargin"]                 = pInvestorPosition.PreMargin
    # ///占用的保证金
    l_dict["UseMargin"]                 = pInvestorPosition.UseMargin
    # ///冻结的保证金
    l_dict["FrozenMargin"]              = pInvestorPosition.FrozenMargin

    # ///冻结的资金
    l_dict["FrozenCash"]                = pInvestorPosition.FrozenCash
    # ///冻结的手续费
    l_dict["FrozenCommission"]          = pInvestorPosition.FrozenCommission
    # ///资金差额
    l_dict["CashIn"]                    = pInvestorPosition.CashIn
    # ///手续费
    l_dict["Commission"]                = pInvestorPosition.Commission
    # ///平仓盈亏
    l_dict["CloseProfit"]               = pInvestorPosition.CloseProfit
    # ///持仓盈亏
    l_dict["PositionProfit"]            = pInvestorPosition.PositionProfit
    # ///上次结算价
    l_dict["PreSettlementPrice"]        = pInvestorPosition.PreSettlementPrice
    # ///本次结算价
    l_dict["SettlementPrice"]           = pInvestorPosition.SettlementPrice
    # ///交易日
    l_dict["TradingDay"]                = pInvestorPosition.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pInvestorPosition.SettlementID
    # ///开仓成本
    l_dict["OpenCost"]                  = pInvestorPosition.OpenCost
    # ///交易所保证金
    l_dict["ExchangeMargin"]            = pInvestorPosition.ExchangeMargin
    # ///组合成交形成的持仓
    l_dict["CombPosition"]              = pInvestorPosition.CombPosition
    # ///组合多头冻结
    l_dict["CombLongFrozen"]            = pInvestorPosition.CombLongFrozen
    # ///组合空头冻结
    l_dict["CombShortFrozen"]           = pInvestorPosition.CombShortFrozen
    # ///逐日盯市平仓盈亏
    l_dict["CloseProfitByDate"]         = pInvestorPosition.CloseProfitByDate
    # ///逐笔对冲平仓盈亏
    l_dict["CloseProfitByTrade"]        = pInvestorPosition.CloseProfitByTrade
    # ///今日持仓
    l_dict["TodayPosition"]             = pInvestorPosition.TodayPosition
    # ///保证金率
    l_dict["MarginRateByMoney"]         = pInvestorPosition.MarginRateByMoney
    # ///保证金率(按手数)
    l_dict["MarginRateByVolume"]        = pInvestorPosition.MarginRateByVolume
    # ///执行冻结
    l_dict["StrikeFrozen"]              = pInvestorPosition.StrikeFrozen
    # ///执行冻结金额
    l_dict["StrikeFrozenAmount"]        = pInvestorPosition.StrikeFrozenAmount

    # ///放弃执行冻结
    l_dict["AbandonFrozen"]             = pInvestorPosition.AbandonFrozen
    # ///交易所代码
    l_dict["ExchangeID"]                = pInvestorPosition.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///执行冻结的昨仓
    l_dict["YdStrikeFrozen"]            = pInvestorPosition.YdStrikeFrozen
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInvestorPosition.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询资金账户响应
    '''


    if bIsLast == True:
      self.req_call['QryTradingAccount'] = 1


    self.PTP_Algos.push_OnRspQryTradingAccount("T_TradingAccount",pTradingAccount)

    l_dict={}

    """CThostFtdcTradingAccountField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTradingAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pTradingAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///上次质押金额
    l_dict["PreMortgage"]               = pTradingAccount.PreMortgage
    # ///上次信用额度
    l_dict["PreCredit"]                 = pTradingAccount.PreCredit
    # ///上次存款额
    l_dict["PreDeposit"]                = pTradingAccount.PreDeposit
    # ///上次结算准备金
    l_dict["PreBalance"]                = pTradingAccount.PreBalance
    # ///上次占用的保证金
    l_dict["PreMargin"]                 = pTradingAccount.PreMargin
    # ///利息基数
    l_dict["InterestBase"]              = pTradingAccount.InterestBase
    # ///利息收入
    l_dict["Interest"]                  = pTradingAccount.Interest
    # ///入金金额
    l_dict["Deposit"]                   = pTradingAccount.Deposit
    # ///出金金额
    l_dict["Withdraw"]                  = pTradingAccount.Withdraw
    # ///冻结的保证金
    l_dict["FrozenMargin"]              = pTradingAccount.FrozenMargin
    # ///冻结的资金
    l_dict["FrozenCash"]                = pTradingAccount.FrozenCash
    # ///冻结的手续费
    l_dict["FrozenCommission"]          = pTradingAccount.FrozenCommission
    # ///当前保证金总额
    l_dict["CurrMargin"]                = pTradingAccount.CurrMargin
    # ///资金差额
    l_dict["CashIn"]                    = pTradingAccount.CashIn
    # ///手续费
    l_dict["Commission"]                = pTradingAccount.Commission
    # ///平仓盈亏
    l_dict["CloseProfit"]               = pTradingAccount.CloseProfit
    # ///持仓盈亏
    l_dict["PositionProfit"]            = pTradingAccount.PositionProfit
    # ///期货结算准备金
    l_dict["Balance"]                   = pTradingAccount.Balance
    # ///可用资金
    l_dict["Available"]                 = pTradingAccount.Available
    # ///可取资金
    l_dict["WithdrawQuota"]             = pTradingAccount.WithdrawQuota
    # ///基本准备金
    l_dict["Reserve"]                   = pTradingAccount.Reserve

    # ///交易日
    l_dict["TradingDay"]                = pTradingAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pTradingAccount.SettlementID
    # ///信用额度
    l_dict["Credit"]                    = pTradingAccount.Credit
    # ///质押金额
    l_dict["Mortgage"]                  = pTradingAccount.Mortgage
    # ///交易所保证金
    l_dict["ExchangeMargin"]            = pTradingAccount.ExchangeMargin
    # ///投资者交割保证金
    l_dict["DeliveryMargin"]            = pTradingAccount.DeliveryMargin
    # ///交易所交割保证金
    l_dict["ExchangeDeliveryMargin"]    = pTradingAccount.ExchangeDeliveryMargin
    # ///保底期货结算准备金
    l_dict["ReserveBalance"]            = pTradingAccount.ReserveBalance
    # ///币种代码
    l_dict["CurrencyID"]                = pTradingAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///上次货币质入金额
    l_dict["PreFundMortgageIn"]         = pTradingAccount.PreFundMortgageIn
    # ///上次货币质出金额
    l_dict["PreFundMortgageOut"]        = pTradingAccount.PreFundMortgageOut
    # ///货币质入金额
    l_dict["FundMortgageIn"]            = pTradingAccount.FundMortgageIn
    # ///货币质出金额
    l_dict["FundMortgageOut"]           = pTradingAccount.FundMortgageOut
    # ///货币质押余额
    l_dict["FundMortgageAvailable"]     = pTradingAccount.FundMortgageAvailable
    # ///可质押货币金额
    l_dict["MortgageableFund"]          = pTradingAccount.MortgageableFund
    # ///特殊产品占用保证金
    l_dict["SpecProductMargin"]         = pTradingAccount.SpecProductMargin
    # ///特殊产品冻结保证金
    l_dict["SpecProductFrozenMargin"]   = pTradingAccount.SpecProductFrozenMargin
    # ///特殊产品手续费
    l_dict["SpecProductCommission"]     = pTradingAccount.SpecProductCommission
    # ///特殊产品冻结手续费
    l_dict["SpecProductFrozenCommission = pTradingAccount.SpecProductFrozenCommission
    # ///特殊产品持仓盈亏
    l_dict["SpecProductPositionProfit"] = pTradingAccount.SpecProductPositionProfit
    # ///特殊产品平仓盈亏
    l_dict["SpecProductCloseProfit"]    = pTradingAccount.SpecProductCloseProfit

    # ///根据持仓盈亏算法计算的特殊产品持仓盈亏
    l_dict["SpecProductPositionProfitBy = pTradingAccount.SpecProductPositionProfitByAlg
    # ///特殊产品交易所保证金
    l_dict["SpecProductExchangeMargin"] = pTradingAccount.SpecProductExchangeMargin
    # ///业务类型
    l_dict["BizType"]                   = pTradingAccount.BizType.decode(encoding="gb18030", errors="ignore")
    # ///延时换汇冻结金额
    l_dict["FrozenSwap"]                = pTradingAccount.FrozenSwap
    # ///剩余换汇额度
    l_dict["RemainSwap"]                = pTradingAccount.RemainSwap

    #"""

  def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资者响应
    '''


    if bIsLast == True:
      self.req_call['QryInvestor'] = 1


    self.PTP_Algos.DumpRspDict("T_Investor",pInvestor)

    l_dict={}

    """CThostFtdcInvestorField

    # ///投资者代码
    l_dict["InvestorID"]                = pInvestor.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInvestor.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者分组代码
    l_dict["InvestorGroupID"]           = pInvestor.InvestorGroupID.decode(encoding="gb18030", errors="ignore")
    # ///投资者名称
    l_dict["InvestorName"]              = pInvestor.InvestorName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdentifiedCardType"]        = pInvestor.IdentifiedCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pInvestor.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///是否活跃
    l_dict["IsActive"]                  = pInvestor.IsActive
    # ///联系电话
    l_dict["Telephone"]                 = pInvestor.Telephone.decode(encoding="gb18030", errors="ignore")
    # ///通讯地址
    l_dict["Address"]                   = pInvestor.Address.decode(encoding="gb18030", errors="ignore")
    # ///开户日期
    l_dict["OpenDate"]                  = pInvestor.OpenDate.decode(encoding="gb18030", errors="ignore")
    # ///手机
    l_dict["Mobile"]                    = pInvestor.Mobile.decode(encoding="gb18030", errors="ignore")
    # ///手续费率模板代码
    l_dict["CommModelID"]               = pInvestor.CommModelID.decode(encoding="gb18030", errors="ignore")
    # ///保证金率模板代码
    l_dict["MarginModelID"]             = pInvestor.MarginModelID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryTradingCode(self, pTradingCode, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询交易编码响应
    '''


    if bIsLast == True:
      self.req_call['QryTradingCode'] = 1


    self.PTP_Algos.DumpRspDict("T_TradingCode",pTradingCode)

    l_dict={}

    """CThostFtdcTradingCodeField

    # ///投资者代码
    l_dict["InvestorID"]                = pTradingCode.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTradingCode.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pTradingCode.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pTradingCode.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///是否活跃
    l_dict["IsActive"]                  = pTradingCode.IsActive
    # ///交易编码类型
    l_dict["ClientIDType"]              = pTradingCode.ClientIDType.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pTradingCode.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///业务类型
    l_dict["BizType"]                   = pTradingCode.BizType.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pTradingCode.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryInstrumentMarginRate(self, pInstrumentMarginRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询合约保证金率响应
    '''


    if bIsLast == True:
      self.req_call['QryInstrumentMarginRate'] = 1


    self.PTP_Algos.DumpRspDict("T_InstrumentMarginRate",pInstrumentMarginRate)

    l_dict={}

    """CThostFtdcInstrumentMarginRateField

    # ///合约代码
    l_dict["InstrumentID"]              = pInstrumentMarginRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pInstrumentMarginRate.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInstrumentMarginRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInstrumentMarginRate.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInstrumentMarginRate.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///多头保证金率
    l_dict["LongMarginRatioByMoney"]    = pInstrumentMarginRate.LongMarginRatioByMoney
    # ///多头保证金费
    l_dict["LongMarginRatioByVolume"]   = pInstrumentMarginRate.LongMarginRatioByVolume
    # ///空头保证金率
    l_dict["ShortMarginRatioByMoney"]   = pInstrumentMarginRate.ShortMarginRatioByMoney
    # ///空头保证金费
    l_dict["ShortMarginRatioByVolume"]  = pInstrumentMarginRate.ShortMarginRatioByVolume
    # ///是否相对交易所收取
    l_dict["IsRelative"]                = pInstrumentMarginRate.IsRelative
    # ///交易所代码
    l_dict["ExchangeID"]                = pInstrumentMarginRate.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInstrumentMarginRate.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryInstrumentCommissionRate(self, pInstrumentCommissionRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询合约手续费率响应
    '''


    if bIsLast == True:
      self.req_call['QryInstrumentCommissionRate'] = 1


    self.PTP_Algos.DumpRspDict("T_InstrumentCommissionRate",pInstrumentCommissionRate)

    l_dict={}

    """CThostFtdcInstrumentCommissionRateField

    # ///合约代码
    l_dict["InstrumentID"]              = pInstrumentCommissionRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pInstrumentCommissionRate.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInstrumentCommissionRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInstrumentCommissionRate.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///开仓手续费率
    l_dict["OpenRatioByMoney"]          = pInstrumentCommissionRate.OpenRatioByMoney
    # ///开仓手续费
    l_dict["OpenRatioByVolume"]         = pInstrumentCommissionRate.OpenRatioByVolume
    # ///平仓手续费率
    l_dict["CloseRatioByMoney"]         = pInstrumentCommissionRate.CloseRatioByMoney
    # ///平仓手续费
    l_dict["CloseRatioByVolume"]        = pInstrumentCommissionRate.CloseRatioByVolume
    # ///平今手续费率
    l_dict["CloseTodayRatioByMoney"]    = pInstrumentCommissionRate.CloseTodayRatioByMoney
    # ///平今手续费
    l_dict["CloseTodayRatioByVolume"]   = pInstrumentCommissionRate.CloseTodayRatioByVolume
    # ///交易所代码
    l_dict["ExchangeID"]                = pInstrumentCommissionRate.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///业务类型
    l_dict["BizType"]                   = pInstrumentCommissionRate.BizType.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInstrumentCommissionRate.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryExchange(self, pExchange, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询交易所响应
    '''


    if bIsLast == True:
      self.req_call['QryExchange'] = 1


    self.PTP_Algos.DumpRspDict("T_Exchange",pExchange)

    l_dict={}

    """CThostFtdcExchangeField

    # ///交易所代码
    l_dict["ExchangeID"]                = pExchange.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///交易所名称
    l_dict["ExchangeName"]              = pExchange.ExchangeName.decode(encoding="gb18030", errors="ignore")
    # ///交易所属性
    l_dict["ExchangeProperty"]          = pExchange.ExchangeProperty.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryProduct(self, pProduct, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询产品响应
    '''


    if bIsLast == True:
      self.req_call['QryProduct'] = 1


    self.PTP_Algos.DumpRspDict("T_Product",pProduct)

    l_dict={}

    """CThostFtdcProductField

    # ///产品代码
    l_dict["ProductID"]                 = pProduct.ProductID.decode(encoding="gb18030", errors="ignore")
    # ///产品名称
    l_dict["ProductName"]               = pProduct.ProductName.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pProduct.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///产品类型
    l_dict["ProductClass"]              = pProduct.ProductClass.decode(encoding="gb18030", errors="ignore")
    # ///合约数量乘数
    l_dict["VolumeMultiple"]            = pProduct.VolumeMultiple
    # ///最小变动价位
    l_dict["PriceTick"]                 = pProduct.PriceTick
    # ///市价单最大下单量
    l_dict["MaxMarketOrderVolume"]      = pProduct.MaxMarketOrderVolume
    # ///市价单最小下单量
    l_dict["MinMarketOrderVolume"]      = pProduct.MinMarketOrderVolume
    # ///限价单最大下单量
    l_dict["MaxLimitOrderVolume"]       = pProduct.MaxLimitOrderVolume
    # ///限价单最小下单量
    l_dict["MinLimitOrderVolume"]       = pProduct.MinLimitOrderVolume
    # ///持仓类型
    l_dict["PositionType"]              = pProduct.PositionType.decode(encoding="gb18030", errors="ignore")
    # ///持仓日期类型
    l_dict["PositionDateType"]          = pProduct.PositionDateType.decode(encoding="gb18030", errors="ignore")
    # ///平仓处理类型
    l_dict["CloseDealType"]             = pProduct.CloseDealType.decode(encoding="gb18030", errors="ignore")
    # ///交易币种类型
    l_dict["TradeCurrencyID"]           = pProduct.TradeCurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///质押资金可用范围
    l_dict["MortgageFundUseRange"]      = pProduct.MortgageFundUseRange.decode(encoding="gb18030", errors="ignore")
    # ///交易所产品代码
    l_dict["ExchangeProductID"]         = pProduct.ExchangeProductID.decode(encoding="gb18030", errors="ignore")
    # ///合约基础商品乘数
    l_dict["UnderlyingMultiple"]        = pProduct.UnderlyingMultiple

    #"""

  def OnRspQryInstrument(self, pInstrument, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询合约响应
    '''


    if bIsLast == True:
      self.req_call['QryInstrument'] = 1


    self.PTP_Algos.push_OnRspQryInstrument("T_Instrument",pInstrument)

    l_dict={}

    """CThostFtdcInstrumentField

    # ///合约代码
    l_dict["InstrumentID"]              = pInstrument.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInstrument.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///合约名称
    l_dict["InstrumentName"]            = pInstrument.InstrumentName.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pInstrument.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///产品代码
    l_dict["ProductID"]                 = pInstrument.ProductID.decode(encoding="gb18030", errors="ignore")
    # ///产品类型
    l_dict["ProductClass"]              = pInstrument.ProductClass.decode(encoding="gb18030", errors="ignore")
    # ///交割年份
    l_dict["DeliveryYear"]              = pInstrument.DeliveryYear
    # ///交割月
    l_dict["DeliveryMonth"]             = pInstrument.DeliveryMonth
    # ///市价单最大下单量
    l_dict["MaxMarketOrderVolume"]      = pInstrument.MaxMarketOrderVolume
    # ///市价单最小下单量
    l_dict["MinMarketOrderVolume"]      = pInstrument.MinMarketOrderVolume
    # ///限价单最大下单量
    l_dict["MaxLimitOrderVolume"]       = pInstrument.MaxLimitOrderVolume
    # ///限价单最小下单量
    l_dict["MinLimitOrderVolume"]       = pInstrument.MinLimitOrderVolume
    # ///合约数量乘数
    l_dict["VolumeMultiple"]            = pInstrument.VolumeMultiple
    # ///最小变动价位
    l_dict["PriceTick"]                 = pInstrument.PriceTick
    # ///创建日
    l_dict["CreateDate"]                = pInstrument.CreateDate.decode(encoding="gb18030", errors="ignore")
    # ///上市日
    l_dict["OpenDate"]                  = pInstrument.OpenDate.decode(encoding="gb18030", errors="ignore")
    # ///到期日
    l_dict["ExpireDate"]                = pInstrument.ExpireDate.decode(encoding="gb18030", errors="ignore")
    # ///开始交割日
    l_dict["StartDelivDate"]            = pInstrument.StartDelivDate.decode(encoding="gb18030", errors="ignore")
    # ///结束交割日
    l_dict["EndDelivDate"]              = pInstrument.EndDelivDate.decode(encoding="gb18030", errors="ignore")

    # ///合约生命周期状态
    l_dict["InstLifePhase"]             = pInstrument.InstLifePhase.decode(encoding="gb18030", errors="ignore")
    # ///当前是否交易
    l_dict["IsTrading"]                 = pInstrument.IsTrading
    # ///持仓类型
    l_dict["PositionType"]              = pInstrument.PositionType.decode(encoding="gb18030", errors="ignore")
    # ///持仓日期类型
    l_dict["PositionDateType"]          = pInstrument.PositionDateType.decode(encoding="gb18030", errors="ignore")
    # ///多头保证金率
    l_dict["LongMarginRatio"]           = pInstrument.LongMarginRatio
    # ///空头保证金率
    l_dict["ShortMarginRatio"]          = pInstrument.ShortMarginRatio
    # ///是否使用大额单边保证金算法
    l_dict["MaxMarginSideAlgorithm"]    = pInstrument.MaxMarginSideAlgorithm.decode(encoding="gb18030", errors="ignore")
    # ///基础商品代码
    l_dict["UnderlyingInstrID"]         = pInstrument.UnderlyingInstrID.decode(encoding="gb18030", errors="ignore")
    # ///执行价
    l_dict["StrikePrice"]               = pInstrument.StrikePrice
    # ///期权类型
    l_dict["OptionsType"]               = pInstrument.OptionsType.decode(encoding="gb18030", errors="ignore")
    # ///合约基础商品乘数
    l_dict["UnderlyingMultiple"]        = pInstrument.UnderlyingMultiple
    # ///组合类型
    l_dict["CombinationType"]           = pInstrument.CombinationType.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryDepthMarketData(self, pDepthMarketData, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询行情响应
    '''


    if bIsLast == True:
      self.req_call['QryDepthMarketData'] = 1


    self.PTP_Algos.DumpRspDict("T_DepthMarketData",pDepthMarketData)

    l_dict={}

    """CThostFtdcDepthMarketDataField

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

  def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资者结算结果响应
    '''


    if bIsLast == True:
      self.req_call['QrySettlementInfo'] = 1


    self.PTP_Algos.push_OnRspQrySettlementInfo("T_SettlementInfo",pSettlementInfo)

    l_dict={}

    """CThostFtdcSettlementInfoField

    # ///交易日
    l_dict["TradingDay"]                = pSettlementInfo.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pSettlementInfo.SettlementID
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pSettlementInfo.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pSettlementInfo.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pSettlementInfo.SequenceNo
    # ///消息正文
    l_dict["Content"]                   = pSettlementInfo.Content.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pSettlementInfo.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pSettlementInfo.CurrencyID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryTransferBank(self, pTransferBank, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询转帐银行响应
    '''


    if bIsLast == True:
      self.req_call['QryTransferBank'] = 1


    self.PTP_Algos.DumpRspDict("T_TransferBank",pTransferBank)

    l_dict={}

    """CThostFtdcTransferBankField

    # ///银行代码
    l_dict["BankID"]                    = pTransferBank.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分中心代码
    l_dict["BankBrchID"]                = pTransferBank.BankBrchID.decode(encoding="gb18030", errors="ignore")
    # ///银行名称
    l_dict["BankName"]                  = pTransferBank.BankName.decode(encoding="gb18030", errors="ignore")
    # ///是否活跃
    l_dict["IsActive"]                  = pTransferBank.IsActive

    #"""

  def OnRspQryInvestorPositionDetail(self, pInvestorPositionDetail, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资者持仓明细响应
    '''


    if bIsLast == True:
      self.req_call['QryInvestorPositionDetail'] = 1


    self.PTP_Algos.DumpRspDict("T_InvestorPositionDetail",pInvestorPositionDetail)

    l_dict={}

    """CThostFtdcInvestorPositionDetailField

    # ///合约代码
    l_dict["InstrumentID"]              = pInvestorPositionDetail.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInvestorPositionDetail.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInvestorPositionDetail.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInvestorPositionDetail.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///买卖
    l_dict["Direction"]                 = pInvestorPositionDetail.Direction.decode(encoding="gb18030", errors="ignore")
    # ///开仓日期
    l_dict["OpenDate"]                  = pInvestorPositionDetail.OpenDate.decode(encoding="gb18030", errors="ignore")
    # ///成交编号
    l_dict["TradeID"]                   = pInvestorPositionDetail.TradeID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInvestorPositionDetail.Volume
    # ///开仓价
    l_dict["OpenPrice"]                 = pInvestorPositionDetail.OpenPrice
    # ///交易日
    l_dict["TradingDay"]                = pInvestorPositionDetail.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pInvestorPositionDetail.SettlementID
    # ///成交类型
    l_dict["TradeType"]                 = pInvestorPositionDetail.TradeType.decode(encoding="gb18030", errors="ignore")
    # ///组合合约代码
    l_dict["CombInstrumentID"]          = pInvestorPositionDetail.CombInstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInvestorPositionDetail.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///逐日盯市平仓盈亏
    l_dict["CloseProfitByDate"]         = pInvestorPositionDetail.CloseProfitByDate
    # ///逐笔对冲平仓盈亏
    l_dict["CloseProfitByTrade"]        = pInvestorPositionDetail.CloseProfitByTrade
    # ///逐日盯市持仓盈亏
    l_dict["PositionProfitByDate"]      = pInvestorPositionDetail.PositionProfitByDate

    # ///逐笔对冲持仓盈亏
    l_dict["PositionProfitByTrade"]     = pInvestorPositionDetail.PositionProfitByTrade
    # ///投资者保证金
    l_dict["Margin"]                    = pInvestorPositionDetail.Margin
    # ///交易所保证金
    l_dict["ExchMargin"]                = pInvestorPositionDetail.ExchMargin
    # ///保证金率
    l_dict["MarginRateByMoney"]         = pInvestorPositionDetail.MarginRateByMoney
    # ///保证金率(按手数)
    l_dict["MarginRateByVolume"]        = pInvestorPositionDetail.MarginRateByVolume
    # ///昨结算价
    l_dict["LastSettlementPrice"]       = pInvestorPositionDetail.LastSettlementPrice
    # ///结算价
    l_dict["SettlementPrice"]           = pInvestorPositionDetail.SettlementPrice
    # ///平仓量
    l_dict["CloseVolume"]               = pInvestorPositionDetail.CloseVolume
    # ///平仓金额
    l_dict["CloseAmount"]               = pInvestorPositionDetail.CloseAmount
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInvestorPositionDetail.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryNotice(self, pNotice, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询客户通知响应
    '''


    if bIsLast == True:
      self.req_call['QryNotice'] = 1


    self.PTP_Algos.DumpRspDict("T_Notice",pNotice)

    l_dict={}

    """CThostFtdcNoticeField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pNotice.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///消息正文
    l_dict["Content"]                   = pNotice.Content.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司通知内容序列号
    l_dict["SequenceLabel"]             = pNotice.SequenceLabel.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询结算信息确认响应
    '''


    if bIsLast == True:
      self.req_call['QrySettlementInfoConfirm'] = 1


    self.PTP_Algos.DumpRspDict("T_SettlementInfoConfirm",pSettlementInfoConfirm)

    l_dict={}

    """CThostFtdcSettlementInfoConfirmField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pSettlementInfoConfirm.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pSettlementInfoConfirm.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///确认日期
    l_dict["ConfirmDate"]               = pSettlementInfoConfirm.ConfirmDate.decode(encoding="gb18030", errors="ignore")
    # ///确认时间
    l_dict["ConfirmTime"]               = pSettlementInfoConfirm.ConfirmTime.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pSettlementInfoConfirm.SettlementID
    # ///投资者帐号
    l_dict["AccountID"]                 = pSettlementInfoConfirm.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pSettlementInfoConfirm.CurrencyID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryInvestorPositionCombineDetail(self, pInvestorPositionCombineDetail, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资者持仓明细响应
    '''


    if bIsLast == True:
      self.req_call['QryInvestorPositionCombineDetail'] = 1


    self.PTP_Algos.DumpRspDict("T_InvestorPositionCombineDetail",pInvestorPositionCombineDetail)

    l_dict={}

    """CThostFtdcInvestorPositionCombineDetailField

    # ///交易日
    l_dict["TradingDay"]                = pInvestorPositionCombineDetail.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///开仓日期
    l_dict["OpenDate"]                  = pInvestorPositionCombineDetail.OpenDate.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInvestorPositionCombineDetail.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pInvestorPositionCombineDetail.SettlementID
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInvestorPositionCombineDetail.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInvestorPositionCombineDetail.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///组合编号
    l_dict["ComTradeID"]                = pInvestorPositionCombineDetail.ComTradeID.decode(encoding="gb18030", errors="ignore")
    # ///撮合编号
    l_dict["TradeID"]                   = pInvestorPositionCombineDetail.TradeID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInvestorPositionCombineDetail.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInvestorPositionCombineDetail.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///买卖
    l_dict["Direction"]                 = pInvestorPositionCombineDetail.Direction.decode(encoding="gb18030", errors="ignore")
    # ///持仓量
    l_dict["TotalAmt"]                  = pInvestorPositionCombineDetail.TotalAmt
    # ///投资者保证金
    l_dict["Margin"]                    = pInvestorPositionCombineDetail.Margin
    # ///交易所保证金
    l_dict["ExchMargin"]                = pInvestorPositionCombineDetail.ExchMargin
    # ///保证金率
    l_dict["MarginRateByMoney"]         = pInvestorPositionCombineDetail.MarginRateByMoney
    # ///保证金率(按手数)
    l_dict["MarginRateByVolume"]        = pInvestorPositionCombineDetail.MarginRateByVolume

    # ///单腿编号
    l_dict["LegID"]                     = pInvestorPositionCombineDetail.LegID
    # ///单腿乘数
    l_dict["LegMultiple"]               = pInvestorPositionCombineDetail.LegMultiple
    # ///组合持仓合约编码
    l_dict["CombInstrumentID"]          = pInvestorPositionCombineDetail.CombInstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///成交组号
    l_dict["TradeGroupID"]              = pInvestorPositionCombineDetail.TradeGroupID
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInvestorPositionCombineDetail.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryCFMMCTradingAccountKey(self, pCFMMCTradingAccountKey, pRspInfo, nRequestID, bIsLast):
    '''
    ///查询保证金监管系统经纪公司资金账户密钥响应
    '''


    if bIsLast == True:
      self.req_call['QryCFMMCTradingAccountKey'] = 1


    self.PTP_Algos.DumpRspDict("T_CFMMCTradingAccountKey",pCFMMCTradingAccountKey)

    l_dict={}

    """CThostFtdcCFMMCTradingAccountKeyField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pCFMMCTradingAccountKey.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司统一编码
    l_dict["ParticipantID"]             = pCFMMCTradingAccountKey.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pCFMMCTradingAccountKey.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///密钥编号
    l_dict["KeyID"]                     = pCFMMCTradingAccountKey.KeyID
    # ///动态密钥
    l_dict["CurrentKey"]                = pCFMMCTradingAccountKey.CurrentKey.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryEWarrantOffset(self, pEWarrantOffset, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询仓单折抵信息响应
    '''


    if bIsLast == True:
      self.req_call['QryEWarrantOffset'] = 1


    self.PTP_Algos.DumpRspDict("T_EWarrantOffset",pEWarrantOffset)

    l_dict={}

    """CThostFtdcEWarrantOffsetField

    # ///交易日期
    l_dict["TradingDay"]                = pEWarrantOffset.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pEWarrantOffset.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pEWarrantOffset.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pEWarrantOffset.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pEWarrantOffset.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pEWarrantOffset.Direction.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pEWarrantOffset.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pEWarrantOffset.Volume
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pEWarrantOffset.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryInvestorProductGroupMargin(self, pInvestorProductGroupMargin, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资者品种/跨品种保证金响应
    '''


    if bIsLast == True:
      self.req_call['QryInvestorProductGroupMargin'] = 1


    self.PTP_Algos.DumpRspDict("T_InvestorProductGroupMargin",pInvestorProductGroupMargin)

    l_dict={}

    """CThostFtdcInvestorProductGroupMarginField

    # ///品种/跨品种标示
    l_dict["ProductGroupID"]            = pInvestorProductGroupMargin.ProductGroupID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInvestorProductGroupMargin.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInvestorProductGroupMargin.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///交易日
    l_dict["TradingDay"]                = pInvestorProductGroupMargin.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pInvestorProductGroupMargin.SettlementID
    # ///冻结的保证金
    l_dict["FrozenMargin"]              = pInvestorProductGroupMargin.FrozenMargin
    # ///多头冻结的保证金
    l_dict["LongFrozenMargin"]          = pInvestorProductGroupMargin.LongFrozenMargin
    # ///空头冻结的保证金
    l_dict["ShortFrozenMargin"]         = pInvestorProductGroupMargin.ShortFrozenMargin
    # ///占用的保证金
    l_dict["UseMargin"]                 = pInvestorProductGroupMargin.UseMargin
    # ///多头保证金
    l_dict["LongUseMargin"]             = pInvestorProductGroupMargin.LongUseMargin
    # ///空头保证金
    l_dict["ShortUseMargin"]            = pInvestorProductGroupMargin.ShortUseMargin
    # ///交易所保证金
    l_dict["ExchMargin"]                = pInvestorProductGroupMargin.ExchMargin
    # ///交易所多头保证金
    l_dict["LongExchMargin"]            = pInvestorProductGroupMargin.LongExchMargin
    # ///交易所空头保证金
    l_dict["ShortExchMargin"]           = pInvestorProductGroupMargin.ShortExchMargin
    # ///平仓盈亏
    l_dict["CloseProfit"]               = pInvestorProductGroupMargin.CloseProfit
    # ///冻结的手续费
    l_dict["FrozenCommission"]          = pInvestorProductGroupMargin.FrozenCommission
    # ///手续费
    l_dict["Commission"]                = pInvestorProductGroupMargin.Commission
    # ///冻结的资金
    l_dict["FrozenCash"]                = pInvestorProductGroupMargin.FrozenCash
    # ///资金差额
    l_dict["CashIn"]                    = pInvestorProductGroupMargin.CashIn

    # ///持仓盈亏
    l_dict["PositionProfit"]            = pInvestorProductGroupMargin.PositionProfit
    # ///折抵总金额
    l_dict["OffsetAmount"]              = pInvestorProductGroupMargin.OffsetAmount
    # ///多头折抵总金额
    l_dict["LongOffsetAmount"]          = pInvestorProductGroupMargin.LongOffsetAmount
    # ///空头折抵总金额
    l_dict["ShortOffsetAmount"]         = pInvestorProductGroupMargin.ShortOffsetAmount
    # ///交易所折抵总金额
    l_dict["ExchOffsetAmount"]          = pInvestorProductGroupMargin.ExchOffsetAmount
    # ///交易所多头折抵总金额
    l_dict["LongExchOffsetAmount"]      = pInvestorProductGroupMargin.LongExchOffsetAmount
    # ///交易所空头折抵总金额
    l_dict["ShortExchOffsetAmount"]     = pInvestorProductGroupMargin.ShortExchOffsetAmount
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInvestorProductGroupMargin.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInvestorProductGroupMargin.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInvestorProductGroupMargin.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryExchangeMarginRate(self, pExchangeMarginRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询交易所保证金率响应
    '''


    if bIsLast == True:
      self.req_call['QryExchangeMarginRate'] = 1


    self.PTP_Algos.DumpRspDict("T_ExchangeMarginRate",pExchangeMarginRate)

    l_dict={}

    """CThostFtdcExchangeMarginRateField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pExchangeMarginRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pExchangeMarginRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pExchangeMarginRate.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///多头保证金率
    l_dict["LongMarginRatioByMoney"]    = pExchangeMarginRate.LongMarginRatioByMoney
    # ///多头保证金费
    l_dict["LongMarginRatioByVolume"]   = pExchangeMarginRate.LongMarginRatioByVolume
    # ///空头保证金率
    l_dict["ShortMarginRatioByMoney"]   = pExchangeMarginRate.ShortMarginRatioByMoney
    # ///空头保证金费
    l_dict["ShortMarginRatioByVolume"]  = pExchangeMarginRate.ShortMarginRatioByVolume
    # ///交易所代码
    l_dict["ExchangeID"]                = pExchangeMarginRate.ExchangeID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryExchangeMarginRateAdjust(self, pExchangeMarginRateAdjust, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询交易所调整保证金率响应
    '''


    if bIsLast == True:
      self.req_call['QryExchangeMarginRateAdjust'] = 1


    self.PTP_Algos.DumpRspDict("T_ExchangeMarginRateAdjust",pExchangeMarginRateAdjust)

    l_dict={}

    """CThostFtdcExchangeMarginRateAdjustField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pExchangeMarginRateAdjust.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pExchangeMarginRateAdjust.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pExchangeMarginRateAdjust.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///跟随交易所投资者多头保证金率
    l_dict["LongMarginRatioByMoney"]    = pExchangeMarginRateAdjust.LongMarginRatioByMoney
    # ///跟随交易所投资者多头保证金费
    l_dict["LongMarginRatioByVolume"]   = pExchangeMarginRateAdjust.LongMarginRatioByVolume
    # ///跟随交易所投资者空头保证金率
    l_dict["ShortMarginRatioByMoney"]   = pExchangeMarginRateAdjust.ShortMarginRatioByMoney
    # ///跟随交易所投资者空头保证金费
    l_dict["ShortMarginRatioByVolume"]  = pExchangeMarginRateAdjust.ShortMarginRatioByVolume
    # ///交易所多头保证金率
    l_dict["ExchLongMarginRatioByMoney" = pExchangeMarginRateAdjust.ExchLongMarginRatioByMoney
    # ///交易所多头保证金费
    l_dict["ExchLongMarginRatioByVolume = pExchangeMarginRateAdjust.ExchLongMarginRatioByVolume
    # ///交易所空头保证金率
    l_dict["ExchShortMarginRatioByMoney = pExchangeMarginRateAdjust.ExchShortMarginRatioByMoney
    # ///交易所空头保证金费
    l_dict["ExchShortMarginRatioByVolum = pExchangeMarginRateAdjust.ExchShortMarginRatioByVolume
    # ///不跟随交易所投资者多头保证金率
    l_dict["NoLongMarginRatioByMoney"]  = pExchangeMarginRateAdjust.NoLongMarginRatioByMoney
    # ///不跟随交易所投资者多头保证金费
    l_dict["NoLongMarginRatioByVolume"] = pExchangeMarginRateAdjust.NoLongMarginRatioByVolume
    # ///不跟随交易所投资者空头保证金率
    l_dict["NoShortMarginRatioByMoney"] = pExchangeMarginRateAdjust.NoShortMarginRatioByMoney
    # ///不跟随交易所投资者空头保证金费
    l_dict["NoShortMarginRatioByVolume" = pExchangeMarginRateAdjust.NoShortMarginRatioByVolume

    #"""

  def OnRspQryExchangeRate(self, pExchangeRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询汇率响应
    '''


    if bIsLast == True:
      self.req_call['QryExchangeRate'] = 1


    self.PTP_Algos.DumpRspDict("T_ExchangeRate",pExchangeRate)

    l_dict={}

    """CThostFtdcExchangeRateField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pExchangeRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///源币种
    l_dict["FromCurrencyID"]            = pExchangeRate.FromCurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///源币种单位数量
    l_dict["FromCurrencyUnit"]          = pExchangeRate.FromCurrencyUnit
    # ///目标币种
    l_dict["ToCurrencyID"]              = pExchangeRate.ToCurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///汇率
    l_dict["ExchangeRate"]              = pExchangeRate.ExchangeRate

    #"""

  def OnRspQrySecAgentACIDMap(self, pSecAgentACIDMap, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询二级代理操作员银期权限响应
    '''


    if bIsLast == True:
      self.req_call['QrySecAgentACIDMap'] = 1


    self.PTP_Algos.DumpRspDict("T_SecAgentACIDMap",pSecAgentACIDMap)

    l_dict={}

    """CThostFtdcSecAgentACIDMapField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pSecAgentACIDMap.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pSecAgentACIDMap.UserID.decode(encoding="gb18030", errors="ignore")
    # ///资金账户
    l_dict["AccountID"]                 = pSecAgentACIDMap.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种
    l_dict["CurrencyID"]                = pSecAgentACIDMap.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///境外中介机构资金帐号
    l_dict["BrokerSecAgentID"]          = pSecAgentACIDMap.BrokerSecAgentID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryProductExchRate(self, pProductExchRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询产品报价汇率
    '''


    if bIsLast == True:
      self.req_call['QryProductExchRate'] = 1


    self.PTP_Algos.DumpRspDict("T_ProductExchRate",pProductExchRate)

    l_dict={}

    """CThostFtdcProductExchRateField

    # ///产品代码
    l_dict["ProductID"]                 = pProductExchRate.ProductID.decode(encoding="gb18030", errors="ignore")
    # ///报价币种类型
    l_dict["QuoteCurrencyID"]           = pProductExchRate.QuoteCurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///汇率
    l_dict["ExchangeRate"]              = pProductExchRate.ExchangeRate
    # ///交易所代码
    l_dict["ExchangeID"]                = pProductExchRate.ExchangeID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryProductGroup(self, pProductGroup, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询产品组
    '''


    if bIsLast == True:
      self.req_call['QryProductGroup'] = 1


    self.PTP_Algos.DumpRspDict("T_ProductGroup",pProductGroup)

    l_dict={}

    """CThostFtdcProductGroupField

    # ///产品代码
    l_dict["ProductID"]                 = pProductGroup.ProductID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pProductGroup.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///产品组代码
    l_dict["ProductGroupID"]            = pProductGroup.ProductGroupID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryMMInstrumentCommissionRate(self, pMMInstrumentCommissionRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询做市商合约手续费率响应
    '''


    if bIsLast == True:
      self.req_call['QryMMInstrumentCommissionRate'] = 1


    self.PTP_Algos.DumpRspDict("T_MMInstrumentCommissionRate",pMMInstrumentCommissionRate)

    l_dict={}

    """CThostFtdcMMInstrumentCommissionRateField

    # ///合约代码
    l_dict["InstrumentID"]              = pMMInstrumentCommissionRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pMMInstrumentCommissionRate.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pMMInstrumentCommissionRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pMMInstrumentCommissionRate.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///开仓手续费率
    l_dict["OpenRatioByMoney"]          = pMMInstrumentCommissionRate.OpenRatioByMoney
    # ///开仓手续费
    l_dict["OpenRatioByVolume"]         = pMMInstrumentCommissionRate.OpenRatioByVolume
    # ///平仓手续费率
    l_dict["CloseRatioByMoney"]         = pMMInstrumentCommissionRate.CloseRatioByMoney
    # ///平仓手续费
    l_dict["CloseRatioByVolume"]        = pMMInstrumentCommissionRate.CloseRatioByVolume
    # ///平今手续费率
    l_dict["CloseTodayRatioByMoney"]    = pMMInstrumentCommissionRate.CloseTodayRatioByMoney
    # ///平今手续费
    l_dict["CloseTodayRatioByVolume"]   = pMMInstrumentCommissionRate.CloseTodayRatioByVolume

    #"""

  def OnRspQryMMOptionInstrCommRate(self, pMMOptionInstrCommRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询做市商期权合约手续费响应
    '''


    if bIsLast == True:
      self.req_call['QryMMOptionInstrCommRate'] = 1


    self.PTP_Algos.DumpRspDict("T_MMOptionInstrCommRate",pMMOptionInstrCommRate)

    l_dict={}

    """CThostFtdcMMOptionInstrCommRateField

    # ///合约代码
    l_dict["InstrumentID"]              = pMMOptionInstrCommRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pMMOptionInstrCommRate.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pMMOptionInstrCommRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pMMOptionInstrCommRate.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///开仓手续费率
    l_dict["OpenRatioByMoney"]          = pMMOptionInstrCommRate.OpenRatioByMoney
    # ///开仓手续费
    l_dict["OpenRatioByVolume"]         = pMMOptionInstrCommRate.OpenRatioByVolume
    # ///平仓手续费率
    l_dict["CloseRatioByMoney"]         = pMMOptionInstrCommRate.CloseRatioByMoney
    # ///平仓手续费
    l_dict["CloseRatioByVolume"]        = pMMOptionInstrCommRate.CloseRatioByVolume
    # ///平今手续费率
    l_dict["CloseTodayRatioByMoney"]    = pMMOptionInstrCommRate.CloseTodayRatioByMoney
    # ///平今手续费
    l_dict["CloseTodayRatioByVolume"]   = pMMOptionInstrCommRate.CloseTodayRatioByVolume
    # ///执行手续费率
    l_dict["StrikeRatioByMoney"]        = pMMOptionInstrCommRate.StrikeRatioByMoney
    # ///执行手续费
    l_dict["StrikeRatioByVolume"]       = pMMOptionInstrCommRate.StrikeRatioByVolume

    #"""

  def OnRspQryInstrumentOrderCommRate(self, pInstrumentOrderCommRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询报单手续费响应
    '''


    if bIsLast == True:
      self.req_call['QryInstrumentOrderCommRate'] = 1


    self.PTP_Algos.DumpRspDict("T_InstrumentOrderCommRate",pInstrumentOrderCommRate)

    l_dict={}

    """CThostFtdcInstrumentOrderCommRateField

    # ///合约代码
    l_dict["InstrumentID"]              = pInstrumentOrderCommRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pInstrumentOrderCommRate.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInstrumentOrderCommRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInstrumentOrderCommRate.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInstrumentOrderCommRate.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///报单手续费
    l_dict["OrderCommByVolume"]         = pInstrumentOrderCommRate.OrderCommByVolume
    # ///撤单手续费
    l_dict["OrderActionCommByVolume"]   = pInstrumentOrderCommRate.OrderActionCommByVolume
    # ///交易所代码
    l_dict["ExchangeID"]                = pInstrumentOrderCommRate.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInstrumentOrderCommRate.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQrySecAgentTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询资金账户响应
    '''


    if bIsLast == True:
      self.req_call['QrySecAgentTradingAccount'] = 1


    self.PTP_Algos.DumpRspDict("T_TradingAccount",pTradingAccount)

    l_dict={}

    """CThostFtdcTradingAccountField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTradingAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pTradingAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///上次质押金额
    l_dict["PreMortgage"]               = pTradingAccount.PreMortgage
    # ///上次信用额度
    l_dict["PreCredit"]                 = pTradingAccount.PreCredit
    # ///上次存款额
    l_dict["PreDeposit"]                = pTradingAccount.PreDeposit
    # ///上次结算准备金
    l_dict["PreBalance"]                = pTradingAccount.PreBalance
    # ///上次占用的保证金
    l_dict["PreMargin"]                 = pTradingAccount.PreMargin
    # ///利息基数
    l_dict["InterestBase"]              = pTradingAccount.InterestBase
    # ///利息收入
    l_dict["Interest"]                  = pTradingAccount.Interest
    # ///入金金额
    l_dict["Deposit"]                   = pTradingAccount.Deposit
    # ///出金金额
    l_dict["Withdraw"]                  = pTradingAccount.Withdraw
    # ///冻结的保证金
    l_dict["FrozenMargin"]              = pTradingAccount.FrozenMargin
    # ///冻结的资金
    l_dict["FrozenCash"]                = pTradingAccount.FrozenCash
    # ///冻结的手续费
    l_dict["FrozenCommission"]          = pTradingAccount.FrozenCommission
    # ///当前保证金总额
    l_dict["CurrMargin"]                = pTradingAccount.CurrMargin
    # ///资金差额
    l_dict["CashIn"]                    = pTradingAccount.CashIn
    # ///手续费
    l_dict["Commission"]                = pTradingAccount.Commission
    # ///平仓盈亏
    l_dict["CloseProfit"]               = pTradingAccount.CloseProfit
    # ///持仓盈亏
    l_dict["PositionProfit"]            = pTradingAccount.PositionProfit
    # ///期货结算准备金
    l_dict["Balance"]                   = pTradingAccount.Balance
    # ///可用资金
    l_dict["Available"]                 = pTradingAccount.Available
    # ///可取资金
    l_dict["WithdrawQuota"]             = pTradingAccount.WithdrawQuota
    # ///基本准备金
    l_dict["Reserve"]                   = pTradingAccount.Reserve

    # ///交易日
    l_dict["TradingDay"]                = pTradingAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pTradingAccount.SettlementID
    # ///信用额度
    l_dict["Credit"]                    = pTradingAccount.Credit
    # ///质押金额
    l_dict["Mortgage"]                  = pTradingAccount.Mortgage
    # ///交易所保证金
    l_dict["ExchangeMargin"]            = pTradingAccount.ExchangeMargin
    # ///投资者交割保证金
    l_dict["DeliveryMargin"]            = pTradingAccount.DeliveryMargin
    # ///交易所交割保证金
    l_dict["ExchangeDeliveryMargin"]    = pTradingAccount.ExchangeDeliveryMargin
    # ///保底期货结算准备金
    l_dict["ReserveBalance"]            = pTradingAccount.ReserveBalance
    # ///币种代码
    l_dict["CurrencyID"]                = pTradingAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///上次货币质入金额
    l_dict["PreFundMortgageIn"]         = pTradingAccount.PreFundMortgageIn
    # ///上次货币质出金额
    l_dict["PreFundMortgageOut"]        = pTradingAccount.PreFundMortgageOut
    # ///货币质入金额
    l_dict["FundMortgageIn"]            = pTradingAccount.FundMortgageIn
    # ///货币质出金额
    l_dict["FundMortgageOut"]           = pTradingAccount.FundMortgageOut
    # ///货币质押余额
    l_dict["FundMortgageAvailable"]     = pTradingAccount.FundMortgageAvailable
    # ///可质押货币金额
    l_dict["MortgageableFund"]          = pTradingAccount.MortgageableFund
    # ///特殊产品占用保证金
    l_dict["SpecProductMargin"]         = pTradingAccount.SpecProductMargin
    # ///特殊产品冻结保证金
    l_dict["SpecProductFrozenMargin"]   = pTradingAccount.SpecProductFrozenMargin
    # ///特殊产品手续费
    l_dict["SpecProductCommission"]     = pTradingAccount.SpecProductCommission
    # ///特殊产品冻结手续费
    l_dict["SpecProductFrozenCommission = pTradingAccount.SpecProductFrozenCommission
    # ///特殊产品持仓盈亏
    l_dict["SpecProductPositionProfit"] = pTradingAccount.SpecProductPositionProfit
    # ///特殊产品平仓盈亏
    l_dict["SpecProductCloseProfit"]    = pTradingAccount.SpecProductCloseProfit

    # ///根据持仓盈亏算法计算的特殊产品持仓盈亏
    l_dict["SpecProductPositionProfitBy = pTradingAccount.SpecProductPositionProfitByAlg
    # ///特殊产品交易所保证金
    l_dict["SpecProductExchangeMargin"] = pTradingAccount.SpecProductExchangeMargin
    # ///业务类型
    l_dict["BizType"]                   = pTradingAccount.BizType.decode(encoding="gb18030", errors="ignore")
    # ///延时换汇冻结金额
    l_dict["FrozenSwap"]                = pTradingAccount.FrozenSwap
    # ///剩余换汇额度
    l_dict["RemainSwap"]                = pTradingAccount.RemainSwap

    #"""

  def OnRspQrySecAgentCheckMode(self, pSecAgentCheckMode, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询二级代理商资金校验模式响应
    '''


    if bIsLast == True:
      self.req_call['QrySecAgentCheckMode'] = 1


    self.PTP_Algos.DumpRspDict("T_SecAgentCheckMode",pSecAgentCheckMode)

    l_dict={}

    """CThostFtdcSecAgentCheckModeField

    # ///投资者代码
    l_dict["InvestorID"]                = pSecAgentCheckMode.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pSecAgentCheckMode.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///币种
    l_dict["CurrencyID"]                = pSecAgentCheckMode.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///境外中介机构资金帐号
    l_dict["BrokerSecAgentID"]          = pSecAgentCheckMode.BrokerSecAgentID.decode(encoding="gb18030", errors="ignore")
    # ///是否需要校验自己的资金账户
    l_dict["CheckSelfAccount"]          = pSecAgentCheckMode.CheckSelfAccount

    #"""

  def OnRspQryOptionInstrTradeCost(self, pOptionInstrTradeCost, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询期权交易成本响应
    '''


    if bIsLast == True:
      self.req_call['QryOptionInstrTradeCost'] = 1


    self.PTP_Algos.DumpRspDict("T_OptionInstrTradeCost",pOptionInstrTradeCost)

    l_dict={}

    """CThostFtdcOptionInstrTradeCostField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOptionInstrTradeCost.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOptionInstrTradeCost.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOptionInstrTradeCost.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pOptionInstrTradeCost.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权合约保证金不变部分
    l_dict["FixedMargin"]               = pOptionInstrTradeCost.FixedMargin
    # ///期权合约最小保证金
    l_dict["MiniMargin"]                = pOptionInstrTradeCost.MiniMargin
    # ///期权合约权利金
    l_dict["Royalty"]                   = pOptionInstrTradeCost.Royalty
    # ///交易所期权合约保证金不变部分
    l_dict["ExchFixedMargin"]           = pOptionInstrTradeCost.ExchFixedMargin
    # ///交易所期权合约最小保证金
    l_dict["ExchMiniMargin"]            = pOptionInstrTradeCost.ExchMiniMargin
    # ///交易所代码
    l_dict["ExchangeID"]                = pOptionInstrTradeCost.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOptionInstrTradeCost.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryOptionInstrCommRate(self, pOptionInstrCommRate, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询期权合约手续费响应
    '''


    if bIsLast == True:
      self.req_call['QryOptionInstrCommRate'] = 1


    self.PTP_Algos.DumpRspDict("T_OptionInstrCommRate",pOptionInstrCommRate)

    l_dict={}

    """CThostFtdcOptionInstrCommRateField

    # ///合约代码
    l_dict["InstrumentID"]              = pOptionInstrCommRate.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pOptionInstrCommRate.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOptionInstrCommRate.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOptionInstrCommRate.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///开仓手续费率
    l_dict["OpenRatioByMoney"]          = pOptionInstrCommRate.OpenRatioByMoney
    # ///开仓手续费
    l_dict["OpenRatioByVolume"]         = pOptionInstrCommRate.OpenRatioByVolume
    # ///平仓手续费率
    l_dict["CloseRatioByMoney"]         = pOptionInstrCommRate.CloseRatioByMoney
    # ///平仓手续费
    l_dict["CloseRatioByVolume"]        = pOptionInstrCommRate.CloseRatioByVolume
    # ///平今手续费率
    l_dict["CloseTodayRatioByMoney"]    = pOptionInstrCommRate.CloseTodayRatioByMoney
    # ///平今手续费
    l_dict["CloseTodayRatioByVolume"]   = pOptionInstrCommRate.CloseTodayRatioByVolume
    # ///执行手续费率
    l_dict["StrikeRatioByMoney"]        = pOptionInstrCommRate.StrikeRatioByMoney
    # ///执行手续费
    l_dict["StrikeRatioByVolume"]       = pOptionInstrCommRate.StrikeRatioByVolume
    # ///交易所代码
    l_dict["ExchangeID"]                = pOptionInstrCommRate.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOptionInstrCommRate.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryExecOrder(self, pExecOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询执行宣告响应
    '''


    if bIsLast == True:
      self.req_call['QryExecOrder'] = 1


    self.PTP_Algos.DumpRspDict("T_ExecOrder",pExecOrder)

    l_dict={}

    """CThostFtdcExecOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pExecOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pExecOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pExecOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告引用
    l_dict["ExecOrderRef"]              = pExecOrder.ExecOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pExecOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pExecOrder.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pExecOrder.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pExecOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pExecOrder.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pExecOrder.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///执行类型
    l_dict["ActionType"]                = pExecOrder.ActionType.decode(encoding="gb18030", errors="ignore")
    # ///保留头寸申请的持仓方向
    l_dict["PosiDirection"]             = pExecOrder.PosiDirection.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后是否保留期货头寸的标记,该字段已废弃
    l_dict["ReservePositionFlag"]       = pExecOrder.ReservePositionFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后生成的头寸是否自动平仓
    l_dict["CloseFlag"]                 = pExecOrder.CloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地执行宣告编号
    l_dict["ExecOrderLocalID"]          = pExecOrder.ExecOrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pExecOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pExecOrder.ParticipantID.decode(encoding="gb18030", errors="ignore")

    # ///客户代码
    l_dict["ClientID"]                  = pExecOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pExecOrder.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pExecOrder.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pExecOrder.InstallID
    # ///执行宣告提交状态
    l_dict["OrderSubmitStatus"]         = pExecOrder.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pExecOrder.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pExecOrder.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pExecOrder.SettlementID
    # ///执行宣告编号
    l_dict["ExecOrderSysID"]            = pExecOrder.ExecOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单日期
    l_dict["InsertDate"]                = pExecOrder.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pExecOrder.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pExecOrder.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///执行结果
    l_dict["ExecResult"]                = pExecOrder.ExecResult.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pExecOrder.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pExecOrder.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pExecOrder.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pExecOrder.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pExecOrder.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pExecOrder.StatusMsg.decode(encoding="gb18030", errors="ignore")

    # ///操作用户代码
    l_dict["ActiveUserID"]              = pExecOrder.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerExecOrderSeq"]        = pExecOrder.BrokerExecOrderSeq
    # ///营业部编号
    l_dict["BranchID"]                  = pExecOrder.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pExecOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pExecOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pExecOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pExecOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pExecOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryForQuote(self, pForQuote, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询询价响应
    '''


    if bIsLast == True:
      self.req_call['QryForQuote'] = 1


    self.PTP_Algos.DumpRspDict("T_ForQuote",pForQuote)

    l_dict={}

    """CThostFtdcForQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pForQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pForQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pForQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///询价引用
    l_dict["ForQuoteRef"]               = pForQuote.ForQuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pForQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///本地询价编号
    l_dict["ForQuoteLocalID"]           = pForQuote.ForQuoteLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pForQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pForQuote.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pForQuote.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pForQuote.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pForQuote.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pForQuote.InstallID
    # ///报单日期
    l_dict["InsertDate"]                = pForQuote.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pForQuote.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///询价状态
    l_dict["ForQuoteStatus"]            = pForQuote.ForQuoteStatus.decode(encoding="gb18030", errors="ignore")
    # ///前置编号
    l_dict["FrontID"]                   = pForQuote.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pForQuote.SessionID
    # ///状态信息
    l_dict["StatusMsg"]                 = pForQuote.StatusMsg.decode(encoding="gb18030", errors="ignore")

    # ///操作用户代码
    l_dict["ActiveUserID"]              = pForQuote.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司询价编号
    l_dict["BrokerForQutoSeq"]          = pForQuote.BrokerForQutoSeq
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pForQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pForQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pForQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryQuote(self, pQuote, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询报价响应
    '''


    if bIsLast == True:
      self.req_call['QryQuote'] = 1


    self.PTP_Algos.DumpRspDict("T_Quote",pQuote)

    l_dict={}

    """CThostFtdcQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报价引用
    l_dict["QuoteRef"]                  = pQuote.QuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///卖价格
    l_dict["AskPrice"]                  = pQuote.AskPrice
    # ///买价格
    l_dict["BidPrice"]                  = pQuote.BidPrice
    # ///卖数量
    l_dict["AskVolume"]                 = pQuote.AskVolume
    # ///买数量
    l_dict["BidVolume"]                 = pQuote.BidVolume
    # ///请求编号
    l_dict["RequestID"]                 = pQuote.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pQuote.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///卖开平标志
    l_dict["AskOffsetFlag"]             = pQuote.AskOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///买开平标志
    l_dict["BidOffsetFlag"]             = pQuote.BidOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///卖投机套保标志
    l_dict["AskHedgeFlag"]              = pQuote.AskHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///买投机套保标志
    l_dict["BidHedgeFlag"]              = pQuote.BidHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地报价编号
    l_dict["QuoteLocalID"]              = pQuote.QuoteLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pQuote.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pQuote.ClientID.decode(encoding="gb18030", errors="ignore")

    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pQuote.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pQuote.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pQuote.InstallID
    # ///报价提示序号
    l_dict["NotifySequence"]            = pQuote.NotifySequence
    # ///报价提交状态
    l_dict["OrderSubmitStatus"]         = pQuote.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///交易日
    l_dict["TradingDay"]                = pQuote.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pQuote.SettlementID
    # ///报价编号
    l_dict["QuoteSysID"]                = pQuote.QuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单日期
    l_dict["InsertDate"]                = pQuote.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pQuote.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pQuote.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///报价状态
    l_dict["QuoteStatus"]               = pQuote.QuoteStatus.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pQuote.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pQuote.SequenceNo
    # ///卖方报单编号
    l_dict["AskOrderSysID"]             = pQuote.AskOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///买方报单编号
    l_dict["BidOrderSysID"]             = pQuote.BidOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///前置编号
    l_dict["FrontID"]                   = pQuote.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pQuote.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pQuote.UserProductInfo.decode(encoding="gb18030", errors="ignore")

    # ///状态信息
    l_dict["StatusMsg"]                 = pQuote.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pQuote.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报价编号
    l_dict["BrokerQuoteSeq"]            = pQuote.BrokerQuoteSeq
    # ///衍生卖报单引用
    l_dict["AskOrderRef"]               = pQuote.AskOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///衍生买报单引用
    l_dict["BidOrderRef"]               = pQuote.BidOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///应价编号
    l_dict["ForQuoteSysID"]             = pQuote.ForQuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pQuote.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pQuote.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pQuote.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryOptionSelfClose(self, pOptionSelfClose, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询期权自对冲响应
    '''


    if bIsLast == True:
      self.req_call['QryOptionSelfClose'] = 1


    self.PTP_Algos.DumpRspDict("T_OptionSelfClose",pOptionSelfClose)

    l_dict={}

    """CThostFtdcOptionSelfCloseField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOptionSelfClose.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOptionSelfClose.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOptionSelfClose.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲引用
    l_dict["OptionSelfCloseRef"]        = pOptionSelfClose.OptionSelfCloseRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pOptionSelfClose.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pOptionSelfClose.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pOptionSelfClose.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pOptionSelfClose.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pOptionSelfClose.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权的头寸是否自对冲
    l_dict["OptSelfCloseFlag"]          = pOptionSelfClose.OptSelfCloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地期权自对冲编号
    l_dict["OptionSelfCloseLocalID"]    = pOptionSelfClose.OptionSelfCloseLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pOptionSelfClose.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pOptionSelfClose.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pOptionSelfClose.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pOptionSelfClose.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pOptionSelfClose.TraderID.decode(encoding="gb18030", errors="ignore")

    # ///安装编号
    l_dict["InstallID"]                 = pOptionSelfClose.InstallID
    # ///期权自对冲提交状态
    l_dict["OrderSubmitStatus"]         = pOptionSelfClose.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pOptionSelfClose.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pOptionSelfClose.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pOptionSelfClose.SettlementID
    # ///期权自对冲编号
    l_dict["OptionSelfCloseSysID"]      = pOptionSelfClose.OptionSelfCloseSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单日期
    l_dict["InsertDate"]                = pOptionSelfClose.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pOptionSelfClose.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pOptionSelfClose.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///自对冲结果
    l_dict["ExecResult"]                = pOptionSelfClose.ExecResult.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pOptionSelfClose.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pOptionSelfClose.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pOptionSelfClose.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pOptionSelfClose.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pOptionSelfClose.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pOptionSelfClose.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pOptionSelfClose.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerOptionSelfCloseSeq"]  = pOptionSelfClose.BrokerOptionSelfCloseSeq

    # ///营业部编号
    l_dict["BranchID"]                  = pOptionSelfClose.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOptionSelfClose.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pOptionSelfClose.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pOptionSelfClose.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pOptionSelfClose.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pOptionSelfClose.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryInvestUnit(self, pInvestUnit, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询投资单元响应
    '''


    if bIsLast == True:
      self.req_call['QryInvestUnit'] = 1


    self.PTP_Algos.DumpRspDict("T_InvestUnit",pInvestUnit)

    l_dict={}

    """CThostFtdcInvestUnitField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInvestUnit.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInvestUnit.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInvestUnit.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///投资者单元名称
    l_dict["InvestorUnitName"]          = pInvestUnit.InvestorUnitName.decode(encoding="gb18030", errors="ignore")
    # ///投资者分组代码
    l_dict["InvestorGroupID"]           = pInvestUnit.InvestorGroupID.decode(encoding="gb18030", errors="ignore")
    # ///手续费率模板代码
    l_dict["CommModelID"]               = pInvestUnit.CommModelID.decode(encoding="gb18030", errors="ignore")
    # ///保证金率模板代码
    l_dict["MarginModelID"]             = pInvestUnit.MarginModelID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInvestUnit.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pInvestUnit.CurrencyID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryCombInstrumentGuard(self, pCombInstrumentGuard, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询组合合约安全系数响应
    '''


    if bIsLast == True:
      self.req_call['QryCombInstrumentGuard'] = 1


    self.PTP_Algos.DumpRspDict("T_CombInstrumentGuard",pCombInstrumentGuard)

    l_dict={}

    """CThostFtdcCombInstrumentGuardField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pCombInstrumentGuard.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pCombInstrumentGuard.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///
    l_dict["GuarantRatio"]              = pCombInstrumentGuard.GuarantRatio
    # ///交易所代码
    l_dict["ExchangeID"]                = pCombInstrumentGuard.ExchangeID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryCombAction(self, pCombAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询申请组合响应
    '''


    if bIsLast == True:
      self.req_call['QryCombAction'] = 1


    self.PTP_Algos.DumpRspDict("T_CombAction",pCombAction)

    l_dict={}

    """CThostFtdcCombActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pCombAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pCombAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pCombAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///组合引用
    l_dict["CombActionRef"]             = pCombAction.CombActionRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pCombAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pCombAction.Direction.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pCombAction.Volume
    # ///组合指令方向
    l_dict["CombDirection"]             = pCombAction.CombDirection.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pCombAction.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地申请组合编号
    l_dict["ActionLocalID"]             = pCombAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pCombAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pCombAction.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pCombAction.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pCombAction.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pCombAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pCombAction.InstallID
    # ///组合状态
    l_dict["ActionStatus"]              = pCombAction.ActionStatus.decode(encoding="gb18030", errors="ignore")

    # ///报单提示序号
    l_dict["NotifySequence"]            = pCombAction.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pCombAction.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pCombAction.SettlementID
    # ///序号
    l_dict["SequenceNo"]                = pCombAction.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pCombAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pCombAction.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pCombAction.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pCombAction.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pCombAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pCombAction.MacAddress.decode(encoding="gb18030", errors="ignore")
    # ///组合编号
    l_dict["ComTradeID"]                = pCombAction.ComTradeID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pCombAction.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pCombAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryTransferSerial(self, pTransferSerial, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询转帐流水响应
    '''


    if bIsLast == True:
      self.req_call['QryTransferSerial'] = 1


    self.PTP_Algos.DumpRspDict("T_TransferSerial",pTransferSerial)

    l_dict={}

    """CThostFtdcTransferSerialField

    # ///平台流水号
    l_dict["PlateSerial"]               = pTransferSerial.PlateSerial
    # ///交易发起方日期
    l_dict["TradeDate"]                 = pTransferSerial.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradingDay"]                = pTransferSerial.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pTransferSerial.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///交易代码
    l_dict["TradeCode"]                 = pTransferSerial.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///会话编号
    l_dict["SessionID"]                 = pTransferSerial.SessionID
    # ///银行编码
    l_dict["BankID"]                    = pTransferSerial.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构编码
    l_dict["BankBranchID"]              = pTransferSerial.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pTransferSerial.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pTransferSerial.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pTransferSerial.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///期货公司编码
    l_dict["BrokerID"]                  = pTransferSerial.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pTransferSerial.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期货公司帐号类型
    l_dict["FutureAccType"]             = pTransferSerial.FutureAccType.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pTransferSerial.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pTransferSerial.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pTransferSerial.FutureSerial

    # ///证件类型
    l_dict["IdCardType"]                = pTransferSerial.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pTransferSerial.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pTransferSerial.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易金额
    l_dict["TradeAmount"]               = pTransferSerial.TradeAmount
    # ///应收客户费用
    l_dict["CustFee"]                   = pTransferSerial.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pTransferSerial.BrokerFee
    # ///有效标志
    l_dict["AvailabilityFlag"]          = pTransferSerial.AvailabilityFlag.decode(encoding="gb18030", errors="ignore")
    # ///操作员
    l_dict["OperatorCode"]              = pTransferSerial.OperatorCode.decode(encoding="gb18030", errors="ignore")
    # ///新银行帐号
    l_dict["BankNewAccount"]            = pTransferSerial.BankNewAccount.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pTransferSerial.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pTransferSerial.ErrorMsg.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryAccountregister(self, pAccountregister, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询银期签约关系响应
    '''


    if bIsLast == True:
      self.req_call['QryAccountregister'] = 1


    self.PTP_Algos.DumpRspDict("T_Accountregister",pAccountregister)

    l_dict={}

    """CThostFtdcAccountregisterField

    # ///交易日期
    l_dict["TradeDay"]                  = pAccountregister.TradeDay.decode(encoding="gb18030", errors="ignore")
    # ///银行编码
    l_dict["BankID"]                    = pAccountregister.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构编码
    l_dict["BankBranchID"]              = pAccountregister.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pAccountregister.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///期货公司编码
    l_dict["BrokerID"]                  = pAccountregister.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期货公司分支机构编码
    l_dict["BrokerBranchID"]            = pAccountregister.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pAccountregister.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pAccountregister.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pAccountregister.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户姓名
    l_dict["CustomerName"]              = pAccountregister.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pAccountregister.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///开销户类别
    l_dict["OpenOrDestroy"]             = pAccountregister.OpenOrDestroy.decode(encoding="gb18030", errors="ignore")
    # ///签约日期
    l_dict["RegDate"]                   = pAccountregister.RegDate.decode(encoding="gb18030", errors="ignore")
    # ///解约日期
    l_dict["OutDate"]                   = pAccountregister.OutDate.decode(encoding="gb18030", errors="ignore")
    # ///交易ID
    l_dict["TID"]                       = pAccountregister.TID
    # ///客户类型
    l_dict["CustType"]                  = pAccountregister.CustType.decode(encoding="gb18030", errors="ignore")

    # ///银行帐号类型
    l_dict["BankAccType"]               = pAccountregister.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pAccountregister.LongCustomerName.decode(encoding="gb18030", errors="ignore")

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

  def OnRtnOrder(self, pOrder):
    '''
    ///报单通知
    '''


    self.PTP_Algos.push_OnRtnOrder("T_Order",pOrder)

    l_dict={}

    """CThostFtdcOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")
    # ///止损价
    l_dict["StopPrice"]                 = pOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")
    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pOrder.IsAutoSuspend

    # ///业务单元
    l_dict["BusinessUnit"]              = pOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pOrder.RequestID
    # ///本地报单编号
    l_dict["OrderLocalID"]              = pOrder.OrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pOrder.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pOrder.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pOrder.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pOrder.InstallID
    # ///报单提交状态
    l_dict["OrderSubmitStatus"]         = pOrder.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pOrder.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pOrder.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pOrder.SettlementID
    # ///报单编号
    l_dict["OrderSysID"]                = pOrder.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单来源
    l_dict["OrderSource"]               = pOrder.OrderSource.decode(encoding="gb18030", errors="ignore")
    # ///报单状态
    l_dict["OrderStatus"]               = pOrder.OrderStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单类型
    l_dict["OrderType"]                 = pOrder.OrderType.decode(encoding="gb18030", errors="ignore")
    # ///今成交数量
    l_dict["VolumeTraded"]              = pOrder.VolumeTraded
    # ///剩余数量
    l_dict["VolumeTotal"]               = pOrder.VolumeTotal

    # ///报单日期
    l_dict["InsertDate"]                = pOrder.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///委托时间
    l_dict["InsertTime"]                = pOrder.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///激活时间
    l_dict["ActiveTime"]                = pOrder.ActiveTime.decode(encoding="gb18030", errors="ignore")
    # ///挂起时间
    l_dict["SuspendTime"]               = pOrder.SuspendTime.decode(encoding="gb18030", errors="ignore")
    # ///最后修改时间
    l_dict["UpdateTime"]                = pOrder.UpdateTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pOrder.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///最后修改交易所交易员代码
    l_dict["ActiveTraderID"]            = pOrder.ActiveTraderID.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pOrder.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pOrder.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pOrder.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pOrder.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pOrder.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pOrder.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///用户强评标志
    l_dict["UserForceClose"]            = pOrder.UserForceClose
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pOrder.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerOrderSeq"]            = pOrder.BrokerOrderSeq
    # ///相关报单
    l_dict["RelativeOrderSysID"]        = pOrder.RelativeOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///郑商所成交数量
    l_dict["ZCETotalTradedVolume"]      = pOrder.ZCETotalTradedVolume
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pOrder.IsSwapOrder
    # ///营业部编号
    l_dict["BranchID"]                  = pOrder.BranchID.decode(encoding="gb18030", errors="ignore")

    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnTrade(self, pTrade):
    '''
    ///成交通知
    '''


    self.PTP_Algos.DumpRspDict("T_Trade",pTrade)

    l_dict={}

    """CThostFtdcTradeField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTrade.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pTrade.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pTrade.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pTrade.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pTrade.UserID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pTrade.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///成交编号
    l_dict["TradeID"]                   = pTrade.TradeID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pTrade.Direction.decode(encoding="gb18030", errors="ignore")
    # ///报单编号
    l_dict["OrderSysID"]                = pTrade.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pTrade.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pTrade.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///交易角色
    l_dict["TradingRole"]               = pTrade.TradingRole.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pTrade.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pTrade.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pTrade.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["Price"]                     = pTrade.Price
    # ///数量
    l_dict["Volume"]                    = pTrade.Volume
    # ///成交时期
    l_dict["TradeDate"]                 = pTrade.TradeDate.decode(encoding="gb18030", errors="ignore")

    # ///成交时间
    l_dict["TradeTime"]                 = pTrade.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///成交类型
    l_dict["TradeType"]                 = pTrade.TradeType.decode(encoding="gb18030", errors="ignore")
    # ///成交价来源
    l_dict["PriceSource"]               = pTrade.PriceSource.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pTrade.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///本地报单编号
    l_dict["OrderLocalID"]              = pTrade.OrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pTrade.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///业务单元
    l_dict["BusinessUnit"]              = pTrade.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pTrade.SequenceNo
    # ///交易日
    l_dict["TradingDay"]                = pTrade.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pTrade.SettlementID
    # ///经纪公司报单编号
    l_dict["BrokerOrderSeq"]            = pTrade.BrokerOrderSeq
    # ///成交来源
    l_dict["TradeSource"]               = pTrade.TradeSource.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pTrade.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
    '''
    ///报单录入错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_InputOrder",pInputOrder)

    l_dict={}

    """CThostFtdcInputOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pInputOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pInputOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pInputOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pInputOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pInputOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pInputOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pInputOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pInputOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pInputOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pInputOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pInputOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pInputOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")
    # ///止损价
    l_dict["StopPrice"]                 = pInputOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pInputOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")

    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pInputOrder.IsAutoSuspend
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pInputOrder.RequestID
    # ///用户强评标志
    l_dict["UserForceClose"]            = pInputOrder.UserForceClose
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pInputOrder.IsSwapOrder
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInputOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pInputOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
    '''
    ///报单操作错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_OrderAction",pOrderAction)

    l_dict={}

    """CThostFtdcOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报单操作引用
    l_dict["OrderActionRef"]            = pOrderAction.OrderActionRef
    # ///报单引用
    l_dict["OrderRef"]                  = pOrderAction.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///报单编号
    l_dict["OrderSysID"]                = pOrderAction.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pOrderAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pOrderAction.LimitPrice
    # ///数量变化
    l_dict["VolumeChange"]              = pOrderAction.VolumeChange
    # ///操作日期
    l_dict["ActionDate"]                = pOrderAction.ActionDate.decode(encoding="gb18030", errors="ignore")
    # ///操作时间
    l_dict["ActionTime"]                = pOrderAction.ActionTime.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pOrderAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pOrderAction.InstallID
    # ///本地报单编号
    l_dict["OrderLocalID"]              = pOrderAction.OrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///操作本地编号
    l_dict["ActionLocalID"]             = pOrderAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pOrderAction.ParticipantID.decode(encoding="gb18030", errors="ignore")

    # ///客户代码
    l_dict["ClientID"]                  = pOrderAction.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///业务单元
    l_dict["BusinessUnit"]              = pOrderAction.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///报单操作状态
    l_dict["OrderActionStatus"]         = pOrderAction.OrderActionStatus.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pOrderAction.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOrderAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pOrderAction.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnInstrumentStatus(self, pInstrumentStatus):
    '''
    ///合约交易状态通知
    '''


    self.PTP_Algos.push_OnRtnInstrumentStatus("T_InstrumentStatus",pInstrumentStatus)

    l_dict={}

    """CThostFtdcInstrumentStatusField

    # ///交易所代码
    l_dict["ExchangeID"]                = pInstrumentStatus.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pInstrumentStatus.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///结算组代码
    l_dict["SettlementGroupID"]         = pInstrumentStatus.SettlementGroupID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInstrumentStatus.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///合约交易状态
    l_dict["InstrumentStatus"]          = pInstrumentStatus.InstrumentStatus.decode(encoding="gb18030", errors="ignore")
    # ///交易阶段编号
    l_dict["TradingSegmentSN"]          = pInstrumentStatus.TradingSegmentSN
    # ///进入本状态时间
    l_dict["EnterTime"]                 = pInstrumentStatus.EnterTime.decode(encoding="gb18030", errors="ignore")
    # ///进入本状态原因
    l_dict["EnterReason"]               = pInstrumentStatus.EnterReason.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnBulletin(self, pBulletin):
    '''
    ///交易所公告通知
    '''


    self.PTP_Algos.DumpRspDict("T_Bulletin",pBulletin)

    l_dict={}

    """CThostFtdcBulletinField

    # ///交易所代码
    l_dict["ExchangeID"]                = pBulletin.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///交易日
    l_dict["TradingDay"]                = pBulletin.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///公告编号
    l_dict["BulletinID"]                = pBulletin.BulletinID
    # ///序列号
    l_dict["SequenceNo"]                = pBulletin.SequenceNo
    # ///公告类型
    l_dict["NewsType"]                  = pBulletin.NewsType.decode(encoding="gb18030", errors="ignore")
    # ///紧急程度
    l_dict["NewsUrgency"]               = pBulletin.NewsUrgency.decode(encoding="gb18030", errors="ignore")
    # ///发送时间
    l_dict["SendTime"]                  = pBulletin.SendTime.decode(encoding="gb18030", errors="ignore")
    # ///消息摘要
    l_dict["Abstract"]                  = pBulletin.Abstract.decode(encoding="gb18030", errors="ignore")
    # ///消息来源
    l_dict["ComeFrom"]                  = pBulletin.ComeFrom.decode(encoding="gb18030", errors="ignore")
    # ///消息正文
    l_dict["Content"]                   = pBulletin.Content.decode(encoding="gb18030", errors="ignore")
    # ///WEB地址
    l_dict["URLLink"]                   = pBulletin.URLLink.decode(encoding="gb18030", errors="ignore")
    # ///市场代码
    l_dict["MarketID"]                  = pBulletin.MarketID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnTradingNotice(self, pTradingNoticeInfo):
    '''
    ///交易通知
    '''


    self.PTP_Algos.DumpRspDict("T_TradingNoticeInfo",pTradingNoticeInfo)

    l_dict={}

    """CThostFtdcTradingNoticeInfoField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTradingNoticeInfo.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pTradingNoticeInfo.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///发送时间
    l_dict["SendTime"]                  = pTradingNoticeInfo.SendTime.decode(encoding="gb18030", errors="ignore")
    # ///消息正文
    l_dict["FieldContent"]              = pTradingNoticeInfo.FieldContent.decode(encoding="gb18030", errors="ignore")
    # ///序列系列号
    l_dict["SequenceSeries"]            = pTradingNoticeInfo.SequenceSeries
    # ///序列号
    l_dict["SequenceNo"]                = pTradingNoticeInfo.SequenceNo
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pTradingNoticeInfo.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnErrorConditionalOrder(self, pErrorConditionalOrder):
    '''
    ///提示条件单校验错误
    '''


    self.PTP_Algos.DumpRspDict("T_ErrorConditionalOrder",pErrorConditionalOrder)

    l_dict={}

    """CThostFtdcErrorConditionalOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pErrorConditionalOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pErrorConditionalOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pErrorConditionalOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pErrorConditionalOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pErrorConditionalOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pErrorConditionalOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pErrorConditionalOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pErrorConditionalOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pErrorConditionalOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pErrorConditionalOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pErrorConditionalOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pErrorConditionalOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pErrorConditionalOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pErrorConditionalOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pErrorConditionalOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pErrorConditionalOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")

    # ///止损价
    l_dict["StopPrice"]                 = pErrorConditionalOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pErrorConditionalOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")
    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pErrorConditionalOrder.IsAutoSuspend
    # ///业务单元
    l_dict["BusinessUnit"]              = pErrorConditionalOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pErrorConditionalOrder.RequestID
    # ///本地报单编号
    l_dict["OrderLocalID"]              = pErrorConditionalOrder.OrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pErrorConditionalOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pErrorConditionalOrder.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pErrorConditionalOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pErrorConditionalOrder.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pErrorConditionalOrder.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pErrorConditionalOrder.InstallID
    # ///报单提交状态
    l_dict["OrderSubmitStatus"]         = pErrorConditionalOrder.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pErrorConditionalOrder.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pErrorConditionalOrder.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pErrorConditionalOrder.SettlementID
    # ///报单编号
    l_dict["OrderSysID"]                = pErrorConditionalOrder.OrderSysID.decode(encoding="gb18030", errors="ignore")

    # ///报单来源
    l_dict["OrderSource"]               = pErrorConditionalOrder.OrderSource.decode(encoding="gb18030", errors="ignore")
    # ///报单状态
    l_dict["OrderStatus"]               = pErrorConditionalOrder.OrderStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单类型
    l_dict["OrderType"]                 = pErrorConditionalOrder.OrderType.decode(encoding="gb18030", errors="ignore")
    # ///今成交数量
    l_dict["VolumeTraded"]              = pErrorConditionalOrder.VolumeTraded
    # ///剩余数量
    l_dict["VolumeTotal"]               = pErrorConditionalOrder.VolumeTotal
    # ///报单日期
    l_dict["InsertDate"]                = pErrorConditionalOrder.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///委托时间
    l_dict["InsertTime"]                = pErrorConditionalOrder.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///激活时间
    l_dict["ActiveTime"]                = pErrorConditionalOrder.ActiveTime.decode(encoding="gb18030", errors="ignore")
    # ///挂起时间
    l_dict["SuspendTime"]               = pErrorConditionalOrder.SuspendTime.decode(encoding="gb18030", errors="ignore")
    # ///最后修改时间
    l_dict["UpdateTime"]                = pErrorConditionalOrder.UpdateTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pErrorConditionalOrder.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///最后修改交易所交易员代码
    l_dict["ActiveTraderID"]            = pErrorConditionalOrder.ActiveTraderID.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pErrorConditionalOrder.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pErrorConditionalOrder.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pErrorConditionalOrder.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pErrorConditionalOrder.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pErrorConditionalOrder.UserProductInfo.decode(encoding="gb18030", errors="ignore")

    # ///状态信息
    l_dict["StatusMsg"]                 = pErrorConditionalOrder.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///用户强评标志
    l_dict["UserForceClose"]            = pErrorConditionalOrder.UserForceClose
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pErrorConditionalOrder.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerOrderSeq"]            = pErrorConditionalOrder.BrokerOrderSeq
    # ///相关报单
    l_dict["RelativeOrderSysID"]        = pErrorConditionalOrder.RelativeOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///郑商所成交数量
    l_dict["ZCETotalTradedVolume"]      = pErrorConditionalOrder.ZCETotalTradedVolume
    # ///错误代码
    l_dict["ErrorID"]                   = pErrorConditionalOrder.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pErrorConditionalOrder.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pErrorConditionalOrder.IsSwapOrder
    # ///营业部编号
    l_dict["BranchID"]                  = pErrorConditionalOrder.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pErrorConditionalOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pErrorConditionalOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pErrorConditionalOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pErrorConditionalOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pErrorConditionalOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnExecOrder(self, pExecOrder):
    '''
    ///执行宣告通知
    '''


    self.PTP_Algos.DumpRspDict("T_ExecOrder",pExecOrder)

    l_dict={}

    """CThostFtdcExecOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pExecOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pExecOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pExecOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告引用
    l_dict["ExecOrderRef"]              = pExecOrder.ExecOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pExecOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pExecOrder.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pExecOrder.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pExecOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pExecOrder.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pExecOrder.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///执行类型
    l_dict["ActionType"]                = pExecOrder.ActionType.decode(encoding="gb18030", errors="ignore")
    # ///保留头寸申请的持仓方向
    l_dict["PosiDirection"]             = pExecOrder.PosiDirection.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后是否保留期货头寸的标记,该字段已废弃
    l_dict["ReservePositionFlag"]       = pExecOrder.ReservePositionFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后生成的头寸是否自动平仓
    l_dict["CloseFlag"]                 = pExecOrder.CloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地执行宣告编号
    l_dict["ExecOrderLocalID"]          = pExecOrder.ExecOrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pExecOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pExecOrder.ParticipantID.decode(encoding="gb18030", errors="ignore")

    # ///客户代码
    l_dict["ClientID"]                  = pExecOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pExecOrder.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pExecOrder.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pExecOrder.InstallID
    # ///执行宣告提交状态
    l_dict["OrderSubmitStatus"]         = pExecOrder.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pExecOrder.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pExecOrder.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pExecOrder.SettlementID
    # ///执行宣告编号
    l_dict["ExecOrderSysID"]            = pExecOrder.ExecOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单日期
    l_dict["InsertDate"]                = pExecOrder.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pExecOrder.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pExecOrder.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///执行结果
    l_dict["ExecResult"]                = pExecOrder.ExecResult.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pExecOrder.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pExecOrder.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pExecOrder.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pExecOrder.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pExecOrder.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pExecOrder.StatusMsg.decode(encoding="gb18030", errors="ignore")

    # ///操作用户代码
    l_dict["ActiveUserID"]              = pExecOrder.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerExecOrderSeq"]        = pExecOrder.BrokerExecOrderSeq
    # ///营业部编号
    l_dict["BranchID"]                  = pExecOrder.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pExecOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pExecOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pExecOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pExecOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pExecOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnExecOrderInsert(self, pInputExecOrder, pRspInfo):
    '''
    ///执行宣告录入错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_InputExecOrder",pInputExecOrder)

    l_dict={}

    """CThostFtdcInputExecOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputExecOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputExecOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputExecOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告引用
    l_dict["ExecOrderRef"]              = pInputExecOrder.ExecOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputExecOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInputExecOrder.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pInputExecOrder.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputExecOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///开平标志
    l_dict["OffsetFlag"]                = pInputExecOrder.OffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInputExecOrder.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///执行类型
    l_dict["ActionType"]                = pInputExecOrder.ActionType.decode(encoding="gb18030", errors="ignore")
    # ///保留头寸申请的持仓方向
    l_dict["PosiDirection"]             = pInputExecOrder.PosiDirection.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后是否保留期货头寸的标记,该字段已废弃
    l_dict["ReservePositionFlag"]       = pInputExecOrder.ReservePositionFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权后生成的头寸是否自动平仓
    l_dict["CloseFlag"]                 = pInputExecOrder.CloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputExecOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputExecOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInputExecOrder.AccountID.decode(encoding="gb18030", errors="ignore")

    # ///币种代码
    l_dict["CurrencyID"]                = pInputExecOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputExecOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputExecOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputExecOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnExecOrderAction(self, pExecOrderAction, pRspInfo):
    '''
    ///执行宣告操作错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_ExecOrderAction",pExecOrderAction)

    l_dict={}

    """CThostFtdcExecOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pExecOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pExecOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告操作引用
    l_dict["ExecOrderActionRef"]        = pExecOrderAction.ExecOrderActionRef
    # ///执行宣告引用
    l_dict["ExecOrderRef"]              = pExecOrderAction.ExecOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pExecOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pExecOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pExecOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pExecOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///执行宣告操作编号
    l_dict["ExecOrderSysID"]            = pExecOrderAction.ExecOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pExecOrderAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///操作日期
    l_dict["ActionDate"]                = pExecOrderAction.ActionDate.decode(encoding="gb18030", errors="ignore")
    # ///操作时间
    l_dict["ActionTime"]                = pExecOrderAction.ActionTime.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pExecOrderAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pExecOrderAction.InstallID
    # ///本地执行宣告编号
    l_dict["ExecOrderLocalID"]          = pExecOrderAction.ExecOrderLocalID.decode(encoding="gb18030", errors="ignore")
    # ///操作本地编号
    l_dict["ActionLocalID"]             = pExecOrderAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pExecOrderAction.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pExecOrderAction.ClientID.decode(encoding="gb18030", errors="ignore")

    # ///业务单元
    l_dict["BusinessUnit"]              = pExecOrderAction.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///报单操作状态
    l_dict["OrderActionStatus"]         = pExecOrderAction.OrderActionStatus.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pExecOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///执行类型
    l_dict["ActionType"]                = pExecOrderAction.ActionType.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pExecOrderAction.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pExecOrderAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pExecOrderAction.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pExecOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pExecOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pExecOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnForQuoteInsert(self, pInputForQuote, pRspInfo):
    '''
    ///询价录入错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_InputForQuote",pInputForQuote)

    l_dict={}

    """CThostFtdcInputForQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputForQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputForQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputForQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///询价引用
    l_dict["ForQuoteRef"]               = pInputForQuote.ForQuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputForQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputForQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputForQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputForQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputForQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnQuote(self, pQuote):
    '''
    ///报价通知
    '''


    self.PTP_Algos.DumpRspDict("T_Quote",pQuote)

    l_dict={}

    """CThostFtdcQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报价引用
    l_dict["QuoteRef"]                  = pQuote.QuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///卖价格
    l_dict["AskPrice"]                  = pQuote.AskPrice
    # ///买价格
    l_dict["BidPrice"]                  = pQuote.BidPrice
    # ///卖数量
    l_dict["AskVolume"]                 = pQuote.AskVolume
    # ///买数量
    l_dict["BidVolume"]                 = pQuote.BidVolume
    # ///请求编号
    l_dict["RequestID"]                 = pQuote.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pQuote.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///卖开平标志
    l_dict["AskOffsetFlag"]             = pQuote.AskOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///买开平标志
    l_dict["BidOffsetFlag"]             = pQuote.BidOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///卖投机套保标志
    l_dict["AskHedgeFlag"]              = pQuote.AskHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///买投机套保标志
    l_dict["BidHedgeFlag"]              = pQuote.BidHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地报价编号
    l_dict["QuoteLocalID"]              = pQuote.QuoteLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pQuote.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pQuote.ClientID.decode(encoding="gb18030", errors="ignore")

    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pQuote.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pQuote.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pQuote.InstallID
    # ///报价提示序号
    l_dict["NotifySequence"]            = pQuote.NotifySequence
    # ///报价提交状态
    l_dict["OrderSubmitStatus"]         = pQuote.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///交易日
    l_dict["TradingDay"]                = pQuote.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pQuote.SettlementID
    # ///报价编号
    l_dict["QuoteSysID"]                = pQuote.QuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单日期
    l_dict["InsertDate"]                = pQuote.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pQuote.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pQuote.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///报价状态
    l_dict["QuoteStatus"]               = pQuote.QuoteStatus.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pQuote.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pQuote.SequenceNo
    # ///卖方报单编号
    l_dict["AskOrderSysID"]             = pQuote.AskOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///买方报单编号
    l_dict["BidOrderSysID"]             = pQuote.BidOrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///前置编号
    l_dict["FrontID"]                   = pQuote.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pQuote.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pQuote.UserProductInfo.decode(encoding="gb18030", errors="ignore")

    # ///状态信息
    l_dict["StatusMsg"]                 = pQuote.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pQuote.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报价编号
    l_dict["BrokerQuoteSeq"]            = pQuote.BrokerQuoteSeq
    # ///衍生卖报单引用
    l_dict["AskOrderRef"]               = pQuote.AskOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///衍生买报单引用
    l_dict["BidOrderRef"]               = pQuote.BidOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///应价编号
    l_dict["ForQuoteSysID"]             = pQuote.ForQuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pQuote.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pQuote.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pQuote.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnQuoteInsert(self, pInputQuote, pRspInfo):
    '''
    ///报价录入错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_InputQuote",pInputQuote)

    l_dict={}

    """CThostFtdcInputQuoteField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputQuote.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputQuote.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputQuote.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报价引用
    l_dict["QuoteRef"]                  = pInputQuote.QuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputQuote.UserID.decode(encoding="gb18030", errors="ignore")
    # ///卖价格
    l_dict["AskPrice"]                  = pInputQuote.AskPrice
    # ///买价格
    l_dict["BidPrice"]                  = pInputQuote.BidPrice
    # ///卖数量
    l_dict["AskVolume"]                 = pInputQuote.AskVolume
    # ///买数量
    l_dict["BidVolume"]                 = pInputQuote.BidVolume
    # ///请求编号
    l_dict["RequestID"]                 = pInputQuote.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputQuote.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///卖开平标志
    l_dict["AskOffsetFlag"]             = pInputQuote.AskOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///买开平标志
    l_dict["BidOffsetFlag"]             = pInputQuote.BidOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///卖投机套保标志
    l_dict["AskHedgeFlag"]              = pInputQuote.AskHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///买投机套保标志
    l_dict["BidHedgeFlag"]              = pInputQuote.BidHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///衍生卖报单引用
    l_dict["AskOrderRef"]               = pInputQuote.AskOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///衍生买报单引用
    l_dict["BidOrderRef"]               = pInputQuote.BidOrderRef.decode(encoding="gb18030", errors="ignore")
    # ///应价编号
    l_dict["ForQuoteSysID"]             = pInputQuote.ForQuoteSysID.decode(encoding="gb18030", errors="ignore")

    # ///交易所代码
    l_dict["ExchangeID"]                = pInputQuote.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputQuote.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputQuote.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputQuote.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputQuote.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnQuoteAction(self, pQuoteAction, pRspInfo):
    '''
    ///报价操作错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_QuoteAction",pQuoteAction)

    l_dict={}

    """CThostFtdcQuoteActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pQuoteAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pQuoteAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报价操作引用
    l_dict["QuoteActionRef"]            = pQuoteAction.QuoteActionRef
    # ///报价引用
    l_dict["QuoteRef"]                  = pQuoteAction.QuoteRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pQuoteAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pQuoteAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pQuoteAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pQuoteAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///报价操作编号
    l_dict["QuoteSysID"]                = pQuoteAction.QuoteSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pQuoteAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///操作日期
    l_dict["ActionDate"]                = pQuoteAction.ActionDate.decode(encoding="gb18030", errors="ignore")
    # ///操作时间
    l_dict["ActionTime"]                = pQuoteAction.ActionTime.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pQuoteAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pQuoteAction.InstallID
    # ///本地报价编号
    l_dict["QuoteLocalID"]              = pQuoteAction.QuoteLocalID.decode(encoding="gb18030", errors="ignore")
    # ///操作本地编号
    l_dict["ActionLocalID"]             = pQuoteAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pQuoteAction.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pQuoteAction.ClientID.decode(encoding="gb18030", errors="ignore")

    # ///业务单元
    l_dict["BusinessUnit"]              = pQuoteAction.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///报单操作状态
    l_dict["OrderActionStatus"]         = pQuoteAction.OrderActionStatus.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pQuoteAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pQuoteAction.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pQuoteAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pQuoteAction.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pQuoteAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pQuoteAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pQuoteAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

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

  def OnRtnCFMMCTradingAccountToken(self, pCFMMCTradingAccountToken):
    '''
    ///保证金监控中心用户令牌
    '''


    self.PTP_Algos.DumpRspDict("T_CFMMCTradingAccountToken",pCFMMCTradingAccountToken)

    l_dict={}

    """CThostFtdcCFMMCTradingAccountTokenField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pCFMMCTradingAccountToken.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司统一编码
    l_dict["ParticipantID"]             = pCFMMCTradingAccountToken.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pCFMMCTradingAccountToken.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///密钥编号
    l_dict["KeyID"]                     = pCFMMCTradingAccountToken.KeyID
    # ///动态令牌
    l_dict["Token"]                     = pCFMMCTradingAccountToken.Token.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnBatchOrderAction(self, pBatchOrderAction, pRspInfo):
    '''
    ///批量报单操作错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_BatchOrderAction",pBatchOrderAction)

    l_dict={}

    """CThostFtdcBatchOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pBatchOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pBatchOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报单操作引用
    l_dict["OrderActionRef"]            = pBatchOrderAction.OrderActionRef
    # ///请求编号
    l_dict["RequestID"]                 = pBatchOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pBatchOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pBatchOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pBatchOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///操作日期
    l_dict["ActionDate"]                = pBatchOrderAction.ActionDate.decode(encoding="gb18030", errors="ignore")
    # ///操作时间
    l_dict["ActionTime"]                = pBatchOrderAction.ActionTime.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pBatchOrderAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pBatchOrderAction.InstallID
    # ///操作本地编号
    l_dict["ActionLocalID"]             = pBatchOrderAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pBatchOrderAction.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pBatchOrderAction.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///业务单元
    l_dict["BusinessUnit"]              = pBatchOrderAction.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///报单操作状态
    l_dict["OrderActionStatus"]         = pBatchOrderAction.OrderActionStatus.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pBatchOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pBatchOrderAction.StatusMsg.decode(encoding="gb18030", errors="ignore")

    # ///投资单元代码
    l_dict["InvestUnitID"]              = pBatchOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pBatchOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pBatchOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnOptionSelfClose(self, pOptionSelfClose):
    '''
    ///期权自对冲通知
    '''


    self.PTP_Algos.DumpRspDict("T_OptionSelfClose",pOptionSelfClose)

    l_dict={}

    """CThostFtdcOptionSelfCloseField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOptionSelfClose.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOptionSelfClose.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOptionSelfClose.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲引用
    l_dict["OptionSelfCloseRef"]        = pOptionSelfClose.OptionSelfCloseRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pOptionSelfClose.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pOptionSelfClose.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pOptionSelfClose.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pOptionSelfClose.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pOptionSelfClose.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权的头寸是否自对冲
    l_dict["OptSelfCloseFlag"]          = pOptionSelfClose.OptSelfCloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地期权自对冲编号
    l_dict["OptionSelfCloseLocalID"]    = pOptionSelfClose.OptionSelfCloseLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pOptionSelfClose.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pOptionSelfClose.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pOptionSelfClose.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pOptionSelfClose.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pOptionSelfClose.TraderID.decode(encoding="gb18030", errors="ignore")

    # ///安装编号
    l_dict["InstallID"]                 = pOptionSelfClose.InstallID
    # ///期权自对冲提交状态
    l_dict["OrderSubmitStatus"]         = pOptionSelfClose.OrderSubmitStatus.decode(encoding="gb18030", errors="ignore")
    # ///报单提示序号
    l_dict["NotifySequence"]            = pOptionSelfClose.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pOptionSelfClose.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pOptionSelfClose.SettlementID
    # ///期权自对冲编号
    l_dict["OptionSelfCloseSysID"]      = pOptionSelfClose.OptionSelfCloseSysID.decode(encoding="gb18030", errors="ignore")
    # ///报单日期
    l_dict["InsertDate"]                = pOptionSelfClose.InsertDate.decode(encoding="gb18030", errors="ignore")
    # ///插入时间
    l_dict["InsertTime"]                = pOptionSelfClose.InsertTime.decode(encoding="gb18030", errors="ignore")
    # ///撤销时间
    l_dict["CancelTime"]                = pOptionSelfClose.CancelTime.decode(encoding="gb18030", errors="ignore")
    # ///自对冲结果
    l_dict["ExecResult"]                = pOptionSelfClose.ExecResult.decode(encoding="gb18030", errors="ignore")
    # ///结算会员编号
    l_dict["ClearingPartID"]            = pOptionSelfClose.ClearingPartID.decode(encoding="gb18030", errors="ignore")
    # ///序号
    l_dict["SequenceNo"]                = pOptionSelfClose.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pOptionSelfClose.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pOptionSelfClose.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pOptionSelfClose.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pOptionSelfClose.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///操作用户代码
    l_dict["ActiveUserID"]              = pOptionSelfClose.ActiveUserID.decode(encoding="gb18030", errors="ignore")
    # ///经纪公司报单编号
    l_dict["BrokerOptionSelfCloseSeq"]  = pOptionSelfClose.BrokerOptionSelfCloseSeq

    # ///营业部编号
    l_dict["BranchID"]                  = pOptionSelfClose.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOptionSelfClose.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pOptionSelfClose.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pOptionSelfClose.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pOptionSelfClose.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pOptionSelfClose.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnOptionSelfCloseInsert(self, pInputOptionSelfClose, pRspInfo):
    '''
    ///期权自对冲录入错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_InputOptionSelfClose",pInputOptionSelfClose)

    l_dict={}

    """CThostFtdcInputOptionSelfCloseField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputOptionSelfClose.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputOptionSelfClose.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputOptionSelfClose.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲引用
    l_dict["OptionSelfCloseRef"]        = pInputOptionSelfClose.OptionSelfCloseRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputOptionSelfClose.UserID.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInputOptionSelfClose.Volume
    # ///请求编号
    l_dict["RequestID"]                 = pInputOptionSelfClose.RequestID
    # ///业务单元
    l_dict["BusinessUnit"]              = pInputOptionSelfClose.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInputOptionSelfClose.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///期权行权的头寸是否自对冲
    l_dict["OptSelfCloseFlag"]          = pInputOptionSelfClose.OptSelfCloseFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputOptionSelfClose.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputOptionSelfClose.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///资金账号
    l_dict["AccountID"]                 = pInputOptionSelfClose.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pInputOptionSelfClose.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pInputOptionSelfClose.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputOptionSelfClose.IPAddress.decode(encoding="gb18030", errors="ignore")

    # ///Mac地址
    l_dict["MacAddress"]                = pInputOptionSelfClose.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnOptionSelfCloseAction(self, pOptionSelfCloseAction, pRspInfo):
    '''
    ///期权自对冲操作错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_OptionSelfCloseAction",pOptionSelfCloseAction)

    l_dict={}

    """CThostFtdcOptionSelfCloseActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pOptionSelfCloseAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pOptionSelfCloseAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲操作引用
    l_dict["OptionSelfCloseActionRef"]  = pOptionSelfCloseAction.OptionSelfCloseActionRef
    # ///期权自对冲引用
    l_dict["OptionSelfCloseRef"]        = pOptionSelfCloseAction.OptionSelfCloseRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pOptionSelfCloseAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pOptionSelfCloseAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pOptionSelfCloseAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pOptionSelfCloseAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///期权自对冲操作编号
    l_dict["OptionSelfCloseSysID"]      = pOptionSelfCloseAction.OptionSelfCloseSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pOptionSelfCloseAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///操作日期
    l_dict["ActionDate"]                = pOptionSelfCloseAction.ActionDate.decode(encoding="gb18030", errors="ignore")
    # ///操作时间
    l_dict["ActionTime"]                = pOptionSelfCloseAction.ActionTime.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pOptionSelfCloseAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pOptionSelfCloseAction.InstallID
    # ///本地期权自对冲编号
    l_dict["OptionSelfCloseLocalID"]    = pOptionSelfCloseAction.OptionSelfCloseLocalID.decode(encoding="gb18030", errors="ignore")
    # ///操作本地编号
    l_dict["ActionLocalID"]             = pOptionSelfCloseAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pOptionSelfCloseAction.ParticipantID.decode(encoding="gb18030", errors="ignore")

    # ///客户代码
    l_dict["ClientID"]                  = pOptionSelfCloseAction.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///业务单元
    l_dict["BusinessUnit"]              = pOptionSelfCloseAction.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///报单操作状态
    l_dict["OrderActionStatus"]         = pOptionSelfCloseAction.OrderActionStatus.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pOptionSelfCloseAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pOptionSelfCloseAction.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pOptionSelfCloseAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pOptionSelfCloseAction.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pOptionSelfCloseAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pOptionSelfCloseAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pOptionSelfCloseAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnCombAction(self, pCombAction):
    '''
    ///申请组合通知
    '''


    self.PTP_Algos.DumpRspDict("T_CombAction",pCombAction)

    l_dict={}

    """CThostFtdcCombActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pCombAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pCombAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pCombAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///组合引用
    l_dict["CombActionRef"]             = pCombAction.CombActionRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pCombAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pCombAction.Direction.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pCombAction.Volume
    # ///组合指令方向
    l_dict["CombDirection"]             = pCombAction.CombDirection.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pCombAction.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///本地申请组合编号
    l_dict["ActionLocalID"]             = pCombAction.ActionLocalID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pCombAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///会员代码
    l_dict["ParticipantID"]             = pCombAction.ParticipantID.decode(encoding="gb18030", errors="ignore")
    # ///客户代码
    l_dict["ClientID"]                  = pCombAction.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///合约在交易所的代码
    l_dict["ExchangeInstID"]            = pCombAction.ExchangeInstID.decode(encoding="gb18030", errors="ignore")
    # ///交易所交易员代码
    l_dict["TraderID"]                  = pCombAction.TraderID.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pCombAction.InstallID
    # ///组合状态
    l_dict["ActionStatus"]              = pCombAction.ActionStatus.decode(encoding="gb18030", errors="ignore")

    # ///报单提示序号
    l_dict["NotifySequence"]            = pCombAction.NotifySequence
    # ///交易日
    l_dict["TradingDay"]                = pCombAction.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///结算编号
    l_dict["SettlementID"]              = pCombAction.SettlementID
    # ///序号
    l_dict["SequenceNo"]                = pCombAction.SequenceNo
    # ///前置编号
    l_dict["FrontID"]                   = pCombAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pCombAction.SessionID
    # ///用户端产品信息
    l_dict["UserProductInfo"]           = pCombAction.UserProductInfo.decode(encoding="gb18030", errors="ignore")
    # ///状态信息
    l_dict["StatusMsg"]                 = pCombAction.StatusMsg.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pCombAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pCombAction.MacAddress.decode(encoding="gb18030", errors="ignore")
    # ///组合编号
    l_dict["ComTradeID"]                = pCombAction.ComTradeID.decode(encoding="gb18030", errors="ignore")
    # ///营业部编号
    l_dict["BranchID"]                  = pCombAction.BranchID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pCombAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnCombActionInsert(self, pInputCombAction, pRspInfo):
    '''
    ///申请组合录入错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_InputCombAction",pInputCombAction)

    l_dict={}

    """CThostFtdcInputCombActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pInputCombAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pInputCombAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pInputCombAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///组合引用
    l_dict["CombActionRef"]             = pInputCombAction.CombActionRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pInputCombAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pInputCombAction.Direction.decode(encoding="gb18030", errors="ignore")
    # ///数量
    l_dict["Volume"]                    = pInputCombAction.Volume
    # ///组合指令方向
    l_dict["CombDirection"]             = pInputCombAction.CombDirection.decode(encoding="gb18030", errors="ignore")
    # ///投机套保标志
    l_dict["HedgeFlag"]                 = pInputCombAction.HedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pInputCombAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pInputCombAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pInputCombAction.MacAddress.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pInputCombAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryContractBank(self, pContractBank, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询签约银行响应
    '''


    if bIsLast == True:
      self.req_call['QryContractBank'] = 1


    self.PTP_Algos.DumpRspDict("T_ContractBank",pContractBank)

    l_dict={}

    """CThostFtdcContractBankField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pContractBank.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pContractBank.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分中心代码
    l_dict["BankBrchID"]                = pContractBank.BankBrchID.decode(encoding="gb18030", errors="ignore")
    # ///银行名称
    l_dict["BankName"]                  = pContractBank.BankName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryParkedOrder(self, pParkedOrder, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询预埋单响应
    '''


    if bIsLast == True:
      self.req_call['QryParkedOrder'] = 1


    self.PTP_Algos.DumpRspDict("T_ParkedOrder",pParkedOrder)

    l_dict={}

    """CThostFtdcParkedOrderField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pParkedOrder.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pParkedOrder.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pParkedOrder.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///报单引用
    l_dict["OrderRef"]                  = pParkedOrder.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///用户代码
    l_dict["UserID"]                    = pParkedOrder.UserID.decode(encoding="gb18030", errors="ignore")
    # ///报单价格条件
    l_dict["OrderPriceType"]            = pParkedOrder.OrderPriceType.decode(encoding="gb18030", errors="ignore")
    # ///买卖方向
    l_dict["Direction"]                 = pParkedOrder.Direction.decode(encoding="gb18030", errors="ignore")
    # ///组合开平标志
    l_dict["CombOffsetFlag"]            = pParkedOrder.CombOffsetFlag.decode(encoding="gb18030", errors="ignore")
    # ///组合投机套保标志
    l_dict["CombHedgeFlag"]             = pParkedOrder.CombHedgeFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pParkedOrder.LimitPrice
    # ///数量
    l_dict["VolumeTotalOriginal"]       = pParkedOrder.VolumeTotalOriginal
    # ///有效期类型
    l_dict["TimeCondition"]             = pParkedOrder.TimeCondition.decode(encoding="gb18030", errors="ignore")
    # ///GTD日期
    l_dict["GTDDate"]                   = pParkedOrder.GTDDate.decode(encoding="gb18030", errors="ignore")
    # ///成交量类型
    l_dict["VolumeCondition"]           = pParkedOrder.VolumeCondition.decode(encoding="gb18030", errors="ignore")
    # ///最小成交量
    l_dict["MinVolume"]                 = pParkedOrder.MinVolume
    # ///触发条件
    l_dict["ContingentCondition"]       = pParkedOrder.ContingentCondition.decode(encoding="gb18030", errors="ignore")
    # ///止损价
    l_dict["StopPrice"]                 = pParkedOrder.StopPrice
    # ///强平原因
    l_dict["ForceCloseReason"]          = pParkedOrder.ForceCloseReason.decode(encoding="gb18030", errors="ignore")

    # ///自动挂起标志
    l_dict["IsAutoSuspend"]             = pParkedOrder.IsAutoSuspend
    # ///业务单元
    l_dict["BusinessUnit"]              = pParkedOrder.BusinessUnit.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pParkedOrder.RequestID
    # ///用户强评标志
    l_dict["UserForceClose"]            = pParkedOrder.UserForceClose
    # ///交易所代码
    l_dict["ExchangeID"]                = pParkedOrder.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///预埋报单编号
    l_dict["ParkedOrderID"]             = pParkedOrder.ParkedOrderID.decode(encoding="gb18030", errors="ignore")
    # ///用户类型
    l_dict["UserType"]                  = pParkedOrder.UserType.decode(encoding="gb18030", errors="ignore")
    # ///预埋单状态
    l_dict["Status"]                    = pParkedOrder.Status.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pParkedOrder.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pParkedOrder.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///互换单标志
    l_dict["IsSwapOrder"]               = pParkedOrder.IsSwapOrder
    # ///资金账号
    l_dict["AccountID"]                 = pParkedOrder.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pParkedOrder.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///交易编码
    l_dict["ClientID"]                  = pParkedOrder.ClientID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pParkedOrder.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pParkedOrder.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pParkedOrder.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryParkedOrderAction(self, pParkedOrderAction, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询预埋撤单响应
    '''


    if bIsLast == True:
      self.req_call['QryParkedOrderAction'] = 1


    self.PTP_Algos.DumpRspDict("T_ParkedOrderAction",pParkedOrderAction)

    l_dict={}

    """CThostFtdcParkedOrderActionField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pParkedOrderAction.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pParkedOrderAction.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///报单操作引用
    l_dict["OrderActionRef"]            = pParkedOrderAction.OrderActionRef
    # ///报单引用
    l_dict["OrderRef"]                  = pParkedOrderAction.OrderRef.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pParkedOrderAction.RequestID
    # ///前置编号
    l_dict["FrontID"]                   = pParkedOrderAction.FrontID
    # ///会话编号
    l_dict["SessionID"]                 = pParkedOrderAction.SessionID
    # ///交易所代码
    l_dict["ExchangeID"]                = pParkedOrderAction.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///报单编号
    l_dict["OrderSysID"]                = pParkedOrderAction.OrderSysID.decode(encoding="gb18030", errors="ignore")
    # ///操作标志
    l_dict["ActionFlag"]                = pParkedOrderAction.ActionFlag.decode(encoding="gb18030", errors="ignore")
    # ///价格
    l_dict["LimitPrice"]                = pParkedOrderAction.LimitPrice
    # ///数量变化
    l_dict["VolumeChange"]              = pParkedOrderAction.VolumeChange
    # ///用户代码
    l_dict["UserID"]                    = pParkedOrderAction.UserID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pParkedOrderAction.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///预埋撤单单编号
    l_dict["ParkedOrderActionID"]       = pParkedOrderAction.ParkedOrderActionID.decode(encoding="gb18030", errors="ignore")
    # ///用户类型
    l_dict["UserType"]                  = pParkedOrderAction.UserType.decode(encoding="gb18030", errors="ignore")
    # ///预埋撤单状态
    l_dict["Status"]                    = pParkedOrderAction.Status.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pParkedOrderAction.ErrorID

    # ///错误信息
    l_dict["ErrorMsg"]                  = pParkedOrderAction.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pParkedOrderAction.InvestUnitID.decode(encoding="gb18030", errors="ignore")
    # ///IP地址
    l_dict["IPAddress"]                 = pParkedOrderAction.IPAddress.decode(encoding="gb18030", errors="ignore")
    # ///Mac地址
    l_dict["MacAddress"]                = pParkedOrderAction.MacAddress.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryTradingNotice(self, pTradingNotice, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询交易通知响应
    '''


    if bIsLast == True:
      self.req_call['QryTradingNotice'] = 1


    self.PTP_Algos.DumpRspDict("T_TradingNotice",pTradingNotice)

    l_dict={}

    """CThostFtdcTradingNoticeField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pTradingNotice.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者范围
    l_dict["InvestorRange"]             = pTradingNotice.InvestorRange.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pTradingNotice.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///序列系列号
    l_dict["SequenceSeries"]            = pTradingNotice.SequenceSeries
    # ///用户代码
    l_dict["UserID"]                    = pTradingNotice.UserID.decode(encoding="gb18030", errors="ignore")
    # ///发送时间
    l_dict["SendTime"]                  = pTradingNotice.SendTime.decode(encoding="gb18030", errors="ignore")
    # ///序列号
    l_dict["SequenceNo"]                = pTradingNotice.SequenceNo
    # ///消息正文
    l_dict["FieldContent"]              = pTradingNotice.FieldContent.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pTradingNotice.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryBrokerTradingParams(self, pBrokerTradingParams, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询经纪公司交易参数响应
    '''


    if bIsLast == True:
      self.req_call['QryBrokerTradingParams'] = 1


    self.PTP_Algos.DumpRspDict("T_BrokerTradingParams",pBrokerTradingParams)

    l_dict={}

    """CThostFtdcBrokerTradingParamsField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pBrokerTradingParams.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pBrokerTradingParams.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///保证金价格类型
    l_dict["MarginPriceType"]           = pBrokerTradingParams.MarginPriceType.decode(encoding="gb18030", errors="ignore")
    # ///盈亏算法
    l_dict["Algorithm"]                 = pBrokerTradingParams.Algorithm.decode(encoding="gb18030", errors="ignore")
    # ///可用是否包含平仓盈利
    l_dict["AvailIncludeCloseProfit"]   = pBrokerTradingParams.AvailIncludeCloseProfit.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pBrokerTradingParams.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///期权权利金价格类型
    l_dict["OptionRoyaltyPriceType"]    = pBrokerTradingParams.OptionRoyaltyPriceType.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pBrokerTradingParams.AccountID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQryBrokerTradingAlgos(self, pBrokerTradingAlgos, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询经纪公司交易算法响应
    '''


    if bIsLast == True:
      self.req_call['QryBrokerTradingAlgos'] = 1


    self.PTP_Algos.DumpRspDict("T_BrokerTradingAlgos",pBrokerTradingAlgos)

    l_dict={}

    """CThostFtdcBrokerTradingAlgosField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pBrokerTradingAlgos.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///交易所代码
    l_dict["ExchangeID"]                = pBrokerTradingAlgos.ExchangeID.decode(encoding="gb18030", errors="ignore")
    # ///合约代码
    l_dict["InstrumentID"]              = pBrokerTradingAlgos.InstrumentID.decode(encoding="gb18030", errors="ignore")
    # ///持仓处理算法编号
    l_dict["HandlePositionAlgoID"]      = pBrokerTradingAlgos.HandlePositionAlgoID.decode(encoding="gb18030", errors="ignore")
    # ///寻找保证金率算法编号
    l_dict["FindMarginRateAlgoID"]      = pBrokerTradingAlgos.FindMarginRateAlgoID.decode(encoding="gb18030", errors="ignore")
    # ///资金处理算法编号
    l_dict["HandleTradingAccountAlgoID" = pBrokerTradingAlgos.HandleTradingAccountAlgoID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQueryCFMMCTradingAccountToken(self, pQueryCFMMCTradingAccountToken, pRspInfo, nRequestID, bIsLast):
    '''
    ///请求查询监控中心用户令牌
    '''


    if bIsLast == True:
      self.req_call['QueryCFMMCTradingAccountToken'] = 1


    self.PTP_Algos.DumpRspDict("T_QueryCFMMCTradingAccountToken",pQueryCFMMCTradingAccountToken)

    l_dict={}

    """CThostFtdcQueryCFMMCTradingAccountTokenField

    # ///经纪公司代码
    l_dict["BrokerID"]                  = pQueryCFMMCTradingAccountToken.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///投资者代码
    l_dict["InvestorID"]                = pQueryCFMMCTradingAccountToken.InvestorID.decode(encoding="gb18030", errors="ignore")
    # ///投资单元代码
    l_dict["InvestUnitID"]              = pQueryCFMMCTradingAccountToken.InvestUnitID.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnFromBankToFutureByBank(self, pRspTransfer):
    '''
    ///银行发起银行资金转期货通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspTransfer",pRspTransfer)

    l_dict={}

    """CThostFtdcRspTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pRspTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pRspTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pRspTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspTransfer.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspTransfer.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnFromFutureToBankByBank(self, pRspTransfer):
    '''
    ///银行发起期货资金转银行通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspTransfer",pRspTransfer)

    l_dict={}

    """CThostFtdcRspTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pRspTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pRspTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pRspTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspTransfer.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspTransfer.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnRepealFromBankToFutureByBank(self, pRspRepeal):
    '''
    ///银行发起冲正银行转期货通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspRepeal",pRspRepeal)

    l_dict={}

    """CThostFtdcRspRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pRspRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pRspRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pRspRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pRspRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pRspRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pRspRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pRspRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pRspRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pRspRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pRspRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspRepeal.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspRepeal.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnRepealFromFutureToBankByBank(self, pRspRepeal):
    '''
    ///银行发起冲正期货转银行通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspRepeal",pRspRepeal)

    l_dict={}

    """CThostFtdcRspRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pRspRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pRspRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pRspRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pRspRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pRspRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pRspRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pRspRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pRspRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pRspRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pRspRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspRepeal.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspRepeal.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnFromBankToFutureByFuture(self, pRspTransfer):
    '''
    ///期货发起银行资金转期货通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspTransfer",pRspTransfer)

    l_dict={}

    """CThostFtdcRspTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pRspTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pRspTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pRspTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspTransfer.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspTransfer.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnFromFutureToBankByFuture(self, pRspTransfer):
    '''
    ///期货发起期货资金转银行通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspTransfer",pRspTransfer)

    l_dict={}

    """CThostFtdcRspTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pRspTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pRspTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pRspTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspTransfer.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspTransfer.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnRepealFromBankToFutureByFutureManual(self, pRspRepeal):
    '''
    ///系统运行时期货端手工发起冲正银行转期货请求，银行处理完毕后报盘发回的通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspRepeal",pRspRepeal)

    l_dict={}

    """CThostFtdcRspRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pRspRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pRspRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pRspRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pRspRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pRspRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pRspRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pRspRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pRspRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pRspRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pRspRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspRepeal.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspRepeal.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnRepealFromFutureToBankByFutureManual(self, pRspRepeal):
    '''
    ///系统运行时期货端手工发起冲正期货转银行请求，银行处理完毕后报盘发回的通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspRepeal",pRspRepeal)

    l_dict={}

    """CThostFtdcRspRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pRspRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pRspRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pRspRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pRspRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pRspRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pRspRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pRspRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pRspRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pRspRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pRspRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspRepeal.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspRepeal.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnQueryBankBalanceByFuture(self, pNotifyQueryAccount):
    '''
    ///期货发起查询银行余额通知
    '''


    self.PTP_Algos.DumpRspDict("T_NotifyQueryAccount",pNotifyQueryAccount)

    l_dict={}

    """CThostFtdcNotifyQueryAccountField

    # ///业务功能码
    l_dict["TradeCode"]                 = pNotifyQueryAccount.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pNotifyQueryAccount.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pNotifyQueryAccount.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pNotifyQueryAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pNotifyQueryAccount.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pNotifyQueryAccount.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pNotifyQueryAccount.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pNotifyQueryAccount.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pNotifyQueryAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pNotifyQueryAccount.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pNotifyQueryAccount.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pNotifyQueryAccount.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pNotifyQueryAccount.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pNotifyQueryAccount.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pNotifyQueryAccount.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pNotifyQueryAccount.CustType.decode(encoding="gb18030", errors="ignore")

    # ///银行帐号
    l_dict["BankAccount"]               = pNotifyQueryAccount.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pNotifyQueryAccount.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pNotifyQueryAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pNotifyQueryAccount.Password.decode(encoding="gb18030", errors="ignore")
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pNotifyQueryAccount.FutureSerial
    # ///安装编号
    l_dict["InstallID"]                 = pNotifyQueryAccount.InstallID
    # ///用户标识
    l_dict["UserID"]                    = pNotifyQueryAccount.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pNotifyQueryAccount.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pNotifyQueryAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pNotifyQueryAccount.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pNotifyQueryAccount.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pNotifyQueryAccount.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pNotifyQueryAccount.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pNotifyQueryAccount.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pNotifyQueryAccount.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pNotifyQueryAccount.BankPwdFlag.decode(encoding="gb18030", errors="ignore")

    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pNotifyQueryAccount.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pNotifyQueryAccount.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pNotifyQueryAccount.RequestID
    # ///交易ID
    l_dict["TID"]                       = pNotifyQueryAccount.TID
    # ///银行可用金额
    l_dict["BankUseAmount"]             = pNotifyQueryAccount.BankUseAmount
    # ///银行可取金额
    l_dict["BankFetchAmount"]           = pNotifyQueryAccount.BankFetchAmount
    # ///错误代码
    l_dict["ErrorID"]                   = pNotifyQueryAccount.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pNotifyQueryAccount.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pNotifyQueryAccount.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnBankToFutureByFuture(self, pReqTransfer, pRspInfo):
    '''
    ///期货发起银行资金转期货错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_ReqTransfer",pReqTransfer)

    l_dict={}

    """CThostFtdcReqTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pReqTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pReqTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pReqTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pReqTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pReqTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pReqTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pReqTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pReqTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pReqTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pReqTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pReqTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pReqTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pReqTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnFutureToBankByFuture(self, pReqTransfer, pRspInfo):
    '''
    ///期货发起期货资金转银行错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_ReqTransfer",pReqTransfer)

    l_dict={}

    """CThostFtdcReqTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pReqTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pReqTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pReqTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pReqTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pReqTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pReqTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pReqTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pReqTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pReqTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pReqTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pReqTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pReqTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pReqTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnRepealBankToFutureByFutureManual(self, pReqRepeal, pRspInfo):
    '''
    ///系统运行时期货端手工发起冲正银行转期货错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_ReqRepeal",pReqRepeal)

    l_dict={}

    """CThostFtdcReqRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pReqRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pReqRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pReqRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pReqRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pReqRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pReqRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pReqRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pReqRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pReqRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pReqRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pReqRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pReqRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pReqRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pReqRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pReqRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pReqRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pReqRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pReqRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pReqRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pReqRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnRepealFutureToBankByFutureManual(self, pReqRepeal, pRspInfo):
    '''
    ///系统运行时期货端手工发起冲正期货转银行错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_ReqRepeal",pReqRepeal)

    l_dict={}

    """CThostFtdcReqRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pReqRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pReqRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pReqRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pReqRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pReqRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pReqRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pReqRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pReqRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pReqRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pReqRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pReqRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pReqRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pReqRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pReqRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pReqRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pReqRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pReqRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pReqRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pReqRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pReqRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnErrRtnQueryBankBalanceByFuture(self, pReqQueryAccount, pRspInfo):
    '''
    ///期货发起查询银行余额错误回报
    '''


    self.PTP_Algos.DumpRspDict("T_ReqQueryAccount",pReqQueryAccount)

    l_dict={}

    """CThostFtdcReqQueryAccountField

    # ///业务功能码
    l_dict["TradeCode"]                 = pReqQueryAccount.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqQueryAccount.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqQueryAccount.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqQueryAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqQueryAccount.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqQueryAccount.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqQueryAccount.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqQueryAccount.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqQueryAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqQueryAccount.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqQueryAccount.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pReqQueryAccount.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqQueryAccount.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqQueryAccount.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqQueryAccount.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqQueryAccount.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqQueryAccount.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pReqQueryAccount.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqQueryAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqQueryAccount.Password.decode(encoding="gb18030", errors="ignore")
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqQueryAccount.FutureSerial
    # ///安装编号
    l_dict["InstallID"]                 = pReqQueryAccount.InstallID
    # ///用户标识
    l_dict["UserID"]                    = pReqQueryAccount.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqQueryAccount.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqQueryAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqQueryAccount.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqQueryAccount.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqQueryAccount.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqQueryAccount.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqQueryAccount.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqQueryAccount.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqQueryAccount.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqQueryAccount.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqQueryAccount.OperNo.decode(encoding="gb18030", errors="ignore")

    # ///请求编号
    l_dict["RequestID"]                 = pReqQueryAccount.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqQueryAccount.TID
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqQueryAccount.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnRepealFromBankToFutureByFuture(self, pRspRepeal):
    '''
    ///期货发起冲正银行转期货请求，银行处理完毕后报盘发回的通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspRepeal",pRspRepeal)

    l_dict={}

    """CThostFtdcRspRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pRspRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pRspRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pRspRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pRspRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pRspRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pRspRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pRspRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pRspRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pRspRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pRspRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspRepeal.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspRepeal.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnRepealFromFutureToBankByFuture(self, pRspRepeal):
    '''
    ///期货发起冲正期货转银行请求，银行处理完毕后报盘发回的通知
    '''


    self.PTP_Algos.DumpRspDict("T_RspRepeal",pRspRepeal)

    l_dict={}

    """CThostFtdcRspRepealField

    # ///冲正时间间隔
    l_dict["RepealTimeInterval"]        = pRspRepeal.RepealTimeInterval
    # ///已经冲正次数
    l_dict["RepealedTimes"]             = pRspRepeal.RepealedTimes
    # ///银行冲正标志
    l_dict["BankRepealFlag"]            = pRspRepeal.BankRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///期商冲正标志
    l_dict["BrokerRepealFlag"]          = pRspRepeal.BrokerRepealFlag.decode(encoding="gb18030", errors="ignore")
    # ///被冲正平台流水号
    l_dict["PlateRepealSerial"]         = pRspRepeal.PlateRepealSerial
    # ///被冲正银行流水号
    l_dict["BankRepealSerial"]          = pRspRepeal.BankRepealSerial.decode(encoding="gb18030", errors="ignore")
    # ///被冲正期货流水号
    l_dict["FutureRepealSerial"]        = pRspRepeal.FutureRepealSerial
    # ///业务功能码
    l_dict["TradeCode"]                 = pRspRepeal.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pRspRepeal.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pRspRepeal.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pRspRepeal.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pRspRepeal.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pRspRepeal.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pRspRepeal.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pRspRepeal.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pRspRepeal.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pRspRepeal.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pRspRepeal.LastFragment.decode(encoding="gb18030", errors="ignore")

    # ///会话号
    l_dict["SessionID"]                 = pRspRepeal.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pRspRepeal.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pRspRepeal.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pRspRepeal.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pRspRepeal.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pRspRepeal.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pRspRepeal.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pRspRepeal.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pRspRepeal.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pRspRepeal.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pRspRepeal.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pRspRepeal.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pRspRepeal.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pRspRepeal.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pRspRepeal.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pRspRepeal.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pRspRepeal.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pRspRepeal.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pRspRepeal.BrokerFee

    # ///发送方给接收方的消息
    l_dict["Message"]                   = pRspRepeal.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pRspRepeal.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pRspRepeal.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pRspRepeal.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pRspRepeal.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pRspRepeal.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pRspRepeal.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pRspRepeal.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pRspRepeal.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pRspRepeal.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pRspRepeal.RequestID
    # ///交易ID
    l_dict["TID"]                       = pRspRepeal.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pRspRepeal.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pRspRepeal.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pRspRepeal.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pRspRepeal.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspFromBankToFutureByFuture(self, pReqTransfer, pRspInfo, nRequestID, bIsLast):
    '''
    ///期货发起银行资金转期货应答
    '''


    if bIsLast == True:
      self.req_call['FromBankToFutureByFuture'] = 1


    self.PTP_Algos.DumpRspDict("T_ReqTransfer",pReqTransfer)

    l_dict={}

    """CThostFtdcReqTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pReqTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pReqTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pReqTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pReqTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pReqTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pReqTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pReqTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pReqTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pReqTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pReqTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pReqTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pReqTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pReqTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspFromFutureToBankByFuture(self, pReqTransfer, pRspInfo, nRequestID, bIsLast):
    '''
    ///期货发起期货资金转银行应答
    '''


    if bIsLast == True:
      self.req_call['FromFutureToBankByFuture'] = 1


    self.PTP_Algos.DumpRspDict("T_ReqTransfer",pReqTransfer)

    l_dict={}

    """CThostFtdcReqTransferField

    # ///业务功能码
    l_dict["TradeCode"]                 = pReqTransfer.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqTransfer.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqTransfer.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqTransfer.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqTransfer.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqTransfer.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqTransfer.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqTransfer.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqTransfer.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqTransfer.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqTransfer.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pReqTransfer.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqTransfer.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqTransfer.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqTransfer.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqTransfer.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqTransfer.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pReqTransfer.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqTransfer.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqTransfer.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pReqTransfer.InstallID
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqTransfer.FutureSerial
    # ///用户标识
    l_dict["UserID"]                    = pReqTransfer.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqTransfer.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqTransfer.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///转帐金额
    l_dict["TradeAmount"]               = pReqTransfer.TradeAmount
    # ///期货可取金额
    l_dict["FutureFetchAmount"]         = pReqTransfer.FutureFetchAmount
    # ///费用支付标志
    l_dict["FeePayFlag"]                = pReqTransfer.FeePayFlag.decode(encoding="gb18030", errors="ignore")
    # ///应收客户费用
    l_dict["CustFee"]                   = pReqTransfer.CustFee
    # ///应收期货公司费用
    l_dict["BrokerFee"]                 = pReqTransfer.BrokerFee
    # ///发送方给接收方的消息
    l_dict["Message"]                   = pReqTransfer.Message.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqTransfer.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqTransfer.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqTransfer.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqTransfer.BankSecuAccType.decode(encoding="gb18030", errors="ignore")

    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqTransfer.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqTransfer.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqTransfer.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqTransfer.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqTransfer.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///请求编号
    l_dict["RequestID"]                 = pReqTransfer.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqTransfer.TID
    # ///转账交易状态
    l_dict["TransferStatus"]            = pReqTransfer.TransferStatus.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqTransfer.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRspQueryBankAccountMoneyByFuture(self, pReqQueryAccount, pRspInfo, nRequestID, bIsLast):
    '''
    ///期货发起查询银行余额应答
    '''


    if bIsLast == True:
      self.req_call['QueryBankAccountMoneyByFuture'] = 1


    self.PTP_Algos.DumpRspDict("T_ReqQueryAccount",pReqQueryAccount)

    l_dict={}

    """CThostFtdcReqQueryAccountField

    # ///业务功能码
    l_dict["TradeCode"]                 = pReqQueryAccount.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pReqQueryAccount.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pReqQueryAccount.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pReqQueryAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pReqQueryAccount.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pReqQueryAccount.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pReqQueryAccount.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pReqQueryAccount.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pReqQueryAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pReqQueryAccount.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pReqQueryAccount.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pReqQueryAccount.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pReqQueryAccount.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pReqQueryAccount.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pReqQueryAccount.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///客户类型
    l_dict["CustType"]                  = pReqQueryAccount.CustType.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pReqQueryAccount.BankAccount.decode(encoding="gb18030", errors="ignore")

    # ///银行密码
    l_dict["BankPassWord"]              = pReqQueryAccount.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pReqQueryAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pReqQueryAccount.Password.decode(encoding="gb18030", errors="ignore")
    # ///期货公司流水号
    l_dict["FutureSerial"]              = pReqQueryAccount.FutureSerial
    # ///安装编号
    l_dict["InstallID"]                 = pReqQueryAccount.InstallID
    # ///用户标识
    l_dict["UserID"]                    = pReqQueryAccount.UserID.decode(encoding="gb18030", errors="ignore")
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pReqQueryAccount.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pReqQueryAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pReqQueryAccount.Digest.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pReqQueryAccount.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pReqQueryAccount.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pReqQueryAccount.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pReqQueryAccount.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pReqQueryAccount.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pReqQueryAccount.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pReqQueryAccount.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pReqQueryAccount.OperNo.decode(encoding="gb18030", errors="ignore")

    # ///请求编号
    l_dict["RequestID"]                 = pReqQueryAccount.RequestID
    # ///交易ID
    l_dict["TID"]                       = pReqQueryAccount.TID
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pReqQueryAccount.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnOpenAccountByBank(self, pOpenAccount):
    '''
    ///银行发起银期开户通知
    '''


    self.PTP_Algos.DumpRspDict("T_OpenAccount",pOpenAccount)

    l_dict={}

    """CThostFtdcOpenAccountField

    # ///业务功能码
    l_dict["TradeCode"]                 = pOpenAccount.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pOpenAccount.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pOpenAccount.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pOpenAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pOpenAccount.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pOpenAccount.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pOpenAccount.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pOpenAccount.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pOpenAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pOpenAccount.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pOpenAccount.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pOpenAccount.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pOpenAccount.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pOpenAccount.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pOpenAccount.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///性别
    l_dict["Gender"]                    = pOpenAccount.Gender.decode(encoding="gb18030", errors="ignore")
    # ///国家代码
    l_dict["CountryCode"]               = pOpenAccount.CountryCode.decode(encoding="gb18030", errors="ignore")

    # ///客户类型
    l_dict["CustType"]                  = pOpenAccount.CustType.decode(encoding="gb18030", errors="ignore")
    # ///地址
    l_dict["Address"]                   = pOpenAccount.Address.decode(encoding="gb18030", errors="ignore")
    # ///邮编
    l_dict["ZipCode"]                   = pOpenAccount.ZipCode.decode(encoding="gb18030", errors="ignore")
    # ///电话号码
    l_dict["Telephone"]                 = pOpenAccount.Telephone.decode(encoding="gb18030", errors="ignore")
    # ///手机
    l_dict["MobilePhone"]               = pOpenAccount.MobilePhone.decode(encoding="gb18030", errors="ignore")
    # ///传真
    l_dict["Fax"]                       = pOpenAccount.Fax.decode(encoding="gb18030", errors="ignore")
    # ///电子邮件
    l_dict["EMail"]                     = pOpenAccount.EMail.decode(encoding="gb18030", errors="ignore")
    # ///资金账户状态
    l_dict["MoneyAccountStatus"]        = pOpenAccount.MoneyAccountStatus.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pOpenAccount.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pOpenAccount.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pOpenAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pOpenAccount.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pOpenAccount.InstallID
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pOpenAccount.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pOpenAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///汇钞标志
    l_dict["CashExchangeCode"]          = pOpenAccount.CashExchangeCode.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pOpenAccount.Digest.decode(encoding="gb18030", errors="ignore")

    # ///银行帐号类型
    l_dict["BankAccType"]               = pOpenAccount.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pOpenAccount.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pOpenAccount.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pOpenAccount.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pOpenAccount.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pOpenAccount.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pOpenAccount.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pOpenAccount.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///交易ID
    l_dict["TID"]                       = pOpenAccount.TID
    # ///用户标识
    l_dict["UserID"]                    = pOpenAccount.UserID.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pOpenAccount.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pOpenAccount.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pOpenAccount.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnCancelAccountByBank(self, pCancelAccount):
    '''
    ///银行发起银期销户通知
    '''


    self.PTP_Algos.DumpRspDict("T_CancelAccount",pCancelAccount)

    l_dict={}

    """CThostFtdcCancelAccountField

    # ///业务功能码
    l_dict["TradeCode"]                 = pCancelAccount.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pCancelAccount.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pCancelAccount.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pCancelAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pCancelAccount.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pCancelAccount.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pCancelAccount.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pCancelAccount.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pCancelAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pCancelAccount.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pCancelAccount.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pCancelAccount.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pCancelAccount.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pCancelAccount.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pCancelAccount.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///性别
    l_dict["Gender"]                    = pCancelAccount.Gender.decode(encoding="gb18030", errors="ignore")
    # ///国家代码
    l_dict["CountryCode"]               = pCancelAccount.CountryCode.decode(encoding="gb18030", errors="ignore")

    # ///客户类型
    l_dict["CustType"]                  = pCancelAccount.CustType.decode(encoding="gb18030", errors="ignore")
    # ///地址
    l_dict["Address"]                   = pCancelAccount.Address.decode(encoding="gb18030", errors="ignore")
    # ///邮编
    l_dict["ZipCode"]                   = pCancelAccount.ZipCode.decode(encoding="gb18030", errors="ignore")
    # ///电话号码
    l_dict["Telephone"]                 = pCancelAccount.Telephone.decode(encoding="gb18030", errors="ignore")
    # ///手机
    l_dict["MobilePhone"]               = pCancelAccount.MobilePhone.decode(encoding="gb18030", errors="ignore")
    # ///传真
    l_dict["Fax"]                       = pCancelAccount.Fax.decode(encoding="gb18030", errors="ignore")
    # ///电子邮件
    l_dict["EMail"]                     = pCancelAccount.EMail.decode(encoding="gb18030", errors="ignore")
    # ///资金账户状态
    l_dict["MoneyAccountStatus"]        = pCancelAccount.MoneyAccountStatus.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pCancelAccount.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pCancelAccount.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pCancelAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pCancelAccount.Password.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pCancelAccount.InstallID
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pCancelAccount.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")
    # ///币种代码
    l_dict["CurrencyID"]                = pCancelAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///汇钞标志
    l_dict["CashExchangeCode"]          = pCancelAccount.CashExchangeCode.decode(encoding="gb18030", errors="ignore")
    # ///摘要
    l_dict["Digest"]                    = pCancelAccount.Digest.decode(encoding="gb18030", errors="ignore")

    # ///银行帐号类型
    l_dict["BankAccType"]               = pCancelAccount.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///渠道标志
    l_dict["DeviceID"]                  = pCancelAccount.DeviceID.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号类型
    l_dict["BankSecuAccType"]           = pCancelAccount.BankSecuAccType.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pCancelAccount.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///期货单位帐号
    l_dict["BankSecuAcc"]               = pCancelAccount.BankSecuAcc.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pCancelAccount.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pCancelAccount.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易柜员
    l_dict["OperNo"]                    = pCancelAccount.OperNo.decode(encoding="gb18030", errors="ignore")
    # ///交易ID
    l_dict["TID"]                       = pCancelAccount.TID
    # ///用户标识
    l_dict["UserID"]                    = pCancelAccount.UserID.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pCancelAccount.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pCancelAccount.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pCancelAccount.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

  def OnRtnChangeAccountByBank(self, pChangeAccount):
    '''
    ///银行发起变更银行账号通知
    '''


    self.PTP_Algos.DumpRspDict("T_ChangeAccount",pChangeAccount)

    l_dict={}

    """CThostFtdcChangeAccountField

    # ///业务功能码
    l_dict["TradeCode"]                 = pChangeAccount.TradeCode.decode(encoding="gb18030", errors="ignore")
    # ///银行代码
    l_dict["BankID"]                    = pChangeAccount.BankID.decode(encoding="gb18030", errors="ignore")
    # ///银行分支机构代码
    l_dict["BankBranchID"]              = pChangeAccount.BankBranchID.decode(encoding="gb18030", errors="ignore")
    # ///期商代码
    l_dict["BrokerID"]                  = pChangeAccount.BrokerID.decode(encoding="gb18030", errors="ignore")
    # ///期商分支机构代码
    l_dict["BrokerBranchID"]            = pChangeAccount.BrokerBranchID.decode(encoding="gb18030", errors="ignore")
    # ///交易日期
    l_dict["TradeDate"]                 = pChangeAccount.TradeDate.decode(encoding="gb18030", errors="ignore")
    # ///交易时间
    l_dict["TradeTime"]                 = pChangeAccount.TradeTime.decode(encoding="gb18030", errors="ignore")
    # ///银行流水号
    l_dict["BankSerial"]                = pChangeAccount.BankSerial.decode(encoding="gb18030", errors="ignore")
    # ///交易系统日期
    l_dict["TradingDay"]                = pChangeAccount.TradingDay.decode(encoding="gb18030", errors="ignore")
    # ///银期平台消息流水号
    l_dict["PlateSerial"]               = pChangeAccount.PlateSerial
    # ///最后分片标志
    l_dict["LastFragment"]              = pChangeAccount.LastFragment.decode(encoding="gb18030", errors="ignore")
    # ///会话号
    l_dict["SessionID"]                 = pChangeAccount.SessionID
    # ///客户姓名
    l_dict["CustomerName"]              = pChangeAccount.CustomerName.decode(encoding="gb18030", errors="ignore")
    # ///证件类型
    l_dict["IdCardType"]                = pChangeAccount.IdCardType.decode(encoding="gb18030", errors="ignore")
    # ///证件号码
    l_dict["IdentifiedCardNo"]          = pChangeAccount.IdentifiedCardNo.decode(encoding="gb18030", errors="ignore")
    # ///性别
    l_dict["Gender"]                    = pChangeAccount.Gender.decode(encoding="gb18030", errors="ignore")
    # ///国家代码
    l_dict["CountryCode"]               = pChangeAccount.CountryCode.decode(encoding="gb18030", errors="ignore")

    # ///客户类型
    l_dict["CustType"]                  = pChangeAccount.CustType.decode(encoding="gb18030", errors="ignore")
    # ///地址
    l_dict["Address"]                   = pChangeAccount.Address.decode(encoding="gb18030", errors="ignore")
    # ///邮编
    l_dict["ZipCode"]                   = pChangeAccount.ZipCode.decode(encoding="gb18030", errors="ignore")
    # ///电话号码
    l_dict["Telephone"]                 = pChangeAccount.Telephone.decode(encoding="gb18030", errors="ignore")
    # ///手机
    l_dict["MobilePhone"]               = pChangeAccount.MobilePhone.decode(encoding="gb18030", errors="ignore")
    # ///传真
    l_dict["Fax"]                       = pChangeAccount.Fax.decode(encoding="gb18030", errors="ignore")
    # ///电子邮件
    l_dict["EMail"]                     = pChangeAccount.EMail.decode(encoding="gb18030", errors="ignore")
    # ///资金账户状态
    l_dict["MoneyAccountStatus"]        = pChangeAccount.MoneyAccountStatus.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号
    l_dict["BankAccount"]               = pChangeAccount.BankAccount.decode(encoding="gb18030", errors="ignore")
    # ///银行密码
    l_dict["BankPassWord"]              = pChangeAccount.BankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///新银行帐号
    l_dict["NewBankAccount"]            = pChangeAccount.NewBankAccount.decode(encoding="gb18030", errors="ignore")
    # ///新银行密码
    l_dict["NewBankPassWord"]           = pChangeAccount.NewBankPassWord.decode(encoding="gb18030", errors="ignore")
    # ///投资者帐号
    l_dict["AccountID"]                 = pChangeAccount.AccountID.decode(encoding="gb18030", errors="ignore")
    # ///期货密码
    l_dict["Password"]                  = pChangeAccount.Password.decode(encoding="gb18030", errors="ignore")
    # ///银行帐号类型
    l_dict["BankAccType"]               = pChangeAccount.BankAccType.decode(encoding="gb18030", errors="ignore")
    # ///安装编号
    l_dict["InstallID"]                 = pChangeAccount.InstallID
    # ///验证客户证件号码标志
    l_dict["VerifyCertNoFlag"]          = pChangeAccount.VerifyCertNoFlag.decode(encoding="gb18030", errors="ignore")

    # ///币种代码
    l_dict["CurrencyID"]                = pChangeAccount.CurrencyID.decode(encoding="gb18030", errors="ignore")
    # ///期货公司银行编码
    l_dict["BrokerIDByBank"]            = pChangeAccount.BrokerIDByBank.decode(encoding="gb18030", errors="ignore")
    # ///银行密码标志
    l_dict["BankPwdFlag"]               = pChangeAccount.BankPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///期货资金密码核对标志
    l_dict["SecuPwdFlag"]               = pChangeAccount.SecuPwdFlag.decode(encoding="gb18030", errors="ignore")
    # ///交易ID
    l_dict["TID"]                       = pChangeAccount.TID
    # ///摘要
    l_dict["Digest"]                    = pChangeAccount.Digest.decode(encoding="gb18030", errors="ignore")
    # ///错误代码
    l_dict["ErrorID"]                   = pChangeAccount.ErrorID
    # ///错误信息
    l_dict["ErrorMsg"]                  = pChangeAccount.ErrorMsg.decode(encoding="gb18030", errors="ignore")
    # ///长客户姓名
    l_dict["LongCustomerName"]          = pChangeAccount.LongCustomerName.decode(encoding="gb18030", errors="ignore")

    #"""

# 以下是简单的接口组合案例
      
  def get_Position(self, instrumentID):
    return self.PTP_Algos.get_Position(instrumentID)
    
  def get_InstrumentAttr(self, instrumentID):    
    return self.PTP_Algos.get_InstrumentAttr(instrumentID)
    
  def get_ReqOrderList(self, instrumentID): 
    return self.PTP_Algos.get_ReqOrderList(instrumentID)
    
  def get_Order_list(self, instrumentID):
    return self.PTP_Algos.get_Order_list(instrumentID)
    
  def get_exchangeID_of_instrument(self,  instrument_id):
    l_ExchageID = ""
    try:
      #if not isinstance(trader, py_CtpTrader) or not isinstance(instrument_id, str) or len(instrument_id) == 0:
      if not isinstance(instrument_id, str) or len(instrument_id) == 0:
        return l_ExchageID

      l_instrument_Attr_dict = self.get_InstrumentAttr(instrument_id)
      if l_instrument_Attr_dict is None:
         return l_ExchageID

      l_ExchageID = l_instrument_Attr_dict["ExchangeID"]
          
    except Exception as err:
      myEnv.logger.error("get_exchangeID_of_instrument failed", exc_info=True)
      l_ExchageID = ""
          
    return l_ExchageID 
        
  def ai_buy_open(self, investor_id, instrument_id, order_price, order_vol, last_price=0, exchange_ID=""):
    l_retVal = -1
    try:
      l_ExchageID = exchange_ID
      if l_ExchageID is None or len(l_ExchageID) == 0:
          l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

      pBuyOpen = py_ApiStructure.InputOrderField(
          BrokerID=self.broker_id,
          InvestorID=investor_id,
          ExchangeID=l_ExchageID,
          InstrumentID=instrument_id,
          UserID=investor_id,
          OrderPriceType="2",
          Direction="0",
          CombOffsetFlag="0",  # ///开仓
          CombHedgeFlag="1",
          LimitPrice=order_price,
          VolumeTotalOriginal=order_vol,
          TimeCondition="3",
          VolumeCondition="1",
          MinVolume=1,
          ContingentCondition="1",
          StopPrice=0,
          ForceCloseReason="0",
          IsAutoSuspend=0
      )
      l_retVal = self.ReqOrderInsert(pBuyOpen, "ai_buy_open", last_price)
      self.PTP_Algos.restOrderFactor(instrument_id)

      l_order_list = self.get_Order_list(instrument_id)
      if not l_order_list is None:
        for it_Order in l_order_list:
          # 如果有反方向报单
          # (1)撤掉卖及高价的买
          if (it_Order["CombOffsetFlag"] == "0") and ((it_Order["Direction"] == "1") or (
                  it_Order["Direction"] == "0" and it_Order["LimitPrice"] < order_price)):
              l_OrderSysID = it_Order["OrderSysID"]
              pOrderAction = py_ApiStructure.InputOrderActionField(
                  BrokerID=self.broker_id,
                  InvestorID=investor_id,
                  UserID=investor_id,
                  ExchangeID=l_ExchageID,
                  ActionFlag="0",  # ///删除报单
                  OrderSysID=l_OrderSysID,
                  InstrumentID=instrument_id
              )
              self.ReqOrderAction(pOrderAction)

      l_retVal = 0
      return l_retVal

    except Exception as err:
        myEnv.logger.error("ai_buy_open", exc_info=True)
        return l_retVal

  def ai_sell_open(self, investor_id, instrument_id, order_price, order_vol, last_price=0,
                   exchange_ID=""):
      l_retVal = -1
      try:
          l_ExchageID = exchange_ID
          if l_ExchageID is None or len(l_ExchageID) == 0:
              l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

          pSellOpen = py_ApiStructure.InputOrderField(
              BrokerID=self.broker_id,
              InvestorID=investor_id,
              ExchangeID=l_ExchageID,
              InstrumentID=instrument_id,
              UserID=investor_id,
              OrderPriceType="2",
              Direction="1",
              CombOffsetFlag="0",  # ///开仓
              CombHedgeFlag="1",
              LimitPrice=order_price,
              VolumeTotalOriginal=order_vol,
              TimeCondition="3",
              VolumeCondition="1",
              MinVolume=1,
              ContingentCondition="1",
              StopPrice=0,
              ForceCloseReason="0",
              IsAutoSuspend=0
          )
          l_retVal = self.ReqOrderInsert(pSellOpen, "ai_sell_open", last_price)
          self.PTP_Algos.restOrderFactor(instrument_id)

          l_order_list = self.get_Order_list(instrument_id)
          if not l_order_list is None:
              for it_Order in l_order_list:
                # 如果有反方向报单
                # (1)撤掉买及低价的卖
                # 如果有买方向报单
                if (it_Order["CombOffsetFlag"] == "0") and ((it_Order["Direction"] == "0") or (
                        it_Order["Direction"] == "1" and it_Order["LimitPrice"] > order_price)):
                    l_OrderSysID = it_Order["OrderSysID"]
                    pOrderAction = py_ApiStructure.InputOrderActionField(

BrokerID=self.broker_id,
                        InvestorID=investor_id,
                        UserID=investor_id,
                        ExchangeID=l_ExchageID,
                        ActionFlag="0",  # ///删除报单
                        OrderSysID=l_OrderSysID,
                        InstrumentID=instrument_id
                    )
                    self.ReqOrderAction(pOrderAction)

          return l_retVal

      except Exception as err:
          myEnv.logger.error("ai_sell_open", exc_info=True)


  def withdraw_buy(self, investor_id, instrument_id, exchange_ID=""):
    l_retVal = -1
    try:
      l_ExchageID = exchange_ID
      if l_ExchageID is None or len(l_ExchageID) == 0:
          l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

      l_order_list = self.get_Order_list(instrument_id)
      if not l_order_list is None:
        for it_Order in l_order_list:
          # (1)撤掉买
          if it_Order["Direction"] == "0" and it_Order["OrderStatus"] not in ["0", "5", "a"]:
            l_OrderSysID = it_Order["OrderSysID"]
            pOrderAction = py_ApiStructure.InputOrderActionField(
                BrokerID=self.broker_id,
                InvestorID=investor_id,
                UserID=investor_id,
                ExchangeID=l_ExchageID,
                ActionFlag="0",  # ///删除报单
                OrderSysID=l_OrderSysID,
                InstrumentID=instrument_id
            )
            self.ReqOrderAction(pOrderAction)

      l_retVal = 0
      return l_retVal

    except Exception as err:
        myEnv.logger.error("withdraw_buy", exc_info=True)
        return l_retVal

  def withdraw_sell(self, investor_id, instrument_id, exchange_ID=""):
      l_retVal = -1
      try:
          l_ExchageID = exchange_ID
          if l_ExchageID is None or len(l_ExchageID) == 0:
              l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

          l_order_list = self.get_Order_list(instrument_id)
          if not l_order_list is None:
              for it_Order in l_order_list:
                  # (1)撤掉买
                  if it_Order["Direction"] == "1" and it_Order["OrderStatus"] not in ["0", "5", "a"]:
                      l_OrderSysID = it_Order["OrderSysID"]
                      pOrderAction = py_ApiStructure.InputOrderActionField(
                          BrokerID=self.broker_id,
                          InvestorID=investor_id,
                          UserID=investor_id,
                          ExchangeID=l_ExchageID,
                          ActionFlag="0",  # ///删除报单
                          OrderSysID=l_OrderSysID,
                          InstrumentID=instrument_id
                      )
                      self.ReqOrderAction(pOrderAction)

          l_retVal = 0
          return l_retVal

      except Exception as err:
          myEnv.logger.error("withdraw_sell", exc_info=True)
          return l_retVal

  def buy_open(self, investor_id, instrument_id, order_price, order_vol, last_price=0, exchange_ID=""):
      l_retVal = -1
      try:
          l_ExchageID = exchange_ID
          if l_ExchageID is None or len(l_ExchageID) == 0:
              l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

          pBuyOpen = py_ApiStructure.InputOrderField(
              BrokerID=self.broker_id,
              InvestorID=investor_id,
              ExchangeID=l_ExchageID,
              InstrumentID=instrument_id,
              UserID=investor_id,
              OrderPriceType="2",
              Direction="0",
              CombOffsetFlag="0",  # ///开仓
              CombHedgeFlag="1",
              LimitPrice=order_price,
              VolumeTotalOriginal=order_vol,
              TimeCondition="3",
              VolumeCondition="1",
              MinVolume=1,
              ContingentCondition="1",
              StopPrice=0,
              ForceCloseReason="0",
              IsAutoSuspend=0
          )
          l_retVal = self.ReqOrderInsert(pBuyOpen, "buy_open", last_price)
          self.PTP_Algos.restOrderFactor(instrument_id)

      except Exception as err:
          myEnv.logger.error("buy_open", exc_info=True)
          l_retVal = -1

      return l_retVal


  def sell_open(self, investor_id, instrument_id, order_price, order_vol, last_price=0,
                exchange_ID=""):
      l_retVal = -1
      try:
          l_ExchageID = exchange_ID
          if l_ExchageID is None or len(l_ExchageID) == 0:
              l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

          pSellOpen = py_ApiStructure.InputOrderField(
              BrokerID=self.broker_id,
              InvestorID=investor_id,
              ExchangeID=l_ExchageID,
              InstrumentID=instrument_id,
              UserID=investor_id,
              OrderPriceType="2",
              Direction="1",
              CombOffsetFlag="0",  # ///开仓
              CombHedgeFlag="1",
              LimitPrice=order_price,
              VolumeTotalOriginal=order_vol,
              TimeCondition="3",
              VolumeCondition="1",
              MinVolume=1,
              ContingentCondition="1",
              StopPrice=0,
              ForceCloseReason="0",
              IsAutoSuspend=0
          )
          l_retVal = self.ReqOrderInsert(pSellOpen, "sell_open", last_price)
          self.PTP_Algos.restOrderFactor(instrument_id)


      except Exception as err:
          myEnv.logger.error("sell_open", exc_info=True)
          l_retVal = -1
      return l_retVal



  def buy_close(self, investor_id, instrument_id, order_price, order_vol, last_price=0,
                exchange_ID=""):
      l_retVal = -1
      try:
          l_ExchageID = exchange_ID
          if l_ExchageID is None or len(l_ExchageID) == 0:
              l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

          # 获取仓位
          l_position_list = self.get_Position(instrument_id)
          l_remain = order_vol
          if not l_position_list is None:
              for it_pos in l_position_list:
                  if it_pos["PosiDirection"] == "3" and it_pos["Position"] > 0 and l_remain > 0:  # ///空头
                      l_close_vol = 1
                      if l_ExchageID == "SHFE":
                          if it_pos["TodayPosition"] > 0:
                              l_CombOffsetFlag = "3"  # 平今
                              l_close_vol = min(it_pos["TodayPosition"], l_remain)
                          else:
                              l_CombOffsetFlag = "4"  # 平昨
                              l_close_vol = min(it_pos["YdPosition"], l_remain)
                      else:
                          l_CombOffsetFlag = "1"  # 平仓
                          l_close_vol = min(it_pos["Position"], l_remain)

                      # 改进，撤掉以前价格不合理的平仓
                      # 报买平单
                      pBuyClose = py_ApiStructure.InputOrderField(
                          BrokerID=self.broker_id,
                          InvestorID=investor_id,
                          ExchangeID=l_ExchageID,
                          InstrumentID=instrument_id,
                          UserID=investor_id,
                          OrderPriceType="2",
                          Direction="0",
                          CombOffsetFlag=l_CombOffsetFlag,
                          CombHedgeFlag="1",
                          LimitPrice=order_price,  # 可以考虑减少一个tick确保能卖掉
                          VolumeTotalOriginal=l_close_vol,
                          TimeCondition="3",
                          VolumeCondition="1",
                          MinVolume=1,
                          ContingentCondition="1",
                          StopPrice=0,
                          ForceCloseReason="0",
                          IsAutoSuspend=0
                      )
                      l_retVal = self.ReqOrderInsert(pBuyClose, "buy_close", last_price)
                      self.PTP_Algos.restOrderFactor(instrument_id)
                      l_remain = l_remain - l_close_vol
      except Exception as err:
          myEnv.logger.error("buy_close", exc_info=True)


  def sell_close(self, investor_id, instrument_id, order_price, order_vol, last_price=0,
                 exchange_ID=""):
    l_retVal = -1
    try:
      l_ExchageID = exchange_ID
      if l_ExchageID is None or len(l_ExchageID) == 0:
          l_ExchageID = self.get_exchangeID_of_instrument( instrument_id)

      # 获取仓位
      l_position_list = self.get_Position(instrument_id)
      l_remain = order_vol
      # TThostFtdcVolumeType	YdPosition;    ///上日持仓
      # TThostFtdcVolumeType	Position;      ///今日总持仓
      # TThostFtdcVolumeType	TodayPosition; ///今日持仓
      if not l_position_list is None:
        for it_pos in l_position_list:
              if it_pos["PosiDirection"] == "2" and it_pos["Position"] > 0 and l_remain > 0:  # ///多头
                  l_close_vol = 1
                  if l_ExchageID == "SHFE":
                      if it_pos["TodayPosition"] > 0:
                          l_CombOffsetFlag = "3"  # 平今
                          l_close_vol = min(it_pos["TodayPosition"], l_remain)
                      else:
                          l_CombOffsetFlag = "4"  # 平昨
                          l_close_vol = min(it_pos["YdPosition"], l_remain)
                  else:
                      l_CombOffsetFlag = "1"  # 平仓
                      l_close_vol = min(it_pos["Position"], l_remain)

                  # 改进，撤掉以前价格不合理的平仓，
                  # 报卖平单
                  pSellClose = py_ApiStructure.InputOrderField(
                      BrokerID=self.broker_id,
                      InvestorID=investor_id,
                      ExchangeID=l_ExchageID,
                      InstrumentID=instrument_id,
                      UserID=investor_id,
                      OrderPriceType="2",
                      Direction="1",
                      CombOffsetFlag=l_CombOffsetFlag,
                      CombHedgeFlag="1",
                      LimitPrice=order_price,  # 可以考虑减少一个tick确保能卖掉
                      VolumeTotalOriginal=l_close_vol,
                      TimeCondition="3",
                      VolumeCondition="1",
                      MinVolume=1,
                      ContingentCondition="1",
                      StopPrice=0,
                      ForceCloseReason="0",
                      IsAutoSuspend=0
                  )
                  l_retVal = self.ReqOrderInsert(pSellClose, "sell_close", last_price)
                  self.PTP_Algos.restOrderFactor(instrument_id)
                  l_remain = l_remain - l_close_vol
    except Exception as err:
        myEnv.logger.error("sell_close", exc_info=True)

