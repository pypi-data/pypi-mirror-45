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
from .cython2c.cTraderApi cimport CTraderSpi, CTraderApi, CreateFtdcTraderApi

cdef class TraderApiWrapper:
  cdef CTraderApi *_api
  cdef CTraderSpi *_spi

  def __cinit__(self):
    funName = "%s.%s" % ("TraderApiWrapper", "__cinit__")
    printString("TraderApicall_stack","call->",funName) 
    self._api = NULL
    self._spi = NULL          
 
    self.RequestID = 1  
    printString("TraderApicall_stack","call-<",funName)

  def Inc_RequestID(self):
    self.RequestID = self.RequestID + 1
    return self.RequestID 
  
  def __dealloc__(self):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)
    self.Release()
    printString("TraderApicall_stack","call-<",funName)


  """
  *CreateFtdcTraderApi
  *GetApiVersion
  Release
  Init
  Join
  *GetTradingDay
  RegisterFront
  RegisterNameServer
  RegisterFensUserInfo
  RegisterSpi
  SubscribePrivateTopic
  SubscribePublicTopic 

  SPI:
  OnFrontConnected
  OnFrontDisconnected
  OnHeartBeatWarning
  """ 

  @staticmethod
  def GetApiVersion():
    funName = "%s.%s" % ("Trader", "GetApiVersion")
    printString("TraderApicall_stack","call->",funName)
    return CTraderApi.GetApiVersion()
    printString("TraderApicall_stack","call-<",funName)

  def Release(self):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)

    if self._api is not NULL:
        self._api.RegisterSpi(NULL)
        self._api.Release()
        self._api = NULL
        self._spi = NULL

    printString("TraderApicall_stack","call-<",funName)



  def Init_Base(self):
    bInit=-1
    try:
      self._api = CreateFtdcTraderApi(self.pszFlowPath.encode())
      if not self._api:
          raise MemoryError()
          
      self._spi = new CTraderSpi(<PyObject *> self)
      if not self._spi:
        raise MemoryError()
      
      bInit=0
        
    except Exception as err: 
      myEnv.logger.error("Init_Base", exc_info=True)
    
    return bInit

  def Init_Net(self):
    try:
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName)

      bInit=-1
      if self._api is not NULL and self._spi  is not NULL: 
      
        self._api.RegisterSpi(self._spi)
        logDes="step(RegisterSpi) 1(of 4 step)"
        myEnv.logger.info(logDes) 

        self.SubscribePrivateTopic(self.PrivateSubscribeTopic)
        self.SubscribePublicTopic( self.PublicSubscribeTopic)
        logDes="step(SubscribeTopic) 2(of 4 step)"        
        myEnv.logger.info(logDes) 

        #SSL前置格式：ssl://192.168.0.1:41205
        #TCP前置格式：tcp://192.168.0.1:41205
        #此处注册多个前置，连接的时候会随机选择一个
        #pUserMdApi->RegisterFront(“tcp://192.168.0.1:41213”);
        #pUserMdApi->RegisterFront(“tcp://192.168.0.2:41213”);
        for server in self.trader_server:
          #server = "tcp://" + self.md_server + ":" + str(self.md_port)
          myEnv.logger.info("regist " + server)
          self.RegisterFront(server.encode())
        logDes="step(RegisterFront) 3(of 4 step)"        
        myEnv.logger.info(logDes) 

        time.sleep(1)

        self._api.Init()
        logDes="step(Infra_Init) 4(of 4 step)"        
        myEnv.logger.info(logDes) 
      else:
        myEnv.logger.error("BaseEnv has not been inited")  

      printString("TraderApicall_stack","call-<",funName)      
      bInit=0
    except Exception as err:
      myEnv.logger.error("Tader.Init", exc_info=True) 
    
    return bInit     

  def Join(self):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)

    cdef int result
    try:
      if self._api is not NULL:
        with nogil:
          result = self._api.Join()
        return result

    except Exception as err:
        myEnv.logger.error("Join", exc_info=True)

    printString("TraderApicall_stack","call-<",funName)


  def GetTradingDay(self):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)

    cdef const_char *result

    try:
      if self._api is not NULL:
        with nogil:
          result = self._api.GetTradingDay()
        return result
    except Exception as err:
        myEnv.logger.error("GetTradingDay", exc_info=True)

    printString("TraderApicall_stack","call-<",funName)



  def RegisterFront(self, char *pszFrontAddress):
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName)

      try:
        if self._api is not NULL:
          self._api.RegisterFront(pszFrontAddress)
      except Exception as err:
        myEnv.logger.error("RegisterFront", exc_info=True)

      printString("TraderApicall_stack","call-<",funName)

  def RegisterNameServer(self, char *pszNsAddress):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)

    try:
      if self._api is not NULL:
        self._api.RegisterNameServer(pszNsAddress)
    except Exception as err:
      myEnv.logger.error("RegisterNameServer", exc_info=True)

    printString("TraderApicall_stack","call-<",funName)

  def RegisterFensUserInfo(self, pFensUserInfo):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)

    cdef size_t address
    try:
      if self._api is not NULL:
        address = ctypes.addressof(pFensUserInfo)

        self._api.RegisterFensUserInfo(<CThostFtdcFensUserInfoField *> address)

    except Exception as err:
      myEnv.logger.error("RegisterFensUserInfo", exc_info=True)

    printString("TraderApicall_stack","call-<",funName)

  def SubscribePrivateTopic(self, THOST_TE_RESUME_TYPE nResumeType):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)
    try:
      if self._api is not NULL:
        self._api.SubscribePrivateTopic(nResumeType)
    except Exception as err:
      myEnv.logger.error("SubscribePrivateTopic", exc_info=True)
    printString("TraderApicall_stack","call-<",funName)



  #订阅公共流。
  #@param nResumeType 公共流重传方式
  #        THOST_TERT_RESTART:从本交易日开始重传
  #        THOST_TERT_RESUME:从上次收到的续传
  #        THOST_TERT_QUICK:只传送登录后公共流的内容
  #@remark 该方法要在Init方法前调用。若不调用则不会收到公共流的数据。
  def SubscribePublicTopic(self, THOST_TE_RESUME_TYPE nResumeType):
    funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    printString("TraderApicall_stack","call->",funName)
    try:
      if self._api is not NULL:
        self._api.SubscribePublicTopic(nResumeType)
    except Exception as err:
      myEnv.logger.error("SubscribePublicTopic", exc_info=True)

    printString("TraderApicall_stack","call-<",funName)

  #客户端认证请求
  def  ReqAuthenticate(self, pReqAuthenticateField, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pReqAuthenticateField)
        with nogil:
          result = self._api.ReqAuthenticate(<CThostFtdcReqAuthenticateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqAuthenticate', exc_info=True)

    return result


  #用户登录请求
  def  ReqUserLogin(self, pReqUserLoginField, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pReqUserLoginField)
        with nogil:
          result = self._api.ReqUserLogin(<CThostFtdcReqUserLoginField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
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
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pUserLogout)
        with nogil:
          result = self._api.ReqUserLogout(<CThostFtdcUserLogoutField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqUserLogout', exc_info=True)

    return result


  #用户口令更新请求
  def  ReqUserPasswordUpdate(self, pUserPasswordUpdate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pUserPasswordUpdate)
        with nogil:
          result = self._api.ReqUserPasswordUpdate(<CThostFtdcUserPasswordUpdateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqUserPasswordUpdate', exc_info=True)

    return result


  #资金账户口令更新请求
  def  ReqTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pTradingAccountPasswordUpdate)
        with nogil:
          result = self._api.ReqTradingAccountPasswordUpdate(<CThostFtdcTradingAccountPasswordUpdateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqTradingAccountPasswordUpdate', exc_info=True)

    return result


  #登录请求2
  def  ReqUserLogin2(self, pReqUserLogin, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pReqUserLogin)
        with nogil:
          result = self._api.ReqUserLogin2(<CThostFtdcReqUserLoginField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqUserLogin2', exc_info=True)

    return result


  #用户口令更新请求2
  def  ReqUserPasswordUpdate2(self, pUserPasswordUpdate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pUserPasswordUpdate)
        with nogil:
          result = self._api.ReqUserPasswordUpdate2(<CThostFtdcUserPasswordUpdateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqUserPasswordUpdate2', exc_info=True)

    return result


  #报单录入请求
  def  ReqOrderInsert(self, pInputOrder, int nRequestID, express="ctp", md_lastPrice=0):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputOrder)
        with nogil:
          result = self._api.ReqOrderInsert(<CThostFtdcInputOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqOrderInsert', exc_info=True)

    return result


  #预埋单录入请求
  def  ReqParkedOrderInsert(self, pParkedOrder, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pParkedOrder)
        with nogil:
          result = self._api.ReqParkedOrderInsert(<CThostFtdcParkedOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqParkedOrderInsert', exc_info=True)

    return result


  #预埋撤单录入请求
  def  ReqParkedOrderAction(self, pParkedOrderAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pParkedOrderAction)
        with nogil:
          result = self._api.ReqParkedOrderAction(<CThostFtdcParkedOrderActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqParkedOrderAction', exc_info=True)

    return result


  #报单操作请求
  def  ReqOrderAction(self, pInputOrderAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputOrderAction)
        with nogil:
          result = self._api.ReqOrderAction(<CThostFtdcInputOrderActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqOrderAction', exc_info=True)

    return result


  #查询最大报单数量请求
  def  ReqQueryMaxOrderVolume(self, pQueryMaxOrderVolume, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQueryMaxOrderVolume)
        with nogil:
          result = self._api.ReqQueryMaxOrderVolume(<CThostFtdcQueryMaxOrderVolumeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQueryMaxOrderVolume', exc_info=True)

    return result


  #投资者结算结果确认
  def  ReqSettlementInfoConfirm(self, pSettlementInfoConfirm, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pSettlementInfoConfirm)
        with nogil:
          result = self._api.ReqSettlementInfoConfirm(<CThostFtdcSettlementInfoConfirmField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqSettlementInfoConfirm', exc_info=True)

    return result


  #请求删除预埋单
  def  ReqRemoveParkedOrder(self, pRemoveParkedOrder, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pRemoveParkedOrder)
        with nogil:
          result = self._api.ReqRemoveParkedOrder(<CThostFtdcRemoveParkedOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqRemoveParkedOrder', exc_info=True)

    return result


  #请求删除预埋撤单
  def  ReqRemoveParkedOrderAction(self, pRemoveParkedOrderAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pRemoveParkedOrderAction)
        with nogil:
          result = self._api.ReqRemoveParkedOrderAction(<CThostFtdcRemoveParkedOrderActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqRemoveParkedOrderAction', exc_info=True)

    return result


  #执行宣告录入请求
  def  ReqExecOrderInsert(self, pInputExecOrder, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputExecOrder)
        with nogil:
          result = self._api.ReqExecOrderInsert(<CThostFtdcInputExecOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqExecOrderInsert', exc_info=True)

    return result


  #执行宣告操作请求
  def  ReqExecOrderAction(self, pInputExecOrderAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputExecOrderAction)
        with nogil:
          result = self._api.ReqExecOrderAction(<CThostFtdcInputExecOrderActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqExecOrderAction', exc_info=True)

    return result


  #询价录入请求
  def  ReqForQuoteInsert(self, pInputForQuote, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputForQuote)
        with nogil:
          result = self._api.ReqForQuoteInsert(<CThostFtdcInputForQuoteField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqForQuoteInsert', exc_info=True)

    return result


  #报价录入请求
  def  ReqQuoteInsert(self, pInputQuote, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputQuote)
        with nogil:
          result = self._api.ReqQuoteInsert(<CThostFtdcInputQuoteField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQuoteInsert', exc_info=True)

    return result


  #报价操作请求
  def  ReqQuoteAction(self, pInputQuoteAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputQuoteAction)
        with nogil:
          result = self._api.ReqQuoteAction(<CThostFtdcInputQuoteActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQuoteAction', exc_info=True)

    return result


  #批量报单操作请求
  def  ReqBatchOrderAction(self, pInputBatchOrderAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputBatchOrderAction)
        with nogil:
          result = self._api.ReqBatchOrderAction(<CThostFtdcInputBatchOrderActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqBatchOrderAction', exc_info=True)

    return result


  #期权自对冲录入请求
  def  ReqOptionSelfCloseInsert(self, pInputOptionSelfClose, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputOptionSelfClose)
        with nogil:
          result = self._api.ReqOptionSelfCloseInsert(<CThostFtdcInputOptionSelfCloseField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqOptionSelfCloseInsert', exc_info=True)

    return result


  #期权自对冲操作请求
  def  ReqOptionSelfCloseAction(self, pInputOptionSelfCloseAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputOptionSelfCloseAction)
        with nogil:
          result = self._api.ReqOptionSelfCloseAction(<CThostFtdcInputOptionSelfCloseActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqOptionSelfCloseAction', exc_info=True)

    return result


  #申请组合录入请求
  def  ReqCombActionInsert(self, pInputCombAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pInputCombAction)
        with nogil:
          result = self._api.ReqCombActionInsert(<CThostFtdcInputCombActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqCombActionInsert', exc_info=True)

    return result


  #请求查询报单
  def  ReqQryOrder(self, pQryOrder, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryOrder)
        with nogil:
          result = self._api.ReqQryOrder(<CThostFtdcQryOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryOrder', exc_info=True)

    return result


  #请求查询成交
  def  ReqQryTrade(self, pQryTrade, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTrade)
        with nogil:
          result = self._api.ReqQryTrade(<CThostFtdcQryTradeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryTrade', exc_info=True)

    return result


  #请求查询投资者持仓
  def  ReqQryInvestorPosition(self, pQryInvestorPosition, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInvestorPosition)
        with nogil:
          result = self._api.ReqQryInvestorPosition(<CThostFtdcQryInvestorPositionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInvestorPosition', exc_info=True)

    return result


  #请求查询资金账户
  def  ReqQryTradingAccount(self, pQryTradingAccount, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTradingAccount)
        with nogil:
          result = self._api.ReqQryTradingAccount(<CThostFtdcQryTradingAccountField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryTradingAccount', exc_info=True)

    return result


  #请求查询投资者
  def  ReqQryInvestor(self, pQryInvestor, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInvestor)
        with nogil:
          result = self._api.ReqQryInvestor(<CThostFtdcQryInvestorField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInvestor', exc_info=True)

    return result


  #请求查询交易编码
  def  ReqQryTradingCode(self, pQryTradingCode, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTradingCode)
        with nogil:
          result = self._api.ReqQryTradingCode(<CThostFtdcQryTradingCodeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryTradingCode', exc_info=True)

    return result


  #请求查询合约保证金率
  def  ReqQryInstrumentMarginRate(self, pQryInstrumentMarginRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInstrumentMarginRate)
        with nogil:
          result = self._api.ReqQryInstrumentMarginRate(<CThostFtdcQryInstrumentMarginRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInstrumentMarginRate', exc_info=True)

    return result


  #请求查询合约手续费率
  def  ReqQryInstrumentCommissionRate(self, pQryInstrumentCommissionRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInstrumentCommissionRate)
        with nogil:
          result = self._api.ReqQryInstrumentCommissionRate(<CThostFtdcQryInstrumentCommissionRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInstrumentCommissionRate', exc_info=True)

    return result


  #请求查询交易所
  def  ReqQryExchange(self, pQryExchange, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryExchange)
        with nogil:
          result = self._api.ReqQryExchange(<CThostFtdcQryExchangeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryExchange', exc_info=True)

    return result


  #请求查询产品
  def  ReqQryProduct(self, pQryProduct, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryProduct)
        with nogil:
          result = self._api.ReqQryProduct(<CThostFtdcQryProductField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryProduct', exc_info=True)

    return result


  #请求查询合约
  def  ReqQryInstrument(self, pQryInstrument, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInstrument)
        with nogil:
          result = self._api.ReqQryInstrument(<CThostFtdcQryInstrumentField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInstrument', exc_info=True)

    return result


  #请求查询行情
  def  ReqQryDepthMarketData(self, pQryDepthMarketData, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryDepthMarketData)
        with nogil:
          result = self._api.ReqQryDepthMarketData(<CThostFtdcQryDepthMarketDataField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryDepthMarketData', exc_info=True)

    return result


  #请求查询投资者结算结果
  def  ReqQrySettlementInfo(self, pQrySettlementInfo, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQrySettlementInfo)
        with nogil:
          result = self._api.ReqQrySettlementInfo(<CThostFtdcQrySettlementInfoField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQrySettlementInfo', exc_info=True)

    return result


  #请求查询转帐银行
  def  ReqQryTransferBank(self, pQryTransferBank, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTransferBank)
        with nogil:
          result = self._api.ReqQryTransferBank(<CThostFtdcQryTransferBankField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryTransferBank', exc_info=True)

    return result


  #请求查询投资者持仓明细
  def  ReqQryInvestorPositionDetail(self, pQryInvestorPositionDetail, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInvestorPositionDetail)
        with nogil:
          result = self._api.ReqQryInvestorPositionDetail(<CThostFtdcQryInvestorPositionDetailField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInvestorPositionDetail', exc_info=True)

    return result


  #请求查询客户通知
  def  ReqQryNotice(self, pQryNotice, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryNotice)
        with nogil:
          result = self._api.ReqQryNotice(<CThostFtdcQryNoticeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryNotice', exc_info=True)

    return result


  #请求查询结算信息确认
  def  ReqQrySettlementInfoConfirm(self, pQrySettlementInfoConfirm, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQrySettlementInfoConfirm)
        with nogil:
          result = self._api.ReqQrySettlementInfoConfirm(<CThostFtdcQrySettlementInfoConfirmField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQrySettlementInfoConfirm', exc_info=True)

    return result


  #请求查询投资者持仓明细
  def  ReqQryInvestorPositionCombineDetail(self, pQryInvestorPositionCombineDetail, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInvestorPositionCombineDetail)
        with nogil:
          result = self._api.ReqQryInvestorPositionCombineDetail(<CThostFtdcQryInvestorPositionCombineDetailField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInvestorPositionCombineDetail', exc_info=True)

    return result


  #请求查询保证金监管系统经纪公司资金账户密钥
  def  ReqQryCFMMCTradingAccountKey(self, pQryCFMMCTradingAccountKey, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryCFMMCTradingAccountKey)
        with nogil:
          result = self._api.ReqQryCFMMCTradingAccountKey(<CThostFtdcQryCFMMCTradingAccountKeyField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryCFMMCTradingAccountKey', exc_info=True)

    return result


  #请求查询仓单折抵信息
  def  ReqQryEWarrantOffset(self, pQryEWarrantOffset, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryEWarrantOffset)
        with nogil:
          result = self._api.ReqQryEWarrantOffset(<CThostFtdcQryEWarrantOffsetField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryEWarrantOffset', exc_info=True)

    return result


  #请求查询投资者品种/跨品种保证金
  def  ReqQryInvestorProductGroupMargin(self, pQryInvestorProductGroupMargin, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInvestorProductGroupMargin)
        with nogil:
          result = self._api.ReqQryInvestorProductGroupMargin(<CThostFtdcQryInvestorProductGroupMarginField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInvestorProductGroupMargin', exc_info=True)

    return result


  #请求查询交易所保证金率
  def  ReqQryExchangeMarginRate(self, pQryExchangeMarginRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryExchangeMarginRate)
        with nogil:
          result = self._api.ReqQryExchangeMarginRate(<CThostFtdcQryExchangeMarginRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryExchangeMarginRate', exc_info=True)

    return result


  #请求查询交易所调整保证金率
  def  ReqQryExchangeMarginRateAdjust(self, pQryExchangeMarginRateAdjust, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryExchangeMarginRateAdjust)
        with nogil:
          result = self._api.ReqQryExchangeMarginRateAdjust(<CThostFtdcQryExchangeMarginRateAdjustField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryExchangeMarginRateAdjust', exc_info=True)

    return result


  #请求查询汇率
  def  ReqQryExchangeRate(self, pQryExchangeRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryExchangeRate)
        with nogil:
          result = self._api.ReqQryExchangeRate(<CThostFtdcQryExchangeRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryExchangeRate', exc_info=True)

    return result


  #请求查询二级代理操作员银期权限
  def  ReqQrySecAgentACIDMap(self, pQrySecAgentACIDMap, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQrySecAgentACIDMap)
        with nogil:
          result = self._api.ReqQrySecAgentACIDMap(<CThostFtdcQrySecAgentACIDMapField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQrySecAgentACIDMap', exc_info=True)

    return result


  #请求查询产品报价汇率
  def  ReqQryProductExchRate(self, pQryProductExchRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryProductExchRate)
        with nogil:
          result = self._api.ReqQryProductExchRate(<CThostFtdcQryProductExchRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryProductExchRate', exc_info=True)

    return result


  #请求查询产品组
  def  ReqQryProductGroup(self, pQryProductGroup, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryProductGroup)
        with nogil:
          result = self._api.ReqQryProductGroup(<CThostFtdcQryProductGroupField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryProductGroup', exc_info=True)

    return result


  #请求查询做市商合约手续费率
  def  ReqQryMMInstrumentCommissionRate(self, pQryMMInstrumentCommissionRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryMMInstrumentCommissionRate)
        with nogil:
          result = self._api.ReqQryMMInstrumentCommissionRate(<CThostFtdcQryMMInstrumentCommissionRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryMMInstrumentCommissionRate', exc_info=True)

    return result


  #请求查询做市商期权合约手续费
  def  ReqQryMMOptionInstrCommRate(self, pQryMMOptionInstrCommRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryMMOptionInstrCommRate)
        with nogil:
          result = self._api.ReqQryMMOptionInstrCommRate(<CThostFtdcQryMMOptionInstrCommRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryMMOptionInstrCommRate', exc_info=True)

    return result


  #请求查询报单手续费
  def  ReqQryInstrumentOrderCommRate(self, pQryInstrumentOrderCommRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInstrumentOrderCommRate)
        with nogil:
          result = self._api.ReqQryInstrumentOrderCommRate(<CThostFtdcQryInstrumentOrderCommRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInstrumentOrderCommRate', exc_info=True)

    return result


  #请求查询资金账户
  def  ReqQrySecAgentTradingAccount(self, pQryTradingAccount, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTradingAccount)
        with nogil:
          result = self._api.ReqQrySecAgentTradingAccount(<CThostFtdcQryTradingAccountField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQrySecAgentTradingAccount', exc_info=True)

    return result


  #请求查询二级代理商资金校验模式
  def  ReqQrySecAgentCheckMode(self, pQrySecAgentCheckMode, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQrySecAgentCheckMode)
        with nogil:
          result = self._api.ReqQrySecAgentCheckMode(<CThostFtdcQrySecAgentCheckModeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQrySecAgentCheckMode', exc_info=True)

    return result


  #请求查询期权交易成本
  def  ReqQryOptionInstrTradeCost(self, pQryOptionInstrTradeCost, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryOptionInstrTradeCost)
        with nogil:
          result = self._api.ReqQryOptionInstrTradeCost(<CThostFtdcQryOptionInstrTradeCostField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryOptionInstrTradeCost', exc_info=True)

    return result


  #请求查询期权合约手续费
  def  ReqQryOptionInstrCommRate(self, pQryOptionInstrCommRate, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryOptionInstrCommRate)
        with nogil:
          result = self._api.ReqQryOptionInstrCommRate(<CThostFtdcQryOptionInstrCommRateField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryOptionInstrCommRate', exc_info=True)

    return result


  #请求查询执行宣告
  def  ReqQryExecOrder(self, pQryExecOrder, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryExecOrder)
        with nogil:
          result = self._api.ReqQryExecOrder(<CThostFtdcQryExecOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryExecOrder', exc_info=True)

    return result


  #请求查询询价
  def  ReqQryForQuote(self, pQryForQuote, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryForQuote)
        with nogil:
          result = self._api.ReqQryForQuote(<CThostFtdcQryForQuoteField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryForQuote', exc_info=True)

    return result


  #请求查询报价
  def  ReqQryQuote(self, pQryQuote, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryQuote)
        with nogil:
          result = self._api.ReqQryQuote(<CThostFtdcQryQuoteField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryQuote', exc_info=True)

    return result


  #请求查询期权自对冲
  def  ReqQryOptionSelfClose(self, pQryOptionSelfClose, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryOptionSelfClose)
        with nogil:
          result = self._api.ReqQryOptionSelfClose(<CThostFtdcQryOptionSelfCloseField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryOptionSelfClose', exc_info=True)

    return result


  #请求查询投资单元
  def  ReqQryInvestUnit(self, pQryInvestUnit, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryInvestUnit)
        with nogil:
          result = self._api.ReqQryInvestUnit(<CThostFtdcQryInvestUnitField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryInvestUnit', exc_info=True)

    return result


  #请求查询组合合约安全系数
  def  ReqQryCombInstrumentGuard(self, pQryCombInstrumentGuard, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryCombInstrumentGuard)
        with nogil:
          result = self._api.ReqQryCombInstrumentGuard(<CThostFtdcQryCombInstrumentGuardField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryCombInstrumentGuard', exc_info=True)

    return result


  #请求查询申请组合
  def  ReqQryCombAction(self, pQryCombAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryCombAction)
        with nogil:
          result = self._api.ReqQryCombAction(<CThostFtdcQryCombActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryCombAction', exc_info=True)

    return result


  #请求查询转帐流水
  def  ReqQryTransferSerial(self, pQryTransferSerial, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTransferSerial)
        with nogil:
          result = self._api.ReqQryTransferSerial(<CThostFtdcQryTransferSerialField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryTransferSerial', exc_info=True)

    return result


  #请求查询银期签约关系
  def  ReqQryAccountregister(self, pQryAccountregister, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryAccountregister)
        with nogil:
          result = self._api.ReqQryAccountregister(<CThostFtdcQryAccountregisterField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryAccountregister', exc_info=True)

    return result


  #请求查询签约银行
  def  ReqQryContractBank(self, pQryContractBank, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryContractBank)
        with nogil:
          result = self._api.ReqQryContractBank(<CThostFtdcQryContractBankField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryContractBank', exc_info=True)

    return result


  #请求查询预埋单
  def  ReqQryParkedOrder(self, pQryParkedOrder, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryParkedOrder)
        with nogil:
          result = self._api.ReqQryParkedOrder(<CThostFtdcQryParkedOrderField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryParkedOrder', exc_info=True)

    return result


  #请求查询预埋撤单
  def  ReqQryParkedOrderAction(self, pQryParkedOrderAction, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryParkedOrderAction)
        with nogil:
          result = self._api.ReqQryParkedOrderAction(<CThostFtdcQryParkedOrderActionField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryParkedOrderAction', exc_info=True)

    return result


  #请求查询交易通知
  def  ReqQryTradingNotice(self, pQryTradingNotice, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryTradingNotice)
        with nogil:
          result = self._api.ReqQryTradingNotice(<CThostFtdcQryTradingNoticeField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryTradingNotice', exc_info=True)

    return result


  #请求查询经纪公司交易参数
  def  ReqQryBrokerTradingParams(self, pQryBrokerTradingParams, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryBrokerTradingParams)
        with nogil:
          result = self._api.ReqQryBrokerTradingParams(<CThostFtdcQryBrokerTradingParamsField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryBrokerTradingParams', exc_info=True)

    return result


  #请求查询经纪公司交易算法
  def  ReqQryBrokerTradingAlgos(self, pQryBrokerTradingAlgos, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQryBrokerTradingAlgos)
        with nogil:
          result = self._api.ReqQryBrokerTradingAlgos(<CThostFtdcQryBrokerTradingAlgosField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQryBrokerTradingAlgos', exc_info=True)

    return result


  #请求查询监控中心用户令牌
  def  ReqQueryCFMMCTradingAccountToken(self, pQueryCFMMCTradingAccountToken, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pQueryCFMMCTradingAccountToken)
        with nogil:
          result = self._api.ReqQueryCFMMCTradingAccountToken(<CThostFtdcQueryCFMMCTradingAccountTokenField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQueryCFMMCTradingAccountToken', exc_info=True)

    return result


  #期货发起银行资金转期货请求
  def  ReqFromBankToFutureByFuture(self, pReqTransfer, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pReqTransfer)
        with nogil:
          result = self._api.ReqFromBankToFutureByFuture(<CThostFtdcReqTransferField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqFromBankToFutureByFuture', exc_info=True)

    return result


  #期货发起期货资金转银行请求
  def  ReqFromFutureToBankByFuture(self, pReqTransfer, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

         
      if self._api is not NULL:
        address = ctypes.addressof(pReqTransfer)
        with nogil:
          result = self._api.ReqFromFutureToBankByFuture(<CThostFtdcReqTransferField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqFromFutureToBankByFuture', exc_info=True)

    return result


  #期货发起查询银行余额请求
  def  ReqQueryBankAccountMoneyByFuture(self, pReqQueryAccount, int nRequestID):

    cdef int result = 0
    cdef size_t address = 0
    try:
      dwTime  = self.Inc_RequestID()
      funName = "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
      printString("TraderApicall_stack","call->",funName,dwTime)

      if self._api is not NULL:
        address = ctypes.addressof(pReqQueryAccount)
        with nogil:
          result = self._api.ReqQueryBankAccountMoneyByFuture(<CThostFtdcReqQueryAccountField *> address, nRequestID)

      printString("TraderApicall_stack","call-<",funName, dwTime)
    except Exception as err:
      myEnv.logger.error('ReqQueryBankAccountMoneyByFuture', exc_info=True)

    return result


"""
当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
"""
cdef extern int   TraderSpi_OnFrontConnected(self) except -1:

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
cdef extern int   TraderSpi_OnFrontDisconnected(self
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
cdef extern int   TraderSpi_OnHeartBeatWarning(self
    , int nTimeLapse) except -1:

  try:
      self.OnHeartBeatWarning(nTimeLapse)
  except Exception as err:
      myEnv.logger.error('OnHeartBeatWarning', exc_info=True)

  return 0


"""
客户端认证响应
"""
cdef extern int   TraderSpi_OnRspAuthenticate(self
    , CThostFtdcRspAuthenticateField *pRspAuthenticateField
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRspAuthenticateField != NULL:
      self.OnRspAuthenticate(None if pRspAuthenticateField is NULL else py_ApiStructure.RspAuthenticateField.from_address(<size_t> pRspAuthenticateField)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspAuthenticate', exc_info=True)

  return 0


"""
登录请求响应
"""
cdef extern int   TraderSpi_OnRspUserLogin(self
    , CThostFtdcRspUserLoginField *pRspUserLogin
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRspUserLogin != NULL:
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
cdef extern int   TraderSpi_OnRspUserLogout(self
    , CThostFtdcUserLogoutField *pUserLogout
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pUserLogout != NULL:
      self.OnRspUserLogout(None if pUserLogout is NULL else py_ApiStructure.UserLogoutField.from_address(<size_t> pUserLogout)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspUserLogout', exc_info=True)

  return 0


"""
用户口令更新请求响应
"""
cdef extern int   TraderSpi_OnRspUserPasswordUpdate(self
    , CThostFtdcUserPasswordUpdateField *pUserPasswordUpdate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pUserPasswordUpdate != NULL:
      self.OnRspUserPasswordUpdate(None if pUserPasswordUpdate is NULL else py_ApiStructure.UserPasswordUpdateField.from_address(<size_t> pUserPasswordUpdate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspUserPasswordUpdate', exc_info=True)

  return 0


"""
资金账户口令更新请求响应
"""
cdef extern int   TraderSpi_OnRspTradingAccountPasswordUpdate(self
    , CThostFtdcTradingAccountPasswordUpdateField *pTradingAccountPasswordUpdate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTradingAccountPasswordUpdate != NULL:
      self.OnRspTradingAccountPasswordUpdate(None if pTradingAccountPasswordUpdate is NULL else py_ApiStructure.TradingAccountPasswordUpdateField.from_address(<size_t> pTradingAccountPasswordUpdate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspTradingAccountPasswordUpdate', exc_info=True)

  return 0


"""
报单录入请求响应
"""
cdef extern int   TraderSpi_OnRspOrderInsert(self
    , CThostFtdcInputOrderField *pInputOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputOrder != NULL:
      self.OnRspOrderInsert(None if pInputOrder is NULL else py_ApiStructure.InputOrderField.from_address(<size_t> pInputOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspOrderInsert', exc_info=True)

  return 0


"""
预埋单录入请求响应
"""
cdef extern int   TraderSpi_OnRspParkedOrderInsert(self
    , CThostFtdcParkedOrderField *pParkedOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pParkedOrder != NULL:
      self.OnRspParkedOrderInsert(None if pParkedOrder is NULL else py_ApiStructure.ParkedOrderField.from_address(<size_t> pParkedOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspParkedOrderInsert', exc_info=True)

  return 0


"""
预埋撤单录入请求响应
"""
cdef extern int   TraderSpi_OnRspParkedOrderAction(self
    , CThostFtdcParkedOrderActionField *pParkedOrderAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pParkedOrderAction != NULL:
      self.OnRspParkedOrderAction(None if pParkedOrderAction is NULL else py_ApiStructure.ParkedOrderActionField.from_address(<size_t> pParkedOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspParkedOrderAction', exc_info=True)

  return 0


"""
报单操作请求响应
"""
cdef extern int   TraderSpi_OnRspOrderAction(self
    , CThostFtdcInputOrderActionField *pInputOrderAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputOrderAction != NULL:
      self.OnRspOrderAction(None if pInputOrderAction is NULL else py_ApiStructure.InputOrderActionField.from_address(<size_t> pInputOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspOrderAction', exc_info=True)

  return 0


"""
查询最大报单数量响应
"""
cdef extern int   TraderSpi_OnRspQueryMaxOrderVolume(self
    , CThostFtdcQueryMaxOrderVolumeField *pQueryMaxOrderVolume
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pQueryMaxOrderVolume != NULL:
      self.OnRspQueryMaxOrderVolume(None if pQueryMaxOrderVolume is NULL else py_ApiStructure.QueryMaxOrderVolumeField.from_address(<size_t> pQueryMaxOrderVolume)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQueryMaxOrderVolume', exc_info=True)

  return 0


"""
投资者结算结果确认响应
"""
cdef extern int   TraderSpi_OnRspSettlementInfoConfirm(self
    , CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSettlementInfoConfirm != NULL:
      self.OnRspSettlementInfoConfirm(None if pSettlementInfoConfirm is NULL else py_ApiStructure.SettlementInfoConfirmField.from_address(<size_t> pSettlementInfoConfirm)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspSettlementInfoConfirm', exc_info=True)

  return 0


"""
删除预埋单响应
"""
cdef extern int   TraderSpi_OnRspRemoveParkedOrder(self
    , CThostFtdcRemoveParkedOrderField *pRemoveParkedOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRemoveParkedOrder != NULL:
      self.OnRspRemoveParkedOrder(None if pRemoveParkedOrder is NULL else py_ApiStructure.RemoveParkedOrderField.from_address(<size_t> pRemoveParkedOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspRemoveParkedOrder', exc_info=True)

  return 0


"""
删除预埋撤单响应
"""
cdef extern int   TraderSpi_OnRspRemoveParkedOrderAction(self
    , CThostFtdcRemoveParkedOrderActionField *pRemoveParkedOrderAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRemoveParkedOrderAction != NULL:
      self.OnRspRemoveParkedOrderAction(None if pRemoveParkedOrderAction is NULL else py_ApiStructure.RemoveParkedOrderActionField.from_address(<size_t> pRemoveParkedOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspRemoveParkedOrderAction', exc_info=True)

  return 0


"""
执行宣告录入请求响应
"""
cdef extern int   TraderSpi_OnRspExecOrderInsert(self
    , CThostFtdcInputExecOrderField *pInputExecOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputExecOrder != NULL:
      self.OnRspExecOrderInsert(None if pInputExecOrder is NULL else py_ApiStructure.InputExecOrderField.from_address(<size_t> pInputExecOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspExecOrderInsert', exc_info=True)

  return 0


"""
执行宣告操作请求响应
"""
cdef extern int   TraderSpi_OnRspExecOrderAction(self
    , CThostFtdcInputExecOrderActionField *pInputExecOrderAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputExecOrderAction != NULL:
      self.OnRspExecOrderAction(None if pInputExecOrderAction is NULL else py_ApiStructure.InputExecOrderActionField.from_address(<size_t> pInputExecOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspExecOrderAction', exc_info=True)

  return 0


"""
询价录入请求响应
"""
cdef extern int   TraderSpi_OnRspForQuoteInsert(self
    , CThostFtdcInputForQuoteField *pInputForQuote
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputForQuote != NULL:
      self.OnRspForQuoteInsert(None if pInputForQuote is NULL else py_ApiStructure.InputForQuoteField.from_address(<size_t> pInputForQuote)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspForQuoteInsert', exc_info=True)

  return 0


"""
报价录入请求响应
"""
cdef extern int   TraderSpi_OnRspQuoteInsert(self
    , CThostFtdcInputQuoteField *pInputQuote
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputQuote != NULL:
      self.OnRspQuoteInsert(None if pInputQuote is NULL else py_ApiStructure.InputQuoteField.from_address(<size_t> pInputQuote)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQuoteInsert', exc_info=True)

  return 0


"""
报价操作请求响应
"""
cdef extern int   TraderSpi_OnRspQuoteAction(self
    , CThostFtdcInputQuoteActionField *pInputQuoteAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputQuoteAction != NULL:
      self.OnRspQuoteAction(None if pInputQuoteAction is NULL else py_ApiStructure.InputQuoteActionField.from_address(<size_t> pInputQuoteAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQuoteAction', exc_info=True)

  return 0


"""
批量报单操作请求响应
"""
cdef extern int   TraderSpi_OnRspBatchOrderAction(self
    , CThostFtdcInputBatchOrderActionField *pInputBatchOrderAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputBatchOrderAction != NULL:
      self.OnRspBatchOrderAction(None if pInputBatchOrderAction is NULL else py_ApiStructure.InputBatchOrderActionField.from_address(<size_t> pInputBatchOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspBatchOrderAction', exc_info=True)

  return 0


"""
期权自对冲录入请求响应
"""
cdef extern int   TraderSpi_OnRspOptionSelfCloseInsert(self
    , CThostFtdcInputOptionSelfCloseField *pInputOptionSelfClose
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputOptionSelfClose != NULL:
      self.OnRspOptionSelfCloseInsert(None if pInputOptionSelfClose is NULL else py_ApiStructure.InputOptionSelfCloseField.from_address(<size_t> pInputOptionSelfClose)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspOptionSelfCloseInsert', exc_info=True)

  return 0


"""
期权自对冲操作请求响应
"""
cdef extern int   TraderSpi_OnRspOptionSelfCloseAction(self
    , CThostFtdcInputOptionSelfCloseActionField *pInputOptionSelfCloseAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputOptionSelfCloseAction != NULL:
      self.OnRspOptionSelfCloseAction(None if pInputOptionSelfCloseAction is NULL else py_ApiStructure.InputOptionSelfCloseActionField.from_address(<size_t> pInputOptionSelfCloseAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspOptionSelfCloseAction', exc_info=True)

  return 0


"""
申请组合录入请求响应
"""
cdef extern int   TraderSpi_OnRspCombActionInsert(self
    , CThostFtdcInputCombActionField *pInputCombAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInputCombAction != NULL:
      self.OnRspCombActionInsert(None if pInputCombAction is NULL else py_ApiStructure.InputCombActionField.from_address(<size_t> pInputCombAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspCombActionInsert', exc_info=True)

  return 0


"""
请求查询报单响应
"""
cdef extern int   TraderSpi_OnRspQryOrder(self
    , CThostFtdcOrderField *pOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pOrder != NULL:
      self.OnRspQryOrder(None if pOrder is NULL else py_ApiStructure.OrderField.from_address(<size_t> pOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryOrder', exc_info=True)

  return 0


"""
请求查询成交响应
"""
cdef extern int   TraderSpi_OnRspQryTrade(self
    , CThostFtdcTradeField *pTrade
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTrade != NULL:
      self.OnRspQryTrade(None if pTrade is NULL else py_ApiStructure.TradeField.from_address(<size_t> pTrade)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryTrade', exc_info=True)

  return 0


"""
请求查询投资者持仓响应
"""
cdef extern int   TraderSpi_OnRspQryInvestorPosition(self
    , CThostFtdcInvestorPositionField *pInvestorPosition
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInvestorPosition != NULL:
      self.OnRspQryInvestorPosition(None if pInvestorPosition is NULL else py_ApiStructure.InvestorPositionField.from_address(<size_t> pInvestorPosition)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInvestorPosition', exc_info=True)

  return 0


"""
请求查询资金账户响应
"""
cdef extern int   TraderSpi_OnRspQryTradingAccount(self
    , CThostFtdcTradingAccountField *pTradingAccount
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTradingAccount != NULL:
      self.OnRspQryTradingAccount(None if pTradingAccount is NULL else py_ApiStructure.TradingAccountField.from_address(<size_t> pTradingAccount)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryTradingAccount', exc_info=True)

  return 0


"""
请求查询投资者响应
"""
cdef extern int   TraderSpi_OnRspQryInvestor(self
    , CThostFtdcInvestorField *pInvestor
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInvestor != NULL:
      self.OnRspQryInvestor(None if pInvestor is NULL else py_ApiStructure.InvestorField.from_address(<size_t> pInvestor)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInvestor', exc_info=True)

  return 0


"""
请求查询交易编码响应
"""
cdef extern int   TraderSpi_OnRspQryTradingCode(self
    , CThostFtdcTradingCodeField *pTradingCode
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTradingCode != NULL:
      self.OnRspQryTradingCode(None if pTradingCode is NULL else py_ApiStructure.TradingCodeField.from_address(<size_t> pTradingCode)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryTradingCode', exc_info=True)

  return 0


"""
请求查询合约保证金率响应
"""
cdef extern int   TraderSpi_OnRspQryInstrumentMarginRate(self
    , CThostFtdcInstrumentMarginRateField *pInstrumentMarginRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInstrumentMarginRate != NULL:
      self.OnRspQryInstrumentMarginRate(None if pInstrumentMarginRate is NULL else py_ApiStructure.InstrumentMarginRateField.from_address(<size_t> pInstrumentMarginRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInstrumentMarginRate', exc_info=True)

  return 0


"""
请求查询合约手续费率响应
"""
cdef extern int   TraderSpi_OnRspQryInstrumentCommissionRate(self
    , CThostFtdcInstrumentCommissionRateField *pInstrumentCommissionRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInstrumentCommissionRate != NULL:
      self.OnRspQryInstrumentCommissionRate(None if pInstrumentCommissionRate is NULL else py_ApiStructure.InstrumentCommissionRateField.from_address(<size_t> pInstrumentCommissionRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInstrumentCommissionRate', exc_info=True)

  return 0


"""
请求查询交易所响应
"""
cdef extern int   TraderSpi_OnRspQryExchange(self
    , CThostFtdcExchangeField *pExchange
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pExchange != NULL:
      self.OnRspQryExchange(None if pExchange is NULL else py_ApiStructure.ExchangeField.from_address(<size_t> pExchange)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryExchange', exc_info=True)

  return 0


"""
请求查询产品响应
"""
cdef extern int   TraderSpi_OnRspQryProduct(self
    , CThostFtdcProductField *pProduct
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pProduct != NULL:
      self.OnRspQryProduct(None if pProduct is NULL else py_ApiStructure.ProductField.from_address(<size_t> pProduct)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryProduct', exc_info=True)

  return 0


"""
请求查询合约响应
"""
cdef extern int   TraderSpi_OnRspQryInstrument(self
    , CThostFtdcInstrumentField *pInstrument
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInstrument != NULL:
      self.OnRspQryInstrument(None if pInstrument is NULL else py_ApiStructure.InstrumentField.from_address(<size_t> pInstrument)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInstrument', exc_info=True)

  return 0


"""
请求查询行情响应
"""
cdef extern int   TraderSpi_OnRspQryDepthMarketData(self
    , CThostFtdcDepthMarketDataField *pDepthMarketData
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pDepthMarketData != NULL:
      self.OnRspQryDepthMarketData(None if pDepthMarketData is NULL else py_ApiStructure.DepthMarketDataField.from_address(<size_t> pDepthMarketData)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryDepthMarketData', exc_info=True)

  return 0


"""
请求查询投资者结算结果响应
"""
cdef extern int   TraderSpi_OnRspQrySettlementInfo(self
    , CThostFtdcSettlementInfoField *pSettlementInfo
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSettlementInfo != NULL:
      self.OnRspQrySettlementInfo(None if pSettlementInfo is NULL else py_ApiStructure.SettlementInfoField.from_address(<size_t> pSettlementInfo)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQrySettlementInfo', exc_info=True)

  return 0


"""
请求查询转帐银行响应
"""
cdef extern int   TraderSpi_OnRspQryTransferBank(self
    , CThostFtdcTransferBankField *pTransferBank
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTransferBank != NULL:
      self.OnRspQryTransferBank(None if pTransferBank is NULL else py_ApiStructure.TransferBankField.from_address(<size_t> pTransferBank)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryTransferBank', exc_info=True)

  return 0


"""
请求查询投资者持仓明细响应
"""
cdef extern int   TraderSpi_OnRspQryInvestorPositionDetail(self
    , CThostFtdcInvestorPositionDetailField *pInvestorPositionDetail
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInvestorPositionDetail != NULL:
      self.OnRspQryInvestorPositionDetail(None if pInvestorPositionDetail is NULL else py_ApiStructure.InvestorPositionDetailField.from_address(<size_t> pInvestorPositionDetail)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInvestorPositionDetail', exc_info=True)

  return 0


"""
请求查询客户通知响应
"""
cdef extern int   TraderSpi_OnRspQryNotice(self
    , CThostFtdcNoticeField *pNotice
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pNotice != NULL:
      self.OnRspQryNotice(None if pNotice is NULL else py_ApiStructure.NoticeField.from_address(<size_t> pNotice)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryNotice', exc_info=True)

  return 0


"""
请求查询结算信息确认响应
"""
cdef extern int   TraderSpi_OnRspQrySettlementInfoConfirm(self
    , CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSettlementInfoConfirm != NULL:
      self.OnRspQrySettlementInfoConfirm(None if pSettlementInfoConfirm is NULL else py_ApiStructure.SettlementInfoConfirmField.from_address(<size_t> pSettlementInfoConfirm)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQrySettlementInfoConfirm', exc_info=True)

  return 0


"""
请求查询投资者持仓明细响应
"""
cdef extern int   TraderSpi_OnRspQryInvestorPositionCombineDetail(self
    , CThostFtdcInvestorPositionCombineDetailField *pInvestorPositionCombineDetail
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInvestorPositionCombineDetail != NULL:
      self.OnRspQryInvestorPositionCombineDetail(None if pInvestorPositionCombineDetail is NULL else py_ApiStructure.InvestorPositionCombineDetailField.from_address(<size_t> pInvestorPositionCombineDetail)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInvestorPositionCombineDetail', exc_info=True)

  return 0


"""
查询保证金监管系统经纪公司资金账户密钥响应
"""
cdef extern int   TraderSpi_OnRspQryCFMMCTradingAccountKey(self
    , CThostFtdcCFMMCTradingAccountKeyField *pCFMMCTradingAccountKey
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pCFMMCTradingAccountKey != NULL:
      self.OnRspQryCFMMCTradingAccountKey(None if pCFMMCTradingAccountKey is NULL else py_ApiStructure.CFMMCTradingAccountKeyField.from_address(<size_t> pCFMMCTradingAccountKey)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryCFMMCTradingAccountKey', exc_info=True)

  return 0


"""
请求查询仓单折抵信息响应
"""
cdef extern int   TraderSpi_OnRspQryEWarrantOffset(self
    , CThostFtdcEWarrantOffsetField *pEWarrantOffset
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pEWarrantOffset != NULL:
      self.OnRspQryEWarrantOffset(None if pEWarrantOffset is NULL else py_ApiStructure.EWarrantOffsetField.from_address(<size_t> pEWarrantOffset)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryEWarrantOffset', exc_info=True)

  return 0


"""
请求查询投资者品种/跨品种保证金响应
"""
cdef extern int   TraderSpi_OnRspQryInvestorProductGroupMargin(self
    , CThostFtdcInvestorProductGroupMarginField *pInvestorProductGroupMargin
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInvestorProductGroupMargin != NULL:
      self.OnRspQryInvestorProductGroupMargin(None if pInvestorProductGroupMargin is NULL else py_ApiStructure.InvestorProductGroupMarginField.from_address(<size_t> pInvestorProductGroupMargin)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInvestorProductGroupMargin', exc_info=True)

  return 0


"""
请求查询交易所保证金率响应
"""
cdef extern int   TraderSpi_OnRspQryExchangeMarginRate(self
    , CThostFtdcExchangeMarginRateField *pExchangeMarginRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pExchangeMarginRate != NULL:
      self.OnRspQryExchangeMarginRate(None if pExchangeMarginRate is NULL else py_ApiStructure.ExchangeMarginRateField.from_address(<size_t> pExchangeMarginRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryExchangeMarginRate', exc_info=True)

  return 0


"""
请求查询交易所调整保证金率响应
"""
cdef extern int   TraderSpi_OnRspQryExchangeMarginRateAdjust(self
    , CThostFtdcExchangeMarginRateAdjustField *pExchangeMarginRateAdjust
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pExchangeMarginRateAdjust != NULL:
      self.OnRspQryExchangeMarginRateAdjust(None if pExchangeMarginRateAdjust is NULL else py_ApiStructure.ExchangeMarginRateAdjustField.from_address(<size_t> pExchangeMarginRateAdjust)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryExchangeMarginRateAdjust', exc_info=True)

  return 0


"""
请求查询汇率响应
"""
cdef extern int   TraderSpi_OnRspQryExchangeRate(self
    , CThostFtdcExchangeRateField *pExchangeRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pExchangeRate != NULL:
      self.OnRspQryExchangeRate(None if pExchangeRate is NULL else py_ApiStructure.ExchangeRateField.from_address(<size_t> pExchangeRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryExchangeRate', exc_info=True)

  return 0


"""
请求查询二级代理操作员银期权限响应
"""
cdef extern int   TraderSpi_OnRspQrySecAgentACIDMap(self
    , CThostFtdcSecAgentACIDMapField *pSecAgentACIDMap
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSecAgentACIDMap != NULL:
      self.OnRspQrySecAgentACIDMap(None if pSecAgentACIDMap is NULL else py_ApiStructure.SecAgentACIDMapField.from_address(<size_t> pSecAgentACIDMap)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQrySecAgentACIDMap', exc_info=True)

  return 0


"""
请求查询产品报价汇率
"""
cdef extern int   TraderSpi_OnRspQryProductExchRate(self
    , CThostFtdcProductExchRateField *pProductExchRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pProductExchRate != NULL:
      self.OnRspQryProductExchRate(None if pProductExchRate is NULL else py_ApiStructure.ProductExchRateField.from_address(<size_t> pProductExchRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryProductExchRate', exc_info=True)

  return 0


"""
请求查询产品组
"""
cdef extern int   TraderSpi_OnRspQryProductGroup(self
    , CThostFtdcProductGroupField *pProductGroup
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pProductGroup != NULL:
      self.OnRspQryProductGroup(None if pProductGroup is NULL else py_ApiStructure.ProductGroupField.from_address(<size_t> pProductGroup)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryProductGroup', exc_info=True)

  return 0


"""
请求查询做市商合约手续费率响应
"""
cdef extern int   TraderSpi_OnRspQryMMInstrumentCommissionRate(self
    , CThostFtdcMMInstrumentCommissionRateField *pMMInstrumentCommissionRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pMMInstrumentCommissionRate != NULL:
      self.OnRspQryMMInstrumentCommissionRate(None if pMMInstrumentCommissionRate is NULL else py_ApiStructure.MMInstrumentCommissionRateField.from_address(<size_t> pMMInstrumentCommissionRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryMMInstrumentCommissionRate', exc_info=True)

  return 0


"""
请求查询做市商期权合约手续费响应
"""
cdef extern int   TraderSpi_OnRspQryMMOptionInstrCommRate(self
    , CThostFtdcMMOptionInstrCommRateField *pMMOptionInstrCommRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pMMOptionInstrCommRate != NULL:
      self.OnRspQryMMOptionInstrCommRate(None if pMMOptionInstrCommRate is NULL else py_ApiStructure.MMOptionInstrCommRateField.from_address(<size_t> pMMOptionInstrCommRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryMMOptionInstrCommRate', exc_info=True)

  return 0


"""
请求查询报单手续费响应
"""
cdef extern int   TraderSpi_OnRspQryInstrumentOrderCommRate(self
    , CThostFtdcInstrumentOrderCommRateField *pInstrumentOrderCommRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInstrumentOrderCommRate != NULL:
      self.OnRspQryInstrumentOrderCommRate(None if pInstrumentOrderCommRate is NULL else py_ApiStructure.InstrumentOrderCommRateField.from_address(<size_t> pInstrumentOrderCommRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInstrumentOrderCommRate', exc_info=True)

  return 0


"""
请求查询资金账户响应
"""
cdef extern int   TraderSpi_OnRspQrySecAgentTradingAccount(self
    , CThostFtdcTradingAccountField *pTradingAccount
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTradingAccount != NULL:
      self.OnRspQrySecAgentTradingAccount(None if pTradingAccount is NULL else py_ApiStructure.TradingAccountField.from_address(<size_t> pTradingAccount)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQrySecAgentTradingAccount', exc_info=True)

  return 0


"""
请求查询二级代理商资金校验模式响应
"""
cdef extern int   TraderSpi_OnRspQrySecAgentCheckMode(self
    , CThostFtdcSecAgentCheckModeField *pSecAgentCheckMode
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pSecAgentCheckMode != NULL:
      self.OnRspQrySecAgentCheckMode(None if pSecAgentCheckMode is NULL else py_ApiStructure.SecAgentCheckModeField.from_address(<size_t> pSecAgentCheckMode)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQrySecAgentCheckMode', exc_info=True)

  return 0


"""
请求查询期权交易成本响应
"""
cdef extern int   TraderSpi_OnRspQryOptionInstrTradeCost(self
    , CThostFtdcOptionInstrTradeCostField *pOptionInstrTradeCost
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pOptionInstrTradeCost != NULL:
      self.OnRspQryOptionInstrTradeCost(None if pOptionInstrTradeCost is NULL else py_ApiStructure.OptionInstrTradeCostField.from_address(<size_t> pOptionInstrTradeCost)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryOptionInstrTradeCost', exc_info=True)

  return 0


"""
请求查询期权合约手续费响应
"""
cdef extern int   TraderSpi_OnRspQryOptionInstrCommRate(self
    , CThostFtdcOptionInstrCommRateField *pOptionInstrCommRate
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pOptionInstrCommRate != NULL:
      self.OnRspQryOptionInstrCommRate(None if pOptionInstrCommRate is NULL else py_ApiStructure.OptionInstrCommRateField.from_address(<size_t> pOptionInstrCommRate)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryOptionInstrCommRate', exc_info=True)

  return 0


"""
请求查询执行宣告响应
"""
cdef extern int   TraderSpi_OnRspQryExecOrder(self
    , CThostFtdcExecOrderField *pExecOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pExecOrder != NULL:
      self.OnRspQryExecOrder(None if pExecOrder is NULL else py_ApiStructure.ExecOrderField.from_address(<size_t> pExecOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryExecOrder', exc_info=True)

  return 0


"""
请求查询询价响应
"""
cdef extern int   TraderSpi_OnRspQryForQuote(self
    , CThostFtdcForQuoteField *pForQuote
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pForQuote != NULL:
      self.OnRspQryForQuote(None if pForQuote is NULL else py_ApiStructure.ForQuoteField.from_address(<size_t> pForQuote)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryForQuote', exc_info=True)

  return 0


"""
请求查询报价响应
"""
cdef extern int   TraderSpi_OnRspQryQuote(self
    , CThostFtdcQuoteField *pQuote
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pQuote != NULL:
      self.OnRspQryQuote(None if pQuote is NULL else py_ApiStructure.QuoteField.from_address(<size_t> pQuote)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryQuote', exc_info=True)

  return 0


"""
请求查询期权自对冲响应
"""
cdef extern int   TraderSpi_OnRspQryOptionSelfClose(self
    , CThostFtdcOptionSelfCloseField *pOptionSelfClose
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pOptionSelfClose != NULL:
      self.OnRspQryOptionSelfClose(None if pOptionSelfClose is NULL else py_ApiStructure.OptionSelfCloseField.from_address(<size_t> pOptionSelfClose)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryOptionSelfClose', exc_info=True)

  return 0


"""
请求查询投资单元响应
"""
cdef extern int   TraderSpi_OnRspQryInvestUnit(self
    , CThostFtdcInvestUnitField *pInvestUnit
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pInvestUnit != NULL:
      self.OnRspQryInvestUnit(None if pInvestUnit is NULL else py_ApiStructure.InvestUnitField.from_address(<size_t> pInvestUnit)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryInvestUnit', exc_info=True)

  return 0


"""
请求查询组合合约安全系数响应
"""
cdef extern int   TraderSpi_OnRspQryCombInstrumentGuard(self
    , CThostFtdcCombInstrumentGuardField *pCombInstrumentGuard
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pCombInstrumentGuard != NULL:
      self.OnRspQryCombInstrumentGuard(None if pCombInstrumentGuard is NULL else py_ApiStructure.CombInstrumentGuardField.from_address(<size_t> pCombInstrumentGuard)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryCombInstrumentGuard', exc_info=True)

  return 0


"""
请求查询申请组合响应
"""
cdef extern int   TraderSpi_OnRspQryCombAction(self
    , CThostFtdcCombActionField *pCombAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pCombAction != NULL:
      self.OnRspQryCombAction(None if pCombAction is NULL else py_ApiStructure.CombActionField.from_address(<size_t> pCombAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryCombAction', exc_info=True)

  return 0


"""
请求查询转帐流水响应
"""
cdef extern int   TraderSpi_OnRspQryTransferSerial(self
    , CThostFtdcTransferSerialField *pTransferSerial
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTransferSerial != NULL:
      self.OnRspQryTransferSerial(None if pTransferSerial is NULL else py_ApiStructure.TransferSerialField.from_address(<size_t> pTransferSerial)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryTransferSerial', exc_info=True)

  return 0


"""
请求查询银期签约关系响应
"""
cdef extern int   TraderSpi_OnRspQryAccountregister(self
    , CThostFtdcAccountregisterField *pAccountregister
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pAccountregister != NULL:
      self.OnRspQryAccountregister(None if pAccountregister is NULL else py_ApiStructure.AccountregisterField.from_address(<size_t> pAccountregister)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryAccountregister', exc_info=True)

  return 0


"""
错误应答
"""
cdef extern int   TraderSpi_OnRspError(self
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pRspInfo != NULL:
      self.OnRspError(None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspError', exc_info=True)

  return 0


"""
报单通知
"""
cdef extern int   TraderSpi_OnRtnOrder(self
    , CThostFtdcOrderField *pOrder) except -1:

  try:
    if pOrder != NULL:
      self.OnRtnOrder(None if pOrder is NULL else py_ApiStructure.OrderField.from_address(<size_t> pOrder))
  except Exception as err:
      myEnv.logger.error('OnRtnOrder', exc_info=True)

  return 0


"""
成交通知
"""
cdef extern int   TraderSpi_OnRtnTrade(self
    , CThostFtdcTradeField *pTrade) except -1:

  try:
    if pTrade != NULL:
      self.OnRtnTrade(None if pTrade is NULL else py_ApiStructure.TradeField.from_address(<size_t> pTrade))
  except Exception as err:
      myEnv.logger.error('OnRtnTrade', exc_info=True)

  return 0


"""
报单录入错误回报
"""
cdef extern int   TraderSpi_OnErrRtnOrderInsert(self
    , CThostFtdcInputOrderField *pInputOrder
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pInputOrder != NULL:
      self.OnErrRtnOrderInsert(None if pInputOrder is NULL else py_ApiStructure.InputOrderField.from_address(<size_t> pInputOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnOrderInsert', exc_info=True)

  return 0


"""
报单操作错误回报
"""
cdef extern int   TraderSpi_OnErrRtnOrderAction(self
    , CThostFtdcOrderActionField *pOrderAction
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pOrderAction != NULL:
      self.OnErrRtnOrderAction(None if pOrderAction is NULL else py_ApiStructure.OrderActionField.from_address(<size_t> pOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnOrderAction', exc_info=True)

  return 0


"""
合约交易状态通知
"""
cdef extern int   TraderSpi_OnRtnInstrumentStatus(self
    , CThostFtdcInstrumentStatusField *pInstrumentStatus) except -1:

  try:
    if pInstrumentStatus != NULL:
      self.OnRtnInstrumentStatus(None if pInstrumentStatus is NULL else py_ApiStructure.InstrumentStatusField.from_address(<size_t> pInstrumentStatus))
  except Exception as err:
      myEnv.logger.error('OnRtnInstrumentStatus', exc_info=True)

  return 0


"""
交易所公告通知
"""
cdef extern int   TraderSpi_OnRtnBulletin(self
    , CThostFtdcBulletinField *pBulletin) except -1:

  try:
    if pBulletin != NULL:
      self.OnRtnBulletin(None if pBulletin is NULL else py_ApiStructure.BulletinField.from_address(<size_t> pBulletin))
  except Exception as err:
      myEnv.logger.error('OnRtnBulletin', exc_info=True)

  return 0


"""
交易通知
"""
cdef extern int   TraderSpi_OnRtnTradingNotice(self
    , CThostFtdcTradingNoticeInfoField *pTradingNoticeInfo) except -1:

  try:
    if pTradingNoticeInfo != NULL:
      self.OnRtnTradingNotice(None if pTradingNoticeInfo is NULL else py_ApiStructure.TradingNoticeInfoField.from_address(<size_t> pTradingNoticeInfo))
  except Exception as err:
      myEnv.logger.error('OnRtnTradingNotice', exc_info=True)

  return 0


"""
提示条件单校验错误
"""
cdef extern int   TraderSpi_OnRtnErrorConditionalOrder(self
    , CThostFtdcErrorConditionalOrderField *pErrorConditionalOrder) except -1:

  try:
    if pErrorConditionalOrder != NULL:
      self.OnRtnErrorConditionalOrder(None if pErrorConditionalOrder is NULL else py_ApiStructure.ErrorConditionalOrderField.from_address(<size_t> pErrorConditionalOrder))
  except Exception as err:
      myEnv.logger.error('OnRtnErrorConditionalOrder', exc_info=True)

  return 0


"""
执行宣告通知
"""
cdef extern int   TraderSpi_OnRtnExecOrder(self
    , CThostFtdcExecOrderField *pExecOrder) except -1:

  try:
    if pExecOrder != NULL:
      self.OnRtnExecOrder(None if pExecOrder is NULL else py_ApiStructure.ExecOrderField.from_address(<size_t> pExecOrder))
  except Exception as err:
      myEnv.logger.error('OnRtnExecOrder', exc_info=True)

  return 0


"""
执行宣告录入错误回报
"""
cdef extern int   TraderSpi_OnErrRtnExecOrderInsert(self
    , CThostFtdcInputExecOrderField *pInputExecOrder
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pInputExecOrder != NULL:
      self.OnErrRtnExecOrderInsert(None if pInputExecOrder is NULL else py_ApiStructure.InputExecOrderField.from_address(<size_t> pInputExecOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnExecOrderInsert', exc_info=True)

  return 0


"""
执行宣告操作错误回报
"""
cdef extern int   TraderSpi_OnErrRtnExecOrderAction(self
    , CThostFtdcExecOrderActionField *pExecOrderAction
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pExecOrderAction != NULL:
      self.OnErrRtnExecOrderAction(None if pExecOrderAction is NULL else py_ApiStructure.ExecOrderActionField.from_address(<size_t> pExecOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnExecOrderAction', exc_info=True)

  return 0


"""
询价录入错误回报
"""
cdef extern int   TraderSpi_OnErrRtnForQuoteInsert(self
    , CThostFtdcInputForQuoteField *pInputForQuote
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pInputForQuote != NULL:
      self.OnErrRtnForQuoteInsert(None if pInputForQuote is NULL else py_ApiStructure.InputForQuoteField.from_address(<size_t> pInputForQuote)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnForQuoteInsert', exc_info=True)

  return 0


"""
报价通知
"""
cdef extern int   TraderSpi_OnRtnQuote(self
    , CThostFtdcQuoteField *pQuote) except -1:

  try:
    if pQuote != NULL:
      self.OnRtnQuote(None if pQuote is NULL else py_ApiStructure.QuoteField.from_address(<size_t> pQuote))
  except Exception as err:
      myEnv.logger.error('OnRtnQuote', exc_info=True)

  return 0


"""
报价录入错误回报
"""
cdef extern int   TraderSpi_OnErrRtnQuoteInsert(self
    , CThostFtdcInputQuoteField *pInputQuote
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pInputQuote != NULL:
      self.OnErrRtnQuoteInsert(None if pInputQuote is NULL else py_ApiStructure.InputQuoteField.from_address(<size_t> pInputQuote)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnQuoteInsert', exc_info=True)

  return 0


"""
报价操作错误回报
"""
cdef extern int   TraderSpi_OnErrRtnQuoteAction(self
    , CThostFtdcQuoteActionField *pQuoteAction
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pQuoteAction != NULL:
      self.OnErrRtnQuoteAction(None if pQuoteAction is NULL else py_ApiStructure.QuoteActionField.from_address(<size_t> pQuoteAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnQuoteAction', exc_info=True)

  return 0


"""
询价通知
"""
cdef extern int   TraderSpi_OnRtnForQuoteRsp(self
    , CThostFtdcForQuoteRspField *pForQuoteRsp) except -1:

  try:
    if pForQuoteRsp != NULL:
      self.OnRtnForQuoteRsp(None if pForQuoteRsp is NULL else py_ApiStructure.ForQuoteRspField.from_address(<size_t> pForQuoteRsp))
  except Exception as err:
      myEnv.logger.error('OnRtnForQuoteRsp', exc_info=True)

  return 0


"""
保证金监控中心用户令牌
"""
cdef extern int   TraderSpi_OnRtnCFMMCTradingAccountToken(self
    , CThostFtdcCFMMCTradingAccountTokenField *pCFMMCTradingAccountToken) except -1:

  try:
    if pCFMMCTradingAccountToken != NULL:
      self.OnRtnCFMMCTradingAccountToken(None if pCFMMCTradingAccountToken is NULL else py_ApiStructure.CFMMCTradingAccountTokenField.from_address(<size_t> pCFMMCTradingAccountToken))
  except Exception as err:
      myEnv.logger.error('OnRtnCFMMCTradingAccountToken', exc_info=True)

  return 0


"""
批量报单操作错误回报
"""
cdef extern int   TraderSpi_OnErrRtnBatchOrderAction(self
    , CThostFtdcBatchOrderActionField *pBatchOrderAction
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pBatchOrderAction != NULL:
      self.OnErrRtnBatchOrderAction(None if pBatchOrderAction is NULL else py_ApiStructure.BatchOrderActionField.from_address(<size_t> pBatchOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnBatchOrderAction', exc_info=True)

  return 0


"""
期权自对冲通知
"""
cdef extern int   TraderSpi_OnRtnOptionSelfClose(self
    , CThostFtdcOptionSelfCloseField *pOptionSelfClose) except -1:

  try:
    if pOptionSelfClose != NULL:
      self.OnRtnOptionSelfClose(None if pOptionSelfClose is NULL else py_ApiStructure.OptionSelfCloseField.from_address(<size_t> pOptionSelfClose))
  except Exception as err:
      myEnv.logger.error('OnRtnOptionSelfClose', exc_info=True)

  return 0


"""
期权自对冲录入错误回报
"""
cdef extern int   TraderSpi_OnErrRtnOptionSelfCloseInsert(self
    , CThostFtdcInputOptionSelfCloseField *pInputOptionSelfClose
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pInputOptionSelfClose != NULL:
      self.OnErrRtnOptionSelfCloseInsert(None if pInputOptionSelfClose is NULL else py_ApiStructure.InputOptionSelfCloseField.from_address(<size_t> pInputOptionSelfClose)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnOptionSelfCloseInsert', exc_info=True)

  return 0


"""
期权自对冲操作错误回报
"""
cdef extern int   TraderSpi_OnErrRtnOptionSelfCloseAction(self
    , CThostFtdcOptionSelfCloseActionField *pOptionSelfCloseAction
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pOptionSelfCloseAction != NULL:
      self.OnErrRtnOptionSelfCloseAction(None if pOptionSelfCloseAction is NULL else py_ApiStructure.OptionSelfCloseActionField.from_address(<size_t> pOptionSelfCloseAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnOptionSelfCloseAction', exc_info=True)

  return 0


"""
申请组合通知
"""
cdef extern int   TraderSpi_OnRtnCombAction(self
    , CThostFtdcCombActionField *pCombAction) except -1:

  try:
    if pCombAction != NULL:
      self.OnRtnCombAction(None if pCombAction is NULL else py_ApiStructure.CombActionField.from_address(<size_t> pCombAction))
  except Exception as err:
      myEnv.logger.error('OnRtnCombAction', exc_info=True)

  return 0


"""
申请组合录入错误回报
"""
cdef extern int   TraderSpi_OnErrRtnCombActionInsert(self
    , CThostFtdcInputCombActionField *pInputCombAction
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pInputCombAction != NULL:
      self.OnErrRtnCombActionInsert(None if pInputCombAction is NULL else py_ApiStructure.InputCombActionField.from_address(<size_t> pInputCombAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnCombActionInsert', exc_info=True)

  return 0


"""
请求查询签约银行响应
"""
cdef extern int   TraderSpi_OnRspQryContractBank(self
    , CThostFtdcContractBankField *pContractBank
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pContractBank != NULL:
      self.OnRspQryContractBank(None if pContractBank is NULL else py_ApiStructure.ContractBankField.from_address(<size_t> pContractBank)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryContractBank', exc_info=True)

  return 0


"""
请求查询预埋单响应
"""
cdef extern int   TraderSpi_OnRspQryParkedOrder(self
    , CThostFtdcParkedOrderField *pParkedOrder
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pParkedOrder != NULL:
      self.OnRspQryParkedOrder(None if pParkedOrder is NULL else py_ApiStructure.ParkedOrderField.from_address(<size_t> pParkedOrder)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryParkedOrder', exc_info=True)

  return 0


"""
请求查询预埋撤单响应
"""
cdef extern int   TraderSpi_OnRspQryParkedOrderAction(self
    , CThostFtdcParkedOrderActionField *pParkedOrderAction
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pParkedOrderAction != NULL:
      self.OnRspQryParkedOrderAction(None if pParkedOrderAction is NULL else py_ApiStructure.ParkedOrderActionField.from_address(<size_t> pParkedOrderAction)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryParkedOrderAction', exc_info=True)

  return 0


"""
请求查询交易通知响应
"""
cdef extern int   TraderSpi_OnRspQryTradingNotice(self
    , CThostFtdcTradingNoticeField *pTradingNotice
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pTradingNotice != NULL:
      self.OnRspQryTradingNotice(None if pTradingNotice is NULL else py_ApiStructure.TradingNoticeField.from_address(<size_t> pTradingNotice)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryTradingNotice', exc_info=True)

  return 0


"""
请求查询经纪公司交易参数响应
"""
cdef extern int   TraderSpi_OnRspQryBrokerTradingParams(self
    , CThostFtdcBrokerTradingParamsField *pBrokerTradingParams
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pBrokerTradingParams != NULL:
      self.OnRspQryBrokerTradingParams(None if pBrokerTradingParams is NULL else py_ApiStructure.BrokerTradingParamsField.from_address(<size_t> pBrokerTradingParams)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryBrokerTradingParams', exc_info=True)

  return 0


"""
请求查询经纪公司交易算法响应
"""
cdef extern int   TraderSpi_OnRspQryBrokerTradingAlgos(self
    , CThostFtdcBrokerTradingAlgosField *pBrokerTradingAlgos
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pBrokerTradingAlgos != NULL:
      self.OnRspQryBrokerTradingAlgos(None if pBrokerTradingAlgos is NULL else py_ApiStructure.BrokerTradingAlgosField.from_address(<size_t> pBrokerTradingAlgos)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQryBrokerTradingAlgos', exc_info=True)

  return 0


"""
请求查询监控中心用户令牌
"""
cdef extern int   TraderSpi_OnRspQueryCFMMCTradingAccountToken(self
    , CThostFtdcQueryCFMMCTradingAccountTokenField *pQueryCFMMCTradingAccountToken
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pQueryCFMMCTradingAccountToken != NULL:
      self.OnRspQueryCFMMCTradingAccountToken(None if pQueryCFMMCTradingAccountToken is NULL else py_ApiStructure.QueryCFMMCTradingAccountTokenField.from_address(<size_t> pQueryCFMMCTradingAccountToken)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQueryCFMMCTradingAccountToken', exc_info=True)

  return 0


"""
银行发起银行资金转期货通知
"""
cdef extern int   TraderSpi_OnRtnFromBankToFutureByBank(self
    , CThostFtdcRspTransferField *pRspTransfer) except -1:

  try:
    if pRspTransfer != NULL:
      self.OnRtnFromBankToFutureByBank(None if pRspTransfer is NULL else py_ApiStructure.RspTransferField.from_address(<size_t> pRspTransfer))
  except Exception as err:
      myEnv.logger.error('OnRtnFromBankToFutureByBank', exc_info=True)

  return 0


"""
银行发起期货资金转银行通知
"""
cdef extern int   TraderSpi_OnRtnFromFutureToBankByBank(self
    , CThostFtdcRspTransferField *pRspTransfer) except -1:

  try:
    if pRspTransfer != NULL:
      self.OnRtnFromFutureToBankByBank(None if pRspTransfer is NULL else py_ApiStructure.RspTransferField.from_address(<size_t> pRspTransfer))
  except Exception as err:
      myEnv.logger.error('OnRtnFromFutureToBankByBank', exc_info=True)

  return 0


"""
银行发起冲正银行转期货通知
"""
cdef extern int   TraderSpi_OnRtnRepealFromBankToFutureByBank(self
    , CThostFtdcRspRepealField *pRspRepeal) except -1:

  try:
    if pRspRepeal != NULL:
      self.OnRtnRepealFromBankToFutureByBank(None if pRspRepeal is NULL else py_ApiStructure.RspRepealField.from_address(<size_t> pRspRepeal))
  except Exception as err:
      myEnv.logger.error('OnRtnRepealFromBankToFutureByBank', exc_info=True)

  return 0


"""
银行发起冲正期货转银行通知
"""
cdef extern int   TraderSpi_OnRtnRepealFromFutureToBankByBank(self
    , CThostFtdcRspRepealField *pRspRepeal) except -1:

  try:
    if pRspRepeal != NULL:
      self.OnRtnRepealFromFutureToBankByBank(None if pRspRepeal is NULL else py_ApiStructure.RspRepealField.from_address(<size_t> pRspRepeal))
  except Exception as err:
      myEnv.logger.error('OnRtnRepealFromFutureToBankByBank', exc_info=True)

  return 0


"""
期货发起银行资金转期货通知
"""
cdef extern int   TraderSpi_OnRtnFromBankToFutureByFuture(self
    , CThostFtdcRspTransferField *pRspTransfer) except -1:

  try:
    if pRspTransfer != NULL:
      self.OnRtnFromBankToFutureByFuture(None if pRspTransfer is NULL else py_ApiStructure.RspTransferField.from_address(<size_t> pRspTransfer))
  except Exception as err:
      myEnv.logger.error('OnRtnFromBankToFutureByFuture', exc_info=True)

  return 0


"""
期货发起期货资金转银行通知
"""
cdef extern int   TraderSpi_OnRtnFromFutureToBankByFuture(self
    , CThostFtdcRspTransferField *pRspTransfer) except -1:

  try:
    if pRspTransfer != NULL:
      self.OnRtnFromFutureToBankByFuture(None if pRspTransfer is NULL else py_ApiStructure.RspTransferField.from_address(<size_t> pRspTransfer))
  except Exception as err:
      myEnv.logger.error('OnRtnFromFutureToBankByFuture', exc_info=True)

  return 0


"""
系统运行时期货端手工发起冲正银行转期货请求，银行处理完毕后报盘发回的通知
"""
cdef extern int   TraderSpi_OnRtnRepealFromBankToFutureByFutureManual(self
    , CThostFtdcRspRepealField *pRspRepeal) except -1:

  try:
    if pRspRepeal != NULL:
      self.OnRtnRepealFromBankToFutureByFutureManual(None if pRspRepeal is NULL else py_ApiStructure.RspRepealField.from_address(<size_t> pRspRepeal))
  except Exception as err:
      myEnv.logger.error('OnRtnRepealFromBankToFutureByFutureManual', exc_info=True)

  return 0


"""
系统运行时期货端手工发起冲正期货转银行请求，银行处理完毕后报盘发回的通知
"""
cdef extern int   TraderSpi_OnRtnRepealFromFutureToBankByFutureManual(self
    , CThostFtdcRspRepealField *pRspRepeal) except -1:

  try:
    if pRspRepeal != NULL:
      self.OnRtnRepealFromFutureToBankByFutureManual(None if pRspRepeal is NULL else py_ApiStructure.RspRepealField.from_address(<size_t> pRspRepeal))
  except Exception as err:
      myEnv.logger.error('OnRtnRepealFromFutureToBankByFutureManual', exc_info=True)

  return 0


"""
期货发起查询银行余额通知
"""
cdef extern int   TraderSpi_OnRtnQueryBankBalanceByFuture(self
    , CThostFtdcNotifyQueryAccountField *pNotifyQueryAccount) except -1:

  try:
    if pNotifyQueryAccount != NULL:
      self.OnRtnQueryBankBalanceByFuture(None if pNotifyQueryAccount is NULL else py_ApiStructure.NotifyQueryAccountField.from_address(<size_t> pNotifyQueryAccount))
  except Exception as err:
      myEnv.logger.error('OnRtnQueryBankBalanceByFuture', exc_info=True)

  return 0


"""
期货发起银行资金转期货错误回报
"""
cdef extern int   TraderSpi_OnErrRtnBankToFutureByFuture(self
    , CThostFtdcReqTransferField *pReqTransfer
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pReqTransfer != NULL:
      self.OnErrRtnBankToFutureByFuture(None if pReqTransfer is NULL else py_ApiStructure.ReqTransferField.from_address(<size_t> pReqTransfer)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnBankToFutureByFuture', exc_info=True)

  return 0


"""
期货发起期货资金转银行错误回报
"""
cdef extern int   TraderSpi_OnErrRtnFutureToBankByFuture(self
    , CThostFtdcReqTransferField *pReqTransfer
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pReqTransfer != NULL:
      self.OnErrRtnFutureToBankByFuture(None if pReqTransfer is NULL else py_ApiStructure.ReqTransferField.from_address(<size_t> pReqTransfer)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnFutureToBankByFuture', exc_info=True)

  return 0


"""
系统运行时期货端手工发起冲正银行转期货错误回报
"""
cdef extern int   TraderSpi_OnErrRtnRepealBankToFutureByFutureManual(self
    , CThostFtdcReqRepealField *pReqRepeal
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pReqRepeal != NULL:
      self.OnErrRtnRepealBankToFutureByFutureManual(None if pReqRepeal is NULL else py_ApiStructure.ReqRepealField.from_address(<size_t> pReqRepeal)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnRepealBankToFutureByFutureManual', exc_info=True)

  return 0


"""
系统运行时期货端手工发起冲正期货转银行错误回报
"""
cdef extern int   TraderSpi_OnErrRtnRepealFutureToBankByFutureManual(self
    , CThostFtdcReqRepealField *pReqRepeal
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pReqRepeal != NULL:
      self.OnErrRtnRepealFutureToBankByFutureManual(None if pReqRepeal is NULL else py_ApiStructure.ReqRepealField.from_address(<size_t> pReqRepeal)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnRepealFutureToBankByFutureManual', exc_info=True)

  return 0


"""
期货发起查询银行余额错误回报
"""
cdef extern int   TraderSpi_OnErrRtnQueryBankBalanceByFuture(self
    , CThostFtdcReqQueryAccountField *pReqQueryAccount
    , CThostFtdcRspInfoField *pRspInfo) except -1:

  try:
    if pReqQueryAccount != NULL:
      self.OnErrRtnQueryBankBalanceByFuture(None if pReqQueryAccount is NULL else py_ApiStructure.ReqQueryAccountField.from_address(<size_t> pReqQueryAccount)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo))
  except Exception as err:
      myEnv.logger.error('OnErrRtnQueryBankBalanceByFuture', exc_info=True)

  return 0


"""
期货发起冲正银行转期货请求，银行处理完毕后报盘发回的通知
"""
cdef extern int   TraderSpi_OnRtnRepealFromBankToFutureByFuture(self
    , CThostFtdcRspRepealField *pRspRepeal) except -1:

  try:
    if pRspRepeal != NULL:
      self.OnRtnRepealFromBankToFutureByFuture(None if pRspRepeal is NULL else py_ApiStructure.RspRepealField.from_address(<size_t> pRspRepeal))
  except Exception as err:
      myEnv.logger.error('OnRtnRepealFromBankToFutureByFuture', exc_info=True)

  return 0


"""
期货发起冲正期货转银行请求，银行处理完毕后报盘发回的通知
"""
cdef extern int   TraderSpi_OnRtnRepealFromFutureToBankByFuture(self
    , CThostFtdcRspRepealField *pRspRepeal) except -1:

  try:
    if pRspRepeal != NULL:
      self.OnRtnRepealFromFutureToBankByFuture(None if pRspRepeal is NULL else py_ApiStructure.RspRepealField.from_address(<size_t> pRspRepeal))
  except Exception as err:
      myEnv.logger.error('OnRtnRepealFromFutureToBankByFuture', exc_info=True)

  return 0


"""
期货发起银行资金转期货应答
"""
cdef extern int   TraderSpi_OnRspFromBankToFutureByFuture(self
    , CThostFtdcReqTransferField *pReqTransfer
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pReqTransfer != NULL:
      self.OnRspFromBankToFutureByFuture(None if pReqTransfer is NULL else py_ApiStructure.ReqTransferField.from_address(<size_t> pReqTransfer)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspFromBankToFutureByFuture', exc_info=True)

  return 0


"""
期货发起期货资金转银行应答
"""
cdef extern int   TraderSpi_OnRspFromFutureToBankByFuture(self
    , CThostFtdcReqTransferField *pReqTransfer
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pReqTransfer != NULL:
      self.OnRspFromFutureToBankByFuture(None if pReqTransfer is NULL else py_ApiStructure.ReqTransferField.from_address(<size_t> pReqTransfer)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspFromFutureToBankByFuture', exc_info=True)

  return 0


"""
期货发起查询银行余额应答
"""
cdef extern int   TraderSpi_OnRspQueryBankAccountMoneyByFuture(self
    , CThostFtdcReqQueryAccountField *pReqQueryAccount
    , CThostFtdcRspInfoField *pRspInfo
    , int nRequestID
    , cbool bIsLast) except -1:

  try:
    if pReqQueryAccount != NULL:
      self.OnRspQueryBankAccountMoneyByFuture(None if pReqQueryAccount is NULL else py_ApiStructure.ReqQueryAccountField.from_address(<size_t> pReqQueryAccount)
    ,None if pRspInfo is NULL else py_ApiStructure.RspInfoField.from_address(<size_t> pRspInfo)
    ,nRequestID
    ,bIsLast)
  except Exception as err:
      myEnv.logger.error('OnRspQueryBankAccountMoneyByFuture', exc_info=True)

  return 0


"""
银行发起银期开户通知
"""
cdef extern int   TraderSpi_OnRtnOpenAccountByBank(self
    , CThostFtdcOpenAccountField *pOpenAccount) except -1:

  try:
    if pOpenAccount != NULL:
      self.OnRtnOpenAccountByBank(None if pOpenAccount is NULL else py_ApiStructure.OpenAccountField.from_address(<size_t> pOpenAccount))
  except Exception as err:
      myEnv.logger.error('OnRtnOpenAccountByBank', exc_info=True)

  return 0


"""
银行发起银期销户通知
"""
cdef extern int   TraderSpi_OnRtnCancelAccountByBank(self
    , CThostFtdcCancelAccountField *pCancelAccount) except -1:

  try:
    if pCancelAccount != NULL:
      self.OnRtnCancelAccountByBank(None if pCancelAccount is NULL else py_ApiStructure.CancelAccountField.from_address(<size_t> pCancelAccount))
  except Exception as err:
      myEnv.logger.error('OnRtnCancelAccountByBank', exc_info=True)

  return 0


"""
银行发起变更银行账号通知
"""
cdef extern int   TraderSpi_OnRtnChangeAccountByBank(self
    , CThostFtdcChangeAccountField *pChangeAccount) except -1:

  try:
    if pChangeAccount != NULL:
      self.OnRtnChangeAccountByBank(None if pChangeAccount is NULL else py_ApiStructure.ChangeAccountField.from_address(<size_t> pChangeAccount))
  except Exception as err:
      myEnv.logger.error('OnRtnChangeAccountByBank', exc_info=True)

  return 0

