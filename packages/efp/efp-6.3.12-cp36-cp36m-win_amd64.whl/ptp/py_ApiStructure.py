# encoding=utf-8
import ctypes
from ptp.py_base import Base
class DisseminationField(Base):
  """信息分发"""
  _fields_ = [
    ('SequenceSeries',ctypes.c_short)# ///序列系列号
    ,('SequenceNo',ctypes.c_int)# 序列号
]

  def __init__(self,SequenceSeries= 0,SequenceNo=0):

    super(DisseminationField,self).__init__()

    self.SequenceSeries=int(SequenceSeries)
    self.SequenceNo=int(SequenceNo)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.SequenceSeries=int(i_tuple[1])
    self.SequenceNo=int(i_tuple[2])

class ReqUserLoginField(Base):
  """用户登录请求"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Password',ctypes.c_char*41)# 密码
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('InterfaceProductInfo',ctypes.c_char*11)# 接口端产品信息
    ,('ProtocolInfo',ctypes.c_char*11)# 协议信息
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('OneTimePassword',ctypes.c_char*41)# 动态密码
    ,('ClientIPAddress',ctypes.c_char*16)# 终端IP地址
    ,('LoginRemark',ctypes.c_char*36)# 登录备注
]

  def __init__(self,TradingDay= '',BrokerID='',UserID='',Password='',UserProductInfo='',InterfaceProductInfo='',ProtocolInfo='',MacAddress='',OneTimePassword='',ClientIPAddress='',LoginRemark=''):

    super(ReqUserLoginField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.Password=self._to_bytes(Password)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.InterfaceProductInfo=self._to_bytes(InterfaceProductInfo)
    self.ProtocolInfo=self._to_bytes(ProtocolInfo)
    self.MacAddress=self._to_bytes(MacAddress)
    self.OneTimePassword=self._to_bytes(OneTimePassword)
    self.ClientIPAddress=self._to_bytes(ClientIPAddress)
    self.LoginRemark=self._to_bytes(LoginRemark)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.UserID=self._to_bytes(i_tuple[3])
    self.Password=self._to_bytes(i_tuple[4])
    self.UserProductInfo=self._to_bytes(i_tuple[5])
    self.InterfaceProductInfo=self._to_bytes(i_tuple[6])
    self.ProtocolInfo=self._to_bytes(i_tuple[7])
    self.MacAddress=self._to_bytes(i_tuple[8])
    self.OneTimePassword=self._to_bytes(i_tuple[9])
    self.ClientIPAddress=self._to_bytes(i_tuple[10])
    self.LoginRemark=self._to_bytes(i_tuple[11])

class RspUserLoginField(Base):
  """用户登录应答"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('LoginTime',ctypes.c_char*9)# 登录成功时间
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('SystemName',ctypes.c_char*41)# 交易系统名称
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('MaxOrderRef',ctypes.c_char*13)# 最大报单引用
    ,('SHFETime',ctypes.c_char*9)# 上期所时间
    ,('DCETime',ctypes.c_char*9)# 大商所时间
    ,('CZCETime',ctypes.c_char*9)# 郑商所时间
    ,('FFEXTime',ctypes.c_char*9)# 中金所时间
    ,('INETime',ctypes.c_char*9)# 能源中心时间
]

  def __init__(self,TradingDay= '',LoginTime='',BrokerID='',UserID='',SystemName='',FrontID=0,SessionID=0,MaxOrderRef='',SHFETime='',DCETime='',CZCETime='',FFEXTime='',INETime=''):

    super(RspUserLoginField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.LoginTime=self._to_bytes(LoginTime)
    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.SystemName=self._to_bytes(SystemName)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.MaxOrderRef=self._to_bytes(MaxOrderRef)
    self.SHFETime=self._to_bytes(SHFETime)
    self.DCETime=self._to_bytes(DCETime)
    self.CZCETime=self._to_bytes(CZCETime)
    self.FFEXTime=self._to_bytes(FFEXTime)
    self.INETime=self._to_bytes(INETime)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.LoginTime=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.UserID=self._to_bytes(i_tuple[4])
    self.SystemName=self._to_bytes(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.MaxOrderRef=self._to_bytes(i_tuple[8])
    self.SHFETime=self._to_bytes(i_tuple[9])
    self.DCETime=self._to_bytes(i_tuple[10])
    self.CZCETime=self._to_bytes(i_tuple[11])
    self.FFEXTime=self._to_bytes(i_tuple[12])
    self.INETime=self._to_bytes(i_tuple[13])

class UserLogoutField(Base):
  """用户登出请求"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,BrokerID= '',UserID=''):

    super(UserLogoutField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])

class ForceUserLogoutField(Base):
  """强制交易员退出"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,BrokerID= '',UserID=''):

    super(ForceUserLogoutField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])

class ReqAuthenticateField(Base):
  """客户端认证请求"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('AuthCode',ctypes.c_char*17)# 认证码
]

  def __init__(self,BrokerID= '',UserID='',UserProductInfo='',AuthCode=''):

    super(ReqAuthenticateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.AuthCode=self._to_bytes(AuthCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserProductInfo=self._to_bytes(i_tuple[3])
    self.AuthCode=self._to_bytes(i_tuple[4])

class RspAuthenticateField(Base):
  """客户端认证响应"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
]

  def __init__(self,BrokerID= '',UserID='',UserProductInfo=''):

    super(RspAuthenticateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserProductInfo=self._to_bytes(i_tuple[3])

class AuthenticationInfoField(Base):
  """客户端认证信息"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('AuthInfo',ctypes.c_char*129)# 认证信息
    ,('IsResult',ctypes.c_int)# 是否为认证结果
]

  def __init__(self,BrokerID= '',UserID='',UserProductInfo='',AuthInfo='',IsResult=0):

    super(AuthenticationInfoField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.AuthInfo=self._to_bytes(AuthInfo)
    self.IsResult=int(IsResult)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserProductInfo=self._to_bytes(i_tuple[3])
    self.AuthInfo=self._to_bytes(i_tuple[4])
    self.IsResult=int(i_tuple[5])

class RspUserLogin2Field(Base):
  """用户登录应答2"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('LoginTime',ctypes.c_char*9)# 登录成功时间
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('SystemName',ctypes.c_char*41)# 交易系统名称
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('MaxOrderRef',ctypes.c_char*13)# 最大报单引用
    ,('SHFETime',ctypes.c_char*9)# 上期所时间
    ,('DCETime',ctypes.c_char*9)# 大商所时间
    ,('CZCETime',ctypes.c_char*9)# 郑商所时间
    ,('FFEXTime',ctypes.c_char*9)# 中金所时间
    ,('INETime',ctypes.c_char*9)# 能源中心时间
    ,('RandomString',ctypes.c_char*17)# 随机串
]

  def __init__(self,TradingDay= '',LoginTime='',BrokerID='',UserID='',SystemName='',FrontID=0,SessionID=0,MaxOrderRef='',SHFETime='',DCETime='',CZCETime='',FFEXTime='',INETime='',RandomString=''):

    super(RspUserLogin2Field,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.LoginTime=self._to_bytes(LoginTime)
    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.SystemName=self._to_bytes(SystemName)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.MaxOrderRef=self._to_bytes(MaxOrderRef)
    self.SHFETime=self._to_bytes(SHFETime)
    self.DCETime=self._to_bytes(DCETime)
    self.CZCETime=self._to_bytes(CZCETime)
    self.FFEXTime=self._to_bytes(FFEXTime)
    self.INETime=self._to_bytes(INETime)
    self.RandomString=self._to_bytes(RandomString)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.LoginTime=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.UserID=self._to_bytes(i_tuple[4])
    self.SystemName=self._to_bytes(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.MaxOrderRef=self._to_bytes(i_tuple[8])
    self.SHFETime=self._to_bytes(i_tuple[9])
    self.DCETime=self._to_bytes(i_tuple[10])
    self.CZCETime=self._to_bytes(i_tuple[11])
    self.FFEXTime=self._to_bytes(i_tuple[12])
    self.INETime=self._to_bytes(i_tuple[13])
    self.RandomString=self._to_bytes(i_tuple[14])

class TransferHeaderField(Base):
  """银期转帐报文头"""
  _fields_ = [
    ('Version',ctypes.c_char*4)# ///版本号，常量，1.0
    ,('TradeCode',ctypes.c_char*7)# 交易代码，必填
    ,('TradeDate',ctypes.c_char*9)# 交易日期，必填，格式：yyyymmdd
    ,('TradeTime',ctypes.c_char*9)# 交易时间，必填，格式：hhmmss
    ,('TradeSerial',ctypes.c_char*9)# 发起方流水号，N/A
    ,('FutureID',ctypes.c_char*11)# 期货公司代码，必填
    ,('BankID',ctypes.c_char*4)# 银行代码，根据查询银行得到，必填
    ,('BankBrchID',ctypes.c_char*5)# 银行分中心代码，根据查询银行得到，必填
    ,('OperNo',ctypes.c_char*17)# 操作员，N/A
    ,('DeviceID',ctypes.c_char*3)# 交易设备类型，N/A
    ,('RecordNum',ctypes.c_char*7)# 记录数，N/A
    ,('SessionID',ctypes.c_int)# 会话编号，N/A
    ,('RequestID',ctypes.c_int)# 请求编号，N/A
]

  def __init__(self,Version= '',TradeCode='',TradeDate='',TradeTime='',TradeSerial='',FutureID='',BankID='',BankBrchID='',OperNo='',DeviceID='',RecordNum='',SessionID=0,RequestID=0):

    super(TransferHeaderField,self).__init__()

    self.Version=self._to_bytes(Version)
    self.TradeCode=self._to_bytes(TradeCode)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.TradeSerial=self._to_bytes(TradeSerial)
    self.FutureID=self._to_bytes(FutureID)
    self.BankID=self._to_bytes(BankID)
    self.BankBrchID=self._to_bytes(BankBrchID)
    self.OperNo=self._to_bytes(OperNo)
    self.DeviceID=self._to_bytes(DeviceID)
    self.RecordNum=self._to_bytes(RecordNum)
    self.SessionID=int(SessionID)
    self.RequestID=int(RequestID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.Version=self._to_bytes(i_tuple[1])
    self.TradeCode=self._to_bytes(i_tuple[2])
    self.TradeDate=self._to_bytes(i_tuple[3])
    self.TradeTime=self._to_bytes(i_tuple[4])
    self.TradeSerial=self._to_bytes(i_tuple[5])
    self.FutureID=self._to_bytes(i_tuple[6])
    self.BankID=self._to_bytes(i_tuple[7])
    self.BankBrchID=self._to_bytes(i_tuple[8])
    self.OperNo=self._to_bytes(i_tuple[9])
    self.DeviceID=self._to_bytes(i_tuple[10])
    self.RecordNum=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.RequestID=int(i_tuple[13])

class TransferBankToFutureReqField(Base):
  """银行资金转期货请求，TradeCode=202001"""
  _fields_ = [
    ('FutureAccount',ctypes.c_char*13)# ///期货资金账户
    ,('FuturePwdFlag',ctypes.c_char)# 密码标志
    ,('FutureAccPwd',ctypes.c_char*17)# 密码
    ,('TradeAmt',ctypes.c_double)# 转账金额
    ,('CustFee',ctypes.c_double)# 客户手续费
    ,('CurrencyCode',ctypes.c_char*4)# 币种：RMB-人民币 USD-美圆 HKD-港元
]

  def __init__(self,FutureAccount= '',FuturePwdFlag='',FutureAccPwd='',TradeAmt=0.0,CustFee=0.0,CurrencyCode=''):

    super(TransferBankToFutureReqField,self).__init__()

    self.FutureAccount=self._to_bytes(FutureAccount)
    self.FuturePwdFlag=self._to_bytes(FuturePwdFlag)
    self.FutureAccPwd=self._to_bytes(FutureAccPwd)
    self.TradeAmt=float(TradeAmt)
    self.CustFee=float(CustFee)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FutureAccount=self._to_bytes(i_tuple[1])
    self.FuturePwdFlag=self._to_bytes(i_tuple[2])
    self.FutureAccPwd=self._to_bytes(i_tuple[3])
    self.TradeAmt=float(i_tuple[4])
    self.CustFee=float(i_tuple[5])
    self.CurrencyCode=self._to_bytes(i_tuple[6])

class TransferBankToFutureRspField(Base):
  """银行资金转期货请求响应"""
  _fields_ = [
    ('RetCode',ctypes.c_char*5)# ///响应代码
    ,('RetInfo',ctypes.c_char*129)# 响应信息
    ,('FutureAccount',ctypes.c_char*13)# 资金账户
    ,('TradeAmt',ctypes.c_double)# 转帐金额
    ,('CustFee',ctypes.c_double)# 应收客户手续费
    ,('CurrencyCode',ctypes.c_char*4)# 币种
]

  def __init__(self,RetCode= '',RetInfo='',FutureAccount='',TradeAmt=0.0,CustFee=0.0,CurrencyCode=''):

    super(TransferBankToFutureRspField,self).__init__()

    self.RetCode=self._to_bytes(RetCode)
    self.RetInfo=self._to_bytes(RetInfo)
    self.FutureAccount=self._to_bytes(FutureAccount)
    self.TradeAmt=float(TradeAmt)
    self.CustFee=float(CustFee)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.RetCode=self._to_bytes(i_tuple[1])
    self.RetInfo=self._to_bytes(i_tuple[2])
    self.FutureAccount=self._to_bytes(i_tuple[3])
    self.TradeAmt=float(i_tuple[4])
    self.CustFee=float(i_tuple[5])
    self.CurrencyCode=self._to_bytes(i_tuple[6])

class TransferFutureToBankReqField(Base):
  """期货资金转银行请求，TradeCode=202002"""
  _fields_ = [
    ('FutureAccount',ctypes.c_char*13)# ///期货资金账户
    ,('FuturePwdFlag',ctypes.c_char)# 密码标志
    ,('FutureAccPwd',ctypes.c_char*17)# 密码
    ,('TradeAmt',ctypes.c_double)# 转账金额
    ,('CustFee',ctypes.c_double)# 客户手续费
    ,('CurrencyCode',ctypes.c_char*4)# 币种：RMB-人民币 USD-美圆 HKD-港元
]

  def __init__(self,FutureAccount= '',FuturePwdFlag='',FutureAccPwd='',TradeAmt=0.0,CustFee=0.0,CurrencyCode=''):

    super(TransferFutureToBankReqField,self).__init__()

    self.FutureAccount=self._to_bytes(FutureAccount)
    self.FuturePwdFlag=self._to_bytes(FuturePwdFlag)
    self.FutureAccPwd=self._to_bytes(FutureAccPwd)
    self.TradeAmt=float(TradeAmt)
    self.CustFee=float(CustFee)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FutureAccount=self._to_bytes(i_tuple[1])
    self.FuturePwdFlag=self._to_bytes(i_tuple[2])
    self.FutureAccPwd=self._to_bytes(i_tuple[3])
    self.TradeAmt=float(i_tuple[4])
    self.CustFee=float(i_tuple[5])
    self.CurrencyCode=self._to_bytes(i_tuple[6])

class TransferFutureToBankRspField(Base):
  """期货资金转银行请求响应"""
  _fields_ = [
    ('RetCode',ctypes.c_char*5)# ///响应代码
    ,('RetInfo',ctypes.c_char*129)# 响应信息
    ,('FutureAccount',ctypes.c_char*13)# 资金账户
    ,('TradeAmt',ctypes.c_double)# 转帐金额
    ,('CustFee',ctypes.c_double)# 应收客户手续费
    ,('CurrencyCode',ctypes.c_char*4)# 币种
]

  def __init__(self,RetCode= '',RetInfo='',FutureAccount='',TradeAmt=0.0,CustFee=0.0,CurrencyCode=''):

    super(TransferFutureToBankRspField,self).__init__()

    self.RetCode=self._to_bytes(RetCode)
    self.RetInfo=self._to_bytes(RetInfo)
    self.FutureAccount=self._to_bytes(FutureAccount)
    self.TradeAmt=float(TradeAmt)
    self.CustFee=float(CustFee)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.RetCode=self._to_bytes(i_tuple[1])
    self.RetInfo=self._to_bytes(i_tuple[2])
    self.FutureAccount=self._to_bytes(i_tuple[3])
    self.TradeAmt=float(i_tuple[4])
    self.CustFee=float(i_tuple[5])
    self.CurrencyCode=self._to_bytes(i_tuple[6])

class TransferQryBankReqField(Base):
  """查询银行资金请求，TradeCode=204002"""
  _fields_ = [
    ('FutureAccount',ctypes.c_char*13)# ///期货资金账户
    ,('FuturePwdFlag',ctypes.c_char)# 密码标志
    ,('FutureAccPwd',ctypes.c_char*17)# 密码
    ,('CurrencyCode',ctypes.c_char*4)# 币种：RMB-人民币 USD-美圆 HKD-港元
]

  def __init__(self,FutureAccount= '',FuturePwdFlag='',FutureAccPwd='',CurrencyCode=''):

    super(TransferQryBankReqField,self).__init__()

    self.FutureAccount=self._to_bytes(FutureAccount)
    self.FuturePwdFlag=self._to_bytes(FuturePwdFlag)
    self.FutureAccPwd=self._to_bytes(FutureAccPwd)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FutureAccount=self._to_bytes(i_tuple[1])
    self.FuturePwdFlag=self._to_bytes(i_tuple[2])
    self.FutureAccPwd=self._to_bytes(i_tuple[3])
    self.CurrencyCode=self._to_bytes(i_tuple[4])

class TransferQryBankRspField(Base):
  """查询银行资金请求响应"""
  _fields_ = [
    ('RetCode',ctypes.c_char*5)# ///响应代码
    ,('RetInfo',ctypes.c_char*129)# 响应信息
    ,('FutureAccount',ctypes.c_char*13)# 资金账户
    ,('TradeAmt',ctypes.c_double)# 银行余额
    ,('UseAmt',ctypes.c_double)# 银行可用余额
    ,('FetchAmt',ctypes.c_double)# 银行可取余额
    ,('CurrencyCode',ctypes.c_char*4)# 币种
]

  def __init__(self,RetCode= '',RetInfo='',FutureAccount='',TradeAmt=0.0,UseAmt=0.0,FetchAmt=0.0,CurrencyCode=''):

    super(TransferQryBankRspField,self).__init__()

    self.RetCode=self._to_bytes(RetCode)
    self.RetInfo=self._to_bytes(RetInfo)
    self.FutureAccount=self._to_bytes(FutureAccount)
    self.TradeAmt=float(TradeAmt)
    self.UseAmt=float(UseAmt)
    self.FetchAmt=float(FetchAmt)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.RetCode=self._to_bytes(i_tuple[1])
    self.RetInfo=self._to_bytes(i_tuple[2])
    self.FutureAccount=self._to_bytes(i_tuple[3])
    self.TradeAmt=float(i_tuple[4])
    self.UseAmt=float(i_tuple[5])
    self.FetchAmt=float(i_tuple[6])
    self.CurrencyCode=self._to_bytes(i_tuple[7])

class TransferQryDetailReqField(Base):
  """查询银行交易明细请求，TradeCode=204999"""
  _fields_ = [
    ('FutureAccount',ctypes.c_char*13)# ///期货资金账户
]

  def __init__(self,FutureAccount= ''):

    super(TransferQryDetailReqField,self).__init__()

    self.FutureAccount=self._to_bytes(FutureAccount)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FutureAccount=self._to_bytes(i_tuple[1])

class TransferQryDetailRspField(Base):
  """查询银行交易明细请求响应"""
  _fields_ = [
    ('TradeDate',ctypes.c_char*9)# ///交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('TradeCode',ctypes.c_char*7)# 交易代码
    ,('FutureSerial',ctypes.c_int)# 期货流水号
    ,('FutureID',ctypes.c_char*11)# 期货公司代码
    ,('FutureAccount',ctypes.c_char*22)# 资金帐号
    ,('BankSerial',ctypes.c_int)# 银行流水号
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBrchID',ctypes.c_char*5)# 银行分中心代码
    ,('BankAccount',ctypes.c_char*41)# 银行账号
    ,('CertCode',ctypes.c_char*21)# 证件号码
    ,('CurrencyCode',ctypes.c_char*4)# 货币代码
    ,('TxAmount',ctypes.c_double)# 发生金额
    ,('Flag',ctypes.c_char)# 有效标志
]

  def __init__(self,TradeDate= '',TradeTime='',TradeCode='',FutureSerial=0,FutureID='',FutureAccount='',BankSerial=0,BankID='',BankBrchID='',BankAccount='',CertCode='',CurrencyCode='',TxAmount=0.0,Flag=''):

    super(TransferQryDetailRspField,self).__init__()

    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.TradeCode=self._to_bytes(TradeCode)
    self.FutureSerial=int(FutureSerial)
    self.FutureID=self._to_bytes(FutureID)
    self.FutureAccount=self._to_bytes(FutureAccount)
    self.BankSerial=int(BankSerial)
    self.BankID=self._to_bytes(BankID)
    self.BankBrchID=self._to_bytes(BankBrchID)
    self.BankAccount=self._to_bytes(BankAccount)
    self.CertCode=self._to_bytes(CertCode)
    self.CurrencyCode=self._to_bytes(CurrencyCode)
    self.TxAmount=float(TxAmount)
    self.Flag=self._to_bytes(Flag)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeDate=self._to_bytes(i_tuple[1])
    self.TradeTime=self._to_bytes(i_tuple[2])
    self.TradeCode=self._to_bytes(i_tuple[3])
    self.FutureSerial=int(i_tuple[4])
    self.FutureID=self._to_bytes(i_tuple[5])
    self.FutureAccount=self._to_bytes(i_tuple[6])
    self.BankSerial=int(i_tuple[7])
    self.BankID=self._to_bytes(i_tuple[8])
    self.BankBrchID=self._to_bytes(i_tuple[9])
    self.BankAccount=self._to_bytes(i_tuple[10])
    self.CertCode=self._to_bytes(i_tuple[11])
    self.CurrencyCode=self._to_bytes(i_tuple[12])
    self.TxAmount=float(i_tuple[13])
    self.Flag=self._to_bytes(i_tuple[14])

class RspInfoField(Base):
  """响应信息"""
  _fields_ = [
    ('ErrorID',ctypes.c_int)# ///错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,ErrorID= 0,ErrorMsg=''):

    super(RspInfoField,self).__init__()

    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ErrorID=int(i_tuple[1])
    self.ErrorMsg=self._to_bytes(i_tuple[2])

class ExchangeField(Base):
  """交易所"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ExchangeName',ctypes.c_char*61)# 交易所名称
    ,('ExchangeProperty',ctypes.c_char)# 交易所属性
]

  def __init__(self,ExchangeID= '',ExchangeName='',ExchangeProperty=''):

    super(ExchangeField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExchangeName=self._to_bytes(ExchangeName)
    self.ExchangeProperty=self._to_bytes(ExchangeProperty)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ExchangeName=self._to_bytes(i_tuple[2])
    self.ExchangeProperty=self._to_bytes(i_tuple[3])

class ProductField(Base):
  """产品"""
  _fields_ = [
    ('ProductID',ctypes.c_char*31)# ///产品代码
    ,('ProductName',ctypes.c_char*21)# 产品名称
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ProductClass',ctypes.c_char)# 产品类型
    ,('VolumeMultiple',ctypes.c_int)# 合约数量乘数
    ,('PriceTick',ctypes.c_double)# 最小变动价位
    ,('MaxMarketOrderVolume',ctypes.c_int)# 市价单最大下单量
    ,('MinMarketOrderVolume',ctypes.c_int)# 市价单最小下单量
    ,('MaxLimitOrderVolume',ctypes.c_int)# 限价单最大下单量
    ,('MinLimitOrderVolume',ctypes.c_int)# 限价单最小下单量
    ,('PositionType',ctypes.c_char)# 持仓类型
    ,('PositionDateType',ctypes.c_char)# 持仓日期类型
    ,('CloseDealType',ctypes.c_char)# 平仓处理类型
    ,('TradeCurrencyID',ctypes.c_char*4)# 交易币种类型
    ,('MortgageFundUseRange',ctypes.c_char)# 质押资金可用范围
    ,('ExchangeProductID',ctypes.c_char*31)# 交易所产品代码
    ,('UnderlyingMultiple',ctypes.c_double)# 合约基础商品乘数
]

  def __init__(self,ProductID= '',ProductName='',ExchangeID='',ProductClass='',VolumeMultiple=0,PriceTick=0.0,MaxMarketOrderVolume=0,MinMarketOrderVolume=0,MaxLimitOrderVolume=0,MinLimitOrderVolume=0,PositionType='',PositionDateType='',CloseDealType='',TradeCurrencyID='',MortgageFundUseRange='',ExchangeProductID='',UnderlyingMultiple=0.0):

    super(ProductField,self).__init__()

    self.ProductID=self._to_bytes(ProductID)
    self.ProductName=self._to_bytes(ProductName)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ProductClass=self._to_bytes(ProductClass)
    self.VolumeMultiple=int(VolumeMultiple)
    self.PriceTick=float(PriceTick)
    self.MaxMarketOrderVolume=int(MaxMarketOrderVolume)
    self.MinMarketOrderVolume=int(MinMarketOrderVolume)
    self.MaxLimitOrderVolume=int(MaxLimitOrderVolume)
    self.MinLimitOrderVolume=int(MinLimitOrderVolume)
    self.PositionType=self._to_bytes(PositionType)
    self.PositionDateType=self._to_bytes(PositionDateType)
    self.CloseDealType=self._to_bytes(CloseDealType)
    self.TradeCurrencyID=self._to_bytes(TradeCurrencyID)
    self.MortgageFundUseRange=self._to_bytes(MortgageFundUseRange)
    self.ExchangeProductID=self._to_bytes(ExchangeProductID)
    self.UnderlyingMultiple=float(UnderlyingMultiple)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductID=self._to_bytes(i_tuple[1])
    self.ProductName=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.ProductClass=self._to_bytes(i_tuple[4])
    self.VolumeMultiple=int(i_tuple[5])
    self.PriceTick=float(i_tuple[6])
    self.MaxMarketOrderVolume=int(i_tuple[7])
    self.MinMarketOrderVolume=int(i_tuple[8])
    self.MaxLimitOrderVolume=int(i_tuple[9])
    self.MinLimitOrderVolume=int(i_tuple[10])
    self.PositionType=self._to_bytes(i_tuple[11])
    self.PositionDateType=self._to_bytes(i_tuple[12])
    self.CloseDealType=self._to_bytes(i_tuple[13])
    self.TradeCurrencyID=self._to_bytes(i_tuple[14])
    self.MortgageFundUseRange=self._to_bytes(i_tuple[15])
    self.ExchangeProductID=self._to_bytes(i_tuple[16])
    self.UnderlyingMultiple=float(i_tuple[17])

class InstrumentField(Base):
  """合约"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InstrumentName',ctypes.c_char*21)# 合约名称
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ProductID',ctypes.c_char*31)# 产品代码
    ,('ProductClass',ctypes.c_char)# 产品类型
    ,('DeliveryYear',ctypes.c_int)# 交割年份
    ,('DeliveryMonth',ctypes.c_int)# 交割月
    ,('MaxMarketOrderVolume',ctypes.c_int)# 市价单最大下单量
    ,('MinMarketOrderVolume',ctypes.c_int)# 市价单最小下单量
    ,('MaxLimitOrderVolume',ctypes.c_int)# 限价单最大下单量
    ,('MinLimitOrderVolume',ctypes.c_int)# 限价单最小下单量
    ,('VolumeMultiple',ctypes.c_int)# 合约数量乘数
    ,('PriceTick',ctypes.c_double)# 最小变动价位
    ,('CreateDate',ctypes.c_char*9)# 创建日
    ,('OpenDate',ctypes.c_char*9)# 上市日
    ,('ExpireDate',ctypes.c_char*9)# 到期日
    ,('StartDelivDate',ctypes.c_char*9)# 开始交割日
    ,('EndDelivDate',ctypes.c_char*9)# 结束交割日
    ,('InstLifePhase',ctypes.c_char)# 合约生命周期状态
    ,('IsTrading',ctypes.c_int)# 当前是否交易
    ,('PositionType',ctypes.c_char)# 持仓类型
    ,('PositionDateType',ctypes.c_char)# 持仓日期类型
    ,('LongMarginRatio',ctypes.c_double)# 多头保证金率
    ,('ShortMarginRatio',ctypes.c_double)# 空头保证金率
    ,('MaxMarginSideAlgorithm',ctypes.c_char)# 是否使用大额单边保证金算法
    ,('UnderlyingInstrID',ctypes.c_char*31)# 基础商品代码
    ,('StrikePrice',ctypes.c_double)# 执行价
    ,('OptionsType',ctypes.c_char)# 期权类型
    ,('UnderlyingMultiple',ctypes.c_double)# 合约基础商品乘数
    ,('CombinationType',ctypes.c_char)# 组合类型
]

  def __init__(self,InstrumentID= '',ExchangeID='',InstrumentName='',ExchangeInstID='',ProductID='',ProductClass='',DeliveryYear=0,DeliveryMonth=0,MaxMarketOrderVolume=0,MinMarketOrderVolume=0,MaxLimitOrderVolume=0,MinLimitOrderVolume=0,VolumeMultiple=0,PriceTick=0.0,CreateDate='',OpenDate='',ExpireDate='',StartDelivDate='',EndDelivDate='',InstLifePhase='',IsTrading=0,PositionType='',PositionDateType='',LongMarginRatio=0.0,ShortMarginRatio=0.0,MaxMarginSideAlgorithm='',UnderlyingInstrID='',StrikePrice=0.0,OptionsType='',UnderlyingMultiple=0.0,CombinationType=''):

    super(InstrumentField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InstrumentName=self._to_bytes(InstrumentName)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ProductID=self._to_bytes(ProductID)
    self.ProductClass=self._to_bytes(ProductClass)
    self.DeliveryYear=int(DeliveryYear)
    self.DeliveryMonth=int(DeliveryMonth)
    self.MaxMarketOrderVolume=int(MaxMarketOrderVolume)
    self.MinMarketOrderVolume=int(MinMarketOrderVolume)
    self.MaxLimitOrderVolume=int(MaxLimitOrderVolume)
    self.MinLimitOrderVolume=int(MinLimitOrderVolume)
    self.VolumeMultiple=int(VolumeMultiple)
    self.PriceTick=float(PriceTick)
    self.CreateDate=self._to_bytes(CreateDate)
    self.OpenDate=self._to_bytes(OpenDate)
    self.ExpireDate=self._to_bytes(ExpireDate)
    self.StartDelivDate=self._to_bytes(StartDelivDate)
    self.EndDelivDate=self._to_bytes(EndDelivDate)
    self.InstLifePhase=self._to_bytes(InstLifePhase)
    self.IsTrading=int(IsTrading)
    self.PositionType=self._to_bytes(PositionType)
    self.PositionDateType=self._to_bytes(PositionDateType)
    self.LongMarginRatio=float(LongMarginRatio)
    self.ShortMarginRatio=float(ShortMarginRatio)
    self.MaxMarginSideAlgorithm=self._to_bytes(MaxMarginSideAlgorithm)
    self.UnderlyingInstrID=self._to_bytes(UnderlyingInstrID)
    self.StrikePrice=float(StrikePrice)
    self.OptionsType=self._to_bytes(OptionsType)
    self.UnderlyingMultiple=float(UnderlyingMultiple)
    self.CombinationType=self._to_bytes(CombinationType)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.InstrumentName=self._to_bytes(i_tuple[3])
    self.ExchangeInstID=self._to_bytes(i_tuple[4])
    self.ProductID=self._to_bytes(i_tuple[5])
    self.ProductClass=self._to_bytes(i_tuple[6])
    self.DeliveryYear=int(i_tuple[7])
    self.DeliveryMonth=int(i_tuple[8])
    self.MaxMarketOrderVolume=int(i_tuple[9])
    self.MinMarketOrderVolume=int(i_tuple[10])
    self.MaxLimitOrderVolume=int(i_tuple[11])
    self.MinLimitOrderVolume=int(i_tuple[12])
    self.VolumeMultiple=int(i_tuple[13])
    self.PriceTick=float(i_tuple[14])
    self.CreateDate=self._to_bytes(i_tuple[15])
    self.OpenDate=self._to_bytes(i_tuple[16])
    self.ExpireDate=self._to_bytes(i_tuple[17])
    self.StartDelivDate=self._to_bytes(i_tuple[18])
    self.EndDelivDate=self._to_bytes(i_tuple[19])
    self.InstLifePhase=self._to_bytes(i_tuple[20])
    self.IsTrading=int(i_tuple[21])
    self.PositionType=self._to_bytes(i_tuple[22])
    self.PositionDateType=self._to_bytes(i_tuple[23])
    self.LongMarginRatio=float(i_tuple[24])
    self.ShortMarginRatio=float(i_tuple[25])
    self.MaxMarginSideAlgorithm=self._to_bytes(i_tuple[26])
    self.UnderlyingInstrID=self._to_bytes(i_tuple[27])
    self.StrikePrice=float(i_tuple[28])
    self.OptionsType=self._to_bytes(i_tuple[29])
    self.UnderlyingMultiple=float(i_tuple[30])
    self.CombinationType=self._to_bytes(i_tuple[31])

class BrokerField(Base):
  """经纪公司"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('BrokerAbbr',ctypes.c_char*9)# 经纪公司简称
    ,('BrokerName',ctypes.c_char*81)# 经纪公司名称
    ,('IsActive',ctypes.c_int)# 是否活跃
]

  def __init__(self,BrokerID= '',BrokerAbbr='',BrokerName='',IsActive=0):

    super(BrokerField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerAbbr=self._to_bytes(BrokerAbbr)
    self.BrokerName=self._to_bytes(BrokerName)
    self.IsActive=int(IsActive)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.BrokerAbbr=self._to_bytes(i_tuple[2])
    self.BrokerName=self._to_bytes(i_tuple[3])
    self.IsActive=int(i_tuple[4])

class TraderField(Base):
  """交易所交易员"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('Password',ctypes.c_char*41)# 密码
    ,('InstallCount',ctypes.c_int)# 安装数量
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
]

  def __init__(self,ExchangeID= '',TraderID='',ParticipantID='',Password='',InstallCount=0,BrokerID=''):

    super(TraderField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.Password=self._to_bytes(Password)
    self.InstallCount=int(InstallCount)
    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.TraderID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])
    self.Password=self._to_bytes(i_tuple[4])
    self.InstallCount=int(i_tuple[5])
    self.BrokerID=self._to_bytes(i_tuple[6])

class InvestorField(Base):
  """投资者"""
  _fields_ = [
    ('InvestorID',ctypes.c_char*13)# ///投资者代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorGroupID',ctypes.c_char*13)# 投资者分组代码
    ,('InvestorName',ctypes.c_char*81)# 投资者名称
    ,('IdentifiedCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('IsActive',ctypes.c_int)# 是否活跃
    ,('Telephone',ctypes.c_char*41)# 联系电话
    ,('Address',ctypes.c_char*101)# 通讯地址
    ,('OpenDate',ctypes.c_char*9)# 开户日期
    ,('Mobile',ctypes.c_char*41)# 手机
    ,('CommModelID',ctypes.c_char*13)# 手续费率模板代码
    ,('MarginModelID',ctypes.c_char*13)# 保证金率模板代码
]

  def __init__(self,InvestorID= '',BrokerID='',InvestorGroupID='',InvestorName='',IdentifiedCardType='',IdentifiedCardNo='',IsActive=0,Telephone='',Address='',OpenDate='',Mobile='',CommModelID='',MarginModelID=''):

    super(InvestorField,self).__init__()

    self.InvestorID=self._to_bytes(InvestorID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorGroupID=self._to_bytes(InvestorGroupID)
    self.InvestorName=self._to_bytes(InvestorName)
    self.IdentifiedCardType=self._to_bytes(IdentifiedCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.IsActive=int(IsActive)
    self.Telephone=self._to_bytes(Telephone)
    self.Address=self._to_bytes(Address)
    self.OpenDate=self._to_bytes(OpenDate)
    self.Mobile=self._to_bytes(Mobile)
    self.CommModelID=self._to_bytes(CommModelID)
    self.MarginModelID=self._to_bytes(MarginModelID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InvestorID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorGroupID=self._to_bytes(i_tuple[3])
    self.InvestorName=self._to_bytes(i_tuple[4])
    self.IdentifiedCardType=self._to_bytes(i_tuple[5])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[6])
    self.IsActive=int(i_tuple[7])
    self.Telephone=self._to_bytes(i_tuple[8])
    self.Address=self._to_bytes(i_tuple[9])
    self.OpenDate=self._to_bytes(i_tuple[10])
    self.Mobile=self._to_bytes(i_tuple[11])
    self.CommModelID=self._to_bytes(i_tuple[12])
    self.MarginModelID=self._to_bytes(i_tuple[13])

class TradingCodeField(Base):
  """交易编码"""
  _fields_ = [
    ('InvestorID',ctypes.c_char*13)# ///投资者代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('IsActive',ctypes.c_int)# 是否活跃
    ,('ClientIDType',ctypes.c_char)# 交易编码类型
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('BizType',ctypes.c_char)# 业务类型
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InvestorID= '',BrokerID='',ExchangeID='',ClientID='',IsActive=0,ClientIDType='',BranchID='',BizType='',InvestUnitID=''):

    super(TradingCodeField,self).__init__()

    self.InvestorID=self._to_bytes(InvestorID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ClientID=self._to_bytes(ClientID)
    self.IsActive=int(IsActive)
    self.ClientIDType=self._to_bytes(ClientIDType)
    self.BranchID=self._to_bytes(BranchID)
    self.BizType=self._to_bytes(BizType)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InvestorID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.ClientID=self._to_bytes(i_tuple[4])
    self.IsActive=int(i_tuple[5])
    self.ClientIDType=self._to_bytes(i_tuple[6])
    self.BranchID=self._to_bytes(i_tuple[7])
    self.BizType=self._to_bytes(i_tuple[8])
    self.InvestUnitID=self._to_bytes(i_tuple[9])

class PartBrokerField(Base):
  """会员编码和经纪公司编码对照表"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('IsActive',ctypes.c_int)# 是否活跃
]

  def __init__(self,BrokerID= '',ExchangeID='',ParticipantID='',IsActive=0):

    super(PartBrokerField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.IsActive=int(IsActive)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])
    self.IsActive=int(i_tuple[4])

class SuperUserField(Base):
  """管理用户"""
  _fields_ = [
    ('UserID',ctypes.c_char*16)# ///用户代码
    ,('UserName',ctypes.c_char*81)# 用户名称
    ,('Password',ctypes.c_char*41)# 密码
    ,('IsActive',ctypes.c_int)# 是否活跃
]

  def __init__(self,UserID= '',UserName='',Password='',IsActive=0):

    super(SuperUserField,self).__init__()

    self.UserID=self._to_bytes(UserID)
    self.UserName=self._to_bytes(UserName)
    self.Password=self._to_bytes(Password)
    self.IsActive=int(IsActive)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.UserID=self._to_bytes(i_tuple[1])
    self.UserName=self._to_bytes(i_tuple[2])
    self.Password=self._to_bytes(i_tuple[3])
    self.IsActive=int(i_tuple[4])

class SuperUserFunctionField(Base):
  """管理用户功能权限"""
  _fields_ = [
    ('UserID',ctypes.c_char*16)# ///用户代码
    ,('FunctionCode',ctypes.c_char)# 功能代码
]

  def __init__(self,UserID= '',FunctionCode=''):

    super(SuperUserFunctionField,self).__init__()

    self.UserID=self._to_bytes(UserID)
    self.FunctionCode=self._to_bytes(FunctionCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.UserID=self._to_bytes(i_tuple[1])
    self.FunctionCode=self._to_bytes(i_tuple[2])

class InvestorGroupField(Base):
  """投资者组"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorGroupID',ctypes.c_char*13)# 投资者分组代码
    ,('InvestorGroupName',ctypes.c_char*41)# 投资者分组名称
]

  def __init__(self,BrokerID= '',InvestorGroupID='',InvestorGroupName=''):

    super(InvestorGroupField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorGroupID=self._to_bytes(InvestorGroupID)
    self.InvestorGroupName=self._to_bytes(InvestorGroupName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorGroupID=self._to_bytes(i_tuple[2])
    self.InvestorGroupName=self._to_bytes(i_tuple[3])

class TradingAccountField(Base):
  """资金账户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('PreMortgage',ctypes.c_double)# 上次质押金额
    ,('PreCredit',ctypes.c_double)# 上次信用额度
    ,('PreDeposit',ctypes.c_double)# 上次存款额
    ,('PreBalance',ctypes.c_double)# 上次结算准备金
    ,('PreMargin',ctypes.c_double)# 上次占用的保证金
    ,('InterestBase',ctypes.c_double)# 利息基数
    ,('Interest',ctypes.c_double)# 利息收入
    ,('Deposit',ctypes.c_double)# 入金金额
    ,('Withdraw',ctypes.c_double)# 出金金额
    ,('FrozenMargin',ctypes.c_double)# 冻结的保证金
    ,('FrozenCash',ctypes.c_double)# 冻结的资金
    ,('FrozenCommission',ctypes.c_double)# 冻结的手续费
    ,('CurrMargin',ctypes.c_double)# 当前保证金总额
    ,('CashIn',ctypes.c_double)# 资金差额
    ,('Commission',ctypes.c_double)# 手续费
    ,('CloseProfit',ctypes.c_double)# 平仓盈亏
    ,('PositionProfit',ctypes.c_double)# 持仓盈亏
    ,('Balance',ctypes.c_double)# 期货结算准备金
    ,('Available',ctypes.c_double)# 可用资金
    ,('WithdrawQuota',ctypes.c_double)# 可取资金
    ,('Reserve',ctypes.c_double)# 基本准备金
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('Credit',ctypes.c_double)# 信用额度
    ,('Mortgage',ctypes.c_double)# 质押金额
    ,('ExchangeMargin',ctypes.c_double)# 交易所保证金
    ,('DeliveryMargin',ctypes.c_double)# 投资者交割保证金
    ,('ExchangeDeliveryMargin',ctypes.c_double)# 交易所交割保证金
    ,('ReserveBalance',ctypes.c_double)# 保底期货结算准备金
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('PreFundMortgageIn',ctypes.c_double)# 上次货币质入金额
    ,('PreFundMortgageOut',ctypes.c_double)# 上次货币质出金额
    ,('FundMortgageIn',ctypes.c_double)# 货币质入金额
    ,('FundMortgageOut',ctypes.c_double)# 货币质出金额
    ,('FundMortgageAvailable',ctypes.c_double)# 货币质押余额
    ,('MortgageableFund',ctypes.c_double)# 可质押货币金额
    ,('SpecProductMargin',ctypes.c_double)# 特殊产品占用保证金
    ,('SpecProductFrozenMargin',ctypes.c_double)# 特殊产品冻结保证金
    ,('SpecProductCommission',ctypes.c_double)# 特殊产品手续费
    ,('SpecProductFrozenCommission',ctypes.c_double)# 特殊产品冻结手续费
    ,('SpecProductPositionProfit',ctypes.c_double)# 特殊产品持仓盈亏
    ,('SpecProductCloseProfit',ctypes.c_double)# 特殊产品平仓盈亏
    ,('SpecProductPositionProfitByAlg',ctypes.c_double)# 根据持仓盈亏算法计算的特殊产品持仓盈亏
    ,('SpecProductExchangeMargin',ctypes.c_double)# 特殊产品交易所保证金
    ,('BizType',ctypes.c_char)# 业务类型
    ,('FrozenSwap',ctypes.c_double)# 延时换汇冻结金额
    ,('RemainSwap',ctypes.c_double)# 剩余换汇额度
]

  def __init__(self,BrokerID= '',AccountID='',PreMortgage=0.0,PreCredit=0.0,PreDeposit=0.0,PreBalance=0.0,PreMargin=0.0,InterestBase=0.0,Interest=0.0,Deposit=0.0,Withdraw=0.0,FrozenMargin=0.0,FrozenCash=0.0,FrozenCommission=0.0,CurrMargin=0.0,CashIn=0.0,Commission=0.0,CloseProfit=0.0,PositionProfit=0.0,Balance=0.0,Available=0.0,WithdrawQuota=0.0,Reserve=0.0,TradingDay='',SettlementID=0,Credit=0.0,Mortgage=0.0,ExchangeMargin=0.0,DeliveryMargin=0.0,ExchangeDeliveryMargin=0.0,ReserveBalance=0.0,CurrencyID='',PreFundMortgageIn=0.0,PreFundMortgageOut=0.0,FundMortgageIn=0.0,FundMortgageOut=0.0,FundMortgageAvailable=0.0,MortgageableFund=0.0,SpecProductMargin=0.0,SpecProductFrozenMargin=0.0,SpecProductCommission=0.0,SpecProductFrozenCommission=0.0,SpecProductPositionProfit=0.0,SpecProductCloseProfit=0.0,SpecProductPositionProfitByAlg=0.0,SpecProductExchangeMargin=0.0,BizType='',FrozenSwap=0.0,RemainSwap=0.0):

    super(TradingAccountField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.PreMortgage=float(PreMortgage)
    self.PreCredit=float(PreCredit)
    self.PreDeposit=float(PreDeposit)
    self.PreBalance=float(PreBalance)
    self.PreMargin=float(PreMargin)
    self.InterestBase=float(InterestBase)
    self.Interest=float(Interest)
    self.Deposit=float(Deposit)
    self.Withdraw=float(Withdraw)
    self.FrozenMargin=float(FrozenMargin)
    self.FrozenCash=float(FrozenCash)
    self.FrozenCommission=float(FrozenCommission)
    self.CurrMargin=float(CurrMargin)
    self.CashIn=float(CashIn)
    self.Commission=float(Commission)
    self.CloseProfit=float(CloseProfit)
    self.PositionProfit=float(PositionProfit)
    self.Balance=float(Balance)
    self.Available=float(Available)
    self.WithdrawQuota=float(WithdrawQuota)
    self.Reserve=float(Reserve)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.Credit=float(Credit)
    self.Mortgage=float(Mortgage)
    self.ExchangeMargin=float(ExchangeMargin)
    self.DeliveryMargin=float(DeliveryMargin)
    self.ExchangeDeliveryMargin=float(ExchangeDeliveryMargin)
    self.ReserveBalance=float(ReserveBalance)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.PreFundMortgageIn=float(PreFundMortgageIn)
    self.PreFundMortgageOut=float(PreFundMortgageOut)
    self.FundMortgageIn=float(FundMortgageIn)
    self.FundMortgageOut=float(FundMortgageOut)
    self.FundMortgageAvailable=float(FundMortgageAvailable)
    self.MortgageableFund=float(MortgageableFund)
    self.SpecProductMargin=float(SpecProductMargin)
    self.SpecProductFrozenMargin=float(SpecProductFrozenMargin)
    self.SpecProductCommission=float(SpecProductCommission)
    self.SpecProductFrozenCommission=float(SpecProductFrozenCommission)
    self.SpecProductPositionProfit=float(SpecProductPositionProfit)
    self.SpecProductCloseProfit=float(SpecProductCloseProfit)
    self.SpecProductPositionProfitByAlg=float(SpecProductPositionProfitByAlg)
    self.SpecProductExchangeMargin=float(SpecProductExchangeMargin)
    self.BizType=self._to_bytes(BizType)
    self.FrozenSwap=float(FrozenSwap)
    self.RemainSwap=float(RemainSwap)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.PreMortgage=float(i_tuple[3])
    self.PreCredit=float(i_tuple[4])
    self.PreDeposit=float(i_tuple[5])
    self.PreBalance=float(i_tuple[6])
    self.PreMargin=float(i_tuple[7])
    self.InterestBase=float(i_tuple[8])
    self.Interest=float(i_tuple[9])
    self.Deposit=float(i_tuple[10])
    self.Withdraw=float(i_tuple[11])
    self.FrozenMargin=float(i_tuple[12])
    self.FrozenCash=float(i_tuple[13])
    self.FrozenCommission=float(i_tuple[14])
    self.CurrMargin=float(i_tuple[15])
    self.CashIn=float(i_tuple[16])
    self.Commission=float(i_tuple[17])
    self.CloseProfit=float(i_tuple[18])
    self.PositionProfit=float(i_tuple[19])
    self.Balance=float(i_tuple[20])
    self.Available=float(i_tuple[21])
    self.WithdrawQuota=float(i_tuple[22])
    self.Reserve=float(i_tuple[23])
    self.TradingDay=self._to_bytes(i_tuple[24])
    self.SettlementID=int(i_tuple[25])
    self.Credit=float(i_tuple[26])
    self.Mortgage=float(i_tuple[27])
    self.ExchangeMargin=float(i_tuple[28])
    self.DeliveryMargin=float(i_tuple[29])
    self.ExchangeDeliveryMargin=float(i_tuple[30])
    self.ReserveBalance=float(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.PreFundMortgageIn=float(i_tuple[33])
    self.PreFundMortgageOut=float(i_tuple[34])
    self.FundMortgageIn=float(i_tuple[35])
    self.FundMortgageOut=float(i_tuple[36])
    self.FundMortgageAvailable=float(i_tuple[37])
    self.MortgageableFund=float(i_tuple[38])
    self.SpecProductMargin=float(i_tuple[39])
    self.SpecProductFrozenMargin=float(i_tuple[40])
    self.SpecProductCommission=float(i_tuple[41])
    self.SpecProductFrozenCommission=float(i_tuple[42])
    self.SpecProductPositionProfit=float(i_tuple[43])
    self.SpecProductCloseProfit=float(i_tuple[44])
    self.SpecProductPositionProfitByAlg=float(i_tuple[45])
    self.SpecProductExchangeMargin=float(i_tuple[46])
    self.BizType=self._to_bytes(i_tuple[47])
    self.FrozenSwap=float(i_tuple[48])
    self.RemainSwap=float(i_tuple[49])

class InvestorPositionField(Base):
  """投资者持仓"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('PosiDirection',ctypes.c_char)# 持仓多空方向
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('PositionDate',ctypes.c_char)# 持仓日期
    ,('YdPosition',ctypes.c_int)# 上日持仓
    ,('Position',ctypes.c_int)# 今日持仓
    ,('LongFrozen',ctypes.c_int)# 多头冻结
    ,('ShortFrozen',ctypes.c_int)# 空头冻结
    ,('LongFrozenAmount',ctypes.c_double)# 开仓冻结金额
    ,('ShortFrozenAmount',ctypes.c_double)# 开仓冻结金额
    ,('OpenVolume',ctypes.c_int)# 开仓量
    ,('CloseVolume',ctypes.c_int)# 平仓量
    ,('OpenAmount',ctypes.c_double)# 开仓金额
    ,('CloseAmount',ctypes.c_double)# 平仓金额
    ,('PositionCost',ctypes.c_double)# 持仓成本
    ,('PreMargin',ctypes.c_double)# 上次占用的保证金
    ,('UseMargin',ctypes.c_double)# 占用的保证金
    ,('FrozenMargin',ctypes.c_double)# 冻结的保证金
    ,('FrozenCash',ctypes.c_double)# 冻结的资金
    ,('FrozenCommission',ctypes.c_double)# 冻结的手续费
    ,('CashIn',ctypes.c_double)# 资金差额
    ,('Commission',ctypes.c_double)# 手续费
    ,('CloseProfit',ctypes.c_double)# 平仓盈亏
    ,('PositionProfit',ctypes.c_double)# 持仓盈亏
    ,('PreSettlementPrice',ctypes.c_double)# 上次结算价
    ,('SettlementPrice',ctypes.c_double)# 本次结算价
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OpenCost',ctypes.c_double)# 开仓成本
    ,('ExchangeMargin',ctypes.c_double)# 交易所保证金
    ,('CombPosition',ctypes.c_int)# 组合成交形成的持仓
    ,('CombLongFrozen',ctypes.c_int)# 组合多头冻结
    ,('CombShortFrozen',ctypes.c_int)# 组合空头冻结
    ,('CloseProfitByDate',ctypes.c_double)# 逐日盯市平仓盈亏
    ,('CloseProfitByTrade',ctypes.c_double)# 逐笔对冲平仓盈亏
    ,('TodayPosition',ctypes.c_int)# 今日持仓
    ,('MarginRateByMoney',ctypes.c_double)# 保证金率
    ,('MarginRateByVolume',ctypes.c_double)# 保证金率(按手数)
    ,('StrikeFrozen',ctypes.c_int)# 执行冻结
    ,('StrikeFrozenAmount',ctypes.c_double)# 执行冻结金额
    ,('AbandonFrozen',ctypes.c_int)# 放弃执行冻结
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('YdStrikeFrozen',ctypes.c_int)# 执行冻结的昨仓
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',BrokerID='',InvestorID='',PosiDirection='',HedgeFlag='',PositionDate='',YdPosition=0,Position=0,LongFrozen=0,ShortFrozen=0,LongFrozenAmount=0.0,ShortFrozenAmount=0.0,OpenVolume=0,CloseVolume=0,OpenAmount=0.0,CloseAmount=0.0,PositionCost=0.0,PreMargin=0.0,UseMargin=0.0,FrozenMargin=0.0,FrozenCash=0.0,FrozenCommission=0.0,CashIn=0.0,Commission=0.0,CloseProfit=0.0,PositionProfit=0.0,PreSettlementPrice=0.0,SettlementPrice=0.0,TradingDay='',SettlementID=0,OpenCost=0.0,ExchangeMargin=0.0,CombPosition=0,CombLongFrozen=0,CombShortFrozen=0,CloseProfitByDate=0.0,CloseProfitByTrade=0.0,TodayPosition=0,MarginRateByMoney=0.0,MarginRateByVolume=0.0,StrikeFrozen=0,StrikeFrozenAmount=0.0,AbandonFrozen=0,ExchangeID='',YdStrikeFrozen=0,InvestUnitID=''):

    super(InvestorPositionField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.PosiDirection=self._to_bytes(PosiDirection)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.PositionDate=self._to_bytes(PositionDate)
    self.YdPosition=int(YdPosition)
    self.Position=int(Position)
    self.LongFrozen=int(LongFrozen)
    self.ShortFrozen=int(ShortFrozen)
    self.LongFrozenAmount=float(LongFrozenAmount)
    self.ShortFrozenAmount=float(ShortFrozenAmount)
    self.OpenVolume=int(OpenVolume)
    self.CloseVolume=int(CloseVolume)
    self.OpenAmount=float(OpenAmount)
    self.CloseAmount=float(CloseAmount)
    self.PositionCost=float(PositionCost)
    self.PreMargin=float(PreMargin)
    self.UseMargin=float(UseMargin)
    self.FrozenMargin=float(FrozenMargin)
    self.FrozenCash=float(FrozenCash)
    self.FrozenCommission=float(FrozenCommission)
    self.CashIn=float(CashIn)
    self.Commission=float(Commission)
    self.CloseProfit=float(CloseProfit)
    self.PositionProfit=float(PositionProfit)
    self.PreSettlementPrice=float(PreSettlementPrice)
    self.SettlementPrice=float(SettlementPrice)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OpenCost=float(OpenCost)
    self.ExchangeMargin=float(ExchangeMargin)
    self.CombPosition=int(CombPosition)
    self.CombLongFrozen=int(CombLongFrozen)
    self.CombShortFrozen=int(CombShortFrozen)
    self.CloseProfitByDate=float(CloseProfitByDate)
    self.CloseProfitByTrade=float(CloseProfitByTrade)
    self.TodayPosition=int(TodayPosition)
    self.MarginRateByMoney=float(MarginRateByMoney)
    self.MarginRateByVolume=float(MarginRateByVolume)
    self.StrikeFrozen=int(StrikeFrozen)
    self.StrikeFrozenAmount=float(StrikeFrozenAmount)
    self.AbandonFrozen=int(AbandonFrozen)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.YdStrikeFrozen=int(YdStrikeFrozen)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.PosiDirection=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.PositionDate=self._to_bytes(i_tuple[6])
    self.YdPosition=int(i_tuple[7])
    self.Position=int(i_tuple[8])
    self.LongFrozen=int(i_tuple[9])
    self.ShortFrozen=int(i_tuple[10])
    self.LongFrozenAmount=float(i_tuple[11])
    self.ShortFrozenAmount=float(i_tuple[12])
    self.OpenVolume=int(i_tuple[13])
    self.CloseVolume=int(i_tuple[14])
    self.OpenAmount=float(i_tuple[15])
    self.CloseAmount=float(i_tuple[16])
    self.PositionCost=float(i_tuple[17])
    self.PreMargin=float(i_tuple[18])
    self.UseMargin=float(i_tuple[19])
    self.FrozenMargin=float(i_tuple[20])
    self.FrozenCash=float(i_tuple[21])
    self.FrozenCommission=float(i_tuple[22])
    self.CashIn=float(i_tuple[23])
    self.Commission=float(i_tuple[24])
    self.CloseProfit=float(i_tuple[25])
    self.PositionProfit=float(i_tuple[26])
    self.PreSettlementPrice=float(i_tuple[27])
    self.SettlementPrice=float(i_tuple[28])
    self.TradingDay=self._to_bytes(i_tuple[29])
    self.SettlementID=int(i_tuple[30])
    self.OpenCost=float(i_tuple[31])
    self.ExchangeMargin=float(i_tuple[32])
    self.CombPosition=int(i_tuple[33])
    self.CombLongFrozen=int(i_tuple[34])
    self.CombShortFrozen=int(i_tuple[35])
    self.CloseProfitByDate=float(i_tuple[36])
    self.CloseProfitByTrade=float(i_tuple[37])
    self.TodayPosition=int(i_tuple[38])
    self.MarginRateByMoney=float(i_tuple[39])
    self.MarginRateByVolume=float(i_tuple[40])
    self.StrikeFrozen=int(i_tuple[41])
    self.StrikeFrozenAmount=float(i_tuple[42])
    self.AbandonFrozen=int(i_tuple[43])
    self.ExchangeID=self._to_bytes(i_tuple[44])
    self.YdStrikeFrozen=int(i_tuple[45])
    self.InvestUnitID=self._to_bytes(i_tuple[46])

class InstrumentMarginRateField(Base):
  """合约保证金率"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('LongMarginRatioByMoney',ctypes.c_double)# 多头保证金率
    ,('LongMarginRatioByVolume',ctypes.c_double)# 多头保证金费
    ,('ShortMarginRatioByMoney',ctypes.c_double)# 空头保证金率
    ,('ShortMarginRatioByVolume',ctypes.c_double)# 空头保证金费
    ,('IsRelative',ctypes.c_int)# 是否相对交易所收取
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',HedgeFlag='',LongMarginRatioByMoney=0.0,LongMarginRatioByVolume=0.0,ShortMarginRatioByMoney=0.0,ShortMarginRatioByVolume=0.0,IsRelative=0,ExchangeID='',InvestUnitID=''):

    super(InstrumentMarginRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.LongMarginRatioByMoney=float(LongMarginRatioByMoney)
    self.LongMarginRatioByVolume=float(LongMarginRatioByVolume)
    self.ShortMarginRatioByMoney=float(ShortMarginRatioByMoney)
    self.ShortMarginRatioByVolume=float(ShortMarginRatioByVolume)
    self.IsRelative=int(IsRelative)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.LongMarginRatioByMoney=float(i_tuple[6])
    self.LongMarginRatioByVolume=float(i_tuple[7])
    self.ShortMarginRatioByMoney=float(i_tuple[8])
    self.ShortMarginRatioByVolume=float(i_tuple[9])
    self.IsRelative=int(i_tuple[10])
    self.ExchangeID=self._to_bytes(i_tuple[11])
    self.InvestUnitID=self._to_bytes(i_tuple[12])

class InstrumentCommissionRateField(Base):
  """合约手续费率"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OpenRatioByMoney',ctypes.c_double)# 开仓手续费率
    ,('OpenRatioByVolume',ctypes.c_double)# 开仓手续费
    ,('CloseRatioByMoney',ctypes.c_double)# 平仓手续费率
    ,('CloseRatioByVolume',ctypes.c_double)# 平仓手续费
    ,('CloseTodayRatioByMoney',ctypes.c_double)# 平今手续费率
    ,('CloseTodayRatioByVolume',ctypes.c_double)# 平今手续费
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('BizType',ctypes.c_char)# 业务类型
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',OpenRatioByMoney=0.0,OpenRatioByVolume=0.0,CloseRatioByMoney=0.0,CloseRatioByVolume=0.0,CloseTodayRatioByMoney=0.0,CloseTodayRatioByVolume=0.0,ExchangeID='',BizType='',InvestUnitID=''):

    super(InstrumentCommissionRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OpenRatioByMoney=float(OpenRatioByMoney)
    self.OpenRatioByVolume=float(OpenRatioByVolume)
    self.CloseRatioByMoney=float(CloseRatioByMoney)
    self.CloseRatioByVolume=float(CloseRatioByVolume)
    self.CloseTodayRatioByMoney=float(CloseTodayRatioByMoney)
    self.CloseTodayRatioByVolume=float(CloseTodayRatioByVolume)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.BizType=self._to_bytes(BizType)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.OpenRatioByMoney=float(i_tuple[5])
    self.OpenRatioByVolume=float(i_tuple[6])
    self.CloseRatioByMoney=float(i_tuple[7])
    self.CloseRatioByVolume=float(i_tuple[8])
    self.CloseTodayRatioByMoney=float(i_tuple[9])
    self.CloseTodayRatioByVolume=float(i_tuple[10])
    self.ExchangeID=self._to_bytes(i_tuple[11])
    self.BizType=self._to_bytes(i_tuple[12])
    self.InvestUnitID=self._to_bytes(i_tuple[13])

class DepthMarketDataField(Base):
  """深度行情"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('LastPrice',ctypes.c_double)# 最新价
    ,('PreSettlementPrice',ctypes.c_double)# 上次结算价
    ,('PreClosePrice',ctypes.c_double)# 昨收盘
    ,('PreOpenInterest',ctypes.c_double)# 昨持仓量
    ,('OpenPrice',ctypes.c_double)# 今开盘
    ,('HighestPrice',ctypes.c_double)# 最高价
    ,('LowestPrice',ctypes.c_double)# 最低价
    ,('Volume',ctypes.c_int)# 数量
    ,('Turnover',ctypes.c_double)# 成交金额
    ,('OpenInterest',ctypes.c_double)# 持仓量
    ,('ClosePrice',ctypes.c_double)# 今收盘
    ,('SettlementPrice',ctypes.c_double)# 本次结算价
    ,('UpperLimitPrice',ctypes.c_double)# 涨停板价
    ,('LowerLimitPrice',ctypes.c_double)# 跌停板价
    ,('PreDelta',ctypes.c_double)# 昨虚实度
    ,('CurrDelta',ctypes.c_double)# 今虚实度
    ,('UpdateTime',ctypes.c_char*9)# 最后修改时间
    ,('UpdateMillisec',ctypes.c_int)# 最后修改毫秒
    ,('BidPrice1',ctypes.c_double)# 申买价一
    ,('BidVolume1',ctypes.c_int)# 申买量一
    ,('AskPrice1',ctypes.c_double)# 申卖价一
    ,('AskVolume1',ctypes.c_int)# 申卖量一
    ,('BidPrice2',ctypes.c_double)# 申买价二
    ,('BidVolume2',ctypes.c_int)# 申买量二
    ,('AskPrice2',ctypes.c_double)# 申卖价二
    ,('AskVolume2',ctypes.c_int)# 申卖量二
    ,('BidPrice3',ctypes.c_double)# 申买价三
    ,('BidVolume3',ctypes.c_int)# 申买量三
    ,('AskPrice3',ctypes.c_double)# 申卖价三
    ,('AskVolume3',ctypes.c_int)# 申卖量三
    ,('BidPrice4',ctypes.c_double)# 申买价四
    ,('BidVolume4',ctypes.c_int)# 申买量四
    ,('AskPrice4',ctypes.c_double)# 申卖价四
    ,('AskVolume4',ctypes.c_int)# 申卖量四
    ,('BidPrice5',ctypes.c_double)# 申买价五
    ,('BidVolume5',ctypes.c_int)# 申买量五
    ,('AskPrice5',ctypes.c_double)# 申卖价五
    ,('AskVolume5',ctypes.c_int)# 申卖量五
    ,('AveragePrice',ctypes.c_double)# 当日均价
    ,('ActionDay',ctypes.c_char*9)# 业务日期
]

  def __init__(self,TradingDay= '',InstrumentID='',ExchangeID='',ExchangeInstID='',LastPrice=0.0,PreSettlementPrice=0.0,PreClosePrice=0.0,PreOpenInterest=0.0,OpenPrice=0.0,HighestPrice=0.0,LowestPrice=0.0,Volume=0,Turnover=0.0,OpenInterest=0.0,ClosePrice=0.0,SettlementPrice=0.0,UpperLimitPrice=0.0,LowerLimitPrice=0.0,PreDelta=0.0,CurrDelta=0.0,UpdateTime='',UpdateMillisec=0,BidPrice1=0.0,BidVolume1=0,AskPrice1=0.0,AskVolume1=0,BidPrice2=0.0,BidVolume2=0,AskPrice2=0.0,AskVolume2=0,BidPrice3=0.0,BidVolume3=0,AskPrice3=0.0,AskVolume3=0,BidPrice4=0.0,BidVolume4=0,AskPrice4=0.0,AskVolume4=0,BidPrice5=0.0,BidVolume5=0,AskPrice5=0.0,AskVolume5=0,AveragePrice=0.0,ActionDay=''):

    super(DepthMarketDataField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.LastPrice=float(LastPrice)
    self.PreSettlementPrice=float(PreSettlementPrice)
    self.PreClosePrice=float(PreClosePrice)
    self.PreOpenInterest=float(PreOpenInterest)
    self.OpenPrice=float(OpenPrice)
    self.HighestPrice=float(HighestPrice)
    self.LowestPrice=float(LowestPrice)
    self.Volume=int(Volume)
    self.Turnover=float(Turnover)
    self.OpenInterest=float(OpenInterest)
    self.ClosePrice=float(ClosePrice)
    self.SettlementPrice=float(SettlementPrice)
    self.UpperLimitPrice=float(UpperLimitPrice)
    self.LowerLimitPrice=float(LowerLimitPrice)
    self.PreDelta=float(PreDelta)
    self.CurrDelta=float(CurrDelta)
    self.UpdateTime=self._to_bytes(UpdateTime)
    self.UpdateMillisec=int(UpdateMillisec)
    self.BidPrice1=float(BidPrice1)
    self.BidVolume1=int(BidVolume1)
    self.AskPrice1=float(AskPrice1)
    self.AskVolume1=int(AskVolume1)
    self.BidPrice2=float(BidPrice2)
    self.BidVolume2=int(BidVolume2)
    self.AskPrice2=float(AskPrice2)
    self.AskVolume2=int(AskVolume2)
    self.BidPrice3=float(BidPrice3)
    self.BidVolume3=int(BidVolume3)
    self.AskPrice3=float(AskPrice3)
    self.AskVolume3=int(AskVolume3)
    self.BidPrice4=float(BidPrice4)
    self.BidVolume4=int(BidVolume4)
    self.AskPrice4=float(AskPrice4)
    self.AskVolume4=int(AskVolume4)
    self.BidPrice5=float(BidPrice5)
    self.BidVolume5=int(BidVolume5)
    self.AskPrice5=float(AskPrice5)
    self.AskVolume5=int(AskVolume5)
    self.AveragePrice=float(AveragePrice)
    self.ActionDay=self._to_bytes(ActionDay)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.ExchangeInstID=self._to_bytes(i_tuple[4])
    self.LastPrice=float(i_tuple[5])
    self.PreSettlementPrice=float(i_tuple[6])
    self.PreClosePrice=float(i_tuple[7])
    self.PreOpenInterest=float(i_tuple[8])
    self.OpenPrice=float(i_tuple[9])
    self.HighestPrice=float(i_tuple[10])
    self.LowestPrice=float(i_tuple[11])
    self.Volume=int(i_tuple[12])
    self.Turnover=float(i_tuple[13])
    self.OpenInterest=float(i_tuple[14])
    self.ClosePrice=float(i_tuple[15])
    self.SettlementPrice=float(i_tuple[16])
    self.UpperLimitPrice=float(i_tuple[17])
    self.LowerLimitPrice=float(i_tuple[18])
    self.PreDelta=float(i_tuple[19])
    self.CurrDelta=float(i_tuple[20])
    self.UpdateTime=self._to_bytes(i_tuple[21])
    self.UpdateMillisec=int(i_tuple[22])
    self.BidPrice1=float(i_tuple[23])
    self.BidVolume1=int(i_tuple[24])
    self.AskPrice1=float(i_tuple[25])
    self.AskVolume1=int(i_tuple[26])
    self.BidPrice2=float(i_tuple[27])
    self.BidVolume2=int(i_tuple[28])
    self.AskPrice2=float(i_tuple[29])
    self.AskVolume2=int(i_tuple[30])
    self.BidPrice3=float(i_tuple[31])
    self.BidVolume3=int(i_tuple[32])
    self.AskPrice3=float(i_tuple[33])
    self.AskVolume3=int(i_tuple[34])
    self.BidPrice4=float(i_tuple[35])
    self.BidVolume4=int(i_tuple[36])
    self.AskPrice4=float(i_tuple[37])
    self.AskVolume4=int(i_tuple[38])
    self.BidPrice5=float(i_tuple[39])
    self.BidVolume5=int(i_tuple[40])
    self.AskPrice5=float(i_tuple[41])
    self.AskVolume5=int(i_tuple[42])
    self.AveragePrice=float(i_tuple[43])
    self.ActionDay=self._to_bytes(i_tuple[44])

class InstrumentTradingRightField(Base):
  """投资者合约交易权限"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('TradingRight',ctypes.c_char)# 交易权限
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',TradingRight=''):

    super(InstrumentTradingRightField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.TradingRight=self._to_bytes(TradingRight)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.TradingRight=self._to_bytes(i_tuple[5])

class BrokerUserField(Base):
  """经纪公司用户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserName',ctypes.c_char*81)# 用户名称
    ,('UserType',ctypes.c_char)# 用户类型
    ,('IsActive',ctypes.c_int)# 是否活跃
    ,('IsUsingOTP',ctypes.c_int)# 是否使用令牌
    ,('IsAuthForce',ctypes.c_int)# 是否强制终端认证
]

  def __init__(self,BrokerID= '',UserID='',UserName='',UserType='',IsActive=0,IsUsingOTP=0,IsAuthForce=0):

    super(BrokerUserField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserName=self._to_bytes(UserName)
    self.UserType=self._to_bytes(UserType)
    self.IsActive=int(IsActive)
    self.IsUsingOTP=int(IsUsingOTP)
    self.IsAuthForce=int(IsAuthForce)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserName=self._to_bytes(i_tuple[3])
    self.UserType=self._to_bytes(i_tuple[4])
    self.IsActive=int(i_tuple[5])
    self.IsUsingOTP=int(i_tuple[6])
    self.IsAuthForce=int(i_tuple[7])

class BrokerUserPasswordField(Base):
  """经纪公司用户口令"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Password',ctypes.c_char*41)# 密码
    ,('LastUpdateTime',ctypes.c_char*17)# 上次修改时间
    ,('LastLoginTime',ctypes.c_char*17)# 上次登陆时间
    ,('ExpireDate',ctypes.c_char*9)# 密码过期时间
    ,('WeakExpireDate',ctypes.c_char*9)# 弱密码过期时间
]

  def __init__(self,BrokerID= '',UserID='',Password='',LastUpdateTime='',LastLoginTime='',ExpireDate='',WeakExpireDate=''):

    super(BrokerUserPasswordField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.Password=self._to_bytes(Password)
    self.LastUpdateTime=self._to_bytes(LastUpdateTime)
    self.LastLoginTime=self._to_bytes(LastLoginTime)
    self.ExpireDate=self._to_bytes(ExpireDate)
    self.WeakExpireDate=self._to_bytes(WeakExpireDate)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.Password=self._to_bytes(i_tuple[3])
    self.LastUpdateTime=self._to_bytes(i_tuple[4])
    self.LastLoginTime=self._to_bytes(i_tuple[5])
    self.ExpireDate=self._to_bytes(i_tuple[6])
    self.WeakExpireDate=self._to_bytes(i_tuple[7])

class BrokerUserFunctionField(Base):
  """经纪公司用户功能权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('BrokerFunctionCode',ctypes.c_char)# 经纪公司功能代码
]

  def __init__(self,BrokerID= '',UserID='',BrokerFunctionCode=''):

    super(BrokerUserFunctionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.BrokerFunctionCode=self._to_bytes(BrokerFunctionCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.BrokerFunctionCode=self._to_bytes(i_tuple[3])

class TraderOfferField(Base):
  """交易所交易员报盘机"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('Password',ctypes.c_char*41)# 密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('TraderConnectStatus',ctypes.c_char)# 交易所交易员连接状态
    ,('ConnectRequestDate',ctypes.c_char*9)# 发出连接请求的日期
    ,('ConnectRequestTime',ctypes.c_char*9)# 发出连接请求的时间
    ,('LastReportDate',ctypes.c_char*9)# 上次报告日期
    ,('LastReportTime',ctypes.c_char*9)# 上次报告时间
    ,('ConnectDate',ctypes.c_char*9)# 完成连接日期
    ,('ConnectTime',ctypes.c_char*9)# 完成连接时间
    ,('StartDate',ctypes.c_char*9)# 启动日期
    ,('StartTime',ctypes.c_char*9)# 启动时间
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('MaxTradeID',ctypes.c_char*21)# 本席位最大成交编号
    ,('MaxOrderMessageReference',ctypes.c_char*7)# 本席位最大报单备拷
]

  def __init__(self,ExchangeID= '',TraderID='',ParticipantID='',Password='',InstallID=0,OrderLocalID='',TraderConnectStatus='',ConnectRequestDate='',ConnectRequestTime='',LastReportDate='',LastReportTime='',ConnectDate='',ConnectTime='',StartDate='',StartTime='',TradingDay='',BrokerID='',MaxTradeID='',MaxOrderMessageReference=''):

    super(TraderOfferField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.TraderConnectStatus=self._to_bytes(TraderConnectStatus)
    self.ConnectRequestDate=self._to_bytes(ConnectRequestDate)
    self.ConnectRequestTime=self._to_bytes(ConnectRequestTime)
    self.LastReportDate=self._to_bytes(LastReportDate)
    self.LastReportTime=self._to_bytes(LastReportTime)
    self.ConnectDate=self._to_bytes(ConnectDate)
    self.ConnectTime=self._to_bytes(ConnectTime)
    self.StartDate=self._to_bytes(StartDate)
    self.StartTime=self._to_bytes(StartTime)
    self.TradingDay=self._to_bytes(TradingDay)
    self.BrokerID=self._to_bytes(BrokerID)
    self.MaxTradeID=self._to_bytes(MaxTradeID)
    self.MaxOrderMessageReference=self._to_bytes(MaxOrderMessageReference)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.TraderID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])
    self.Password=self._to_bytes(i_tuple[4])
    self.InstallID=int(i_tuple[5])
    self.OrderLocalID=self._to_bytes(i_tuple[6])
    self.TraderConnectStatus=self._to_bytes(i_tuple[7])
    self.ConnectRequestDate=self._to_bytes(i_tuple[8])
    self.ConnectRequestTime=self._to_bytes(i_tuple[9])
    self.LastReportDate=self._to_bytes(i_tuple[10])
    self.LastReportTime=self._to_bytes(i_tuple[11])
    self.ConnectDate=self._to_bytes(i_tuple[12])
    self.ConnectTime=self._to_bytes(i_tuple[13])
    self.StartDate=self._to_bytes(i_tuple[14])
    self.StartTime=self._to_bytes(i_tuple[15])
    self.TradingDay=self._to_bytes(i_tuple[16])
    self.BrokerID=self._to_bytes(i_tuple[17])
    self.MaxTradeID=self._to_bytes(i_tuple[18])
    self.MaxOrderMessageReference=self._to_bytes(i_tuple[19])

class SettlementInfoField(Base):
  """投资者结算结果"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('Content',ctypes.c_char*501)# 消息正文
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,TradingDay= '',SettlementID=0,BrokerID='',InvestorID='',SequenceNo=0,Content='',AccountID='',CurrencyID=''):

    super(SettlementInfoField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.SequenceNo=int(SequenceNo)
    self.Content=self._to_bytes(Content)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.SettlementID=int(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.SequenceNo=int(i_tuple[5])
    self.Content=self._to_bytes(i_tuple[6])
    self.AccountID=self._to_bytes(i_tuple[7])
    self.CurrencyID=self._to_bytes(i_tuple[8])

class InstrumentMarginRateAdjustField(Base):
  """合约保证金率调整"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('LongMarginRatioByMoney',ctypes.c_double)# 多头保证金率
    ,('LongMarginRatioByVolume',ctypes.c_double)# 多头保证金费
    ,('ShortMarginRatioByMoney',ctypes.c_double)# 空头保证金率
    ,('ShortMarginRatioByVolume',ctypes.c_double)# 空头保证金费
    ,('IsRelative',ctypes.c_int)# 是否相对交易所收取
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',HedgeFlag='',LongMarginRatioByMoney=0.0,LongMarginRatioByVolume=0.0,ShortMarginRatioByMoney=0.0,ShortMarginRatioByVolume=0.0,IsRelative=0):

    super(InstrumentMarginRateAdjustField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.LongMarginRatioByMoney=float(LongMarginRatioByMoney)
    self.LongMarginRatioByVolume=float(LongMarginRatioByVolume)
    self.ShortMarginRatioByMoney=float(ShortMarginRatioByMoney)
    self.ShortMarginRatioByVolume=float(ShortMarginRatioByVolume)
    self.IsRelative=int(IsRelative)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.LongMarginRatioByMoney=float(i_tuple[6])
    self.LongMarginRatioByVolume=float(i_tuple[7])
    self.ShortMarginRatioByMoney=float(i_tuple[8])
    self.ShortMarginRatioByVolume=float(i_tuple[9])
    self.IsRelative=int(i_tuple[10])

class ExchangeMarginRateField(Base):
  """交易所保证金率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('LongMarginRatioByMoney',ctypes.c_double)# 多头保证金率
    ,('LongMarginRatioByVolume',ctypes.c_double)# 多头保证金费
    ,('ShortMarginRatioByMoney',ctypes.c_double)# 空头保证金率
    ,('ShortMarginRatioByVolume',ctypes.c_double)# 空头保证金费
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InstrumentID='',HedgeFlag='',LongMarginRatioByMoney=0.0,LongMarginRatioByVolume=0.0,ShortMarginRatioByMoney=0.0,ShortMarginRatioByVolume=0.0,ExchangeID=''):

    super(ExchangeMarginRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.LongMarginRatioByMoney=float(LongMarginRatioByMoney)
    self.LongMarginRatioByVolume=float(LongMarginRatioByVolume)
    self.ShortMarginRatioByMoney=float(ShortMarginRatioByMoney)
    self.ShortMarginRatioByVolume=float(ShortMarginRatioByVolume)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.HedgeFlag=self._to_bytes(i_tuple[3])
    self.LongMarginRatioByMoney=float(i_tuple[4])
    self.LongMarginRatioByVolume=float(i_tuple[5])
    self.ShortMarginRatioByMoney=float(i_tuple[6])
    self.ShortMarginRatioByVolume=float(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])

class ExchangeMarginRateAdjustField(Base):
  """交易所保证金率调整"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('LongMarginRatioByMoney',ctypes.c_double)# 跟随交易所投资者多头保证金率
    ,('LongMarginRatioByVolume',ctypes.c_double)# 跟随交易所投资者多头保证金费
    ,('ShortMarginRatioByMoney',ctypes.c_double)# 跟随交易所投资者空头保证金率
    ,('ShortMarginRatioByVolume',ctypes.c_double)# 跟随交易所投资者空头保证金费
    ,('ExchLongMarginRatioByMoney',ctypes.c_double)# 交易所多头保证金率
    ,('ExchLongMarginRatioByVolume',ctypes.c_double)# 交易所多头保证金费
    ,('ExchShortMarginRatioByMoney',ctypes.c_double)# 交易所空头保证金率
    ,('ExchShortMarginRatioByVolume',ctypes.c_double)# 交易所空头保证金费
    ,('NoLongMarginRatioByMoney',ctypes.c_double)# 不跟随交易所投资者多头保证金率
    ,('NoLongMarginRatioByVolume',ctypes.c_double)# 不跟随交易所投资者多头保证金费
    ,('NoShortMarginRatioByMoney',ctypes.c_double)# 不跟随交易所投资者空头保证金率
    ,('NoShortMarginRatioByVolume',ctypes.c_double)# 不跟随交易所投资者空头保证金费
]

  def __init__(self,BrokerID= '',InstrumentID='',HedgeFlag='',LongMarginRatioByMoney=0.0,LongMarginRatioByVolume=0.0,ShortMarginRatioByMoney=0.0,ShortMarginRatioByVolume=0.0,ExchLongMarginRatioByMoney=0.0,ExchLongMarginRatioByVolume=0.0,ExchShortMarginRatioByMoney=0.0,ExchShortMarginRatioByVolume=0.0,NoLongMarginRatioByMoney=0.0,NoLongMarginRatioByVolume=0.0,NoShortMarginRatioByMoney=0.0,NoShortMarginRatioByVolume=0.0):

    super(ExchangeMarginRateAdjustField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.LongMarginRatioByMoney=float(LongMarginRatioByMoney)
    self.LongMarginRatioByVolume=float(LongMarginRatioByVolume)
    self.ShortMarginRatioByMoney=float(ShortMarginRatioByMoney)
    self.ShortMarginRatioByVolume=float(ShortMarginRatioByVolume)
    self.ExchLongMarginRatioByMoney=float(ExchLongMarginRatioByMoney)
    self.ExchLongMarginRatioByVolume=float(ExchLongMarginRatioByVolume)
    self.ExchShortMarginRatioByMoney=float(ExchShortMarginRatioByMoney)
    self.ExchShortMarginRatioByVolume=float(ExchShortMarginRatioByVolume)
    self.NoLongMarginRatioByMoney=float(NoLongMarginRatioByMoney)
    self.NoLongMarginRatioByVolume=float(NoLongMarginRatioByVolume)
    self.NoShortMarginRatioByMoney=float(NoShortMarginRatioByMoney)
    self.NoShortMarginRatioByVolume=float(NoShortMarginRatioByVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.HedgeFlag=self._to_bytes(i_tuple[3])
    self.LongMarginRatioByMoney=float(i_tuple[4])
    self.LongMarginRatioByVolume=float(i_tuple[5])
    self.ShortMarginRatioByMoney=float(i_tuple[6])
    self.ShortMarginRatioByVolume=float(i_tuple[7])
    self.ExchLongMarginRatioByMoney=float(i_tuple[8])
    self.ExchLongMarginRatioByVolume=float(i_tuple[9])
    self.ExchShortMarginRatioByMoney=float(i_tuple[10])
    self.ExchShortMarginRatioByVolume=float(i_tuple[11])
    self.NoLongMarginRatioByMoney=float(i_tuple[12])
    self.NoLongMarginRatioByVolume=float(i_tuple[13])
    self.NoShortMarginRatioByMoney=float(i_tuple[14])
    self.NoShortMarginRatioByVolume=float(i_tuple[15])

class ExchangeRateField(Base):
  """汇率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('FromCurrencyID',ctypes.c_char*4)# 源币种
    ,('FromCurrencyUnit',ctypes.c_double)# 源币种单位数量
    ,('ToCurrencyID',ctypes.c_char*4)# 目标币种
    ,('ExchangeRate',ctypes.c_double)# 汇率
]

  def __init__(self,BrokerID= '',FromCurrencyID='',FromCurrencyUnit=0.0,ToCurrencyID='',ExchangeRate=0.0):

    super(ExchangeRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.FromCurrencyID=self._to_bytes(FromCurrencyID)
    self.FromCurrencyUnit=float(FromCurrencyUnit)
    self.ToCurrencyID=self._to_bytes(ToCurrencyID)
    self.ExchangeRate=float(ExchangeRate)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.FromCurrencyID=self._to_bytes(i_tuple[2])
    self.FromCurrencyUnit=float(i_tuple[3])
    self.ToCurrencyID=self._to_bytes(i_tuple[4])
    self.ExchangeRate=float(i_tuple[5])

class SettlementRefField(Base):
  """结算引用"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
]

  def __init__(self,TradingDay= '',SettlementID=0):

    super(SettlementRefField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.SettlementID=int(i_tuple[2])

class CurrentTimeField(Base):
  """当前时间"""
  _fields_ = [
    ('CurrDate',ctypes.c_char*9)# ///当前日期
    ,('CurrTime',ctypes.c_char*9)# 当前时间
    ,('CurrMillisec',ctypes.c_int)# 当前时间（毫秒）
    ,('ActionDay',ctypes.c_char*9)# 业务日期
]

  def __init__(self,CurrDate= '',CurrTime='',CurrMillisec=0,ActionDay=''):

    super(CurrentTimeField,self).__init__()

    self.CurrDate=self._to_bytes(CurrDate)
    self.CurrTime=self._to_bytes(CurrTime)
    self.CurrMillisec=int(CurrMillisec)
    self.ActionDay=self._to_bytes(ActionDay)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.CurrDate=self._to_bytes(i_tuple[1])
    self.CurrTime=self._to_bytes(i_tuple[2])
    self.CurrMillisec=int(i_tuple[3])
    self.ActionDay=self._to_bytes(i_tuple[4])

class CommPhaseField(Base):
  """通讯阶段"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('CommPhaseNo',ctypes.c_short)# 通讯时段编号
    ,('SystemID',ctypes.c_char*21)# 系统编号
]

  def __init__(self,TradingDay= '',CommPhaseNo=0,SystemID=''):

    super(CommPhaseField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.CommPhaseNo=int(CommPhaseNo)
    self.SystemID=self._to_bytes(SystemID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.CommPhaseNo=int(i_tuple[2])
    self.SystemID=self._to_bytes(i_tuple[3])

class LoginInfoField(Base):
  """登录信息"""
  _fields_ = [
    ('FrontID',ctypes.c_int)# ///前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('LoginDate',ctypes.c_char*9)# 登录日期
    ,('LoginTime',ctypes.c_char*9)# 登录时间
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('InterfaceProductInfo',ctypes.c_char*11)# 接口端产品信息
    ,('ProtocolInfo',ctypes.c_char*11)# 协议信息
    ,('SystemName',ctypes.c_char*41)# 系统名称
    ,('PasswordDeprecated',ctypes.c_char*41)# 密码,已弃用
    ,('MaxOrderRef',ctypes.c_char*13)# 最大报单引用
    ,('SHFETime',ctypes.c_char*9)# 上期所时间
    ,('DCETime',ctypes.c_char*9)# 大商所时间
    ,('CZCETime',ctypes.c_char*9)# 郑商所时间
    ,('FFEXTime',ctypes.c_char*9)# 中金所时间
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('OneTimePassword',ctypes.c_char*41)# 动态密码
    ,('INETime',ctypes.c_char*9)# 能源中心时间
    ,('IsQryControl',ctypes.c_int)# 查询时是否需要流控
    ,('LoginRemark',ctypes.c_char*36)# 登录备注
    ,('Password',ctypes.c_char*41)# 密码
]

  def __init__(self,FrontID= 0,SessionID=0,BrokerID='',UserID='',LoginDate='',LoginTime='',IPAddress='',UserProductInfo='',InterfaceProductInfo='',ProtocolInfo='',SystemName='',PasswordDeprecated='',MaxOrderRef='',SHFETime='',DCETime='',CZCETime='',FFEXTime='',MacAddress='',OneTimePassword='',INETime='',IsQryControl=0,LoginRemark='',Password=''):

    super(LoginInfoField,self).__init__()

    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.LoginDate=self._to_bytes(LoginDate)
    self.LoginTime=self._to_bytes(LoginTime)
    self.IPAddress=self._to_bytes(IPAddress)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.InterfaceProductInfo=self._to_bytes(InterfaceProductInfo)
    self.ProtocolInfo=self._to_bytes(ProtocolInfo)
    self.SystemName=self._to_bytes(SystemName)
    self.PasswordDeprecated=self._to_bytes(PasswordDeprecated)
    self.MaxOrderRef=self._to_bytes(MaxOrderRef)
    self.SHFETime=self._to_bytes(SHFETime)
    self.DCETime=self._to_bytes(DCETime)
    self.CZCETime=self._to_bytes(CZCETime)
    self.FFEXTime=self._to_bytes(FFEXTime)
    self.MacAddress=self._to_bytes(MacAddress)
    self.OneTimePassword=self._to_bytes(OneTimePassword)
    self.INETime=self._to_bytes(INETime)
    self.IsQryControl=int(IsQryControl)
    self.LoginRemark=self._to_bytes(LoginRemark)
    self.Password=self._to_bytes(Password)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FrontID=int(i_tuple[1])
    self.SessionID=int(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.UserID=self._to_bytes(i_tuple[4])
    self.LoginDate=self._to_bytes(i_tuple[5])
    self.LoginTime=self._to_bytes(i_tuple[6])
    self.IPAddress=self._to_bytes(i_tuple[7])
    self.UserProductInfo=self._to_bytes(i_tuple[8])
    self.InterfaceProductInfo=self._to_bytes(i_tuple[9])
    self.ProtocolInfo=self._to_bytes(i_tuple[10])
    self.SystemName=self._to_bytes(i_tuple[11])
    self.PasswordDeprecated=self._to_bytes(i_tuple[12])
    self.MaxOrderRef=self._to_bytes(i_tuple[13])
    self.SHFETime=self._to_bytes(i_tuple[14])
    self.DCETime=self._to_bytes(i_tuple[15])
    self.CZCETime=self._to_bytes(i_tuple[16])
    self.FFEXTime=self._to_bytes(i_tuple[17])
    self.MacAddress=self._to_bytes(i_tuple[18])
    self.OneTimePassword=self._to_bytes(i_tuple[19])
    self.INETime=self._to_bytes(i_tuple[20])
    self.IsQryControl=int(i_tuple[21])
    self.LoginRemark=self._to_bytes(i_tuple[22])
    self.Password=self._to_bytes(i_tuple[23])

class LogoutAllField(Base):
  """登录信息"""
  _fields_ = [
    ('FrontID',ctypes.c_int)# ///前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('SystemName',ctypes.c_char*41)# 系统名称
]

  def __init__(self,FrontID= 0,SessionID=0,SystemName=''):

    super(LogoutAllField,self).__init__()

    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.SystemName=self._to_bytes(SystemName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FrontID=int(i_tuple[1])
    self.SessionID=int(i_tuple[2])
    self.SystemName=self._to_bytes(i_tuple[3])

class FrontStatusField(Base):
  """前置状态"""
  _fields_ = [
    ('FrontID',ctypes.c_int)# ///前置编号
    ,('LastReportDate',ctypes.c_char*9)# 上次报告日期
    ,('LastReportTime',ctypes.c_char*9)# 上次报告时间
    ,('IsActive',ctypes.c_int)# 是否活跃
]

  def __init__(self,FrontID= 0,LastReportDate='',LastReportTime='',IsActive=0):

    super(FrontStatusField,self).__init__()

    self.FrontID=int(FrontID)
    self.LastReportDate=self._to_bytes(LastReportDate)
    self.LastReportTime=self._to_bytes(LastReportTime)
    self.IsActive=int(IsActive)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FrontID=int(i_tuple[1])
    self.LastReportDate=self._to_bytes(i_tuple[2])
    self.LastReportTime=self._to_bytes(i_tuple[3])
    self.IsActive=int(i_tuple[4])

class UserPasswordUpdateField(Base):
  """用户口令变更"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OldPassword',ctypes.c_char*41)# 原来的口令
    ,('NewPassword',ctypes.c_char*41)# 新的口令
]

  def __init__(self,BrokerID= '',UserID='',OldPassword='',NewPassword=''):

    super(UserPasswordUpdateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.OldPassword=self._to_bytes(OldPassword)
    self.NewPassword=self._to_bytes(NewPassword)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.OldPassword=self._to_bytes(i_tuple[3])
    self.NewPassword=self._to_bytes(i_tuple[4])

class InputOrderField(Base):
  """输入报单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OrderPriceType',ctypes.c_char)# 报单价格条件
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('CombOffsetFlag',ctypes.c_char*5)# 组合开平标志
    ,('CombHedgeFlag',ctypes.c_char*5)# 组合投机套保标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeTotalOriginal',ctypes.c_int)# 数量
    ,('TimeCondition',ctypes.c_char)# 有效期类型
    ,('GTDDate',ctypes.c_char*9)# GTD日期
    ,('VolumeCondition',ctypes.c_char)# 成交量类型
    ,('MinVolume',ctypes.c_int)# 最小成交量
    ,('ContingentCondition',ctypes.c_char)# 触发条件
    ,('StopPrice',ctypes.c_double)# 止损价
    ,('ForceCloseReason',ctypes.c_char)# 强平原因
    ,('IsAutoSuspend',ctypes.c_int)# 自动挂起标志
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('UserForceClose',ctypes.c_int)# 用户强评标志
    ,('IsSwapOrder',ctypes.c_int)# 互换单标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OrderRef='',UserID='',OrderPriceType='',Direction='',CombOffsetFlag='',CombHedgeFlag='',LimitPrice=0.0,VolumeTotalOriginal=0,TimeCondition='',GTDDate='',VolumeCondition='',MinVolume=0,ContingentCondition='',StopPrice=0.0,ForceCloseReason='',IsAutoSuspend=0,BusinessUnit='',RequestID=0,UserForceClose=0,IsSwapOrder=0,ExchangeID='',InvestUnitID='',AccountID='',CurrencyID='',ClientID='',IPAddress='',MacAddress=''):

    super(InputOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OrderRef=self._to_bytes(OrderRef)
    self.UserID=self._to_bytes(UserID)
    self.OrderPriceType=self._to_bytes(OrderPriceType)
    self.Direction=self._to_bytes(Direction)
    self.CombOffsetFlag=self._to_bytes(CombOffsetFlag)
    self.CombHedgeFlag=self._to_bytes(CombHedgeFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeTotalOriginal=int(VolumeTotalOriginal)
    self.TimeCondition=self._to_bytes(TimeCondition)
    self.GTDDate=self._to_bytes(GTDDate)
    self.VolumeCondition=self._to_bytes(VolumeCondition)
    self.MinVolume=int(MinVolume)
    self.ContingentCondition=self._to_bytes(ContingentCondition)
    self.StopPrice=float(StopPrice)
    self.ForceCloseReason=self._to_bytes(ForceCloseReason)
    self.IsAutoSuspend=int(IsAutoSuspend)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.RequestID=int(RequestID)
    self.UserForceClose=int(UserForceClose)
    self.IsSwapOrder=int(IsSwapOrder)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.OrderPriceType=self._to_bytes(i_tuple[6])
    self.Direction=self._to_bytes(i_tuple[7])
    self.CombOffsetFlag=self._to_bytes(i_tuple[8])
    self.CombHedgeFlag=self._to_bytes(i_tuple[9])
    self.LimitPrice=float(i_tuple[10])
    self.VolumeTotalOriginal=int(i_tuple[11])
    self.TimeCondition=self._to_bytes(i_tuple[12])
    self.GTDDate=self._to_bytes(i_tuple[13])
    self.VolumeCondition=self._to_bytes(i_tuple[14])
    self.MinVolume=int(i_tuple[15])
    self.ContingentCondition=self._to_bytes(i_tuple[16])
    self.StopPrice=float(i_tuple[17])
    self.ForceCloseReason=self._to_bytes(i_tuple[18])
    self.IsAutoSuspend=int(i_tuple[19])
    self.BusinessUnit=self._to_bytes(i_tuple[20])
    self.RequestID=int(i_tuple[21])
    self.UserForceClose=int(i_tuple[22])
    self.IsSwapOrder=int(i_tuple[23])
    self.ExchangeID=self._to_bytes(i_tuple[24])
    self.InvestUnitID=self._to_bytes(i_tuple[25])
    self.AccountID=self._to_bytes(i_tuple[26])
    self.CurrencyID=self._to_bytes(i_tuple[27])
    self.ClientID=self._to_bytes(i_tuple[28])
    self.IPAddress=self._to_bytes(i_tuple[29])
    self.MacAddress=self._to_bytes(i_tuple[30])

class OrderField(Base):
  """报单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OrderPriceType',ctypes.c_char)# 报单价格条件
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('CombOffsetFlag',ctypes.c_char*5)# 组合开平标志
    ,('CombHedgeFlag',ctypes.c_char*5)# 组合投机套保标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeTotalOriginal',ctypes.c_int)# 数量
    ,('TimeCondition',ctypes.c_char)# 有效期类型
    ,('GTDDate',ctypes.c_char*9)# GTD日期
    ,('VolumeCondition',ctypes.c_char)# 成交量类型
    ,('MinVolume',ctypes.c_int)# 最小成交量
    ,('ContingentCondition',ctypes.c_char)# 触发条件
    ,('StopPrice',ctypes.c_double)# 止损价
    ,('ForceCloseReason',ctypes.c_char)# 强平原因
    ,('IsAutoSuspend',ctypes.c_int)# 自动挂起标志
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 报单提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('OrderSource',ctypes.c_char)# 报单来源
    ,('OrderStatus',ctypes.c_char)# 报单状态
    ,('OrderType',ctypes.c_char)# 报单类型
    ,('VolumeTraded',ctypes.c_int)# 今成交数量
    ,('VolumeTotal',ctypes.c_int)# 剩余数量
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 委托时间
    ,('ActiveTime',ctypes.c_char*9)# 激活时间
    ,('SuspendTime',ctypes.c_char*9)# 挂起时间
    ,('UpdateTime',ctypes.c_char*9)# 最后修改时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ActiveTraderID',ctypes.c_char*21)# 最后修改交易所交易员代码
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('UserForceClose',ctypes.c_int)# 用户强评标志
    ,('ActiveUserID',ctypes.c_char*16)# 操作用户代码
    ,('BrokerOrderSeq',ctypes.c_int)# 经纪公司报单编号
    ,('RelativeOrderSysID',ctypes.c_char*21)# 相关报单
    ,('ZCETotalTradedVolume',ctypes.c_int)# 郑商所成交数量
    ,('IsSwapOrder',ctypes.c_int)# 互换单标志
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OrderRef='',UserID='',OrderPriceType='',Direction='',CombOffsetFlag='',CombHedgeFlag='',LimitPrice=0.0,VolumeTotalOriginal=0,TimeCondition='',GTDDate='',VolumeCondition='',MinVolume=0,ContingentCondition='',StopPrice=0.0,ForceCloseReason='',IsAutoSuspend=0,BusinessUnit='',RequestID=0,OrderLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,OrderSysID='',OrderSource='',OrderStatus='',OrderType='',VolumeTraded=0,VolumeTotal=0,InsertDate='',InsertTime='',ActiveTime='',SuspendTime='',UpdateTime='',CancelTime='',ActiveTraderID='',ClearingPartID='',SequenceNo=0,FrontID=0,SessionID=0,UserProductInfo='',StatusMsg='',UserForceClose=0,ActiveUserID='',BrokerOrderSeq=0,RelativeOrderSysID='',ZCETotalTradedVolume=0,IsSwapOrder=0,BranchID='',InvestUnitID='',AccountID='',CurrencyID='',IPAddress='',MacAddress=''):

    super(OrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OrderRef=self._to_bytes(OrderRef)
    self.UserID=self._to_bytes(UserID)
    self.OrderPriceType=self._to_bytes(OrderPriceType)
    self.Direction=self._to_bytes(Direction)
    self.CombOffsetFlag=self._to_bytes(CombOffsetFlag)
    self.CombHedgeFlag=self._to_bytes(CombHedgeFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeTotalOriginal=int(VolumeTotalOriginal)
    self.TimeCondition=self._to_bytes(TimeCondition)
    self.GTDDate=self._to_bytes(GTDDate)
    self.VolumeCondition=self._to_bytes(VolumeCondition)
    self.MinVolume=int(MinVolume)
    self.ContingentCondition=self._to_bytes(ContingentCondition)
    self.StopPrice=float(StopPrice)
    self.ForceCloseReason=self._to_bytes(ForceCloseReason)
    self.IsAutoSuspend=int(IsAutoSuspend)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.RequestID=int(RequestID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.OrderSource=self._to_bytes(OrderSource)
    self.OrderStatus=self._to_bytes(OrderStatus)
    self.OrderType=self._to_bytes(OrderType)
    self.VolumeTraded=int(VolumeTraded)
    self.VolumeTotal=int(VolumeTotal)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.ActiveTime=self._to_bytes(ActiveTime)
    self.SuspendTime=self._to_bytes(SuspendTime)
    self.UpdateTime=self._to_bytes(UpdateTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ActiveTraderID=self._to_bytes(ActiveTraderID)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.UserForceClose=int(UserForceClose)
    self.ActiveUserID=self._to_bytes(ActiveUserID)
    self.BrokerOrderSeq=int(BrokerOrderSeq)
    self.RelativeOrderSysID=self._to_bytes(RelativeOrderSysID)
    self.ZCETotalTradedVolume=int(ZCETotalTradedVolume)
    self.IsSwapOrder=int(IsSwapOrder)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.OrderPriceType=self._to_bytes(i_tuple[6])
    self.Direction=self._to_bytes(i_tuple[7])
    self.CombOffsetFlag=self._to_bytes(i_tuple[8])
    self.CombHedgeFlag=self._to_bytes(i_tuple[9])
    self.LimitPrice=float(i_tuple[10])
    self.VolumeTotalOriginal=int(i_tuple[11])
    self.TimeCondition=self._to_bytes(i_tuple[12])
    self.GTDDate=self._to_bytes(i_tuple[13])
    self.VolumeCondition=self._to_bytes(i_tuple[14])
    self.MinVolume=int(i_tuple[15])
    self.ContingentCondition=self._to_bytes(i_tuple[16])
    self.StopPrice=float(i_tuple[17])
    self.ForceCloseReason=self._to_bytes(i_tuple[18])
    self.IsAutoSuspend=int(i_tuple[19])
    self.BusinessUnit=self._to_bytes(i_tuple[20])
    self.RequestID=int(i_tuple[21])
    self.OrderLocalID=self._to_bytes(i_tuple[22])
    self.ExchangeID=self._to_bytes(i_tuple[23])
    self.ParticipantID=self._to_bytes(i_tuple[24])
    self.ClientID=self._to_bytes(i_tuple[25])
    self.ExchangeInstID=self._to_bytes(i_tuple[26])
    self.TraderID=self._to_bytes(i_tuple[27])
    self.InstallID=int(i_tuple[28])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[29])
    self.NotifySequence=int(i_tuple[30])
    self.TradingDay=self._to_bytes(i_tuple[31])
    self.SettlementID=int(i_tuple[32])
    self.OrderSysID=self._to_bytes(i_tuple[33])
    self.OrderSource=self._to_bytes(i_tuple[34])
    self.OrderStatus=self._to_bytes(i_tuple[35])
    self.OrderType=self._to_bytes(i_tuple[36])
    self.VolumeTraded=int(i_tuple[37])
    self.VolumeTotal=int(i_tuple[38])
    self.InsertDate=self._to_bytes(i_tuple[39])
    self.InsertTime=self._to_bytes(i_tuple[40])
    self.ActiveTime=self._to_bytes(i_tuple[41])
    self.SuspendTime=self._to_bytes(i_tuple[42])
    self.UpdateTime=self._to_bytes(i_tuple[43])
    self.CancelTime=self._to_bytes(i_tuple[44])
    self.ActiveTraderID=self._to_bytes(i_tuple[45])
    self.ClearingPartID=self._to_bytes(i_tuple[46])
    self.SequenceNo=int(i_tuple[47])
    self.FrontID=int(i_tuple[48])
    self.SessionID=int(i_tuple[49])
    self.UserProductInfo=self._to_bytes(i_tuple[50])
    self.StatusMsg=self._to_bytes(i_tuple[51])
    self.UserForceClose=int(i_tuple[52])
    self.ActiveUserID=self._to_bytes(i_tuple[53])
    self.BrokerOrderSeq=int(i_tuple[54])
    self.RelativeOrderSysID=self._to_bytes(i_tuple[55])
    self.ZCETotalTradedVolume=int(i_tuple[56])
    self.IsSwapOrder=int(i_tuple[57])
    self.BranchID=self._to_bytes(i_tuple[58])
    self.InvestUnitID=self._to_bytes(i_tuple[59])
    self.AccountID=self._to_bytes(i_tuple[60])
    self.CurrencyID=self._to_bytes(i_tuple[61])
    self.IPAddress=self._to_bytes(i_tuple[62])
    self.MacAddress=self._to_bytes(i_tuple[63])

class ExchangeOrderField(Base):
  """交易所报单"""
  _fields_ = [
    ('OrderPriceType',ctypes.c_char)# ///报单价格条件
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('CombOffsetFlag',ctypes.c_char*5)# 组合开平标志
    ,('CombHedgeFlag',ctypes.c_char*5)# 组合投机套保标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeTotalOriginal',ctypes.c_int)# 数量
    ,('TimeCondition',ctypes.c_char)# 有效期类型
    ,('GTDDate',ctypes.c_char*9)# GTD日期
    ,('VolumeCondition',ctypes.c_char)# 成交量类型
    ,('MinVolume',ctypes.c_int)# 最小成交量
    ,('ContingentCondition',ctypes.c_char)# 触发条件
    ,('StopPrice',ctypes.c_double)# 止损价
    ,('ForceCloseReason',ctypes.c_char)# 强平原因
    ,('IsAutoSuspend',ctypes.c_int)# 自动挂起标志
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 报单提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('OrderSource',ctypes.c_char)# 报单来源
    ,('OrderStatus',ctypes.c_char)# 报单状态
    ,('OrderType',ctypes.c_char)# 报单类型
    ,('VolumeTraded',ctypes.c_int)# 今成交数量
    ,('VolumeTotal',ctypes.c_int)# 剩余数量
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 委托时间
    ,('ActiveTime',ctypes.c_char*9)# 激活时间
    ,('SuspendTime',ctypes.c_char*9)# 挂起时间
    ,('UpdateTime',ctypes.c_char*9)# 最后修改时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ActiveTraderID',ctypes.c_char*21)# 最后修改交易所交易员代码
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,OrderPriceType= '',Direction='',CombOffsetFlag='',CombHedgeFlag='',LimitPrice=0.0,VolumeTotalOriginal=0,TimeCondition='',GTDDate='',VolumeCondition='',MinVolume=0,ContingentCondition='',StopPrice=0.0,ForceCloseReason='',IsAutoSuspend=0,BusinessUnit='',RequestID=0,OrderLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,OrderSysID='',OrderSource='',OrderStatus='',OrderType='',VolumeTraded=0,VolumeTotal=0,InsertDate='',InsertTime='',ActiveTime='',SuspendTime='',UpdateTime='',CancelTime='',ActiveTraderID='',ClearingPartID='',SequenceNo=0,BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeOrderField,self).__init__()

    self.OrderPriceType=self._to_bytes(OrderPriceType)
    self.Direction=self._to_bytes(Direction)
    self.CombOffsetFlag=self._to_bytes(CombOffsetFlag)
    self.CombHedgeFlag=self._to_bytes(CombHedgeFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeTotalOriginal=int(VolumeTotalOriginal)
    self.TimeCondition=self._to_bytes(TimeCondition)
    self.GTDDate=self._to_bytes(GTDDate)
    self.VolumeCondition=self._to_bytes(VolumeCondition)
    self.MinVolume=int(MinVolume)
    self.ContingentCondition=self._to_bytes(ContingentCondition)
    self.StopPrice=float(StopPrice)
    self.ForceCloseReason=self._to_bytes(ForceCloseReason)
    self.IsAutoSuspend=int(IsAutoSuspend)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.RequestID=int(RequestID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.OrderSource=self._to_bytes(OrderSource)
    self.OrderStatus=self._to_bytes(OrderStatus)
    self.OrderType=self._to_bytes(OrderType)
    self.VolumeTraded=int(VolumeTraded)
    self.VolumeTotal=int(VolumeTotal)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.ActiveTime=self._to_bytes(ActiveTime)
    self.SuspendTime=self._to_bytes(SuspendTime)
    self.UpdateTime=self._to_bytes(UpdateTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ActiveTraderID=self._to_bytes(ActiveTraderID)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.OrderPriceType=self._to_bytes(i_tuple[1])
    self.Direction=self._to_bytes(i_tuple[2])
    self.CombOffsetFlag=self._to_bytes(i_tuple[3])
    self.CombHedgeFlag=self._to_bytes(i_tuple[4])
    self.LimitPrice=float(i_tuple[5])
    self.VolumeTotalOriginal=int(i_tuple[6])
    self.TimeCondition=self._to_bytes(i_tuple[7])
    self.GTDDate=self._to_bytes(i_tuple[8])
    self.VolumeCondition=self._to_bytes(i_tuple[9])
    self.MinVolume=int(i_tuple[10])
    self.ContingentCondition=self._to_bytes(i_tuple[11])
    self.StopPrice=float(i_tuple[12])
    self.ForceCloseReason=self._to_bytes(i_tuple[13])
    self.IsAutoSuspend=int(i_tuple[14])
    self.BusinessUnit=self._to_bytes(i_tuple[15])
    self.RequestID=int(i_tuple[16])
    self.OrderLocalID=self._to_bytes(i_tuple[17])
    self.ExchangeID=self._to_bytes(i_tuple[18])
    self.ParticipantID=self._to_bytes(i_tuple[19])
    self.ClientID=self._to_bytes(i_tuple[20])
    self.ExchangeInstID=self._to_bytes(i_tuple[21])
    self.TraderID=self._to_bytes(i_tuple[22])
    self.InstallID=int(i_tuple[23])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[24])
    self.NotifySequence=int(i_tuple[25])
    self.TradingDay=self._to_bytes(i_tuple[26])
    self.SettlementID=int(i_tuple[27])
    self.OrderSysID=self._to_bytes(i_tuple[28])
    self.OrderSource=self._to_bytes(i_tuple[29])
    self.OrderStatus=self._to_bytes(i_tuple[30])
    self.OrderType=self._to_bytes(i_tuple[31])
    self.VolumeTraded=int(i_tuple[32])
    self.VolumeTotal=int(i_tuple[33])
    self.InsertDate=self._to_bytes(i_tuple[34])
    self.InsertTime=self._to_bytes(i_tuple[35])
    self.ActiveTime=self._to_bytes(i_tuple[36])
    self.SuspendTime=self._to_bytes(i_tuple[37])
    self.UpdateTime=self._to_bytes(i_tuple[38])
    self.CancelTime=self._to_bytes(i_tuple[39])
    self.ActiveTraderID=self._to_bytes(i_tuple[40])
    self.ClearingPartID=self._to_bytes(i_tuple[41])
    self.SequenceNo=int(i_tuple[42])
    self.BranchID=self._to_bytes(i_tuple[43])
    self.IPAddress=self._to_bytes(i_tuple[44])
    self.MacAddress=self._to_bytes(i_tuple[45])

class ExchangeOrderInsertErrorField(Base):
  """交易所报单插入失败"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,ExchangeID= '',ParticipantID='',TraderID='',InstallID=0,OrderLocalID='',ErrorID=0,ErrorMsg=''):

    super(ExchangeOrderInsertErrorField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.TraderID=self._to_bytes(i_tuple[3])
    self.InstallID=int(i_tuple[4])
    self.OrderLocalID=self._to_bytes(i_tuple[5])
    self.ErrorID=int(i_tuple[6])
    self.ErrorMsg=self._to_bytes(i_tuple[7])

class InputOrderActionField(Base):
  """输入报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OrderActionRef',ctypes.c_int)# 报单操作引用
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeChange',ctypes.c_int)# 数量变化
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OrderActionRef=0,OrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',OrderSysID='',ActionFlag='',LimitPrice=0.0,VolumeChange=0,UserID='',InstrumentID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(InputOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OrderActionRef=int(OrderActionRef)
    self.OrderRef=self._to_bytes(OrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeChange=int(VolumeChange)
    self.UserID=self._to_bytes(UserID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OrderActionRef=int(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.OrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.LimitPrice=float(i_tuple[11])
    self.VolumeChange=int(i_tuple[12])
    self.UserID=self._to_bytes(i_tuple[13])
    self.InstrumentID=self._to_bytes(i_tuple[14])
    self.InvestUnitID=self._to_bytes(i_tuple[15])
    self.IPAddress=self._to_bytes(i_tuple[16])
    self.MacAddress=self._to_bytes(i_tuple[17])

class OrderActionField(Base):
  """报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OrderActionRef',ctypes.c_int)# 报单操作引用
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeChange',ctypes.c_int)# 数量变化
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OrderActionRef=0,OrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',OrderSysID='',ActionFlag='',LimitPrice=0.0,VolumeChange=0,ActionDate='',ActionTime='',TraderID='',InstallID=0,OrderLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',StatusMsg='',InstrumentID='',BranchID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(OrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OrderActionRef=int(OrderActionRef)
    self.OrderRef=self._to_bytes(OrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeChange=int(VolumeChange)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OrderActionRef=int(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.OrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.LimitPrice=float(i_tuple[11])
    self.VolumeChange=int(i_tuple[12])
    self.ActionDate=self._to_bytes(i_tuple[13])
    self.ActionTime=self._to_bytes(i_tuple[14])
    self.TraderID=self._to_bytes(i_tuple[15])
    self.InstallID=int(i_tuple[16])
    self.OrderLocalID=self._to_bytes(i_tuple[17])
    self.ActionLocalID=self._to_bytes(i_tuple[18])
    self.ParticipantID=self._to_bytes(i_tuple[19])
    self.ClientID=self._to_bytes(i_tuple[20])
    self.BusinessUnit=self._to_bytes(i_tuple[21])
    self.OrderActionStatus=self._to_bytes(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.StatusMsg=self._to_bytes(i_tuple[24])
    self.InstrumentID=self._to_bytes(i_tuple[25])
    self.BranchID=self._to_bytes(i_tuple[26])
    self.InvestUnitID=self._to_bytes(i_tuple[27])
    self.IPAddress=self._to_bytes(i_tuple[28])
    self.MacAddress=self._to_bytes(i_tuple[29])

class ExchangeOrderActionField(Base):
  """交易所报单操作"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeChange',ctypes.c_int)# 数量变化
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,ExchangeID= '',OrderSysID='',ActionFlag='',LimitPrice=0.0,VolumeChange=0,ActionDate='',ActionTime='',TraderID='',InstallID=0,OrderLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeOrderActionField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeChange=int(VolumeChange)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.OrderSysID=self._to_bytes(i_tuple[2])
    self.ActionFlag=self._to_bytes(i_tuple[3])
    self.LimitPrice=float(i_tuple[4])
    self.VolumeChange=int(i_tuple[5])
    self.ActionDate=self._to_bytes(i_tuple[6])
    self.ActionTime=self._to_bytes(i_tuple[7])
    self.TraderID=self._to_bytes(i_tuple[8])
    self.InstallID=int(i_tuple[9])
    self.OrderLocalID=self._to_bytes(i_tuple[10])
    self.ActionLocalID=self._to_bytes(i_tuple[11])
    self.ParticipantID=self._to_bytes(i_tuple[12])
    self.ClientID=self._to_bytes(i_tuple[13])
    self.BusinessUnit=self._to_bytes(i_tuple[14])
    self.OrderActionStatus=self._to_bytes(i_tuple[15])
    self.UserID=self._to_bytes(i_tuple[16])
    self.BranchID=self._to_bytes(i_tuple[17])
    self.IPAddress=self._to_bytes(i_tuple[18])
    self.MacAddress=self._to_bytes(i_tuple[19])

class ExchangeOrderActionErrorField(Base):
  """交易所报单操作失败"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,ExchangeID= '',OrderSysID='',TraderID='',InstallID=0,OrderLocalID='',ActionLocalID='',ErrorID=0,ErrorMsg=''):

    super(ExchangeOrderActionErrorField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.OrderSysID=self._to_bytes(i_tuple[2])
    self.TraderID=self._to_bytes(i_tuple[3])
    self.InstallID=int(i_tuple[4])
    self.OrderLocalID=self._to_bytes(i_tuple[5])
    self.ActionLocalID=self._to_bytes(i_tuple[6])
    self.ErrorID=int(i_tuple[7])
    self.ErrorMsg=self._to_bytes(i_tuple[8])

class ExchangeTradeField(Base):
  """交易所成交"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('TradeID',ctypes.c_char*21)# 成交编号
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('TradingRole',ctypes.c_char)# 交易角色
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('Price',ctypes.c_double)# 价格
    ,('Volume',ctypes.c_int)# 数量
    ,('TradeDate',ctypes.c_char*9)# 成交时期
    ,('TradeTime',ctypes.c_char*9)# 成交时间
    ,('TradeType',ctypes.c_char)# 成交类型
    ,('PriceSource',ctypes.c_char)# 成交价来源
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('TradeSource',ctypes.c_char)# 成交来源
]

  def __init__(self,ExchangeID= '',TradeID='',Direction='',OrderSysID='',ParticipantID='',ClientID='',TradingRole='',ExchangeInstID='',OffsetFlag='',HedgeFlag='',Price=0.0,Volume=0,TradeDate='',TradeTime='',TradeType='',PriceSource='',TraderID='',OrderLocalID='',ClearingPartID='',BusinessUnit='',SequenceNo=0,TradeSource=''):

    super(ExchangeTradeField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TradeID=self._to_bytes(TradeID)
    self.Direction=self._to_bytes(Direction)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.TradingRole=self._to_bytes(TradingRole)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.Price=float(Price)
    self.Volume=int(Volume)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.TradeType=self._to_bytes(TradeType)
    self.PriceSource=self._to_bytes(PriceSource)
    self.TraderID=self._to_bytes(TraderID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.SequenceNo=int(SequenceNo)
    self.TradeSource=self._to_bytes(TradeSource)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.TradeID=self._to_bytes(i_tuple[2])
    self.Direction=self._to_bytes(i_tuple[3])
    self.OrderSysID=self._to_bytes(i_tuple[4])
    self.ParticipantID=self._to_bytes(i_tuple[5])
    self.ClientID=self._to_bytes(i_tuple[6])
    self.TradingRole=self._to_bytes(i_tuple[7])
    self.ExchangeInstID=self._to_bytes(i_tuple[8])
    self.OffsetFlag=self._to_bytes(i_tuple[9])
    self.HedgeFlag=self._to_bytes(i_tuple[10])
    self.Price=float(i_tuple[11])
    self.Volume=int(i_tuple[12])
    self.TradeDate=self._to_bytes(i_tuple[13])
    self.TradeTime=self._to_bytes(i_tuple[14])
    self.TradeType=self._to_bytes(i_tuple[15])
    self.PriceSource=self._to_bytes(i_tuple[16])
    self.TraderID=self._to_bytes(i_tuple[17])
    self.OrderLocalID=self._to_bytes(i_tuple[18])
    self.ClearingPartID=self._to_bytes(i_tuple[19])
    self.BusinessUnit=self._to_bytes(i_tuple[20])
    self.SequenceNo=int(i_tuple[21])
    self.TradeSource=self._to_bytes(i_tuple[22])

class TradeField(Base):
  """成交"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TradeID',ctypes.c_char*21)# 成交编号
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('TradingRole',ctypes.c_char)# 交易角色
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('Price',ctypes.c_double)# 价格
    ,('Volume',ctypes.c_int)# 数量
    ,('TradeDate',ctypes.c_char*9)# 成交时期
    ,('TradeTime',ctypes.c_char*9)# 成交时间
    ,('TradeType',ctypes.c_char)# 成交类型
    ,('PriceSource',ctypes.c_char)# 成交价来源
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('BrokerOrderSeq',ctypes.c_int)# 经纪公司报单编号
    ,('TradeSource',ctypes.c_char)# 成交来源
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OrderRef='',UserID='',ExchangeID='',TradeID='',Direction='',OrderSysID='',ParticipantID='',ClientID='',TradingRole='',ExchangeInstID='',OffsetFlag='',HedgeFlag='',Price=0.0,Volume=0,TradeDate='',TradeTime='',TradeType='',PriceSource='',TraderID='',OrderLocalID='',ClearingPartID='',BusinessUnit='',SequenceNo=0,TradingDay='',SettlementID=0,BrokerOrderSeq=0,TradeSource='',InvestUnitID=''):

    super(TradeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OrderRef=self._to_bytes(OrderRef)
    self.UserID=self._to_bytes(UserID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TradeID=self._to_bytes(TradeID)
    self.Direction=self._to_bytes(Direction)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.TradingRole=self._to_bytes(TradingRole)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.Price=float(Price)
    self.Volume=int(Volume)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.TradeType=self._to_bytes(TradeType)
    self.PriceSource=self._to_bytes(PriceSource)
    self.TraderID=self._to_bytes(TraderID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.SequenceNo=int(SequenceNo)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.BrokerOrderSeq=int(BrokerOrderSeq)
    self.TradeSource=self._to_bytes(TradeSource)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.ExchangeID=self._to_bytes(i_tuple[6])
    self.TradeID=self._to_bytes(i_tuple[7])
    self.Direction=self._to_bytes(i_tuple[8])
    self.OrderSysID=self._to_bytes(i_tuple[9])
    self.ParticipantID=self._to_bytes(i_tuple[10])
    self.ClientID=self._to_bytes(i_tuple[11])
    self.TradingRole=self._to_bytes(i_tuple[12])
    self.ExchangeInstID=self._to_bytes(i_tuple[13])
    self.OffsetFlag=self._to_bytes(i_tuple[14])
    self.HedgeFlag=self._to_bytes(i_tuple[15])
    self.Price=float(i_tuple[16])
    self.Volume=int(i_tuple[17])
    self.TradeDate=self._to_bytes(i_tuple[18])
    self.TradeTime=self._to_bytes(i_tuple[19])
    self.TradeType=self._to_bytes(i_tuple[20])
    self.PriceSource=self._to_bytes(i_tuple[21])
    self.TraderID=self._to_bytes(i_tuple[22])
    self.OrderLocalID=self._to_bytes(i_tuple[23])
    self.ClearingPartID=self._to_bytes(i_tuple[24])
    self.BusinessUnit=self._to_bytes(i_tuple[25])
    self.SequenceNo=int(i_tuple[26])
    self.TradingDay=self._to_bytes(i_tuple[27])
    self.SettlementID=int(i_tuple[28])
    self.BrokerOrderSeq=int(i_tuple[29])
    self.TradeSource=self._to_bytes(i_tuple[30])
    self.InvestUnitID=self._to_bytes(i_tuple[31])

class UserSessionField(Base):
  """用户会话"""
  _fields_ = [
    ('FrontID',ctypes.c_int)# ///前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('LoginDate',ctypes.c_char*9)# 登录日期
    ,('LoginTime',ctypes.c_char*9)# 登录时间
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('InterfaceProductInfo',ctypes.c_char*11)# 接口端产品信息
    ,('ProtocolInfo',ctypes.c_char*11)# 协议信息
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('LoginRemark',ctypes.c_char*36)# 登录备注
]

  def __init__(self,FrontID= 0,SessionID=0,BrokerID='',UserID='',LoginDate='',LoginTime='',IPAddress='',UserProductInfo='',InterfaceProductInfo='',ProtocolInfo='',MacAddress='',LoginRemark=''):

    super(UserSessionField,self).__init__()

    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.LoginDate=self._to_bytes(LoginDate)
    self.LoginTime=self._to_bytes(LoginTime)
    self.IPAddress=self._to_bytes(IPAddress)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.InterfaceProductInfo=self._to_bytes(InterfaceProductInfo)
    self.ProtocolInfo=self._to_bytes(ProtocolInfo)
    self.MacAddress=self._to_bytes(MacAddress)
    self.LoginRemark=self._to_bytes(LoginRemark)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FrontID=int(i_tuple[1])
    self.SessionID=int(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.UserID=self._to_bytes(i_tuple[4])
    self.LoginDate=self._to_bytes(i_tuple[5])
    self.LoginTime=self._to_bytes(i_tuple[6])
    self.IPAddress=self._to_bytes(i_tuple[7])
    self.UserProductInfo=self._to_bytes(i_tuple[8])
    self.InterfaceProductInfo=self._to_bytes(i_tuple[9])
    self.ProtocolInfo=self._to_bytes(i_tuple[10])
    self.MacAddress=self._to_bytes(i_tuple[11])
    self.LoginRemark=self._to_bytes(i_tuple[12])

class QueryMaxOrderVolumeField(Base):
  """查询最大报单数量"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('MaxVolume',ctypes.c_int)# 最大允许报单数量
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',Direction='',OffsetFlag='',HedgeFlag='',MaxVolume=0,ExchangeID='',InvestUnitID=''):

    super(QueryMaxOrderVolumeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.Direction=self._to_bytes(Direction)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.MaxVolume=int(MaxVolume)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.Direction=self._to_bytes(i_tuple[4])
    self.OffsetFlag=self._to_bytes(i_tuple[5])
    self.HedgeFlag=self._to_bytes(i_tuple[6])
    self.MaxVolume=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.InvestUnitID=self._to_bytes(i_tuple[9])

class SettlementInfoConfirmField(Base):
  """投资者结算结果确认信息"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ConfirmDate',ctypes.c_char*9)# 确认日期
    ,('ConfirmTime',ctypes.c_char*9)# 确认时间
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',InvestorID='',ConfirmDate='',ConfirmTime='',SettlementID=0,AccountID='',CurrencyID=''):

    super(SettlementInfoConfirmField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ConfirmDate=self._to_bytes(ConfirmDate)
    self.ConfirmTime=self._to_bytes(ConfirmTime)
    self.SettlementID=int(SettlementID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ConfirmDate=self._to_bytes(i_tuple[3])
    self.ConfirmTime=self._to_bytes(i_tuple[4])
    self.SettlementID=int(i_tuple[5])
    self.AccountID=self._to_bytes(i_tuple[6])
    self.CurrencyID=self._to_bytes(i_tuple[7])

class SyncDepositField(Base):
  """出入金同步"""
  _fields_ = [
    ('DepositSeqNo',ctypes.c_char*15)# ///出入金流水号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Deposit',ctypes.c_double)# 入金金额
    ,('IsForce',ctypes.c_int)# 是否强制进行
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,DepositSeqNo= '',BrokerID='',InvestorID='',Deposit=0.0,IsForce=0,CurrencyID=''):

    super(SyncDepositField,self).__init__()

    self.DepositSeqNo=self._to_bytes(DepositSeqNo)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Deposit=float(Deposit)
    self.IsForce=int(IsForce)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.DepositSeqNo=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.Deposit=float(i_tuple[4])
    self.IsForce=int(i_tuple[5])
    self.CurrencyID=self._to_bytes(i_tuple[6])

class SyncFundMortgageField(Base):
  """货币质押同步"""
  _fields_ = [
    ('MortgageSeqNo',ctypes.c_char*15)# ///货币质押流水号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('FromCurrencyID',ctypes.c_char*4)# 源币种
    ,('MortgageAmount',ctypes.c_double)# 质押金额
    ,('ToCurrencyID',ctypes.c_char*4)# 目标币种
]

  def __init__(self,MortgageSeqNo= '',BrokerID='',InvestorID='',FromCurrencyID='',MortgageAmount=0.0,ToCurrencyID=''):

    super(SyncFundMortgageField,self).__init__()

    self.MortgageSeqNo=self._to_bytes(MortgageSeqNo)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.FromCurrencyID=self._to_bytes(FromCurrencyID)
    self.MortgageAmount=float(MortgageAmount)
    self.ToCurrencyID=self._to_bytes(ToCurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.MortgageSeqNo=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.FromCurrencyID=self._to_bytes(i_tuple[4])
    self.MortgageAmount=float(i_tuple[5])
    self.ToCurrencyID=self._to_bytes(i_tuple[6])

class BrokerSyncField(Base):
  """经纪公司同步"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
]

  def __init__(self,BrokerID= ''):

    super(BrokerSyncField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])

class SyncingInvestorField(Base):
  """正在同步中的投资者"""
  _fields_ = [
    ('InvestorID',ctypes.c_char*13)# ///投资者代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorGroupID',ctypes.c_char*13)# 投资者分组代码
    ,('InvestorName',ctypes.c_char*81)# 投资者名称
    ,('IdentifiedCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('IsActive',ctypes.c_int)# 是否活跃
    ,('Telephone',ctypes.c_char*41)# 联系电话
    ,('Address',ctypes.c_char*101)# 通讯地址
    ,('OpenDate',ctypes.c_char*9)# 开户日期
    ,('Mobile',ctypes.c_char*41)# 手机
    ,('CommModelID',ctypes.c_char*13)# 手续费率模板代码
    ,('MarginModelID',ctypes.c_char*13)# 保证金率模板代码
]

  def __init__(self,InvestorID= '',BrokerID='',InvestorGroupID='',InvestorName='',IdentifiedCardType='',IdentifiedCardNo='',IsActive=0,Telephone='',Address='',OpenDate='',Mobile='',CommModelID='',MarginModelID=''):

    super(SyncingInvestorField,self).__init__()

    self.InvestorID=self._to_bytes(InvestorID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorGroupID=self._to_bytes(InvestorGroupID)
    self.InvestorName=self._to_bytes(InvestorName)
    self.IdentifiedCardType=self._to_bytes(IdentifiedCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.IsActive=int(IsActive)
    self.Telephone=self._to_bytes(Telephone)
    self.Address=self._to_bytes(Address)
    self.OpenDate=self._to_bytes(OpenDate)
    self.Mobile=self._to_bytes(Mobile)
    self.CommModelID=self._to_bytes(CommModelID)
    self.MarginModelID=self._to_bytes(MarginModelID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InvestorID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorGroupID=self._to_bytes(i_tuple[3])
    self.InvestorName=self._to_bytes(i_tuple[4])
    self.IdentifiedCardType=self._to_bytes(i_tuple[5])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[6])
    self.IsActive=int(i_tuple[7])
    self.Telephone=self._to_bytes(i_tuple[8])
    self.Address=self._to_bytes(i_tuple[9])
    self.OpenDate=self._to_bytes(i_tuple[10])
    self.Mobile=self._to_bytes(i_tuple[11])
    self.CommModelID=self._to_bytes(i_tuple[12])
    self.MarginModelID=self._to_bytes(i_tuple[13])

class SyncingTradingCodeField(Base):
  """正在同步中的交易代码"""
  _fields_ = [
    ('InvestorID',ctypes.c_char*13)# ///投资者代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('IsActive',ctypes.c_int)# 是否活跃
    ,('ClientIDType',ctypes.c_char)# 交易编码类型
]

  def __init__(self,InvestorID= '',BrokerID='',ExchangeID='',ClientID='',IsActive=0,ClientIDType=''):

    super(SyncingTradingCodeField,self).__init__()

    self.InvestorID=self._to_bytes(InvestorID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ClientID=self._to_bytes(ClientID)
    self.IsActive=int(IsActive)
    self.ClientIDType=self._to_bytes(ClientIDType)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InvestorID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.ClientID=self._to_bytes(i_tuple[4])
    self.IsActive=int(i_tuple[5])
    self.ClientIDType=self._to_bytes(i_tuple[6])

class SyncingInvestorGroupField(Base):
  """正在同步中的投资者分组"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorGroupID',ctypes.c_char*13)# 投资者分组代码
    ,('InvestorGroupName',ctypes.c_char*41)# 投资者分组名称
]

  def __init__(self,BrokerID= '',InvestorGroupID='',InvestorGroupName=''):

    super(SyncingInvestorGroupField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorGroupID=self._to_bytes(InvestorGroupID)
    self.InvestorGroupName=self._to_bytes(InvestorGroupName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorGroupID=self._to_bytes(i_tuple[2])
    self.InvestorGroupName=self._to_bytes(i_tuple[3])

class SyncingTradingAccountField(Base):
  """正在同步中的交易账号"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('PreMortgage',ctypes.c_double)# 上次质押金额
    ,('PreCredit',ctypes.c_double)# 上次信用额度
    ,('PreDeposit',ctypes.c_double)# 上次存款额
    ,('PreBalance',ctypes.c_double)# 上次结算准备金
    ,('PreMargin',ctypes.c_double)# 上次占用的保证金
    ,('InterestBase',ctypes.c_double)# 利息基数
    ,('Interest',ctypes.c_double)# 利息收入
    ,('Deposit',ctypes.c_double)# 入金金额
    ,('Withdraw',ctypes.c_double)# 出金金额
    ,('FrozenMargin',ctypes.c_double)# 冻结的保证金
    ,('FrozenCash',ctypes.c_double)# 冻结的资金
    ,('FrozenCommission',ctypes.c_double)# 冻结的手续费
    ,('CurrMargin',ctypes.c_double)# 当前保证金总额
    ,('CashIn',ctypes.c_double)# 资金差额
    ,('Commission',ctypes.c_double)# 手续费
    ,('CloseProfit',ctypes.c_double)# 平仓盈亏
    ,('PositionProfit',ctypes.c_double)# 持仓盈亏
    ,('Balance',ctypes.c_double)# 期货结算准备金
    ,('Available',ctypes.c_double)# 可用资金
    ,('WithdrawQuota',ctypes.c_double)# 可取资金
    ,('Reserve',ctypes.c_double)# 基本准备金
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('Credit',ctypes.c_double)# 信用额度
    ,('Mortgage',ctypes.c_double)# 质押金额
    ,('ExchangeMargin',ctypes.c_double)# 交易所保证金
    ,('DeliveryMargin',ctypes.c_double)# 投资者交割保证金
    ,('ExchangeDeliveryMargin',ctypes.c_double)# 交易所交割保证金
    ,('ReserveBalance',ctypes.c_double)# 保底期货结算准备金
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('PreFundMortgageIn',ctypes.c_double)# 上次货币质入金额
    ,('PreFundMortgageOut',ctypes.c_double)# 上次货币质出金额
    ,('FundMortgageIn',ctypes.c_double)# 货币质入金额
    ,('FundMortgageOut',ctypes.c_double)# 货币质出金额
    ,('FundMortgageAvailable',ctypes.c_double)# 货币质押余额
    ,('MortgageableFund',ctypes.c_double)# 可质押货币金额
    ,('SpecProductMargin',ctypes.c_double)# 特殊产品占用保证金
    ,('SpecProductFrozenMargin',ctypes.c_double)# 特殊产品冻结保证金
    ,('SpecProductCommission',ctypes.c_double)# 特殊产品手续费
    ,('SpecProductFrozenCommission',ctypes.c_double)# 特殊产品冻结手续费
    ,('SpecProductPositionProfit',ctypes.c_double)# 特殊产品持仓盈亏
    ,('SpecProductCloseProfit',ctypes.c_double)# 特殊产品平仓盈亏
    ,('SpecProductPositionProfitByAlg',ctypes.c_double)# 根据持仓盈亏算法计算的特殊产品持仓盈亏
    ,('SpecProductExchangeMargin',ctypes.c_double)# 特殊产品交易所保证金
    ,('FrozenSwap',ctypes.c_double)# 延时换汇冻结金额
    ,('RemainSwap',ctypes.c_double)# 剩余换汇额度
]

  def __init__(self,BrokerID= '',AccountID='',PreMortgage=0.0,PreCredit=0.0,PreDeposit=0.0,PreBalance=0.0,PreMargin=0.0,InterestBase=0.0,Interest=0.0,Deposit=0.0,Withdraw=0.0,FrozenMargin=0.0,FrozenCash=0.0,FrozenCommission=0.0,CurrMargin=0.0,CashIn=0.0,Commission=0.0,CloseProfit=0.0,PositionProfit=0.0,Balance=0.0,Available=0.0,WithdrawQuota=0.0,Reserve=0.0,TradingDay='',SettlementID=0,Credit=0.0,Mortgage=0.0,ExchangeMargin=0.0,DeliveryMargin=0.0,ExchangeDeliveryMargin=0.0,ReserveBalance=0.0,CurrencyID='',PreFundMortgageIn=0.0,PreFundMortgageOut=0.0,FundMortgageIn=0.0,FundMortgageOut=0.0,FundMortgageAvailable=0.0,MortgageableFund=0.0,SpecProductMargin=0.0,SpecProductFrozenMargin=0.0,SpecProductCommission=0.0,SpecProductFrozenCommission=0.0,SpecProductPositionProfit=0.0,SpecProductCloseProfit=0.0,SpecProductPositionProfitByAlg=0.0,SpecProductExchangeMargin=0.0,FrozenSwap=0.0,RemainSwap=0.0):

    super(SyncingTradingAccountField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.PreMortgage=float(PreMortgage)
    self.PreCredit=float(PreCredit)
    self.PreDeposit=float(PreDeposit)
    self.PreBalance=float(PreBalance)
    self.PreMargin=float(PreMargin)
    self.InterestBase=float(InterestBase)
    self.Interest=float(Interest)
    self.Deposit=float(Deposit)
    self.Withdraw=float(Withdraw)
    self.FrozenMargin=float(FrozenMargin)
    self.FrozenCash=float(FrozenCash)
    self.FrozenCommission=float(FrozenCommission)
    self.CurrMargin=float(CurrMargin)
    self.CashIn=float(CashIn)
    self.Commission=float(Commission)
    self.CloseProfit=float(CloseProfit)
    self.PositionProfit=float(PositionProfit)
    self.Balance=float(Balance)
    self.Available=float(Available)
    self.WithdrawQuota=float(WithdrawQuota)
    self.Reserve=float(Reserve)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.Credit=float(Credit)
    self.Mortgage=float(Mortgage)
    self.ExchangeMargin=float(ExchangeMargin)
    self.DeliveryMargin=float(DeliveryMargin)
    self.ExchangeDeliveryMargin=float(ExchangeDeliveryMargin)
    self.ReserveBalance=float(ReserveBalance)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.PreFundMortgageIn=float(PreFundMortgageIn)
    self.PreFundMortgageOut=float(PreFundMortgageOut)
    self.FundMortgageIn=float(FundMortgageIn)
    self.FundMortgageOut=float(FundMortgageOut)
    self.FundMortgageAvailable=float(FundMortgageAvailable)
    self.MortgageableFund=float(MortgageableFund)
    self.SpecProductMargin=float(SpecProductMargin)
    self.SpecProductFrozenMargin=float(SpecProductFrozenMargin)
    self.SpecProductCommission=float(SpecProductCommission)
    self.SpecProductFrozenCommission=float(SpecProductFrozenCommission)
    self.SpecProductPositionProfit=float(SpecProductPositionProfit)
    self.SpecProductCloseProfit=float(SpecProductCloseProfit)
    self.SpecProductPositionProfitByAlg=float(SpecProductPositionProfitByAlg)
    self.SpecProductExchangeMargin=float(SpecProductExchangeMargin)
    self.FrozenSwap=float(FrozenSwap)
    self.RemainSwap=float(RemainSwap)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.PreMortgage=float(i_tuple[3])
    self.PreCredit=float(i_tuple[4])
    self.PreDeposit=float(i_tuple[5])
    self.PreBalance=float(i_tuple[6])
    self.PreMargin=float(i_tuple[7])
    self.InterestBase=float(i_tuple[8])
    self.Interest=float(i_tuple[9])
    self.Deposit=float(i_tuple[10])
    self.Withdraw=float(i_tuple[11])
    self.FrozenMargin=float(i_tuple[12])
    self.FrozenCash=float(i_tuple[13])
    self.FrozenCommission=float(i_tuple[14])
    self.CurrMargin=float(i_tuple[15])
    self.CashIn=float(i_tuple[16])
    self.Commission=float(i_tuple[17])
    self.CloseProfit=float(i_tuple[18])
    self.PositionProfit=float(i_tuple[19])
    self.Balance=float(i_tuple[20])
    self.Available=float(i_tuple[21])
    self.WithdrawQuota=float(i_tuple[22])
    self.Reserve=float(i_tuple[23])
    self.TradingDay=self._to_bytes(i_tuple[24])
    self.SettlementID=int(i_tuple[25])
    self.Credit=float(i_tuple[26])
    self.Mortgage=float(i_tuple[27])
    self.ExchangeMargin=float(i_tuple[28])
    self.DeliveryMargin=float(i_tuple[29])
    self.ExchangeDeliveryMargin=float(i_tuple[30])
    self.ReserveBalance=float(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.PreFundMortgageIn=float(i_tuple[33])
    self.PreFundMortgageOut=float(i_tuple[34])
    self.FundMortgageIn=float(i_tuple[35])
    self.FundMortgageOut=float(i_tuple[36])
    self.FundMortgageAvailable=float(i_tuple[37])
    self.MortgageableFund=float(i_tuple[38])
    self.SpecProductMargin=float(i_tuple[39])
    self.SpecProductFrozenMargin=float(i_tuple[40])
    self.SpecProductCommission=float(i_tuple[41])
    self.SpecProductFrozenCommission=float(i_tuple[42])
    self.SpecProductPositionProfit=float(i_tuple[43])
    self.SpecProductCloseProfit=float(i_tuple[44])
    self.SpecProductPositionProfitByAlg=float(i_tuple[45])
    self.SpecProductExchangeMargin=float(i_tuple[46])
    self.FrozenSwap=float(i_tuple[47])
    self.RemainSwap=float(i_tuple[48])

class SyncingInvestorPositionField(Base):
  """正在同步中的投资者持仓"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('PosiDirection',ctypes.c_char)# 持仓多空方向
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('PositionDate',ctypes.c_char)# 持仓日期
    ,('YdPosition',ctypes.c_int)# 上日持仓
    ,('Position',ctypes.c_int)# 今日持仓
    ,('LongFrozen',ctypes.c_int)# 多头冻结
    ,('ShortFrozen',ctypes.c_int)# 空头冻结
    ,('LongFrozenAmount',ctypes.c_double)# 开仓冻结金额
    ,('ShortFrozenAmount',ctypes.c_double)# 开仓冻结金额
    ,('OpenVolume',ctypes.c_int)# 开仓量
    ,('CloseVolume',ctypes.c_int)# 平仓量
    ,('OpenAmount',ctypes.c_double)# 开仓金额
    ,('CloseAmount',ctypes.c_double)# 平仓金额
    ,('PositionCost',ctypes.c_double)# 持仓成本
    ,('PreMargin',ctypes.c_double)# 上次占用的保证金
    ,('UseMargin',ctypes.c_double)# 占用的保证金
    ,('FrozenMargin',ctypes.c_double)# 冻结的保证金
    ,('FrozenCash',ctypes.c_double)# 冻结的资金
    ,('FrozenCommission',ctypes.c_double)# 冻结的手续费
    ,('CashIn',ctypes.c_double)# 资金差额
    ,('Commission',ctypes.c_double)# 手续费
    ,('CloseProfit',ctypes.c_double)# 平仓盈亏
    ,('PositionProfit',ctypes.c_double)# 持仓盈亏
    ,('PreSettlementPrice',ctypes.c_double)# 上次结算价
    ,('SettlementPrice',ctypes.c_double)# 本次结算价
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OpenCost',ctypes.c_double)# 开仓成本
    ,('ExchangeMargin',ctypes.c_double)# 交易所保证金
    ,('CombPosition',ctypes.c_int)# 组合成交形成的持仓
    ,('CombLongFrozen',ctypes.c_int)# 组合多头冻结
    ,('CombShortFrozen',ctypes.c_int)# 组合空头冻结
    ,('CloseProfitByDate',ctypes.c_double)# 逐日盯市平仓盈亏
    ,('CloseProfitByTrade',ctypes.c_double)# 逐笔对冲平仓盈亏
    ,('TodayPosition',ctypes.c_int)# 今日持仓
    ,('MarginRateByMoney',ctypes.c_double)# 保证金率
    ,('MarginRateByVolume',ctypes.c_double)# 保证金率(按手数)
    ,('StrikeFrozen',ctypes.c_int)# 执行冻结
    ,('StrikeFrozenAmount',ctypes.c_double)# 执行冻结金额
    ,('AbandonFrozen',ctypes.c_int)# 放弃执行冻结
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('YdStrikeFrozen',ctypes.c_int)# 执行冻结的昨仓
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',BrokerID='',InvestorID='',PosiDirection='',HedgeFlag='',PositionDate='',YdPosition=0,Position=0,LongFrozen=0,ShortFrozen=0,LongFrozenAmount=0.0,ShortFrozenAmount=0.0,OpenVolume=0,CloseVolume=0,OpenAmount=0.0,CloseAmount=0.0,PositionCost=0.0,PreMargin=0.0,UseMargin=0.0,FrozenMargin=0.0,FrozenCash=0.0,FrozenCommission=0.0,CashIn=0.0,Commission=0.0,CloseProfit=0.0,PositionProfit=0.0,PreSettlementPrice=0.0,SettlementPrice=0.0,TradingDay='',SettlementID=0,OpenCost=0.0,ExchangeMargin=0.0,CombPosition=0,CombLongFrozen=0,CombShortFrozen=0,CloseProfitByDate=0.0,CloseProfitByTrade=0.0,TodayPosition=0,MarginRateByMoney=0.0,MarginRateByVolume=0.0,StrikeFrozen=0,StrikeFrozenAmount=0.0,AbandonFrozen=0,ExchangeID='',YdStrikeFrozen=0,InvestUnitID=''):

    super(SyncingInvestorPositionField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.PosiDirection=self._to_bytes(PosiDirection)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.PositionDate=self._to_bytes(PositionDate)
    self.YdPosition=int(YdPosition)
    self.Position=int(Position)
    self.LongFrozen=int(LongFrozen)
    self.ShortFrozen=int(ShortFrozen)
    self.LongFrozenAmount=float(LongFrozenAmount)
    self.ShortFrozenAmount=float(ShortFrozenAmount)
    self.OpenVolume=int(OpenVolume)
    self.CloseVolume=int(CloseVolume)
    self.OpenAmount=float(OpenAmount)
    self.CloseAmount=float(CloseAmount)
    self.PositionCost=float(PositionCost)
    self.PreMargin=float(PreMargin)
    self.UseMargin=float(UseMargin)
    self.FrozenMargin=float(FrozenMargin)
    self.FrozenCash=float(FrozenCash)
    self.FrozenCommission=float(FrozenCommission)
    self.CashIn=float(CashIn)
    self.Commission=float(Commission)
    self.CloseProfit=float(CloseProfit)
    self.PositionProfit=float(PositionProfit)
    self.PreSettlementPrice=float(PreSettlementPrice)
    self.SettlementPrice=float(SettlementPrice)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OpenCost=float(OpenCost)
    self.ExchangeMargin=float(ExchangeMargin)
    self.CombPosition=int(CombPosition)
    self.CombLongFrozen=int(CombLongFrozen)
    self.CombShortFrozen=int(CombShortFrozen)
    self.CloseProfitByDate=float(CloseProfitByDate)
    self.CloseProfitByTrade=float(CloseProfitByTrade)
    self.TodayPosition=int(TodayPosition)
    self.MarginRateByMoney=float(MarginRateByMoney)
    self.MarginRateByVolume=float(MarginRateByVolume)
    self.StrikeFrozen=int(StrikeFrozen)
    self.StrikeFrozenAmount=float(StrikeFrozenAmount)
    self.AbandonFrozen=int(AbandonFrozen)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.YdStrikeFrozen=int(YdStrikeFrozen)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.PosiDirection=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.PositionDate=self._to_bytes(i_tuple[6])
    self.YdPosition=int(i_tuple[7])
    self.Position=int(i_tuple[8])
    self.LongFrozen=int(i_tuple[9])
    self.ShortFrozen=int(i_tuple[10])
    self.LongFrozenAmount=float(i_tuple[11])
    self.ShortFrozenAmount=float(i_tuple[12])
    self.OpenVolume=int(i_tuple[13])
    self.CloseVolume=int(i_tuple[14])
    self.OpenAmount=float(i_tuple[15])
    self.CloseAmount=float(i_tuple[16])
    self.PositionCost=float(i_tuple[17])
    self.PreMargin=float(i_tuple[18])
    self.UseMargin=float(i_tuple[19])
    self.FrozenMargin=float(i_tuple[20])
    self.FrozenCash=float(i_tuple[21])
    self.FrozenCommission=float(i_tuple[22])
    self.CashIn=float(i_tuple[23])
    self.Commission=float(i_tuple[24])
    self.CloseProfit=float(i_tuple[25])
    self.PositionProfit=float(i_tuple[26])
    self.PreSettlementPrice=float(i_tuple[27])
    self.SettlementPrice=float(i_tuple[28])
    self.TradingDay=self._to_bytes(i_tuple[29])
    self.SettlementID=int(i_tuple[30])
    self.OpenCost=float(i_tuple[31])
    self.ExchangeMargin=float(i_tuple[32])
    self.CombPosition=int(i_tuple[33])
    self.CombLongFrozen=int(i_tuple[34])
    self.CombShortFrozen=int(i_tuple[35])
    self.CloseProfitByDate=float(i_tuple[36])
    self.CloseProfitByTrade=float(i_tuple[37])
    self.TodayPosition=int(i_tuple[38])
    self.MarginRateByMoney=float(i_tuple[39])
    self.MarginRateByVolume=float(i_tuple[40])
    self.StrikeFrozen=int(i_tuple[41])
    self.StrikeFrozenAmount=float(i_tuple[42])
    self.AbandonFrozen=int(i_tuple[43])
    self.ExchangeID=self._to_bytes(i_tuple[44])
    self.YdStrikeFrozen=int(i_tuple[45])
    self.InvestUnitID=self._to_bytes(i_tuple[46])

class SyncingInstrumentMarginRateField(Base):
  """正在同步中的合约保证金率"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('LongMarginRatioByMoney',ctypes.c_double)# 多头保证金率
    ,('LongMarginRatioByVolume',ctypes.c_double)# 多头保证金费
    ,('ShortMarginRatioByMoney',ctypes.c_double)# 空头保证金率
    ,('ShortMarginRatioByVolume',ctypes.c_double)# 空头保证金费
    ,('IsRelative',ctypes.c_int)# 是否相对交易所收取
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',HedgeFlag='',LongMarginRatioByMoney=0.0,LongMarginRatioByVolume=0.0,ShortMarginRatioByMoney=0.0,ShortMarginRatioByVolume=0.0,IsRelative=0):

    super(SyncingInstrumentMarginRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.LongMarginRatioByMoney=float(LongMarginRatioByMoney)
    self.LongMarginRatioByVolume=float(LongMarginRatioByVolume)
    self.ShortMarginRatioByMoney=float(ShortMarginRatioByMoney)
    self.ShortMarginRatioByVolume=float(ShortMarginRatioByVolume)
    self.IsRelative=int(IsRelative)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.LongMarginRatioByMoney=float(i_tuple[6])
    self.LongMarginRatioByVolume=float(i_tuple[7])
    self.ShortMarginRatioByMoney=float(i_tuple[8])
    self.ShortMarginRatioByVolume=float(i_tuple[9])
    self.IsRelative=int(i_tuple[10])

class SyncingInstrumentCommissionRateField(Base):
  """正在同步中的合约手续费率"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OpenRatioByMoney',ctypes.c_double)# 开仓手续费率
    ,('OpenRatioByVolume',ctypes.c_double)# 开仓手续费
    ,('CloseRatioByMoney',ctypes.c_double)# 平仓手续费率
    ,('CloseRatioByVolume',ctypes.c_double)# 平仓手续费
    ,('CloseTodayRatioByMoney',ctypes.c_double)# 平今手续费率
    ,('CloseTodayRatioByVolume',ctypes.c_double)# 平今手续费
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',OpenRatioByMoney=0.0,OpenRatioByVolume=0.0,CloseRatioByMoney=0.0,CloseRatioByVolume=0.0,CloseTodayRatioByMoney=0.0,CloseTodayRatioByVolume=0.0):

    super(SyncingInstrumentCommissionRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OpenRatioByMoney=float(OpenRatioByMoney)
    self.OpenRatioByVolume=float(OpenRatioByVolume)
    self.CloseRatioByMoney=float(CloseRatioByMoney)
    self.CloseRatioByVolume=float(CloseRatioByVolume)
    self.CloseTodayRatioByMoney=float(CloseTodayRatioByMoney)
    self.CloseTodayRatioByVolume=float(CloseTodayRatioByVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.OpenRatioByMoney=float(i_tuple[5])
    self.OpenRatioByVolume=float(i_tuple[6])
    self.CloseRatioByMoney=float(i_tuple[7])
    self.CloseRatioByVolume=float(i_tuple[8])
    self.CloseTodayRatioByMoney=float(i_tuple[9])
    self.CloseTodayRatioByVolume=float(i_tuple[10])

class SyncingInstrumentTradingRightField(Base):
  """正在同步中的合约交易权限"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('TradingRight',ctypes.c_char)# 交易权限
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',TradingRight=''):

    super(SyncingInstrumentTradingRightField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.TradingRight=self._to_bytes(TradingRight)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.TradingRight=self._to_bytes(i_tuple[5])

class QryOrderField(Base):
  """查询报单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('InsertTimeStart',ctypes.c_char*9)# 开始时间
    ,('InsertTimeEnd',ctypes.c_char*9)# 结束时间
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',OrderSysID='',InsertTimeStart='',InsertTimeEnd='',InvestUnitID=''):

    super(QryOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.InsertTimeStart=self._to_bytes(InsertTimeStart)
    self.InsertTimeEnd=self._to_bytes(InsertTimeEnd)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.OrderSysID=self._to_bytes(i_tuple[5])
    self.InsertTimeStart=self._to_bytes(i_tuple[6])
    self.InsertTimeEnd=self._to_bytes(i_tuple[7])
    self.InvestUnitID=self._to_bytes(i_tuple[8])

class QryTradeField(Base):
  """查询成交"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TradeID',ctypes.c_char*21)# 成交编号
    ,('TradeTimeStart',ctypes.c_char*9)# 开始时间
    ,('TradeTimeEnd',ctypes.c_char*9)# 结束时间
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',TradeID='',TradeTimeStart='',TradeTimeEnd='',InvestUnitID=''):

    super(QryTradeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TradeID=self._to_bytes(TradeID)
    self.TradeTimeStart=self._to_bytes(TradeTimeStart)
    self.TradeTimeEnd=self._to_bytes(TradeTimeEnd)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.TradeID=self._to_bytes(i_tuple[5])
    self.TradeTimeStart=self._to_bytes(i_tuple[6])
    self.TradeTimeEnd=self._to_bytes(i_tuple[7])
    self.InvestUnitID=self._to_bytes(i_tuple[8])

class QryInvestorPositionField(Base):
  """查询投资者持仓"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryInvestorPositionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class QryTradingAccountField(Base):
  """查询资金账户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('BizType',ctypes.c_char)# 业务类型
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
]

  def __init__(self,BrokerID= '',InvestorID='',CurrencyID='',BizType='',AccountID=''):

    super(QryTradingAccountField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.BizType=self._to_bytes(BizType)
    self.AccountID=self._to_bytes(AccountID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.CurrencyID=self._to_bytes(i_tuple[3])
    self.BizType=self._to_bytes(i_tuple[4])
    self.AccountID=self._to_bytes(i_tuple[5])

class QryInvestorField(Base):
  """查询投资者"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryInvestorField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class QryTradingCodeField(Base):
  """查询交易编码"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ClientIDType',ctypes.c_char)# 交易编码类型
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID='',ClientID='',ClientIDType='',InvestUnitID=''):

    super(QryTradingCodeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ClientID=self._to_bytes(ClientID)
    self.ClientIDType=self._to_bytes(ClientIDType)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.ClientID=self._to_bytes(i_tuple[4])
    self.ClientIDType=self._to_bytes(i_tuple[5])
    self.InvestUnitID=self._to_bytes(i_tuple[6])

class QryInvestorGroupField(Base):
  """查询投资者组"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
]

  def __init__(self,BrokerID= ''):

    super(QryInvestorGroupField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])

class QryInstrumentMarginRateField(Base):
  """查询合约保证金率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',HedgeFlag='',ExchangeID='',InvestUnitID=''):

    super(QryInstrumentMarginRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.ExchangeID=self._to_bytes(i_tuple[5])
    self.InvestUnitID=self._to_bytes(i_tuple[6])

class QryInstrumentCommissionRateField(Base):
  """查询手续费率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryInstrumentCommissionRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class QryInstrumentTradingRightField(Base):
  """查询合约交易权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID=''):

    super(QryInstrumentTradingRightField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])

class QryBrokerField(Base):
  """查询经纪公司"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
]

  def __init__(self,BrokerID= ''):

    super(QryBrokerField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])

class QryTraderField(Base):
  """查询交易员"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ExchangeID= '',ParticipantID='',TraderID=''):

    super(QryTraderField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.TraderID=self._to_bytes(i_tuple[3])

class QrySuperUserFunctionField(Base):
  """查询管理用户功能权限"""
  _fields_ = [
    ('UserID',ctypes.c_char*16)# ///用户代码
]

  def __init__(self,UserID= ''):

    super(QrySuperUserFunctionField,self).__init__()

    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.UserID=self._to_bytes(i_tuple[1])

class QryUserSessionField(Base):
  """查询用户会话"""
  _fields_ = [
    ('FrontID',ctypes.c_int)# ///前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,FrontID= 0,SessionID=0,BrokerID='',UserID=''):

    super(QryUserSessionField,self).__init__()

    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FrontID=int(i_tuple[1])
    self.SessionID=int(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.UserID=self._to_bytes(i_tuple[4])

class QryPartBrokerField(Base):
  """查询经纪公司会员代码"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
]

  def __init__(self,ExchangeID= '',BrokerID='',ParticipantID=''):

    super(QryPartBrokerField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.ParticipantID=self._to_bytes(ParticipantID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])

class QryFrontStatusField(Base):
  """查询前置状态"""
  _fields_ = [
    ('FrontID',ctypes.c_int)# ///前置编号
]

  def __init__(self,FrontID= 0):

    super(QryFrontStatusField,self).__init__()

    self.FrontID=int(FrontID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.FrontID=int(i_tuple[1])

class QryExchangeOrderField(Base):
  """查询交易所报单"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeInstID='',ExchangeID='',TraderID=''):

    super(QryExchangeOrderField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeInstID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.TraderID=self._to_bytes(i_tuple[5])

class QryOrderActionField(Base):
  """查询报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID=''):

    super(QryOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class QryExchangeOrderActionField(Base):
  """查询交易所报单操作"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeID='',TraderID=''):

    super(QryExchangeOrderActionField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.TraderID=self._to_bytes(i_tuple[4])

class QrySuperUserField(Base):
  """查询管理用户"""
  _fields_ = [
    ('UserID',ctypes.c_char*16)# ///用户代码
]

  def __init__(self,UserID= ''):

    super(QrySuperUserField,self).__init__()

    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.UserID=self._to_bytes(i_tuple[1])

class QryExchangeField(Base):
  """查询交易所"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
]

  def __init__(self,ExchangeID= ''):

    super(QryExchangeField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])

class QryProductField(Base):
  """查询产品"""
  _fields_ = [
    ('ProductID',ctypes.c_char*31)# ///产品代码
    ,('ProductClass',ctypes.c_char)# 产品类型
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,ProductID= '',ProductClass='',ExchangeID=''):

    super(QryProductField,self).__init__()

    self.ProductID=self._to_bytes(ProductID)
    self.ProductClass=self._to_bytes(ProductClass)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductID=self._to_bytes(i_tuple[1])
    self.ProductClass=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class QryInstrumentField(Base):
  """查询合约"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ProductID',ctypes.c_char*31)# 产品代码
]

  def __init__(self,InstrumentID= '',ExchangeID='',ExchangeInstID='',ProductID=''):

    super(QryInstrumentField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ProductID=self._to_bytes(ProductID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.ExchangeInstID=self._to_bytes(i_tuple[3])
    self.ProductID=self._to_bytes(i_tuple[4])

class QryDepthMarketDataField(Base):
  """查询行情"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,InstrumentID= '',ExchangeID=''):

    super(QryDepthMarketDataField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])

class QryBrokerUserField(Base):
  """查询经纪公司用户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,BrokerID= '',UserID=''):

    super(QryBrokerUserField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])

class QryBrokerUserFunctionField(Base):
  """查询经纪公司用户权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,BrokerID= '',UserID=''):

    super(QryBrokerUserFunctionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])

class QryTraderOfferField(Base):
  """查询交易员报盘机"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ExchangeID= '',ParticipantID='',TraderID=''):

    super(QryTraderOfferField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.TraderID=self._to_bytes(i_tuple[3])

class QrySyncDepositField(Base):
  """查询出入金流水"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('DepositSeqNo',ctypes.c_char*15)# 出入金流水号
]

  def __init__(self,BrokerID= '',DepositSeqNo=''):

    super(QrySyncDepositField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.DepositSeqNo=self._to_bytes(DepositSeqNo)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.DepositSeqNo=self._to_bytes(i_tuple[2])

class QrySettlementInfoField(Base):
  """查询投资者结算结果"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',InvestorID='',TradingDay='',AccountID='',CurrencyID=''):

    super(QrySettlementInfoField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.TradingDay=self._to_bytes(TradingDay)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.TradingDay=self._to_bytes(i_tuple[3])
    self.AccountID=self._to_bytes(i_tuple[4])
    self.CurrencyID=self._to_bytes(i_tuple[5])

class QryExchangeMarginRateField(Base):
  """查询交易所保证金率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InstrumentID='',HedgeFlag='',ExchangeID=''):

    super(QryExchangeMarginRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.HedgeFlag=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])

class QryExchangeMarginRateAdjustField(Base):
  """查询交易所调整保证金率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
]

  def __init__(self,BrokerID= '',InstrumentID='',HedgeFlag=''):

    super(QryExchangeMarginRateAdjustField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.HedgeFlag=self._to_bytes(i_tuple[3])

class QryExchangeRateField(Base):
  """查询汇率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('FromCurrencyID',ctypes.c_char*4)# 源币种
    ,('ToCurrencyID',ctypes.c_char*4)# 目标币种
]

  def __init__(self,BrokerID= '',FromCurrencyID='',ToCurrencyID=''):

    super(QryExchangeRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.FromCurrencyID=self._to_bytes(FromCurrencyID)
    self.ToCurrencyID=self._to_bytes(ToCurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.FromCurrencyID=self._to_bytes(i_tuple[2])
    self.ToCurrencyID=self._to_bytes(i_tuple[3])

class QrySyncFundMortgageField(Base):
  """查询货币质押流水"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('MortgageSeqNo',ctypes.c_char*15)# 货币质押流水号
]

  def __init__(self,BrokerID= '',MortgageSeqNo=''):

    super(QrySyncFundMortgageField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.MortgageSeqNo=self._to_bytes(MortgageSeqNo)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.MortgageSeqNo=self._to_bytes(i_tuple[2])

class QryHisOrderField(Base):
  """查询报单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('InsertTimeStart',ctypes.c_char*9)# 开始时间
    ,('InsertTimeEnd',ctypes.c_char*9)# 结束时间
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',OrderSysID='',InsertTimeStart='',InsertTimeEnd='',TradingDay='',SettlementID=0):

    super(QryHisOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.InsertTimeStart=self._to_bytes(InsertTimeStart)
    self.InsertTimeEnd=self._to_bytes(InsertTimeEnd)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.OrderSysID=self._to_bytes(i_tuple[5])
    self.InsertTimeStart=self._to_bytes(i_tuple[6])
    self.InsertTimeEnd=self._to_bytes(i_tuple[7])
    self.TradingDay=self._to_bytes(i_tuple[8])
    self.SettlementID=int(i_tuple[9])

class OptionInstrMiniMarginField(Base):
  """当前期权合约最小保证金"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('MinMargin',ctypes.c_double)# 单位（手）期权合约最小保证金
    ,('ValueMethod',ctypes.c_char)# 取值方式
    ,('IsRelative',ctypes.c_int)# 是否跟随交易所收取
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',MinMargin=0.0,ValueMethod='',IsRelative=0):

    super(OptionInstrMiniMarginField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.MinMargin=float(MinMargin)
    self.ValueMethod=self._to_bytes(ValueMethod)
    self.IsRelative=int(IsRelative)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.MinMargin=float(i_tuple[5])
    self.ValueMethod=self._to_bytes(i_tuple[6])
    self.IsRelative=int(i_tuple[7])

class OptionInstrMarginAdjustField(Base):
  """当前期权合约保证金调整系数"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('SShortMarginRatioByMoney',ctypes.c_double)# 投机空头保证金调整系数
    ,('SShortMarginRatioByVolume',ctypes.c_double)# 投机空头保证金调整系数
    ,('HShortMarginRatioByMoney',ctypes.c_double)# 保值空头保证金调整系数
    ,('HShortMarginRatioByVolume',ctypes.c_double)# 保值空头保证金调整系数
    ,('AShortMarginRatioByMoney',ctypes.c_double)# 套利空头保证金调整系数
    ,('AShortMarginRatioByVolume',ctypes.c_double)# 套利空头保证金调整系数
    ,('IsRelative',ctypes.c_int)# 是否跟随交易所收取
    ,('MShortMarginRatioByMoney',ctypes.c_double)# 做市商空头保证金调整系数
    ,('MShortMarginRatioByVolume',ctypes.c_double)# 做市商空头保证金调整系数
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',SShortMarginRatioByMoney=0.0,SShortMarginRatioByVolume=0.0,HShortMarginRatioByMoney=0.0,HShortMarginRatioByVolume=0.0,AShortMarginRatioByMoney=0.0,AShortMarginRatioByVolume=0.0,IsRelative=0,MShortMarginRatioByMoney=0.0,MShortMarginRatioByVolume=0.0):

    super(OptionInstrMarginAdjustField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.SShortMarginRatioByMoney=float(SShortMarginRatioByMoney)
    self.SShortMarginRatioByVolume=float(SShortMarginRatioByVolume)
    self.HShortMarginRatioByMoney=float(HShortMarginRatioByMoney)
    self.HShortMarginRatioByVolume=float(HShortMarginRatioByVolume)
    self.AShortMarginRatioByMoney=float(AShortMarginRatioByMoney)
    self.AShortMarginRatioByVolume=float(AShortMarginRatioByVolume)
    self.IsRelative=int(IsRelative)
    self.MShortMarginRatioByMoney=float(MShortMarginRatioByMoney)
    self.MShortMarginRatioByVolume=float(MShortMarginRatioByVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.SShortMarginRatioByMoney=float(i_tuple[5])
    self.SShortMarginRatioByVolume=float(i_tuple[6])
    self.HShortMarginRatioByMoney=float(i_tuple[7])
    self.HShortMarginRatioByVolume=float(i_tuple[8])
    self.AShortMarginRatioByMoney=float(i_tuple[9])
    self.AShortMarginRatioByVolume=float(i_tuple[10])
    self.IsRelative=int(i_tuple[11])
    self.MShortMarginRatioByMoney=float(i_tuple[12])
    self.MShortMarginRatioByVolume=float(i_tuple[13])

class OptionInstrCommRateField(Base):
  """当前期权合约手续费的详细内容"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OpenRatioByMoney',ctypes.c_double)# 开仓手续费率
    ,('OpenRatioByVolume',ctypes.c_double)# 开仓手续费
    ,('CloseRatioByMoney',ctypes.c_double)# 平仓手续费率
    ,('CloseRatioByVolume',ctypes.c_double)# 平仓手续费
    ,('CloseTodayRatioByMoney',ctypes.c_double)# 平今手续费率
    ,('CloseTodayRatioByVolume',ctypes.c_double)# 平今手续费
    ,('StrikeRatioByMoney',ctypes.c_double)# 执行手续费率
    ,('StrikeRatioByVolume',ctypes.c_double)# 执行手续费
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',OpenRatioByMoney=0.0,OpenRatioByVolume=0.0,CloseRatioByMoney=0.0,CloseRatioByVolume=0.0,CloseTodayRatioByMoney=0.0,CloseTodayRatioByVolume=0.0,StrikeRatioByMoney=0.0,StrikeRatioByVolume=0.0,ExchangeID='',InvestUnitID=''):

    super(OptionInstrCommRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OpenRatioByMoney=float(OpenRatioByMoney)
    self.OpenRatioByVolume=float(OpenRatioByVolume)
    self.CloseRatioByMoney=float(CloseRatioByMoney)
    self.CloseRatioByVolume=float(CloseRatioByVolume)
    self.CloseTodayRatioByMoney=float(CloseTodayRatioByMoney)
    self.CloseTodayRatioByVolume=float(CloseTodayRatioByVolume)
    self.StrikeRatioByMoney=float(StrikeRatioByMoney)
    self.StrikeRatioByVolume=float(StrikeRatioByVolume)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.OpenRatioByMoney=float(i_tuple[5])
    self.OpenRatioByVolume=float(i_tuple[6])
    self.CloseRatioByMoney=float(i_tuple[7])
    self.CloseRatioByVolume=float(i_tuple[8])
    self.CloseTodayRatioByMoney=float(i_tuple[9])
    self.CloseTodayRatioByVolume=float(i_tuple[10])
    self.StrikeRatioByMoney=float(i_tuple[11])
    self.StrikeRatioByVolume=float(i_tuple[12])
    self.ExchangeID=self._to_bytes(i_tuple[13])
    self.InvestUnitID=self._to_bytes(i_tuple[14])

class OptionInstrTradeCostField(Base):
  """期权交易成本"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('FixedMargin',ctypes.c_double)# 期权合约保证金不变部分
    ,('MiniMargin',ctypes.c_double)# 期权合约最小保证金
    ,('Royalty',ctypes.c_double)# 期权合约权利金
    ,('ExchFixedMargin',ctypes.c_double)# 交易所期权合约保证金不变部分
    ,('ExchMiniMargin',ctypes.c_double)# 交易所期权合约最小保证金
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',HedgeFlag='',FixedMargin=0.0,MiniMargin=0.0,Royalty=0.0,ExchFixedMargin=0.0,ExchMiniMargin=0.0,ExchangeID='',InvestUnitID=''):

    super(OptionInstrTradeCostField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.FixedMargin=float(FixedMargin)
    self.MiniMargin=float(MiniMargin)
    self.Royalty=float(Royalty)
    self.ExchFixedMargin=float(ExchFixedMargin)
    self.ExchMiniMargin=float(ExchMiniMargin)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.FixedMargin=float(i_tuple[5])
    self.MiniMargin=float(i_tuple[6])
    self.Royalty=float(i_tuple[7])
    self.ExchFixedMargin=float(i_tuple[8])
    self.ExchMiniMargin=float(i_tuple[9])
    self.ExchangeID=self._to_bytes(i_tuple[10])
    self.InvestUnitID=self._to_bytes(i_tuple[11])

class QryOptionInstrTradeCostField(Base):
  """期权交易成本查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('InputPrice',ctypes.c_double)# 期权合约报价
    ,('UnderlyingPrice',ctypes.c_double)# 标的价格,填0则用昨结算价
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',HedgeFlag='',InputPrice=0.0,UnderlyingPrice=0.0,ExchangeID='',InvestUnitID=''):

    super(QryOptionInstrTradeCostField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.InputPrice=float(InputPrice)
    self.UnderlyingPrice=float(UnderlyingPrice)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.InputPrice=float(i_tuple[5])
    self.UnderlyingPrice=float(i_tuple[6])
    self.ExchangeID=self._to_bytes(i_tuple[7])
    self.InvestUnitID=self._to_bytes(i_tuple[8])

class QryOptionInstrCommRateField(Base):
  """期权手续费率查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryOptionInstrCommRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class IndexPriceField(Base):
  """股指现货指数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ClosePrice',ctypes.c_double)# 指数现货收盘价
]

  def __init__(self,BrokerID= '',InstrumentID='',ClosePrice=0.0):

    super(IndexPriceField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ClosePrice=float(ClosePrice)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ClosePrice=float(i_tuple[3])

class InputExecOrderField(Base):
  """输入的执行宣告"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExecOrderRef',ctypes.c_char*13)# 执行宣告引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Volume',ctypes.c_int)# 数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ActionType',ctypes.c_char)# 执行类型
    ,('PosiDirection',ctypes.c_char)# 保留头寸申请的持仓方向
    ,('ReservePositionFlag',ctypes.c_char)# 期权行权后是否保留期货头寸的标记,该字段已废弃
    ,('CloseFlag',ctypes.c_char)# 期权行权后生成的头寸是否自动平仓
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExecOrderRef='',UserID='',Volume=0,RequestID=0,BusinessUnit='',OffsetFlag='',HedgeFlag='',ActionType='',PosiDirection='',ReservePositionFlag='',CloseFlag='',ExchangeID='',InvestUnitID='',AccountID='',CurrencyID='',ClientID='',IPAddress='',MacAddress=''):

    super(InputExecOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExecOrderRef=self._to_bytes(ExecOrderRef)
    self.UserID=self._to_bytes(UserID)
    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ActionType=self._to_bytes(ActionType)
    self.PosiDirection=self._to_bytes(PosiDirection)
    self.ReservePositionFlag=self._to_bytes(ReservePositionFlag)
    self.CloseFlag=self._to_bytes(CloseFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExecOrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Volume=int(i_tuple[6])
    self.RequestID=int(i_tuple[7])
    self.BusinessUnit=self._to_bytes(i_tuple[8])
    self.OffsetFlag=self._to_bytes(i_tuple[9])
    self.HedgeFlag=self._to_bytes(i_tuple[10])
    self.ActionType=self._to_bytes(i_tuple[11])
    self.PosiDirection=self._to_bytes(i_tuple[12])
    self.ReservePositionFlag=self._to_bytes(i_tuple[13])
    self.CloseFlag=self._to_bytes(i_tuple[14])
    self.ExchangeID=self._to_bytes(i_tuple[15])
    self.InvestUnitID=self._to_bytes(i_tuple[16])
    self.AccountID=self._to_bytes(i_tuple[17])
    self.CurrencyID=self._to_bytes(i_tuple[18])
    self.ClientID=self._to_bytes(i_tuple[19])
    self.IPAddress=self._to_bytes(i_tuple[20])
    self.MacAddress=self._to_bytes(i_tuple[21])

class InputExecOrderActionField(Base):
  """输入执行宣告操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExecOrderActionRef',ctypes.c_int)# 执行宣告操作引用
    ,('ExecOrderRef',ctypes.c_char*13)# 执行宣告引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',ExecOrderActionRef=0,ExecOrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',ExecOrderSysID='',ActionFlag='',UserID='',InstrumentID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(InputExecOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExecOrderActionRef=int(ExecOrderActionRef)
    self.ExecOrderRef=self._to_bytes(ExecOrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.UserID=self._to_bytes(UserID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExecOrderActionRef=int(i_tuple[3])
    self.ExecOrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.ExecOrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.UserID=self._to_bytes(i_tuple[11])
    self.InstrumentID=self._to_bytes(i_tuple[12])
    self.InvestUnitID=self._to_bytes(i_tuple[13])
    self.IPAddress=self._to_bytes(i_tuple[14])
    self.MacAddress=self._to_bytes(i_tuple[15])

class ExecOrderField(Base):
  """执行宣告"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExecOrderRef',ctypes.c_char*13)# 执行宣告引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Volume',ctypes.c_int)# 数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ActionType',ctypes.c_char)# 执行类型
    ,('PosiDirection',ctypes.c_char)# 保留头寸申请的持仓方向
    ,('ReservePositionFlag',ctypes.c_char)# 期权行权后是否保留期货头寸的标记,该字段已废弃
    ,('CloseFlag',ctypes.c_char)# 期权行权后生成的头寸是否自动平仓
    ,('ExecOrderLocalID',ctypes.c_char*13)# 本地执行宣告编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 执行宣告提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ExecResult',ctypes.c_char)# 执行结果
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('ActiveUserID',ctypes.c_char*16)# 操作用户代码
    ,('BrokerExecOrderSeq',ctypes.c_int)# 经纪公司报单编号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExecOrderRef='',UserID='',Volume=0,RequestID=0,BusinessUnit='',OffsetFlag='',HedgeFlag='',ActionType='',PosiDirection='',ReservePositionFlag='',CloseFlag='',ExecOrderLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,ExecOrderSysID='',InsertDate='',InsertTime='',CancelTime='',ExecResult='',ClearingPartID='',SequenceNo=0,FrontID=0,SessionID=0,UserProductInfo='',StatusMsg='',ActiveUserID='',BrokerExecOrderSeq=0,BranchID='',InvestUnitID='',AccountID='',CurrencyID='',IPAddress='',MacAddress=''):

    super(ExecOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExecOrderRef=self._to_bytes(ExecOrderRef)
    self.UserID=self._to_bytes(UserID)
    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ActionType=self._to_bytes(ActionType)
    self.PosiDirection=self._to_bytes(PosiDirection)
    self.ReservePositionFlag=self._to_bytes(ReservePositionFlag)
    self.CloseFlag=self._to_bytes(CloseFlag)
    self.ExecOrderLocalID=self._to_bytes(ExecOrderLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ExecResult=self._to_bytes(ExecResult)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.ActiveUserID=self._to_bytes(ActiveUserID)
    self.BrokerExecOrderSeq=int(BrokerExecOrderSeq)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExecOrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Volume=int(i_tuple[6])
    self.RequestID=int(i_tuple[7])
    self.BusinessUnit=self._to_bytes(i_tuple[8])
    self.OffsetFlag=self._to_bytes(i_tuple[9])
    self.HedgeFlag=self._to_bytes(i_tuple[10])
    self.ActionType=self._to_bytes(i_tuple[11])
    self.PosiDirection=self._to_bytes(i_tuple[12])
    self.ReservePositionFlag=self._to_bytes(i_tuple[13])
    self.CloseFlag=self._to_bytes(i_tuple[14])
    self.ExecOrderLocalID=self._to_bytes(i_tuple[15])
    self.ExchangeID=self._to_bytes(i_tuple[16])
    self.ParticipantID=self._to_bytes(i_tuple[17])
    self.ClientID=self._to_bytes(i_tuple[18])
    self.ExchangeInstID=self._to_bytes(i_tuple[19])
    self.TraderID=self._to_bytes(i_tuple[20])
    self.InstallID=int(i_tuple[21])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[22])
    self.NotifySequence=int(i_tuple[23])
    self.TradingDay=self._to_bytes(i_tuple[24])
    self.SettlementID=int(i_tuple[25])
    self.ExecOrderSysID=self._to_bytes(i_tuple[26])
    self.InsertDate=self._to_bytes(i_tuple[27])
    self.InsertTime=self._to_bytes(i_tuple[28])
    self.CancelTime=self._to_bytes(i_tuple[29])
    self.ExecResult=self._to_bytes(i_tuple[30])
    self.ClearingPartID=self._to_bytes(i_tuple[31])
    self.SequenceNo=int(i_tuple[32])
    self.FrontID=int(i_tuple[33])
    self.SessionID=int(i_tuple[34])
    self.UserProductInfo=self._to_bytes(i_tuple[35])
    self.StatusMsg=self._to_bytes(i_tuple[36])
    self.ActiveUserID=self._to_bytes(i_tuple[37])
    self.BrokerExecOrderSeq=int(i_tuple[38])
    self.BranchID=self._to_bytes(i_tuple[39])
    self.InvestUnitID=self._to_bytes(i_tuple[40])
    self.AccountID=self._to_bytes(i_tuple[41])
    self.CurrencyID=self._to_bytes(i_tuple[42])
    self.IPAddress=self._to_bytes(i_tuple[43])
    self.MacAddress=self._to_bytes(i_tuple[44])

class ExecOrderActionField(Base):
  """执行宣告操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExecOrderActionRef',ctypes.c_int)# 执行宣告操作引用
    ,('ExecOrderRef',ctypes.c_char*13)# 执行宣告引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('ExecOrderLocalID',ctypes.c_char*13)# 本地执行宣告编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('ActionType',ctypes.c_char)# 执行类型
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',ExecOrderActionRef=0,ExecOrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',ExecOrderSysID='',ActionFlag='',ActionDate='',ActionTime='',TraderID='',InstallID=0,ExecOrderLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',ActionType='',StatusMsg='',InstrumentID='',BranchID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(ExecOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExecOrderActionRef=int(ExecOrderActionRef)
    self.ExecOrderRef=self._to_bytes(ExecOrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.ExecOrderLocalID=self._to_bytes(ExecOrderLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.ActionType=self._to_bytes(ActionType)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExecOrderActionRef=int(i_tuple[3])
    self.ExecOrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.ExecOrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.ActionDate=self._to_bytes(i_tuple[11])
    self.ActionTime=self._to_bytes(i_tuple[12])
    self.TraderID=self._to_bytes(i_tuple[13])
    self.InstallID=int(i_tuple[14])
    self.ExecOrderLocalID=self._to_bytes(i_tuple[15])
    self.ActionLocalID=self._to_bytes(i_tuple[16])
    self.ParticipantID=self._to_bytes(i_tuple[17])
    self.ClientID=self._to_bytes(i_tuple[18])
    self.BusinessUnit=self._to_bytes(i_tuple[19])
    self.OrderActionStatus=self._to_bytes(i_tuple[20])
    self.UserID=self._to_bytes(i_tuple[21])
    self.ActionType=self._to_bytes(i_tuple[22])
    self.StatusMsg=self._to_bytes(i_tuple[23])
    self.InstrumentID=self._to_bytes(i_tuple[24])
    self.BranchID=self._to_bytes(i_tuple[25])
    self.InvestUnitID=self._to_bytes(i_tuple[26])
    self.IPAddress=self._to_bytes(i_tuple[27])
    self.MacAddress=self._to_bytes(i_tuple[28])

class QryExecOrderField(Base):
  """执行宣告查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告编号
    ,('InsertTimeStart',ctypes.c_char*9)# 开始时间
    ,('InsertTimeEnd',ctypes.c_char*9)# 结束时间
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',ExecOrderSysID='',InsertTimeStart='',InsertTimeEnd=''):

    super(QryExecOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.InsertTimeStart=self._to_bytes(InsertTimeStart)
    self.InsertTimeEnd=self._to_bytes(InsertTimeEnd)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.ExecOrderSysID=self._to_bytes(i_tuple[5])
    self.InsertTimeStart=self._to_bytes(i_tuple[6])
    self.InsertTimeEnd=self._to_bytes(i_tuple[7])

class ExchangeExecOrderField(Base):
  """交易所执行宣告信息"""
  _fields_ = [
    ('Volume',ctypes.c_int)# ///数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ActionType',ctypes.c_char)# 执行类型
    ,('PosiDirection',ctypes.c_char)# 保留头寸申请的持仓方向
    ,('ReservePositionFlag',ctypes.c_char)# 期权行权后是否保留期货头寸的标记,该字段已废弃
    ,('CloseFlag',ctypes.c_char)# 期权行权后生成的头寸是否自动平仓
    ,('ExecOrderLocalID',ctypes.c_char*13)# 本地执行宣告编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 执行宣告提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ExecResult',ctypes.c_char)# 执行结果
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,Volume= 0,RequestID=0,BusinessUnit='',OffsetFlag='',HedgeFlag='',ActionType='',PosiDirection='',ReservePositionFlag='',CloseFlag='',ExecOrderLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,ExecOrderSysID='',InsertDate='',InsertTime='',CancelTime='',ExecResult='',ClearingPartID='',SequenceNo=0,BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeExecOrderField,self).__init__()

    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ActionType=self._to_bytes(ActionType)
    self.PosiDirection=self._to_bytes(PosiDirection)
    self.ReservePositionFlag=self._to_bytes(ReservePositionFlag)
    self.CloseFlag=self._to_bytes(CloseFlag)
    self.ExecOrderLocalID=self._to_bytes(ExecOrderLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ExecResult=self._to_bytes(ExecResult)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.Volume=int(i_tuple[1])
    self.RequestID=int(i_tuple[2])
    self.BusinessUnit=self._to_bytes(i_tuple[3])
    self.OffsetFlag=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.ActionType=self._to_bytes(i_tuple[6])
    self.PosiDirection=self._to_bytes(i_tuple[7])
    self.ReservePositionFlag=self._to_bytes(i_tuple[8])
    self.CloseFlag=self._to_bytes(i_tuple[9])
    self.ExecOrderLocalID=self._to_bytes(i_tuple[10])
    self.ExchangeID=self._to_bytes(i_tuple[11])
    self.ParticipantID=self._to_bytes(i_tuple[12])
    self.ClientID=self._to_bytes(i_tuple[13])
    self.ExchangeInstID=self._to_bytes(i_tuple[14])
    self.TraderID=self._to_bytes(i_tuple[15])
    self.InstallID=int(i_tuple[16])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[17])
    self.NotifySequence=int(i_tuple[18])
    self.TradingDay=self._to_bytes(i_tuple[19])
    self.SettlementID=int(i_tuple[20])
    self.ExecOrderSysID=self._to_bytes(i_tuple[21])
    self.InsertDate=self._to_bytes(i_tuple[22])
    self.InsertTime=self._to_bytes(i_tuple[23])
    self.CancelTime=self._to_bytes(i_tuple[24])
    self.ExecResult=self._to_bytes(i_tuple[25])
    self.ClearingPartID=self._to_bytes(i_tuple[26])
    self.SequenceNo=int(i_tuple[27])
    self.BranchID=self._to_bytes(i_tuple[28])
    self.IPAddress=self._to_bytes(i_tuple[29])
    self.MacAddress=self._to_bytes(i_tuple[30])

class QryExchangeExecOrderField(Base):
  """交易所执行宣告查询"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeInstID='',ExchangeID='',TraderID=''):

    super(QryExchangeExecOrderField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeInstID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.TraderID=self._to_bytes(i_tuple[5])

class QryExecOrderActionField(Base):
  """执行宣告操作查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID=''):

    super(QryExecOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class ExchangeExecOrderActionField(Base):
  """交易所执行宣告操作"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('ExecOrderLocalID',ctypes.c_char*13)# 本地执行宣告编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('ActionType',ctypes.c_char)# 执行类型
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,ExchangeID= '',ExecOrderSysID='',ActionFlag='',ActionDate='',ActionTime='',TraderID='',InstallID=0,ExecOrderLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',ActionType='',BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeExecOrderActionField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.ExecOrderLocalID=self._to_bytes(ExecOrderLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.ActionType=self._to_bytes(ActionType)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ExecOrderSysID=self._to_bytes(i_tuple[2])
    self.ActionFlag=self._to_bytes(i_tuple[3])
    self.ActionDate=self._to_bytes(i_tuple[4])
    self.ActionTime=self._to_bytes(i_tuple[5])
    self.TraderID=self._to_bytes(i_tuple[6])
    self.InstallID=int(i_tuple[7])
    self.ExecOrderLocalID=self._to_bytes(i_tuple[8])
    self.ActionLocalID=self._to_bytes(i_tuple[9])
    self.ParticipantID=self._to_bytes(i_tuple[10])
    self.ClientID=self._to_bytes(i_tuple[11])
    self.BusinessUnit=self._to_bytes(i_tuple[12])
    self.OrderActionStatus=self._to_bytes(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.ActionType=self._to_bytes(i_tuple[15])
    self.BranchID=self._to_bytes(i_tuple[16])
    self.IPAddress=self._to_bytes(i_tuple[17])
    self.MacAddress=self._to_bytes(i_tuple[18])

class QryExchangeExecOrderActionField(Base):
  """交易所执行宣告操作查询"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeID='',TraderID=''):

    super(QryExchangeExecOrderActionField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.TraderID=self._to_bytes(i_tuple[4])

class ErrExecOrderField(Base):
  """错误执行宣告"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExecOrderRef',ctypes.c_char*13)# 执行宣告引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Volume',ctypes.c_int)# 数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ActionType',ctypes.c_char)# 执行类型
    ,('PosiDirection',ctypes.c_char)# 保留头寸申请的持仓方向
    ,('ReservePositionFlag',ctypes.c_char)# 期权行权后是否保留期货头寸的标记,该字段已废弃
    ,('CloseFlag',ctypes.c_char)# 期权行权后生成的头寸是否自动平仓
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExecOrderRef='',UserID='',Volume=0,RequestID=0,BusinessUnit='',OffsetFlag='',HedgeFlag='',ActionType='',PosiDirection='',ReservePositionFlag='',CloseFlag='',ExchangeID='',InvestUnitID='',AccountID='',CurrencyID='',ClientID='',IPAddress='',MacAddress='',ErrorID=0,ErrorMsg=''):

    super(ErrExecOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExecOrderRef=self._to_bytes(ExecOrderRef)
    self.UserID=self._to_bytes(UserID)
    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ActionType=self._to_bytes(ActionType)
    self.PosiDirection=self._to_bytes(PosiDirection)
    self.ReservePositionFlag=self._to_bytes(ReservePositionFlag)
    self.CloseFlag=self._to_bytes(CloseFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExecOrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Volume=int(i_tuple[6])
    self.RequestID=int(i_tuple[7])
    self.BusinessUnit=self._to_bytes(i_tuple[8])
    self.OffsetFlag=self._to_bytes(i_tuple[9])
    self.HedgeFlag=self._to_bytes(i_tuple[10])
    self.ActionType=self._to_bytes(i_tuple[11])
    self.PosiDirection=self._to_bytes(i_tuple[12])
    self.ReservePositionFlag=self._to_bytes(i_tuple[13])
    self.CloseFlag=self._to_bytes(i_tuple[14])
    self.ExchangeID=self._to_bytes(i_tuple[15])
    self.InvestUnitID=self._to_bytes(i_tuple[16])
    self.AccountID=self._to_bytes(i_tuple[17])
    self.CurrencyID=self._to_bytes(i_tuple[18])
    self.ClientID=self._to_bytes(i_tuple[19])
    self.IPAddress=self._to_bytes(i_tuple[20])
    self.MacAddress=self._to_bytes(i_tuple[21])
    self.ErrorID=int(i_tuple[22])
    self.ErrorMsg=self._to_bytes(i_tuple[23])

class QryErrExecOrderField(Base):
  """查询错误执行宣告"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryErrExecOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class ErrExecOrderActionField(Base):
  """错误执行宣告操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExecOrderActionRef',ctypes.c_int)# 执行宣告操作引用
    ,('ExecOrderRef',ctypes.c_char*13)# 执行宣告引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExecOrderSysID',ctypes.c_char*21)# 执行宣告操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,BrokerID= '',InvestorID='',ExecOrderActionRef=0,ExecOrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',ExecOrderSysID='',ActionFlag='',UserID='',InstrumentID='',InvestUnitID='',IPAddress='',MacAddress='',ErrorID=0,ErrorMsg=''):

    super(ErrExecOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExecOrderActionRef=int(ExecOrderActionRef)
    self.ExecOrderRef=self._to_bytes(ExecOrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExecOrderSysID=self._to_bytes(ExecOrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.UserID=self._to_bytes(UserID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExecOrderActionRef=int(i_tuple[3])
    self.ExecOrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.ExecOrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.UserID=self._to_bytes(i_tuple[11])
    self.InstrumentID=self._to_bytes(i_tuple[12])
    self.InvestUnitID=self._to_bytes(i_tuple[13])
    self.IPAddress=self._to_bytes(i_tuple[14])
    self.MacAddress=self._to_bytes(i_tuple[15])
    self.ErrorID=int(i_tuple[16])
    self.ErrorMsg=self._to_bytes(i_tuple[17])

class QryErrExecOrderActionField(Base):
  """查询错误执行宣告操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryErrExecOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class OptionInstrTradingRightField(Base):
  """投资者期权合约交易权限"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('TradingRight',ctypes.c_char)# 交易权限
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',Direction='',TradingRight=''):

    super(OptionInstrTradingRightField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Direction=self._to_bytes(Direction)
    self.TradingRight=self._to_bytes(TradingRight)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.Direction=self._to_bytes(i_tuple[5])
    self.TradingRight=self._to_bytes(i_tuple[6])

class QryOptionInstrTradingRightField(Base):
  """查询期权合约交易权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('Direction',ctypes.c_char)# 买卖方向
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',Direction=''):

    super(QryOptionInstrTradingRightField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.Direction=self._to_bytes(Direction)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.Direction=self._to_bytes(i_tuple[4])

class InputForQuoteField(Base):
  """输入的询价"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ForQuoteRef',ctypes.c_char*13)# 询价引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ForQuoteRef='',UserID='',ExchangeID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(InputForQuoteField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ForQuoteRef=self._to_bytes(ForQuoteRef)
    self.UserID=self._to_bytes(UserID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ForQuoteRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.ExchangeID=self._to_bytes(i_tuple[6])
    self.InvestUnitID=self._to_bytes(i_tuple[7])
    self.IPAddress=self._to_bytes(i_tuple[8])
    self.MacAddress=self._to_bytes(i_tuple[9])

class ForQuoteField(Base):
  """询价"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ForQuoteRef',ctypes.c_char*13)# 询价引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('ForQuoteLocalID',ctypes.c_char*13)# 本地询价编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('ForQuoteStatus',ctypes.c_char)# 询价状态
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('ActiveUserID',ctypes.c_char*16)# 操作用户代码
    ,('BrokerForQutoSeq',ctypes.c_int)# 经纪公司询价编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ForQuoteRef='',UserID='',ForQuoteLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,InsertDate='',InsertTime='',ForQuoteStatus='',FrontID=0,SessionID=0,StatusMsg='',ActiveUserID='',BrokerForQutoSeq=0,InvestUnitID='',IPAddress='',MacAddress=''):

    super(ForQuoteField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ForQuoteRef=self._to_bytes(ForQuoteRef)
    self.UserID=self._to_bytes(UserID)
    self.ForQuoteLocalID=self._to_bytes(ForQuoteLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.ForQuoteStatus=self._to_bytes(ForQuoteStatus)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.ActiveUserID=self._to_bytes(ActiveUserID)
    self.BrokerForQutoSeq=int(BrokerForQutoSeq)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ForQuoteRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.ForQuoteLocalID=self._to_bytes(i_tuple[6])
    self.ExchangeID=self._to_bytes(i_tuple[7])
    self.ParticipantID=self._to_bytes(i_tuple[8])
    self.ClientID=self._to_bytes(i_tuple[9])
    self.ExchangeInstID=self._to_bytes(i_tuple[10])
    self.TraderID=self._to_bytes(i_tuple[11])
    self.InstallID=int(i_tuple[12])
    self.InsertDate=self._to_bytes(i_tuple[13])
    self.InsertTime=self._to_bytes(i_tuple[14])
    self.ForQuoteStatus=self._to_bytes(i_tuple[15])
    self.FrontID=int(i_tuple[16])
    self.SessionID=int(i_tuple[17])
    self.StatusMsg=self._to_bytes(i_tuple[18])
    self.ActiveUserID=self._to_bytes(i_tuple[19])
    self.BrokerForQutoSeq=int(i_tuple[20])
    self.InvestUnitID=self._to_bytes(i_tuple[21])
    self.IPAddress=self._to_bytes(i_tuple[22])
    self.MacAddress=self._to_bytes(i_tuple[23])

class QryForQuoteField(Base):
  """询价查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InsertTimeStart',ctypes.c_char*9)# 开始时间
    ,('InsertTimeEnd',ctypes.c_char*9)# 结束时间
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InsertTimeStart='',InsertTimeEnd='',InvestUnitID=''):

    super(QryForQuoteField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InsertTimeStart=self._to_bytes(InsertTimeStart)
    self.InsertTimeEnd=self._to_bytes(InsertTimeEnd)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InsertTimeStart=self._to_bytes(i_tuple[5])
    self.InsertTimeEnd=self._to_bytes(i_tuple[6])
    self.InvestUnitID=self._to_bytes(i_tuple[7])

class ExchangeForQuoteField(Base):
  """交易所询价信息"""
  _fields_ = [
    ('ForQuoteLocalID',ctypes.c_char*13)# ///本地询价编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('ForQuoteStatus',ctypes.c_char)# 询价状态
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,ForQuoteLocalID= '',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,InsertDate='',InsertTime='',ForQuoteStatus='',IPAddress='',MacAddress=''):

    super(ExchangeForQuoteField,self).__init__()

    self.ForQuoteLocalID=self._to_bytes(ForQuoteLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.ForQuoteStatus=self._to_bytes(ForQuoteStatus)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ForQuoteLocalID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])
    self.ClientID=self._to_bytes(i_tuple[4])
    self.ExchangeInstID=self._to_bytes(i_tuple[5])
    self.TraderID=self._to_bytes(i_tuple[6])
    self.InstallID=int(i_tuple[7])
    self.InsertDate=self._to_bytes(i_tuple[8])
    self.InsertTime=self._to_bytes(i_tuple[9])
    self.ForQuoteStatus=self._to_bytes(i_tuple[10])
    self.IPAddress=self._to_bytes(i_tuple[11])
    self.MacAddress=self._to_bytes(i_tuple[12])

class QryExchangeForQuoteField(Base):
  """交易所询价查询"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeInstID='',ExchangeID='',TraderID=''):

    super(QryExchangeForQuoteField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeInstID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.TraderID=self._to_bytes(i_tuple[5])

class InputQuoteField(Base):
  """输入的报价"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('QuoteRef',ctypes.c_char*13)# 报价引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('AskPrice',ctypes.c_double)# 卖价格
    ,('BidPrice',ctypes.c_double)# 买价格
    ,('AskVolume',ctypes.c_int)# 卖数量
    ,('BidVolume',ctypes.c_int)# 买数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('AskOffsetFlag',ctypes.c_char)# 卖开平标志
    ,('BidOffsetFlag',ctypes.c_char)# 买开平标志
    ,('AskHedgeFlag',ctypes.c_char)# 卖投机套保标志
    ,('BidHedgeFlag',ctypes.c_char)# 买投机套保标志
    ,('AskOrderRef',ctypes.c_char*13)# 衍生卖报单引用
    ,('BidOrderRef',ctypes.c_char*13)# 衍生买报单引用
    ,('ForQuoteSysID',ctypes.c_char*21)# 应价编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',QuoteRef='',UserID='',AskPrice=0.0,BidPrice=0.0,AskVolume=0,BidVolume=0,RequestID=0,BusinessUnit='',AskOffsetFlag='',BidOffsetFlag='',AskHedgeFlag='',BidHedgeFlag='',AskOrderRef='',BidOrderRef='',ForQuoteSysID='',ExchangeID='',InvestUnitID='',ClientID='',IPAddress='',MacAddress=''):

    super(InputQuoteField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.QuoteRef=self._to_bytes(QuoteRef)
    self.UserID=self._to_bytes(UserID)
    self.AskPrice=float(AskPrice)
    self.BidPrice=float(BidPrice)
    self.AskVolume=int(AskVolume)
    self.BidVolume=int(BidVolume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.AskOffsetFlag=self._to_bytes(AskOffsetFlag)
    self.BidOffsetFlag=self._to_bytes(BidOffsetFlag)
    self.AskHedgeFlag=self._to_bytes(AskHedgeFlag)
    self.BidHedgeFlag=self._to_bytes(BidHedgeFlag)
    self.AskOrderRef=self._to_bytes(AskOrderRef)
    self.BidOrderRef=self._to_bytes(BidOrderRef)
    self.ForQuoteSysID=self._to_bytes(ForQuoteSysID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.QuoteRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.AskPrice=float(i_tuple[6])
    self.BidPrice=float(i_tuple[7])
    self.AskVolume=int(i_tuple[8])
    self.BidVolume=int(i_tuple[9])
    self.RequestID=int(i_tuple[10])
    self.BusinessUnit=self._to_bytes(i_tuple[11])
    self.AskOffsetFlag=self._to_bytes(i_tuple[12])
    self.BidOffsetFlag=self._to_bytes(i_tuple[13])
    self.AskHedgeFlag=self._to_bytes(i_tuple[14])
    self.BidHedgeFlag=self._to_bytes(i_tuple[15])
    self.AskOrderRef=self._to_bytes(i_tuple[16])
    self.BidOrderRef=self._to_bytes(i_tuple[17])
    self.ForQuoteSysID=self._to_bytes(i_tuple[18])
    self.ExchangeID=self._to_bytes(i_tuple[19])
    self.InvestUnitID=self._to_bytes(i_tuple[20])
    self.ClientID=self._to_bytes(i_tuple[21])
    self.IPAddress=self._to_bytes(i_tuple[22])
    self.MacAddress=self._to_bytes(i_tuple[23])

class InputQuoteActionField(Base):
  """输入报价操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('QuoteActionRef',ctypes.c_int)# 报价操作引用
    ,('QuoteRef',ctypes.c_char*13)# 报价引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('QuoteSysID',ctypes.c_char*21)# 报价操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',QuoteActionRef=0,QuoteRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',QuoteSysID='',ActionFlag='',UserID='',InstrumentID='',InvestUnitID='',ClientID='',IPAddress='',MacAddress=''):

    super(InputQuoteActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.QuoteActionRef=int(QuoteActionRef)
    self.QuoteRef=self._to_bytes(QuoteRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.QuoteSysID=self._to_bytes(QuoteSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.UserID=self._to_bytes(UserID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.QuoteActionRef=int(i_tuple[3])
    self.QuoteRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.QuoteSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.UserID=self._to_bytes(i_tuple[11])
    self.InstrumentID=self._to_bytes(i_tuple[12])
    self.InvestUnitID=self._to_bytes(i_tuple[13])
    self.ClientID=self._to_bytes(i_tuple[14])
    self.IPAddress=self._to_bytes(i_tuple[15])
    self.MacAddress=self._to_bytes(i_tuple[16])

class QuoteField(Base):
  """报价"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('QuoteRef',ctypes.c_char*13)# 报价引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('AskPrice',ctypes.c_double)# 卖价格
    ,('BidPrice',ctypes.c_double)# 买价格
    ,('AskVolume',ctypes.c_int)# 卖数量
    ,('BidVolume',ctypes.c_int)# 买数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('AskOffsetFlag',ctypes.c_char)# 卖开平标志
    ,('BidOffsetFlag',ctypes.c_char)# 买开平标志
    ,('AskHedgeFlag',ctypes.c_char)# 卖投机套保标志
    ,('BidHedgeFlag',ctypes.c_char)# 买投机套保标志
    ,('QuoteLocalID',ctypes.c_char*13)# 本地报价编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('NotifySequence',ctypes.c_int)# 报价提示序号
    ,('OrderSubmitStatus',ctypes.c_char)# 报价提交状态
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('QuoteSysID',ctypes.c_char*21)# 报价编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('QuoteStatus',ctypes.c_char)# 报价状态
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('AskOrderSysID',ctypes.c_char*21)# 卖方报单编号
    ,('BidOrderSysID',ctypes.c_char*21)# 买方报单编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('ActiveUserID',ctypes.c_char*16)# 操作用户代码
    ,('BrokerQuoteSeq',ctypes.c_int)# 经纪公司报价编号
    ,('AskOrderRef',ctypes.c_char*13)# 衍生卖报单引用
    ,('BidOrderRef',ctypes.c_char*13)# 衍生买报单引用
    ,('ForQuoteSysID',ctypes.c_char*21)# 应价编号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',QuoteRef='',UserID='',AskPrice=0.0,BidPrice=0.0,AskVolume=0,BidVolume=0,RequestID=0,BusinessUnit='',AskOffsetFlag='',BidOffsetFlag='',AskHedgeFlag='',BidHedgeFlag='',QuoteLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,NotifySequence=0,OrderSubmitStatus='',TradingDay='',SettlementID=0,QuoteSysID='',InsertDate='',InsertTime='',CancelTime='',QuoteStatus='',ClearingPartID='',SequenceNo=0,AskOrderSysID='',BidOrderSysID='',FrontID=0,SessionID=0,UserProductInfo='',StatusMsg='',ActiveUserID='',BrokerQuoteSeq=0,AskOrderRef='',BidOrderRef='',ForQuoteSysID='',BranchID='',InvestUnitID='',AccountID='',CurrencyID='',IPAddress='',MacAddress=''):

    super(QuoteField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.QuoteRef=self._to_bytes(QuoteRef)
    self.UserID=self._to_bytes(UserID)
    self.AskPrice=float(AskPrice)
    self.BidPrice=float(BidPrice)
    self.AskVolume=int(AskVolume)
    self.BidVolume=int(BidVolume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.AskOffsetFlag=self._to_bytes(AskOffsetFlag)
    self.BidOffsetFlag=self._to_bytes(BidOffsetFlag)
    self.AskHedgeFlag=self._to_bytes(AskHedgeFlag)
    self.BidHedgeFlag=self._to_bytes(BidHedgeFlag)
    self.QuoteLocalID=self._to_bytes(QuoteLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.NotifySequence=int(NotifySequence)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.QuoteSysID=self._to_bytes(QuoteSysID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.QuoteStatus=self._to_bytes(QuoteStatus)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.AskOrderSysID=self._to_bytes(AskOrderSysID)
    self.BidOrderSysID=self._to_bytes(BidOrderSysID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.ActiveUserID=self._to_bytes(ActiveUserID)
    self.BrokerQuoteSeq=int(BrokerQuoteSeq)
    self.AskOrderRef=self._to_bytes(AskOrderRef)
    self.BidOrderRef=self._to_bytes(BidOrderRef)
    self.ForQuoteSysID=self._to_bytes(ForQuoteSysID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.QuoteRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.AskPrice=float(i_tuple[6])
    self.BidPrice=float(i_tuple[7])
    self.AskVolume=int(i_tuple[8])
    self.BidVolume=int(i_tuple[9])
    self.RequestID=int(i_tuple[10])
    self.BusinessUnit=self._to_bytes(i_tuple[11])
    self.AskOffsetFlag=self._to_bytes(i_tuple[12])
    self.BidOffsetFlag=self._to_bytes(i_tuple[13])
    self.AskHedgeFlag=self._to_bytes(i_tuple[14])
    self.BidHedgeFlag=self._to_bytes(i_tuple[15])
    self.QuoteLocalID=self._to_bytes(i_tuple[16])
    self.ExchangeID=self._to_bytes(i_tuple[17])
    self.ParticipantID=self._to_bytes(i_tuple[18])
    self.ClientID=self._to_bytes(i_tuple[19])
    self.ExchangeInstID=self._to_bytes(i_tuple[20])
    self.TraderID=self._to_bytes(i_tuple[21])
    self.InstallID=int(i_tuple[22])
    self.NotifySequence=int(i_tuple[23])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[24])
    self.TradingDay=self._to_bytes(i_tuple[25])
    self.SettlementID=int(i_tuple[26])
    self.QuoteSysID=self._to_bytes(i_tuple[27])
    self.InsertDate=self._to_bytes(i_tuple[28])
    self.InsertTime=self._to_bytes(i_tuple[29])
    self.CancelTime=self._to_bytes(i_tuple[30])
    self.QuoteStatus=self._to_bytes(i_tuple[31])
    self.ClearingPartID=self._to_bytes(i_tuple[32])
    self.SequenceNo=int(i_tuple[33])
    self.AskOrderSysID=self._to_bytes(i_tuple[34])
    self.BidOrderSysID=self._to_bytes(i_tuple[35])
    self.FrontID=int(i_tuple[36])
    self.SessionID=int(i_tuple[37])
    self.UserProductInfo=self._to_bytes(i_tuple[38])
    self.StatusMsg=self._to_bytes(i_tuple[39])
    self.ActiveUserID=self._to_bytes(i_tuple[40])
    self.BrokerQuoteSeq=int(i_tuple[41])
    self.AskOrderRef=self._to_bytes(i_tuple[42])
    self.BidOrderRef=self._to_bytes(i_tuple[43])
    self.ForQuoteSysID=self._to_bytes(i_tuple[44])
    self.BranchID=self._to_bytes(i_tuple[45])
    self.InvestUnitID=self._to_bytes(i_tuple[46])
    self.AccountID=self._to_bytes(i_tuple[47])
    self.CurrencyID=self._to_bytes(i_tuple[48])
    self.IPAddress=self._to_bytes(i_tuple[49])
    self.MacAddress=self._to_bytes(i_tuple[50])

class QuoteActionField(Base):
  """报价操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('QuoteActionRef',ctypes.c_int)# 报价操作引用
    ,('QuoteRef',ctypes.c_char*13)# 报价引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('QuoteSysID',ctypes.c_char*21)# 报价操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('QuoteLocalID',ctypes.c_char*13)# 本地报价编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',QuoteActionRef=0,QuoteRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',QuoteSysID='',ActionFlag='',ActionDate='',ActionTime='',TraderID='',InstallID=0,QuoteLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',StatusMsg='',InstrumentID='',BranchID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(QuoteActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.QuoteActionRef=int(QuoteActionRef)
    self.QuoteRef=self._to_bytes(QuoteRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.QuoteSysID=self._to_bytes(QuoteSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.QuoteLocalID=self._to_bytes(QuoteLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.QuoteActionRef=int(i_tuple[3])
    self.QuoteRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.QuoteSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.ActionDate=self._to_bytes(i_tuple[11])
    self.ActionTime=self._to_bytes(i_tuple[12])
    self.TraderID=self._to_bytes(i_tuple[13])
    self.InstallID=int(i_tuple[14])
    self.QuoteLocalID=self._to_bytes(i_tuple[15])
    self.ActionLocalID=self._to_bytes(i_tuple[16])
    self.ParticipantID=self._to_bytes(i_tuple[17])
    self.ClientID=self._to_bytes(i_tuple[18])
    self.BusinessUnit=self._to_bytes(i_tuple[19])
    self.OrderActionStatus=self._to_bytes(i_tuple[20])
    self.UserID=self._to_bytes(i_tuple[21])
    self.StatusMsg=self._to_bytes(i_tuple[22])
    self.InstrumentID=self._to_bytes(i_tuple[23])
    self.BranchID=self._to_bytes(i_tuple[24])
    self.InvestUnitID=self._to_bytes(i_tuple[25])
    self.IPAddress=self._to_bytes(i_tuple[26])
    self.MacAddress=self._to_bytes(i_tuple[27])

class QryQuoteField(Base):
  """报价查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('QuoteSysID',ctypes.c_char*21)# 报价编号
    ,('InsertTimeStart',ctypes.c_char*9)# 开始时间
    ,('InsertTimeEnd',ctypes.c_char*9)# 结束时间
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',QuoteSysID='',InsertTimeStart='',InsertTimeEnd='',InvestUnitID=''):

    super(QryQuoteField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.QuoteSysID=self._to_bytes(QuoteSysID)
    self.InsertTimeStart=self._to_bytes(InsertTimeStart)
    self.InsertTimeEnd=self._to_bytes(InsertTimeEnd)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.QuoteSysID=self._to_bytes(i_tuple[5])
    self.InsertTimeStart=self._to_bytes(i_tuple[6])
    self.InsertTimeEnd=self._to_bytes(i_tuple[7])
    self.InvestUnitID=self._to_bytes(i_tuple[8])

class ExchangeQuoteField(Base):
  """交易所报价信息"""
  _fields_ = [
    ('AskPrice',ctypes.c_double)# ///卖价格
    ,('BidPrice',ctypes.c_double)# 买价格
    ,('AskVolume',ctypes.c_int)# 卖数量
    ,('BidVolume',ctypes.c_int)# 买数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('AskOffsetFlag',ctypes.c_char)# 卖开平标志
    ,('BidOffsetFlag',ctypes.c_char)# 买开平标志
    ,('AskHedgeFlag',ctypes.c_char)# 卖投机套保标志
    ,('BidHedgeFlag',ctypes.c_char)# 买投机套保标志
    ,('QuoteLocalID',ctypes.c_char*13)# 本地报价编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('NotifySequence',ctypes.c_int)# 报价提示序号
    ,('OrderSubmitStatus',ctypes.c_char)# 报价提交状态
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('QuoteSysID',ctypes.c_char*21)# 报价编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('QuoteStatus',ctypes.c_char)# 报价状态
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('AskOrderSysID',ctypes.c_char*21)# 卖方报单编号
    ,('BidOrderSysID',ctypes.c_char*21)# 买方报单编号
    ,('ForQuoteSysID',ctypes.c_char*21)# 应价编号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,AskPrice= 0.0,BidPrice=0.0,AskVolume=0,BidVolume=0,RequestID=0,BusinessUnit='',AskOffsetFlag='',BidOffsetFlag='',AskHedgeFlag='',BidHedgeFlag='',QuoteLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,NotifySequence=0,OrderSubmitStatus='',TradingDay='',SettlementID=0,QuoteSysID='',InsertDate='',InsertTime='',CancelTime='',QuoteStatus='',ClearingPartID='',SequenceNo=0,AskOrderSysID='',BidOrderSysID='',ForQuoteSysID='',BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeQuoteField,self).__init__()

    self.AskPrice=float(AskPrice)
    self.BidPrice=float(BidPrice)
    self.AskVolume=int(AskVolume)
    self.BidVolume=int(BidVolume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.AskOffsetFlag=self._to_bytes(AskOffsetFlag)
    self.BidOffsetFlag=self._to_bytes(BidOffsetFlag)
    self.AskHedgeFlag=self._to_bytes(AskHedgeFlag)
    self.BidHedgeFlag=self._to_bytes(BidHedgeFlag)
    self.QuoteLocalID=self._to_bytes(QuoteLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.NotifySequence=int(NotifySequence)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.QuoteSysID=self._to_bytes(QuoteSysID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.QuoteStatus=self._to_bytes(QuoteStatus)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.AskOrderSysID=self._to_bytes(AskOrderSysID)
    self.BidOrderSysID=self._to_bytes(BidOrderSysID)
    self.ForQuoteSysID=self._to_bytes(ForQuoteSysID)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.AskPrice=float(i_tuple[1])
    self.BidPrice=float(i_tuple[2])
    self.AskVolume=int(i_tuple[3])
    self.BidVolume=int(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.BusinessUnit=self._to_bytes(i_tuple[6])
    self.AskOffsetFlag=self._to_bytes(i_tuple[7])
    self.BidOffsetFlag=self._to_bytes(i_tuple[8])
    self.AskHedgeFlag=self._to_bytes(i_tuple[9])
    self.BidHedgeFlag=self._to_bytes(i_tuple[10])
    self.QuoteLocalID=self._to_bytes(i_tuple[11])
    self.ExchangeID=self._to_bytes(i_tuple[12])
    self.ParticipantID=self._to_bytes(i_tuple[13])
    self.ClientID=self._to_bytes(i_tuple[14])
    self.ExchangeInstID=self._to_bytes(i_tuple[15])
    self.TraderID=self._to_bytes(i_tuple[16])
    self.InstallID=int(i_tuple[17])
    self.NotifySequence=int(i_tuple[18])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[19])
    self.TradingDay=self._to_bytes(i_tuple[20])
    self.SettlementID=int(i_tuple[21])
    self.QuoteSysID=self._to_bytes(i_tuple[22])
    self.InsertDate=self._to_bytes(i_tuple[23])
    self.InsertTime=self._to_bytes(i_tuple[24])
    self.CancelTime=self._to_bytes(i_tuple[25])
    self.QuoteStatus=self._to_bytes(i_tuple[26])
    self.ClearingPartID=self._to_bytes(i_tuple[27])
    self.SequenceNo=int(i_tuple[28])
    self.AskOrderSysID=self._to_bytes(i_tuple[29])
    self.BidOrderSysID=self._to_bytes(i_tuple[30])
    self.ForQuoteSysID=self._to_bytes(i_tuple[31])
    self.BranchID=self._to_bytes(i_tuple[32])
    self.IPAddress=self._to_bytes(i_tuple[33])
    self.MacAddress=self._to_bytes(i_tuple[34])

class QryExchangeQuoteField(Base):
  """交易所报价查询"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeInstID='',ExchangeID='',TraderID=''):

    super(QryExchangeQuoteField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeInstID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.TraderID=self._to_bytes(i_tuple[5])

class QryQuoteActionField(Base):
  """报价操作查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID=''):

    super(QryQuoteActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class ExchangeQuoteActionField(Base):
  """交易所报价操作"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('QuoteSysID',ctypes.c_char*21)# 报价操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('QuoteLocalID',ctypes.c_char*13)# 本地报价编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,ExchangeID= '',QuoteSysID='',ActionFlag='',ActionDate='',ActionTime='',TraderID='',InstallID=0,QuoteLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',IPAddress='',MacAddress=''):

    super(ExchangeQuoteActionField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.QuoteSysID=self._to_bytes(QuoteSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.QuoteLocalID=self._to_bytes(QuoteLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.QuoteSysID=self._to_bytes(i_tuple[2])
    self.ActionFlag=self._to_bytes(i_tuple[3])
    self.ActionDate=self._to_bytes(i_tuple[4])
    self.ActionTime=self._to_bytes(i_tuple[5])
    self.TraderID=self._to_bytes(i_tuple[6])
    self.InstallID=int(i_tuple[7])
    self.QuoteLocalID=self._to_bytes(i_tuple[8])
    self.ActionLocalID=self._to_bytes(i_tuple[9])
    self.ParticipantID=self._to_bytes(i_tuple[10])
    self.ClientID=self._to_bytes(i_tuple[11])
    self.BusinessUnit=self._to_bytes(i_tuple[12])
    self.OrderActionStatus=self._to_bytes(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.IPAddress=self._to_bytes(i_tuple[15])
    self.MacAddress=self._to_bytes(i_tuple[16])

class QryExchangeQuoteActionField(Base):
  """交易所报价操作查询"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeID='',TraderID=''):

    super(QryExchangeQuoteActionField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.TraderID=self._to_bytes(i_tuple[4])

class OptionInstrDeltaField(Base):
  """期权合约delta值"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Delta',ctypes.c_double)# Delta值
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',Delta=0.0):

    super(OptionInstrDeltaField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Delta=float(Delta)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.Delta=float(i_tuple[5])

class ForQuoteRspField(Base):
  """发给做市商的询价请求"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ForQuoteSysID',ctypes.c_char*21)# 询价编号
    ,('ForQuoteTime',ctypes.c_char*9)# 询价时间
    ,('ActionDay',ctypes.c_char*9)# 业务日期
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,TradingDay= '',InstrumentID='',ForQuoteSysID='',ForQuoteTime='',ActionDay='',ExchangeID=''):

    super(ForQuoteRspField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ForQuoteSysID=self._to_bytes(ForQuoteSysID)
    self.ForQuoteTime=self._to_bytes(ForQuoteTime)
    self.ActionDay=self._to_bytes(ActionDay)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ForQuoteSysID=self._to_bytes(i_tuple[3])
    self.ForQuoteTime=self._to_bytes(i_tuple[4])
    self.ActionDay=self._to_bytes(i_tuple[5])
    self.ExchangeID=self._to_bytes(i_tuple[6])

class StrikeOffsetField(Base):
  """当前期权合约执行偏移值的详细内容"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Offset',ctypes.c_double)# 执行偏移值
    ,('OffsetType',ctypes.c_char)# 执行偏移类型
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',Offset=0.0,OffsetType=''):

    super(StrikeOffsetField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Offset=float(Offset)
    self.OffsetType=self._to_bytes(OffsetType)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.Offset=float(i_tuple[5])
    self.OffsetType=self._to_bytes(i_tuple[6])

class QryStrikeOffsetField(Base):
  """期权执行偏移值查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID=''):

    super(QryStrikeOffsetField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])

class InputBatchOrderActionField(Base):
  """输入批量报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OrderActionRef',ctypes.c_int)# 报单操作引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OrderActionRef=0,RequestID=0,FrontID=0,SessionID=0,ExchangeID='',UserID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(InputBatchOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OrderActionRef=int(OrderActionRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.UserID=self._to_bytes(UserID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OrderActionRef=int(i_tuple[3])
    self.RequestID=int(i_tuple[4])
    self.FrontID=int(i_tuple[5])
    self.SessionID=int(i_tuple[6])
    self.ExchangeID=self._to_bytes(i_tuple[7])
    self.UserID=self._to_bytes(i_tuple[8])
    self.InvestUnitID=self._to_bytes(i_tuple[9])
    self.IPAddress=self._to_bytes(i_tuple[10])
    self.MacAddress=self._to_bytes(i_tuple[11])

class BatchOrderActionField(Base):
  """批量报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OrderActionRef',ctypes.c_int)# 报单操作引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OrderActionRef=0,RequestID=0,FrontID=0,SessionID=0,ExchangeID='',ActionDate='',ActionTime='',TraderID='',InstallID=0,ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',StatusMsg='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(BatchOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OrderActionRef=int(OrderActionRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OrderActionRef=int(i_tuple[3])
    self.RequestID=int(i_tuple[4])
    self.FrontID=int(i_tuple[5])
    self.SessionID=int(i_tuple[6])
    self.ExchangeID=self._to_bytes(i_tuple[7])
    self.ActionDate=self._to_bytes(i_tuple[8])
    self.ActionTime=self._to_bytes(i_tuple[9])
    self.TraderID=self._to_bytes(i_tuple[10])
    self.InstallID=int(i_tuple[11])
    self.ActionLocalID=self._to_bytes(i_tuple[12])
    self.ParticipantID=self._to_bytes(i_tuple[13])
    self.ClientID=self._to_bytes(i_tuple[14])
    self.BusinessUnit=self._to_bytes(i_tuple[15])
    self.OrderActionStatus=self._to_bytes(i_tuple[16])
    self.UserID=self._to_bytes(i_tuple[17])
    self.StatusMsg=self._to_bytes(i_tuple[18])
    self.InvestUnitID=self._to_bytes(i_tuple[19])
    self.IPAddress=self._to_bytes(i_tuple[20])
    self.MacAddress=self._to_bytes(i_tuple[21])

class ExchangeBatchOrderActionField(Base):
  """交易所批量报单操作"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,ExchangeID= '',ActionDate='',ActionTime='',TraderID='',InstallID=0,ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',IPAddress='',MacAddress=''):

    super(ExchangeBatchOrderActionField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ActionDate=self._to_bytes(i_tuple[2])
    self.ActionTime=self._to_bytes(i_tuple[3])
    self.TraderID=self._to_bytes(i_tuple[4])
    self.InstallID=int(i_tuple[5])
    self.ActionLocalID=self._to_bytes(i_tuple[6])
    self.ParticipantID=self._to_bytes(i_tuple[7])
    self.ClientID=self._to_bytes(i_tuple[8])
    self.BusinessUnit=self._to_bytes(i_tuple[9])
    self.OrderActionStatus=self._to_bytes(i_tuple[10])
    self.UserID=self._to_bytes(i_tuple[11])
    self.IPAddress=self._to_bytes(i_tuple[12])
    self.MacAddress=self._to_bytes(i_tuple[13])

class QryBatchOrderActionField(Base):
  """查询批量报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID=''):

    super(QryBatchOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class CombInstrumentGuardField(Base):
  """组合合约安全系数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('GuarantRatio',ctypes.c_double)# 
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InstrumentID='',GuarantRatio=0.0,ExchangeID=''):

    super(CombInstrumentGuardField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.GuarantRatio=float(GuarantRatio)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.GuarantRatio=float(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])

class QryCombInstrumentGuardField(Base):
  """组合合约安全系数查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InstrumentID='',ExchangeID=''):

    super(QryCombInstrumentGuardField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class InputCombActionField(Base):
  """输入的申请组合"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('CombActionRef',ctypes.c_char*13)# 组合引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('Volume',ctypes.c_int)# 数量
    ,('CombDirection',ctypes.c_char)# 组合指令方向
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',CombActionRef='',UserID='',Direction='',Volume=0,CombDirection='',HedgeFlag='',ExchangeID='',IPAddress='',MacAddress='',InvestUnitID=''):

    super(InputCombActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.CombActionRef=self._to_bytes(CombActionRef)
    self.UserID=self._to_bytes(UserID)
    self.Direction=self._to_bytes(Direction)
    self.Volume=int(Volume)
    self.CombDirection=self._to_bytes(CombDirection)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.CombActionRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Direction=self._to_bytes(i_tuple[6])
    self.Volume=int(i_tuple[7])
    self.CombDirection=self._to_bytes(i_tuple[8])
    self.HedgeFlag=self._to_bytes(i_tuple[9])
    self.ExchangeID=self._to_bytes(i_tuple[10])
    self.IPAddress=self._to_bytes(i_tuple[11])
    self.MacAddress=self._to_bytes(i_tuple[12])
    self.InvestUnitID=self._to_bytes(i_tuple[13])

class CombActionField(Base):
  """申请组合"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('CombActionRef',ctypes.c_char*13)# 组合引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('Volume',ctypes.c_int)# 数量
    ,('CombDirection',ctypes.c_char)# 组合指令方向
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ActionLocalID',ctypes.c_char*13)# 本地申请组合编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('ActionStatus',ctypes.c_char)# 组合状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('ComTradeID',ctypes.c_char*21)# 组合编号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',CombActionRef='',UserID='',Direction='',Volume=0,CombDirection='',HedgeFlag='',ActionLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,ActionStatus='',NotifySequence=0,TradingDay='',SettlementID=0,SequenceNo=0,FrontID=0,SessionID=0,UserProductInfo='',StatusMsg='',IPAddress='',MacAddress='',ComTradeID='',BranchID='',InvestUnitID=''):

    super(CombActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.CombActionRef=self._to_bytes(CombActionRef)
    self.UserID=self._to_bytes(UserID)
    self.Direction=self._to_bytes(Direction)
    self.Volume=int(Volume)
    self.CombDirection=self._to_bytes(CombDirection)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.ActionStatus=self._to_bytes(ActionStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.SequenceNo=int(SequenceNo)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
    self.ComTradeID=self._to_bytes(ComTradeID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.CombActionRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Direction=self._to_bytes(i_tuple[6])
    self.Volume=int(i_tuple[7])
    self.CombDirection=self._to_bytes(i_tuple[8])
    self.HedgeFlag=self._to_bytes(i_tuple[9])
    self.ActionLocalID=self._to_bytes(i_tuple[10])
    self.ExchangeID=self._to_bytes(i_tuple[11])
    self.ParticipantID=self._to_bytes(i_tuple[12])
    self.ClientID=self._to_bytes(i_tuple[13])
    self.ExchangeInstID=self._to_bytes(i_tuple[14])
    self.TraderID=self._to_bytes(i_tuple[15])
    self.InstallID=int(i_tuple[16])
    self.ActionStatus=self._to_bytes(i_tuple[17])
    self.NotifySequence=int(i_tuple[18])
    self.TradingDay=self._to_bytes(i_tuple[19])
    self.SettlementID=int(i_tuple[20])
    self.SequenceNo=int(i_tuple[21])
    self.FrontID=int(i_tuple[22])
    self.SessionID=int(i_tuple[23])
    self.UserProductInfo=self._to_bytes(i_tuple[24])
    self.StatusMsg=self._to_bytes(i_tuple[25])
    self.IPAddress=self._to_bytes(i_tuple[26])
    self.MacAddress=self._to_bytes(i_tuple[27])
    self.ComTradeID=self._to_bytes(i_tuple[28])
    self.BranchID=self._to_bytes(i_tuple[29])
    self.InvestUnitID=self._to_bytes(i_tuple[30])

class QryCombActionField(Base):
  """申请组合查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryCombActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class ExchangeCombActionField(Base):
  """交易所申请组合信息"""
  _fields_ = [
    ('Direction',ctypes.c_char)# ///买卖方向
    ,('Volume',ctypes.c_int)# 数量
    ,('CombDirection',ctypes.c_char)# 组合指令方向
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ActionLocalID',ctypes.c_char*13)# 本地申请组合编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('ActionStatus',ctypes.c_char)# 组合状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('ComTradeID',ctypes.c_char*21)# 组合编号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
]

  def __init__(self,Direction= '',Volume=0,CombDirection='',HedgeFlag='',ActionLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,ActionStatus='',NotifySequence=0,TradingDay='',SettlementID=0,SequenceNo=0,IPAddress='',MacAddress='',ComTradeID='',BranchID=''):

    super(ExchangeCombActionField,self).__init__()

    self.Direction=self._to_bytes(Direction)
    self.Volume=int(Volume)
    self.CombDirection=self._to_bytes(CombDirection)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.ActionStatus=self._to_bytes(ActionStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.SequenceNo=int(SequenceNo)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
    self.ComTradeID=self._to_bytes(ComTradeID)
    self.BranchID=self._to_bytes(BranchID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.Direction=self._to_bytes(i_tuple[1])
    self.Volume=int(i_tuple[2])
    self.CombDirection=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.ActionLocalID=self._to_bytes(i_tuple[5])
    self.ExchangeID=self._to_bytes(i_tuple[6])
    self.ParticipantID=self._to_bytes(i_tuple[7])
    self.ClientID=self._to_bytes(i_tuple[8])
    self.ExchangeInstID=self._to_bytes(i_tuple[9])
    self.TraderID=self._to_bytes(i_tuple[10])
    self.InstallID=int(i_tuple[11])
    self.ActionStatus=self._to_bytes(i_tuple[12])
    self.NotifySequence=int(i_tuple[13])
    self.TradingDay=self._to_bytes(i_tuple[14])
    self.SettlementID=int(i_tuple[15])
    self.SequenceNo=int(i_tuple[16])
    self.IPAddress=self._to_bytes(i_tuple[17])
    self.MacAddress=self._to_bytes(i_tuple[18])
    self.ComTradeID=self._to_bytes(i_tuple[19])
    self.BranchID=self._to_bytes(i_tuple[20])

class QryExchangeCombActionField(Base):
  """交易所申请组合查询"""
  _fields_ = [
    ('ParticipantID',ctypes.c_char*11)# ///会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ParticipantID= '',ClientID='',ExchangeInstID='',ExchangeID='',TraderID=''):

    super(QryExchangeCombActionField,self).__init__()

    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ParticipantID=self._to_bytes(i_tuple[1])
    self.ClientID=self._to_bytes(i_tuple[2])
    self.ExchangeInstID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.TraderID=self._to_bytes(i_tuple[5])

class ProductExchRateField(Base):
  """产品报价汇率"""
  _fields_ = [
    ('ProductID',ctypes.c_char*31)# ///产品代码
    ,('QuoteCurrencyID',ctypes.c_char*4)# 报价币种类型
    ,('ExchangeRate',ctypes.c_double)# 汇率
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,ProductID= '',QuoteCurrencyID='',ExchangeRate=0.0,ExchangeID=''):

    super(ProductExchRateField,self).__init__()

    self.ProductID=self._to_bytes(ProductID)
    self.QuoteCurrencyID=self._to_bytes(QuoteCurrencyID)
    self.ExchangeRate=float(ExchangeRate)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductID=self._to_bytes(i_tuple[1])
    self.QuoteCurrencyID=self._to_bytes(i_tuple[2])
    self.ExchangeRate=float(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])

class QryProductExchRateField(Base):
  """产品报价汇率查询"""
  _fields_ = [
    ('ProductID',ctypes.c_char*31)# ///产品代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,ProductID= '',ExchangeID=''):

    super(QryProductExchRateField,self).__init__()

    self.ProductID=self._to_bytes(ProductID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])

class QryForQuoteParamField(Base):
  """查询询价价差参数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InstrumentID='',ExchangeID=''):

    super(QryForQuoteParamField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class ForQuoteParamField(Base):
  """询价价差参数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('LastPrice',ctypes.c_double)# 最新价
    ,('PriceInterval',ctypes.c_double)# 价差
]

  def __init__(self,BrokerID= '',InstrumentID='',ExchangeID='',LastPrice=0.0,PriceInterval=0.0):

    super(ForQuoteParamField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.LastPrice=float(LastPrice)
    self.PriceInterval=float(PriceInterval)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.LastPrice=float(i_tuple[4])
    self.PriceInterval=float(i_tuple[5])

class MMOptionInstrCommRateField(Base):
  """当前做市商期权合约手续费的详细内容"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OpenRatioByMoney',ctypes.c_double)# 开仓手续费率
    ,('OpenRatioByVolume',ctypes.c_double)# 开仓手续费
    ,('CloseRatioByMoney',ctypes.c_double)# 平仓手续费率
    ,('CloseRatioByVolume',ctypes.c_double)# 平仓手续费
    ,('CloseTodayRatioByMoney',ctypes.c_double)# 平今手续费率
    ,('CloseTodayRatioByVolume',ctypes.c_double)# 平今手续费
    ,('StrikeRatioByMoney',ctypes.c_double)# 执行手续费率
    ,('StrikeRatioByVolume',ctypes.c_double)# 执行手续费
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',OpenRatioByMoney=0.0,OpenRatioByVolume=0.0,CloseRatioByMoney=0.0,CloseRatioByVolume=0.0,CloseTodayRatioByMoney=0.0,CloseTodayRatioByVolume=0.0,StrikeRatioByMoney=0.0,StrikeRatioByVolume=0.0):

    super(MMOptionInstrCommRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OpenRatioByMoney=float(OpenRatioByMoney)
    self.OpenRatioByVolume=float(OpenRatioByVolume)
    self.CloseRatioByMoney=float(CloseRatioByMoney)
    self.CloseRatioByVolume=float(CloseRatioByVolume)
    self.CloseTodayRatioByMoney=float(CloseTodayRatioByMoney)
    self.CloseTodayRatioByVolume=float(CloseTodayRatioByVolume)
    self.StrikeRatioByMoney=float(StrikeRatioByMoney)
    self.StrikeRatioByVolume=float(StrikeRatioByVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.OpenRatioByMoney=float(i_tuple[5])
    self.OpenRatioByVolume=float(i_tuple[6])
    self.CloseRatioByMoney=float(i_tuple[7])
    self.CloseRatioByVolume=float(i_tuple[8])
    self.CloseTodayRatioByMoney=float(i_tuple[9])
    self.CloseTodayRatioByVolume=float(i_tuple[10])
    self.StrikeRatioByMoney=float(i_tuple[11])
    self.StrikeRatioByVolume=float(i_tuple[12])

class QryMMOptionInstrCommRateField(Base):
  """做市商期权手续费率查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID=''):

    super(QryMMOptionInstrCommRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])

class MMInstrumentCommissionRateField(Base):
  """做市商合约手续费率"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OpenRatioByMoney',ctypes.c_double)# 开仓手续费率
    ,('OpenRatioByVolume',ctypes.c_double)# 开仓手续费
    ,('CloseRatioByMoney',ctypes.c_double)# 平仓手续费率
    ,('CloseRatioByVolume',ctypes.c_double)# 平仓手续费
    ,('CloseTodayRatioByMoney',ctypes.c_double)# 平今手续费率
    ,('CloseTodayRatioByVolume',ctypes.c_double)# 平今手续费
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',OpenRatioByMoney=0.0,OpenRatioByVolume=0.0,CloseRatioByMoney=0.0,CloseRatioByVolume=0.0,CloseTodayRatioByMoney=0.0,CloseTodayRatioByVolume=0.0):

    super(MMInstrumentCommissionRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OpenRatioByMoney=float(OpenRatioByMoney)
    self.OpenRatioByVolume=float(OpenRatioByVolume)
    self.CloseRatioByMoney=float(CloseRatioByMoney)
    self.CloseRatioByVolume=float(CloseRatioByVolume)
    self.CloseTodayRatioByMoney=float(CloseTodayRatioByMoney)
    self.CloseTodayRatioByVolume=float(CloseTodayRatioByVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.OpenRatioByMoney=float(i_tuple[5])
    self.OpenRatioByVolume=float(i_tuple[6])
    self.CloseRatioByMoney=float(i_tuple[7])
    self.CloseRatioByVolume=float(i_tuple[8])
    self.CloseTodayRatioByMoney=float(i_tuple[9])
    self.CloseTodayRatioByVolume=float(i_tuple[10])

class QryMMInstrumentCommissionRateField(Base):
  """查询做市商合约手续费率"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID=''):

    super(QryMMInstrumentCommissionRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])

class InstrumentOrderCommRateField(Base):
  """当前报单手续费的详细内容"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('OrderCommByVolume',ctypes.c_double)# 报单手续费
    ,('OrderActionCommByVolume',ctypes.c_double)# 撤单手续费
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',HedgeFlag='',OrderCommByVolume=0.0,OrderActionCommByVolume=0.0,ExchangeID='',InvestUnitID=''):

    super(InstrumentOrderCommRateField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.OrderCommByVolume=float(OrderCommByVolume)
    self.OrderActionCommByVolume=float(OrderActionCommByVolume)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.OrderCommByVolume=float(i_tuple[6])
    self.OrderActionCommByVolume=float(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.InvestUnitID=self._to_bytes(i_tuple[9])

class QryInstrumentOrderCommRateField(Base):
  """报单手续费率查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID=''):

    super(QryInstrumentOrderCommRateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])

class TradeParamField(Base):
  """交易参数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('TradeParamID',ctypes.c_char)# 参数代码
    ,('TradeParamValue',ctypes.c_char*256)# 参数代码值
    ,('Memo',ctypes.c_char*161)# 备注
]

  def __init__(self,BrokerID= '',TradeParamID='',TradeParamValue='',Memo=''):

    super(TradeParamField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.TradeParamID=self._to_bytes(TradeParamID)
    self.TradeParamValue=self._to_bytes(TradeParamValue)
    self.Memo=self._to_bytes(Memo)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.TradeParamID=self._to_bytes(i_tuple[2])
    self.TradeParamValue=self._to_bytes(i_tuple[3])
    self.Memo=self._to_bytes(i_tuple[4])

class InstrumentMarginRateULField(Base):
  """合约保证金率调整"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('LongMarginRatioByMoney',ctypes.c_double)# 多头保证金率
    ,('LongMarginRatioByVolume',ctypes.c_double)# 多头保证金费
    ,('ShortMarginRatioByMoney',ctypes.c_double)# 空头保证金率
    ,('ShortMarginRatioByVolume',ctypes.c_double)# 空头保证金费
]

  def __init__(self,InstrumentID= '',InvestorRange='',BrokerID='',InvestorID='',HedgeFlag='',LongMarginRatioByMoney=0.0,LongMarginRatioByVolume=0.0,ShortMarginRatioByMoney=0.0,ShortMarginRatioByVolume=0.0):

    super(InstrumentMarginRateULField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.LongMarginRatioByMoney=float(LongMarginRatioByMoney)
    self.LongMarginRatioByVolume=float(LongMarginRatioByVolume)
    self.ShortMarginRatioByMoney=float(ShortMarginRatioByMoney)
    self.ShortMarginRatioByVolume=float(ShortMarginRatioByVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.BrokerID=self._to_bytes(i_tuple[3])
    self.InvestorID=self._to_bytes(i_tuple[4])
    self.HedgeFlag=self._to_bytes(i_tuple[5])
    self.LongMarginRatioByMoney=float(i_tuple[6])
    self.LongMarginRatioByVolume=float(i_tuple[7])
    self.ShortMarginRatioByMoney=float(i_tuple[8])
    self.ShortMarginRatioByVolume=float(i_tuple[9])

class FutureLimitPosiParamField(Base):
  """期货持仓限制参数"""
  _fields_ = [
    ('InvestorRange',ctypes.c_char)# ///投资者范围
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ProductID',ctypes.c_char*31)# 产品代码
    ,('SpecOpenVolume',ctypes.c_int)# 当日投机开仓数量限制
    ,('ArbiOpenVolume',ctypes.c_int)# 当日套利开仓数量限制
    ,('OpenVolume',ctypes.c_int)# 当日投机+套利开仓数量限制
]

  def __init__(self,InvestorRange= '',BrokerID='',InvestorID='',ProductID='',SpecOpenVolume=0,ArbiOpenVolume=0,OpenVolume=0):

    super(FutureLimitPosiParamField,self).__init__()

    self.InvestorRange=self._to_bytes(InvestorRange)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ProductID=self._to_bytes(ProductID)
    self.SpecOpenVolume=int(SpecOpenVolume)
    self.ArbiOpenVolume=int(ArbiOpenVolume)
    self.OpenVolume=int(OpenVolume)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InvestorRange=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.ProductID=self._to_bytes(i_tuple[4])
    self.SpecOpenVolume=int(i_tuple[5])
    self.ArbiOpenVolume=int(i_tuple[6])
    self.OpenVolume=int(i_tuple[7])

class LoginForbiddenIPField(Base):
  """禁止登录IP"""
  _fields_ = [
    ('IPAddress',ctypes.c_char*16)# ///IP地址
]

  def __init__(self,IPAddress= ''):

    super(LoginForbiddenIPField,self).__init__()

    self.IPAddress=self._to_bytes(IPAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.IPAddress=self._to_bytes(i_tuple[1])

class IPListField(Base):
  """IP列表"""
  _fields_ = [
    ('IPAddress',ctypes.c_char*16)# ///IP地址
    ,('IsWhite',ctypes.c_int)# 是否白名单
]

  def __init__(self,IPAddress= '',IsWhite=0):

    super(IPListField,self).__init__()

    self.IPAddress=self._to_bytes(IPAddress)
    self.IsWhite=int(IsWhite)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.IPAddress=self._to_bytes(i_tuple[1])
    self.IsWhite=int(i_tuple[2])

class InputOptionSelfCloseField(Base):
  """输入的期权自对冲"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OptionSelfCloseRef',ctypes.c_char*13)# 期权自对冲引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Volume',ctypes.c_int)# 数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('OptSelfCloseFlag',ctypes.c_char)# 期权行权的头寸是否自对冲
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OptionSelfCloseRef='',UserID='',Volume=0,RequestID=0,BusinessUnit='',HedgeFlag='',OptSelfCloseFlag='',ExchangeID='',InvestUnitID='',AccountID='',CurrencyID='',ClientID='',IPAddress='',MacAddress=''):

    super(InputOptionSelfCloseField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OptionSelfCloseRef=self._to_bytes(OptionSelfCloseRef)
    self.UserID=self._to_bytes(UserID)
    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.OptSelfCloseFlag=self._to_bytes(OptSelfCloseFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OptionSelfCloseRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Volume=int(i_tuple[6])
    self.RequestID=int(i_tuple[7])
    self.BusinessUnit=self._to_bytes(i_tuple[8])
    self.HedgeFlag=self._to_bytes(i_tuple[9])
    self.OptSelfCloseFlag=self._to_bytes(i_tuple[10])
    self.ExchangeID=self._to_bytes(i_tuple[11])
    self.InvestUnitID=self._to_bytes(i_tuple[12])
    self.AccountID=self._to_bytes(i_tuple[13])
    self.CurrencyID=self._to_bytes(i_tuple[14])
    self.ClientID=self._to_bytes(i_tuple[15])
    self.IPAddress=self._to_bytes(i_tuple[16])
    self.MacAddress=self._to_bytes(i_tuple[17])

class InputOptionSelfCloseActionField(Base):
  """输入期权自对冲操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OptionSelfCloseActionRef',ctypes.c_int)# 期权自对冲操作引用
    ,('OptionSelfCloseRef',ctypes.c_char*13)# 期权自对冲引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OptionSelfCloseSysID',ctypes.c_char*21)# 期权自对冲操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OptionSelfCloseActionRef=0,OptionSelfCloseRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',OptionSelfCloseSysID='',ActionFlag='',UserID='',InstrumentID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(InputOptionSelfCloseActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OptionSelfCloseActionRef=int(OptionSelfCloseActionRef)
    self.OptionSelfCloseRef=self._to_bytes(OptionSelfCloseRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OptionSelfCloseSysID=self._to_bytes(OptionSelfCloseSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.UserID=self._to_bytes(UserID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OptionSelfCloseActionRef=int(i_tuple[3])
    self.OptionSelfCloseRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.OptionSelfCloseSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.UserID=self._to_bytes(i_tuple[11])
    self.InstrumentID=self._to_bytes(i_tuple[12])
    self.InvestUnitID=self._to_bytes(i_tuple[13])
    self.IPAddress=self._to_bytes(i_tuple[14])
    self.MacAddress=self._to_bytes(i_tuple[15])

class OptionSelfCloseField(Base):
  """期权自对冲"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OptionSelfCloseRef',ctypes.c_char*13)# 期权自对冲引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('Volume',ctypes.c_int)# 数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('OptSelfCloseFlag',ctypes.c_char)# 期权行权的头寸是否自对冲
    ,('OptionSelfCloseLocalID',ctypes.c_char*13)# 本地期权自对冲编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 期权自对冲提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OptionSelfCloseSysID',ctypes.c_char*21)# 期权自对冲编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ExecResult',ctypes.c_char)# 自对冲结果
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('ActiveUserID',ctypes.c_char*16)# 操作用户代码
    ,('BrokerOptionSelfCloseSeq',ctypes.c_int)# 经纪公司报单编号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OptionSelfCloseRef='',UserID='',Volume=0,RequestID=0,BusinessUnit='',HedgeFlag='',OptSelfCloseFlag='',OptionSelfCloseLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,OptionSelfCloseSysID='',InsertDate='',InsertTime='',CancelTime='',ExecResult='',ClearingPartID='',SequenceNo=0,FrontID=0,SessionID=0,UserProductInfo='',StatusMsg='',ActiveUserID='',BrokerOptionSelfCloseSeq=0,BranchID='',InvestUnitID='',AccountID='',CurrencyID='',IPAddress='',MacAddress=''):

    super(OptionSelfCloseField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OptionSelfCloseRef=self._to_bytes(OptionSelfCloseRef)
    self.UserID=self._to_bytes(UserID)
    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.OptSelfCloseFlag=self._to_bytes(OptSelfCloseFlag)
    self.OptionSelfCloseLocalID=self._to_bytes(OptionSelfCloseLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OptionSelfCloseSysID=self._to_bytes(OptionSelfCloseSysID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ExecResult=self._to_bytes(ExecResult)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.ActiveUserID=self._to_bytes(ActiveUserID)
    self.BrokerOptionSelfCloseSeq=int(BrokerOptionSelfCloseSeq)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OptionSelfCloseRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.Volume=int(i_tuple[6])
    self.RequestID=int(i_tuple[7])
    self.BusinessUnit=self._to_bytes(i_tuple[8])
    self.HedgeFlag=self._to_bytes(i_tuple[9])
    self.OptSelfCloseFlag=self._to_bytes(i_tuple[10])
    self.OptionSelfCloseLocalID=self._to_bytes(i_tuple[11])
    self.ExchangeID=self._to_bytes(i_tuple[12])
    self.ParticipantID=self._to_bytes(i_tuple[13])
    self.ClientID=self._to_bytes(i_tuple[14])
    self.ExchangeInstID=self._to_bytes(i_tuple[15])
    self.TraderID=self._to_bytes(i_tuple[16])
    self.InstallID=int(i_tuple[17])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[18])
    self.NotifySequence=int(i_tuple[19])
    self.TradingDay=self._to_bytes(i_tuple[20])
    self.SettlementID=int(i_tuple[21])
    self.OptionSelfCloseSysID=self._to_bytes(i_tuple[22])
    self.InsertDate=self._to_bytes(i_tuple[23])
    self.InsertTime=self._to_bytes(i_tuple[24])
    self.CancelTime=self._to_bytes(i_tuple[25])
    self.ExecResult=self._to_bytes(i_tuple[26])
    self.ClearingPartID=self._to_bytes(i_tuple[27])
    self.SequenceNo=int(i_tuple[28])
    self.FrontID=int(i_tuple[29])
    self.SessionID=int(i_tuple[30])
    self.UserProductInfo=self._to_bytes(i_tuple[31])
    self.StatusMsg=self._to_bytes(i_tuple[32])
    self.ActiveUserID=self._to_bytes(i_tuple[33])
    self.BrokerOptionSelfCloseSeq=int(i_tuple[34])
    self.BranchID=self._to_bytes(i_tuple[35])
    self.InvestUnitID=self._to_bytes(i_tuple[36])
    self.AccountID=self._to_bytes(i_tuple[37])
    self.CurrencyID=self._to_bytes(i_tuple[38])
    self.IPAddress=self._to_bytes(i_tuple[39])
    self.MacAddress=self._to_bytes(i_tuple[40])

class OptionSelfCloseActionField(Base):
  """期权自对冲操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OptionSelfCloseActionRef',ctypes.c_int)# 期权自对冲操作引用
    ,('OptionSelfCloseRef',ctypes.c_char*13)# 期权自对冲引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OptionSelfCloseSysID',ctypes.c_char*21)# 期权自对冲操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OptionSelfCloseLocalID',ctypes.c_char*13)# 本地期权自对冲编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OptionSelfCloseActionRef=0,OptionSelfCloseRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',OptionSelfCloseSysID='',ActionFlag='',ActionDate='',ActionTime='',TraderID='',InstallID=0,OptionSelfCloseLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',StatusMsg='',InstrumentID='',BranchID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(OptionSelfCloseActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OptionSelfCloseActionRef=int(OptionSelfCloseActionRef)
    self.OptionSelfCloseRef=self._to_bytes(OptionSelfCloseRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OptionSelfCloseSysID=self._to_bytes(OptionSelfCloseSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OptionSelfCloseLocalID=self._to_bytes(OptionSelfCloseLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OptionSelfCloseActionRef=int(i_tuple[3])
    self.OptionSelfCloseRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.OptionSelfCloseSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.ActionDate=self._to_bytes(i_tuple[11])
    self.ActionTime=self._to_bytes(i_tuple[12])
    self.TraderID=self._to_bytes(i_tuple[13])
    self.InstallID=int(i_tuple[14])
    self.OptionSelfCloseLocalID=self._to_bytes(i_tuple[15])
    self.ActionLocalID=self._to_bytes(i_tuple[16])
    self.ParticipantID=self._to_bytes(i_tuple[17])
    self.ClientID=self._to_bytes(i_tuple[18])
    self.BusinessUnit=self._to_bytes(i_tuple[19])
    self.OrderActionStatus=self._to_bytes(i_tuple[20])
    self.UserID=self._to_bytes(i_tuple[21])
    self.StatusMsg=self._to_bytes(i_tuple[22])
    self.InstrumentID=self._to_bytes(i_tuple[23])
    self.BranchID=self._to_bytes(i_tuple[24])
    self.InvestUnitID=self._to_bytes(i_tuple[25])
    self.IPAddress=self._to_bytes(i_tuple[26])
    self.MacAddress=self._to_bytes(i_tuple[27])

class QryOptionSelfCloseField(Base):
  """期权自对冲查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OptionSelfCloseSysID',ctypes.c_char*21)# 期权自对冲编号
    ,('InsertTimeStart',ctypes.c_char*9)# 开始时间
    ,('InsertTimeEnd',ctypes.c_char*9)# 结束时间
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',OptionSelfCloseSysID='',InsertTimeStart='',InsertTimeEnd=''):

    super(QryOptionSelfCloseField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OptionSelfCloseSysID=self._to_bytes(OptionSelfCloseSysID)
    self.InsertTimeStart=self._to_bytes(InsertTimeStart)
    self.InsertTimeEnd=self._to_bytes(InsertTimeEnd)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.OptionSelfCloseSysID=self._to_bytes(i_tuple[5])
    self.InsertTimeStart=self._to_bytes(i_tuple[6])
    self.InsertTimeEnd=self._to_bytes(i_tuple[7])

class ExchangeOptionSelfCloseField(Base):
  """交易所期权自对冲信息"""
  _fields_ = [
    ('Volume',ctypes.c_int)# ///数量
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('OptSelfCloseFlag',ctypes.c_char)# 期权行权的头寸是否自对冲
    ,('OptionSelfCloseLocalID',ctypes.c_char*13)# 本地期权自对冲编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 期权自对冲提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OptionSelfCloseSysID',ctypes.c_char*21)# 期权自对冲编号
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 插入时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ExecResult',ctypes.c_char)# 自对冲结果
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,Volume= 0,RequestID=0,BusinessUnit='',HedgeFlag='',OptSelfCloseFlag='',OptionSelfCloseLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,OptionSelfCloseSysID='',InsertDate='',InsertTime='',CancelTime='',ExecResult='',ClearingPartID='',SequenceNo=0,BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeOptionSelfCloseField,self).__init__()

    self.Volume=int(Volume)
    self.RequestID=int(RequestID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.OptSelfCloseFlag=self._to_bytes(OptSelfCloseFlag)
    self.OptionSelfCloseLocalID=self._to_bytes(OptionSelfCloseLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OptionSelfCloseSysID=self._to_bytes(OptionSelfCloseSysID)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ExecResult=self._to_bytes(ExecResult)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.Volume=int(i_tuple[1])
    self.RequestID=int(i_tuple[2])
    self.BusinessUnit=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.OptSelfCloseFlag=self._to_bytes(i_tuple[5])
    self.OptionSelfCloseLocalID=self._to_bytes(i_tuple[6])
    self.ExchangeID=self._to_bytes(i_tuple[7])
    self.ParticipantID=self._to_bytes(i_tuple[8])
    self.ClientID=self._to_bytes(i_tuple[9])
    self.ExchangeInstID=self._to_bytes(i_tuple[10])
    self.TraderID=self._to_bytes(i_tuple[11])
    self.InstallID=int(i_tuple[12])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[13])
    self.NotifySequence=int(i_tuple[14])
    self.TradingDay=self._to_bytes(i_tuple[15])
    self.SettlementID=int(i_tuple[16])
    self.OptionSelfCloseSysID=self._to_bytes(i_tuple[17])
    self.InsertDate=self._to_bytes(i_tuple[18])
    self.InsertTime=self._to_bytes(i_tuple[19])
    self.CancelTime=self._to_bytes(i_tuple[20])
    self.ExecResult=self._to_bytes(i_tuple[21])
    self.ClearingPartID=self._to_bytes(i_tuple[22])
    self.SequenceNo=int(i_tuple[23])
    self.BranchID=self._to_bytes(i_tuple[24])
    self.IPAddress=self._to_bytes(i_tuple[25])
    self.MacAddress=self._to_bytes(i_tuple[26])

class QryOptionSelfCloseActionField(Base):
  """期权自对冲操作查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID=''):

    super(QryOptionSelfCloseActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])

class ExchangeOptionSelfCloseActionField(Base):
  """交易所期权自对冲操作"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('OptionSelfCloseSysID',ctypes.c_char*21)# 期权自对冲操作编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OptionSelfCloseLocalID',ctypes.c_char*13)# 本地期权自对冲编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,ExchangeID= '',OptionSelfCloseSysID='',ActionFlag='',ActionDate='',ActionTime='',TraderID='',InstallID=0,OptionSelfCloseLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',BranchID='',IPAddress='',MacAddress=''):

    super(ExchangeOptionSelfCloseActionField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OptionSelfCloseSysID=self._to_bytes(OptionSelfCloseSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OptionSelfCloseLocalID=self._to_bytes(OptionSelfCloseLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.BranchID=self._to_bytes(BranchID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.OptionSelfCloseSysID=self._to_bytes(i_tuple[2])
    self.ActionFlag=self._to_bytes(i_tuple[3])
    self.ActionDate=self._to_bytes(i_tuple[4])
    self.ActionTime=self._to_bytes(i_tuple[5])
    self.TraderID=self._to_bytes(i_tuple[6])
    self.InstallID=int(i_tuple[7])
    self.OptionSelfCloseLocalID=self._to_bytes(i_tuple[8])
    self.ActionLocalID=self._to_bytes(i_tuple[9])
    self.ParticipantID=self._to_bytes(i_tuple[10])
    self.ClientID=self._to_bytes(i_tuple[11])
    self.BusinessUnit=self._to_bytes(i_tuple[12])
    self.OrderActionStatus=self._to_bytes(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.BranchID=self._to_bytes(i_tuple[15])
    self.IPAddress=self._to_bytes(i_tuple[16])
    self.MacAddress=self._to_bytes(i_tuple[17])

class SyncDelaySwapField(Base):
  """延时换汇同步"""
  _fields_ = [
    ('DelaySwapSeqNo',ctypes.c_char*15)# ///换汇流水号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('FromCurrencyID',ctypes.c_char*4)# 源币种
    ,('FromAmount',ctypes.c_double)# 源金额
    ,('FromFrozenSwap',ctypes.c_double)# 源换汇冻结金额(可用冻结)
    ,('FromRemainSwap',ctypes.c_double)# 源剩余换汇额度(可提冻结)
    ,('ToCurrencyID',ctypes.c_char*4)# 目标币种
    ,('ToAmount',ctypes.c_double)# 目标金额
]

  def __init__(self,DelaySwapSeqNo= '',BrokerID='',InvestorID='',FromCurrencyID='',FromAmount=0.0,FromFrozenSwap=0.0,FromRemainSwap=0.0,ToCurrencyID='',ToAmount=0.0):

    super(SyncDelaySwapField,self).__init__()

    self.DelaySwapSeqNo=self._to_bytes(DelaySwapSeqNo)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.FromCurrencyID=self._to_bytes(FromCurrencyID)
    self.FromAmount=float(FromAmount)
    self.FromFrozenSwap=float(FromFrozenSwap)
    self.FromRemainSwap=float(FromRemainSwap)
    self.ToCurrencyID=self._to_bytes(ToCurrencyID)
    self.ToAmount=float(ToAmount)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.DelaySwapSeqNo=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.FromCurrencyID=self._to_bytes(i_tuple[4])
    self.FromAmount=float(i_tuple[5])
    self.FromFrozenSwap=float(i_tuple[6])
    self.FromRemainSwap=float(i_tuple[7])
    self.ToCurrencyID=self._to_bytes(i_tuple[8])
    self.ToAmount=float(i_tuple[9])

class QrySyncDelaySwapField(Base):
  """查询延时换汇同步"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('DelaySwapSeqNo',ctypes.c_char*15)# 延时换汇流水号
]

  def __init__(self,BrokerID= '',DelaySwapSeqNo=''):

    super(QrySyncDelaySwapField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.DelaySwapSeqNo=self._to_bytes(DelaySwapSeqNo)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.DelaySwapSeqNo=self._to_bytes(i_tuple[2])

class InvestUnitField(Base):
  """投资单元"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('InvestorUnitName',ctypes.c_char*81)# 投资者单元名称
    ,('InvestorGroupID',ctypes.c_char*13)# 投资者分组代码
    ,('CommModelID',ctypes.c_char*13)# 手续费率模板代码
    ,('MarginModelID',ctypes.c_char*13)# 保证金率模板代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',InvestorID='',InvestUnitID='',InvestorUnitName='',InvestorGroupID='',CommModelID='',MarginModelID='',AccountID='',CurrencyID=''):

    super(InvestUnitField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.InvestorUnitName=self._to_bytes(InvestorUnitName)
    self.InvestorGroupID=self._to_bytes(InvestorGroupID)
    self.CommModelID=self._to_bytes(CommModelID)
    self.MarginModelID=self._to_bytes(MarginModelID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InvestUnitID=self._to_bytes(i_tuple[3])
    self.InvestorUnitName=self._to_bytes(i_tuple[4])
    self.InvestorGroupID=self._to_bytes(i_tuple[5])
    self.CommModelID=self._to_bytes(i_tuple[6])
    self.MarginModelID=self._to_bytes(i_tuple[7])
    self.AccountID=self._to_bytes(i_tuple[8])
    self.CurrencyID=self._to_bytes(i_tuple[9])

class QryInvestUnitField(Base):
  """查询投资单元"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InvestUnitID=''):

    super(QryInvestUnitField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InvestUnitID=self._to_bytes(i_tuple[3])

class SecAgentCheckModeField(Base):
  """二级代理商资金校验模式"""
  _fields_ = [
    ('InvestorID',ctypes.c_char*13)# ///投资者代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('CurrencyID',ctypes.c_char*4)# 币种
    ,('BrokerSecAgentID',ctypes.c_char*13)# 境外中介机构资金帐号
    ,('CheckSelfAccount',ctypes.c_int)# 是否需要校验自己的资金账户
]

  def __init__(self,InvestorID= '',BrokerID='',CurrencyID='',BrokerSecAgentID='',CheckSelfAccount=0):

    super(SecAgentCheckModeField,self).__init__()

    self.InvestorID=self._to_bytes(InvestorID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.BrokerSecAgentID=self._to_bytes(BrokerSecAgentID)
    self.CheckSelfAccount=int(CheckSelfAccount)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InvestorID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.CurrencyID=self._to_bytes(i_tuple[3])
    self.BrokerSecAgentID=self._to_bytes(i_tuple[4])
    self.CheckSelfAccount=int(i_tuple[5])

class MarketDataField(Base):
  """市场行情"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('LastPrice',ctypes.c_double)# 最新价
    ,('PreSettlementPrice',ctypes.c_double)# 上次结算价
    ,('PreClosePrice',ctypes.c_double)# 昨收盘
    ,('PreOpenInterest',ctypes.c_double)# 昨持仓量
    ,('OpenPrice',ctypes.c_double)# 今开盘
    ,('HighestPrice',ctypes.c_double)# 最高价
    ,('LowestPrice',ctypes.c_double)# 最低价
    ,('Volume',ctypes.c_int)# 数量
    ,('Turnover',ctypes.c_double)# 成交金额
    ,('OpenInterest',ctypes.c_double)# 持仓量
    ,('ClosePrice',ctypes.c_double)# 今收盘
    ,('SettlementPrice',ctypes.c_double)# 本次结算价
    ,('UpperLimitPrice',ctypes.c_double)# 涨停板价
    ,('LowerLimitPrice',ctypes.c_double)# 跌停板价
    ,('PreDelta',ctypes.c_double)# 昨虚实度
    ,('CurrDelta',ctypes.c_double)# 今虚实度
    ,('UpdateTime',ctypes.c_char*9)# 最后修改时间
    ,('UpdateMillisec',ctypes.c_int)# 最后修改毫秒
    ,('ActionDay',ctypes.c_char*9)# 业务日期
]

  def __init__(self,TradingDay= '',InstrumentID='',ExchangeID='',ExchangeInstID='',LastPrice=0.0,PreSettlementPrice=0.0,PreClosePrice=0.0,PreOpenInterest=0.0,OpenPrice=0.0,HighestPrice=0.0,LowestPrice=0.0,Volume=0,Turnover=0.0,OpenInterest=0.0,ClosePrice=0.0,SettlementPrice=0.0,UpperLimitPrice=0.0,LowerLimitPrice=0.0,PreDelta=0.0,CurrDelta=0.0,UpdateTime='',UpdateMillisec=0,ActionDay=''):

    super(MarketDataField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.LastPrice=float(LastPrice)
    self.PreSettlementPrice=float(PreSettlementPrice)
    self.PreClosePrice=float(PreClosePrice)
    self.PreOpenInterest=float(PreOpenInterest)
    self.OpenPrice=float(OpenPrice)
    self.HighestPrice=float(HighestPrice)
    self.LowestPrice=float(LowestPrice)
    self.Volume=int(Volume)
    self.Turnover=float(Turnover)
    self.OpenInterest=float(OpenInterest)
    self.ClosePrice=float(ClosePrice)
    self.SettlementPrice=float(SettlementPrice)
    self.UpperLimitPrice=float(UpperLimitPrice)
    self.LowerLimitPrice=float(LowerLimitPrice)
    self.PreDelta=float(PreDelta)
    self.CurrDelta=float(CurrDelta)
    self.UpdateTime=self._to_bytes(UpdateTime)
    self.UpdateMillisec=int(UpdateMillisec)
    self.ActionDay=self._to_bytes(ActionDay)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.InstrumentID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.ExchangeInstID=self._to_bytes(i_tuple[4])
    self.LastPrice=float(i_tuple[5])
    self.PreSettlementPrice=float(i_tuple[6])
    self.PreClosePrice=float(i_tuple[7])
    self.PreOpenInterest=float(i_tuple[8])
    self.OpenPrice=float(i_tuple[9])
    self.HighestPrice=float(i_tuple[10])
    self.LowestPrice=float(i_tuple[11])
    self.Volume=int(i_tuple[12])
    self.Turnover=float(i_tuple[13])
    self.OpenInterest=float(i_tuple[14])
    self.ClosePrice=float(i_tuple[15])
    self.SettlementPrice=float(i_tuple[16])
    self.UpperLimitPrice=float(i_tuple[17])
    self.LowerLimitPrice=float(i_tuple[18])
    self.PreDelta=float(i_tuple[19])
    self.CurrDelta=float(i_tuple[20])
    self.UpdateTime=self._to_bytes(i_tuple[21])
    self.UpdateMillisec=int(i_tuple[22])
    self.ActionDay=self._to_bytes(i_tuple[23])

class MarketDataBaseField(Base):
  """行情基础属性"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('PreSettlementPrice',ctypes.c_double)# 上次结算价
    ,('PreClosePrice',ctypes.c_double)# 昨收盘
    ,('PreOpenInterest',ctypes.c_double)# 昨持仓量
    ,('PreDelta',ctypes.c_double)# 昨虚实度
]

  def __init__(self,TradingDay= '',PreSettlementPrice=0.0,PreClosePrice=0.0,PreOpenInterest=0.0,PreDelta=0.0):

    super(MarketDataBaseField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.PreSettlementPrice=float(PreSettlementPrice)
    self.PreClosePrice=float(PreClosePrice)
    self.PreOpenInterest=float(PreOpenInterest)
    self.PreDelta=float(PreDelta)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.PreSettlementPrice=float(i_tuple[2])
    self.PreClosePrice=float(i_tuple[3])
    self.PreOpenInterest=float(i_tuple[4])
    self.PreDelta=float(i_tuple[5])

class MarketDataStaticField(Base):
  """行情静态属性"""
  _fields_ = [
    ('OpenPrice',ctypes.c_double)# ///今开盘
    ,('HighestPrice',ctypes.c_double)# 最高价
    ,('LowestPrice',ctypes.c_double)# 最低价
    ,('ClosePrice',ctypes.c_double)# 今收盘
    ,('UpperLimitPrice',ctypes.c_double)# 涨停板价
    ,('LowerLimitPrice',ctypes.c_double)# 跌停板价
    ,('SettlementPrice',ctypes.c_double)# 本次结算价
    ,('CurrDelta',ctypes.c_double)# 今虚实度
]

  def __init__(self,OpenPrice= 0.0,HighestPrice=0.0,LowestPrice=0.0,ClosePrice=0.0,UpperLimitPrice=0.0,LowerLimitPrice=0.0,SettlementPrice=0.0,CurrDelta=0.0):

    super(MarketDataStaticField,self).__init__()

    self.OpenPrice=float(OpenPrice)
    self.HighestPrice=float(HighestPrice)
    self.LowestPrice=float(LowestPrice)
    self.ClosePrice=float(ClosePrice)
    self.UpperLimitPrice=float(UpperLimitPrice)
    self.LowerLimitPrice=float(LowerLimitPrice)
    self.SettlementPrice=float(SettlementPrice)
    self.CurrDelta=float(CurrDelta)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.OpenPrice=float(i_tuple[1])
    self.HighestPrice=float(i_tuple[2])
    self.LowestPrice=float(i_tuple[3])
    self.ClosePrice=float(i_tuple[4])
    self.UpperLimitPrice=float(i_tuple[5])
    self.LowerLimitPrice=float(i_tuple[6])
    self.SettlementPrice=float(i_tuple[7])
    self.CurrDelta=float(i_tuple[8])

class MarketDataLastMatchField(Base):
  """行情最新成交属性"""
  _fields_ = [
    ('LastPrice',ctypes.c_double)# ///最新价
    ,('Volume',ctypes.c_int)# 数量
    ,('Turnover',ctypes.c_double)# 成交金额
    ,('OpenInterest',ctypes.c_double)# 持仓量
]

  def __init__(self,LastPrice= 0.0,Volume=0,Turnover=0.0,OpenInterest=0.0):

    super(MarketDataLastMatchField,self).__init__()

    self.LastPrice=float(LastPrice)
    self.Volume=int(Volume)
    self.Turnover=float(Turnover)
    self.OpenInterest=float(OpenInterest)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.LastPrice=float(i_tuple[1])
    self.Volume=int(i_tuple[2])
    self.Turnover=float(i_tuple[3])
    self.OpenInterest=float(i_tuple[4])

class MarketDataBestPriceField(Base):
  """行情最优价属性"""
  _fields_ = [
    ('BidPrice1',ctypes.c_double)# ///申买价一
    ,('BidVolume1',ctypes.c_int)# 申买量一
    ,('AskPrice1',ctypes.c_double)# 申卖价一
    ,('AskVolume1',ctypes.c_int)# 申卖量一
]

  def __init__(self,BidPrice1= 0.0,BidVolume1=0,AskPrice1=0.0,AskVolume1=0):

    super(MarketDataBestPriceField,self).__init__()

    self.BidPrice1=float(BidPrice1)
    self.BidVolume1=int(BidVolume1)
    self.AskPrice1=float(AskPrice1)
    self.AskVolume1=int(AskVolume1)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BidPrice1=float(i_tuple[1])
    self.BidVolume1=int(i_tuple[2])
    self.AskPrice1=float(i_tuple[3])
    self.AskVolume1=int(i_tuple[4])

class MarketDataBid23Field(Base):
  """行情申买二、三属性"""
  _fields_ = [
    ('BidPrice2',ctypes.c_double)# ///申买价二
    ,('BidVolume2',ctypes.c_int)# 申买量二
    ,('BidPrice3',ctypes.c_double)# 申买价三
    ,('BidVolume3',ctypes.c_int)# 申买量三
]

  def __init__(self,BidPrice2= 0.0,BidVolume2=0,BidPrice3=0.0,BidVolume3=0):

    super(MarketDataBid23Field,self).__init__()

    self.BidPrice2=float(BidPrice2)
    self.BidVolume2=int(BidVolume2)
    self.BidPrice3=float(BidPrice3)
    self.BidVolume3=int(BidVolume3)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BidPrice2=float(i_tuple[1])
    self.BidVolume2=int(i_tuple[2])
    self.BidPrice3=float(i_tuple[3])
    self.BidVolume3=int(i_tuple[4])

class MarketDataAsk23Field(Base):
  """行情申卖二、三属性"""
  _fields_ = [
    ('AskPrice2',ctypes.c_double)# ///申卖价二
    ,('AskVolume2',ctypes.c_int)# 申卖量二
    ,('AskPrice3',ctypes.c_double)# 申卖价三
    ,('AskVolume3',ctypes.c_int)# 申卖量三
]

  def __init__(self,AskPrice2= 0.0,AskVolume2=0,AskPrice3=0.0,AskVolume3=0):

    super(MarketDataAsk23Field,self).__init__()

    self.AskPrice2=float(AskPrice2)
    self.AskVolume2=int(AskVolume2)
    self.AskPrice3=float(AskPrice3)
    self.AskVolume3=int(AskVolume3)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.AskPrice2=float(i_tuple[1])
    self.AskVolume2=int(i_tuple[2])
    self.AskPrice3=float(i_tuple[3])
    self.AskVolume3=int(i_tuple[4])

class MarketDataBid45Field(Base):
  """行情申买四、五属性"""
  _fields_ = [
    ('BidPrice4',ctypes.c_double)# ///申买价四
    ,('BidVolume4',ctypes.c_int)# 申买量四
    ,('BidPrice5',ctypes.c_double)# 申买价五
    ,('BidVolume5',ctypes.c_int)# 申买量五
]

  def __init__(self,BidPrice4= 0.0,BidVolume4=0,BidPrice5=0.0,BidVolume5=0):

    super(MarketDataBid45Field,self).__init__()

    self.BidPrice4=float(BidPrice4)
    self.BidVolume4=int(BidVolume4)
    self.BidPrice5=float(BidPrice5)
    self.BidVolume5=int(BidVolume5)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BidPrice4=float(i_tuple[1])
    self.BidVolume4=int(i_tuple[2])
    self.BidPrice5=float(i_tuple[3])
    self.BidVolume5=int(i_tuple[4])

class MarketDataAsk45Field(Base):
  """行情申卖四、五属性"""
  _fields_ = [
    ('AskPrice4',ctypes.c_double)# ///申卖价四
    ,('AskVolume4',ctypes.c_int)# 申卖量四
    ,('AskPrice5',ctypes.c_double)# 申卖价五
    ,('AskVolume5',ctypes.c_int)# 申卖量五
]

  def __init__(self,AskPrice4= 0.0,AskVolume4=0,AskPrice5=0.0,AskVolume5=0):

    super(MarketDataAsk45Field,self).__init__()

    self.AskPrice4=float(AskPrice4)
    self.AskVolume4=int(AskVolume4)
    self.AskPrice5=float(AskPrice5)
    self.AskVolume5=int(AskVolume5)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.AskPrice4=float(i_tuple[1])
    self.AskVolume4=int(i_tuple[2])
    self.AskPrice5=float(i_tuple[3])
    self.AskVolume5=int(i_tuple[4])

class MarketDataUpdateTimeField(Base):
  """行情更新时间属性"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('UpdateTime',ctypes.c_char*9)# 最后修改时间
    ,('UpdateMillisec',ctypes.c_int)# 最后修改毫秒
    ,('ActionDay',ctypes.c_char*9)# 业务日期
]

  def __init__(self,InstrumentID= '',UpdateTime='',UpdateMillisec=0,ActionDay=''):

    super(MarketDataUpdateTimeField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.UpdateTime=self._to_bytes(UpdateTime)
    self.UpdateMillisec=int(UpdateMillisec)
    self.ActionDay=self._to_bytes(ActionDay)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.UpdateTime=self._to_bytes(i_tuple[2])
    self.UpdateMillisec=int(i_tuple[3])
    self.ActionDay=self._to_bytes(i_tuple[4])

class MarketDataExchangeField(Base):
  """行情交易所代码属性"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
]

  def __init__(self,ExchangeID= ''):

    super(MarketDataExchangeField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])

class SpecificInstrumentField(Base):
  """指定的合约"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
]

  def __init__(self,InstrumentID= ''):

    super(SpecificInstrumentField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])

class InstrumentStatusField(Base):
  """合约状态"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('SettlementGroupID',ctypes.c_char*9)# 结算组代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InstrumentStatus',ctypes.c_char)# 合约交易状态
    ,('TradingSegmentSN',ctypes.c_int)# 交易阶段编号
    ,('EnterTime',ctypes.c_char*9)# 进入本状态时间
    ,('EnterReason',ctypes.c_char)# 进入本状态原因
]

  def __init__(self,ExchangeID= '',ExchangeInstID='',SettlementGroupID='',InstrumentID='',InstrumentStatus='',TradingSegmentSN=0,EnterTime='',EnterReason=''):

    super(InstrumentStatusField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.SettlementGroupID=self._to_bytes(SettlementGroupID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InstrumentStatus=self._to_bytes(InstrumentStatus)
    self.TradingSegmentSN=int(TradingSegmentSN)
    self.EnterTime=self._to_bytes(EnterTime)
    self.EnterReason=self._to_bytes(EnterReason)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ExchangeInstID=self._to_bytes(i_tuple[2])
    self.SettlementGroupID=self._to_bytes(i_tuple[3])
    self.InstrumentID=self._to_bytes(i_tuple[4])
    self.InstrumentStatus=self._to_bytes(i_tuple[5])
    self.TradingSegmentSN=int(i_tuple[6])
    self.EnterTime=self._to_bytes(i_tuple[7])
    self.EnterReason=self._to_bytes(i_tuple[8])

class QryInstrumentStatusField(Base):
  """查询合约状态"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
]

  def __init__(self,ExchangeID= '',ExchangeInstID=''):

    super(QryInstrumentStatusField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ExchangeInstID=self._to_bytes(i_tuple[2])

class InvestorAccountField(Base):
  """投资者账户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',InvestorID='',AccountID='',CurrencyID=''):

    super(InvestorAccountField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.AccountID=self._to_bytes(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])

class PositionProfitAlgorithmField(Base):
  """浮动盈亏算法"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Algorithm',ctypes.c_char)# 盈亏算法
    ,('Memo',ctypes.c_char*161)# 备注
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',Algorithm='',Memo='',CurrencyID=''):

    super(PositionProfitAlgorithmField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.Algorithm=self._to_bytes(Algorithm)
    self.Memo=self._to_bytes(Memo)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.Algorithm=self._to_bytes(i_tuple[3])
    self.Memo=self._to_bytes(i_tuple[4])
    self.CurrencyID=self._to_bytes(i_tuple[5])

class DiscountField(Base):
  """会员资金折扣"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Discount',ctypes.c_double)# 资金折扣比例
]

  def __init__(self,BrokerID= '',InvestorRange='',InvestorID='',Discount=0.0):

    super(DiscountField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Discount=float(Discount)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.Discount=float(i_tuple[4])

class QryTransferBankField(Base):
  """查询转帐银行"""
  _fields_ = [
    ('BankID',ctypes.c_char*4)# ///银行代码
    ,('BankBrchID',ctypes.c_char*5)# 银行分中心代码
]

  def __init__(self,BankID= '',BankBrchID=''):

    super(QryTransferBankField,self).__init__()

    self.BankID=self._to_bytes(BankID)
    self.BankBrchID=self._to_bytes(BankBrchID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BankID=self._to_bytes(i_tuple[1])
    self.BankBrchID=self._to_bytes(i_tuple[2])

class TransferBankField(Base):
  """转帐银行"""
  _fields_ = [
    ('BankID',ctypes.c_char*4)# ///银行代码
    ,('BankBrchID',ctypes.c_char*5)# 银行分中心代码
    ,('BankName',ctypes.c_char*101)# 银行名称
    ,('IsActive',ctypes.c_int)# 是否活跃
]

  def __init__(self,BankID= '',BankBrchID='',BankName='',IsActive=0):

    super(TransferBankField,self).__init__()

    self.BankID=self._to_bytes(BankID)
    self.BankBrchID=self._to_bytes(BankBrchID)
    self.BankName=self._to_bytes(BankName)
    self.IsActive=int(IsActive)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BankID=self._to_bytes(i_tuple[1])
    self.BankBrchID=self._to_bytes(i_tuple[2])
    self.BankName=self._to_bytes(i_tuple[3])
    self.IsActive=int(i_tuple[4])

class QryInvestorPositionDetailField(Base):
  """查询投资者持仓明细"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryInvestorPositionDetailField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class InvestorPositionDetailField(Base):
  """投资者持仓明细"""
  _fields_ = [
    ('InstrumentID',ctypes.c_char*31)# ///合约代码
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('Direction',ctypes.c_char)# 买卖
    ,('OpenDate',ctypes.c_char*9)# 开仓日期
    ,('TradeID',ctypes.c_char*21)# 成交编号
    ,('Volume',ctypes.c_int)# 数量
    ,('OpenPrice',ctypes.c_double)# 开仓价
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('TradeType',ctypes.c_char)# 成交类型
    ,('CombInstrumentID',ctypes.c_char*31)# 组合合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('CloseProfitByDate',ctypes.c_double)# 逐日盯市平仓盈亏
    ,('CloseProfitByTrade',ctypes.c_double)# 逐笔对冲平仓盈亏
    ,('PositionProfitByDate',ctypes.c_double)# 逐日盯市持仓盈亏
    ,('PositionProfitByTrade',ctypes.c_double)# 逐笔对冲持仓盈亏
    ,('Margin',ctypes.c_double)# 投资者保证金
    ,('ExchMargin',ctypes.c_double)# 交易所保证金
    ,('MarginRateByMoney',ctypes.c_double)# 保证金率
    ,('MarginRateByVolume',ctypes.c_double)# 保证金率(按手数)
    ,('LastSettlementPrice',ctypes.c_double)# 昨结算价
    ,('SettlementPrice',ctypes.c_double)# 结算价
    ,('CloseVolume',ctypes.c_int)# 平仓量
    ,('CloseAmount',ctypes.c_double)# 平仓金额
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,InstrumentID= '',BrokerID='',InvestorID='',HedgeFlag='',Direction='',OpenDate='',TradeID='',Volume=0,OpenPrice=0.0,TradingDay='',SettlementID=0,TradeType='',CombInstrumentID='',ExchangeID='',CloseProfitByDate=0.0,CloseProfitByTrade=0.0,PositionProfitByDate=0.0,PositionProfitByTrade=0.0,Margin=0.0,ExchMargin=0.0,MarginRateByMoney=0.0,MarginRateByVolume=0.0,LastSettlementPrice=0.0,SettlementPrice=0.0,CloseVolume=0,CloseAmount=0.0,InvestUnitID=''):

    super(InvestorPositionDetailField,self).__init__()

    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.Direction=self._to_bytes(Direction)
    self.OpenDate=self._to_bytes(OpenDate)
    self.TradeID=self._to_bytes(TradeID)
    self.Volume=int(Volume)
    self.OpenPrice=float(OpenPrice)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.TradeType=self._to_bytes(TradeType)
    self.CombInstrumentID=self._to_bytes(CombInstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.CloseProfitByDate=float(CloseProfitByDate)
    self.CloseProfitByTrade=float(CloseProfitByTrade)
    self.PositionProfitByDate=float(PositionProfitByDate)
    self.PositionProfitByTrade=float(PositionProfitByTrade)
    self.Margin=float(Margin)
    self.ExchMargin=float(ExchMargin)
    self.MarginRateByMoney=float(MarginRateByMoney)
    self.MarginRateByVolume=float(MarginRateByVolume)
    self.LastSettlementPrice=float(LastSettlementPrice)
    self.SettlementPrice=float(SettlementPrice)
    self.CloseVolume=int(CloseVolume)
    self.CloseAmount=float(CloseAmount)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.InstrumentID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.Direction=self._to_bytes(i_tuple[5])
    self.OpenDate=self._to_bytes(i_tuple[6])
    self.TradeID=self._to_bytes(i_tuple[7])
    self.Volume=int(i_tuple[8])
    self.OpenPrice=float(i_tuple[9])
    self.TradingDay=self._to_bytes(i_tuple[10])
    self.SettlementID=int(i_tuple[11])
    self.TradeType=self._to_bytes(i_tuple[12])
    self.CombInstrumentID=self._to_bytes(i_tuple[13])
    self.ExchangeID=self._to_bytes(i_tuple[14])
    self.CloseProfitByDate=float(i_tuple[15])
    self.CloseProfitByTrade=float(i_tuple[16])
    self.PositionProfitByDate=float(i_tuple[17])
    self.PositionProfitByTrade=float(i_tuple[18])
    self.Margin=float(i_tuple[19])
    self.ExchMargin=float(i_tuple[20])
    self.MarginRateByMoney=float(i_tuple[21])
    self.MarginRateByVolume=float(i_tuple[22])
    self.LastSettlementPrice=float(i_tuple[23])
    self.SettlementPrice=float(i_tuple[24])
    self.CloseVolume=int(i_tuple[25])
    self.CloseAmount=float(i_tuple[26])
    self.InvestUnitID=self._to_bytes(i_tuple[27])

class TradingAccountPasswordField(Base):
  """资金账户口令域"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 密码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',Password='',CurrencyID=''):

    super(TradingAccountPasswordField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.Password=self._to_bytes(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])

class MDTraderOfferField(Base):
  """交易所行情报盘机"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('Password',ctypes.c_char*41)# 密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('TraderConnectStatus',ctypes.c_char)# 交易所交易员连接状态
    ,('ConnectRequestDate',ctypes.c_char*9)# 发出连接请求的日期
    ,('ConnectRequestTime',ctypes.c_char*9)# 发出连接请求的时间
    ,('LastReportDate',ctypes.c_char*9)# 上次报告日期
    ,('LastReportTime',ctypes.c_char*9)# 上次报告时间
    ,('ConnectDate',ctypes.c_char*9)# 完成连接日期
    ,('ConnectTime',ctypes.c_char*9)# 完成连接时间
    ,('StartDate',ctypes.c_char*9)# 启动日期
    ,('StartTime',ctypes.c_char*9)# 启动时间
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('MaxTradeID',ctypes.c_char*21)# 本席位最大成交编号
    ,('MaxOrderMessageReference',ctypes.c_char*7)# 本席位最大报单备拷
]

  def __init__(self,ExchangeID= '',TraderID='',ParticipantID='',Password='',InstallID=0,OrderLocalID='',TraderConnectStatus='',ConnectRequestDate='',ConnectRequestTime='',LastReportDate='',LastReportTime='',ConnectDate='',ConnectTime='',StartDate='',StartTime='',TradingDay='',BrokerID='',MaxTradeID='',MaxOrderMessageReference=''):

    super(MDTraderOfferField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TraderID=self._to_bytes(TraderID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.TraderConnectStatus=self._to_bytes(TraderConnectStatus)
    self.ConnectRequestDate=self._to_bytes(ConnectRequestDate)
    self.ConnectRequestTime=self._to_bytes(ConnectRequestTime)
    self.LastReportDate=self._to_bytes(LastReportDate)
    self.LastReportTime=self._to_bytes(LastReportTime)
    self.ConnectDate=self._to_bytes(ConnectDate)
    self.ConnectTime=self._to_bytes(ConnectTime)
    self.StartDate=self._to_bytes(StartDate)
    self.StartTime=self._to_bytes(StartTime)
    self.TradingDay=self._to_bytes(TradingDay)
    self.BrokerID=self._to_bytes(BrokerID)
    self.MaxTradeID=self._to_bytes(MaxTradeID)
    self.MaxOrderMessageReference=self._to_bytes(MaxOrderMessageReference)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.TraderID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])
    self.Password=self._to_bytes(i_tuple[4])
    self.InstallID=int(i_tuple[5])
    self.OrderLocalID=self._to_bytes(i_tuple[6])
    self.TraderConnectStatus=self._to_bytes(i_tuple[7])
    self.ConnectRequestDate=self._to_bytes(i_tuple[8])
    self.ConnectRequestTime=self._to_bytes(i_tuple[9])
    self.LastReportDate=self._to_bytes(i_tuple[10])
    self.LastReportTime=self._to_bytes(i_tuple[11])
    self.ConnectDate=self._to_bytes(i_tuple[12])
    self.ConnectTime=self._to_bytes(i_tuple[13])
    self.StartDate=self._to_bytes(i_tuple[14])
    self.StartTime=self._to_bytes(i_tuple[15])
    self.TradingDay=self._to_bytes(i_tuple[16])
    self.BrokerID=self._to_bytes(i_tuple[17])
    self.MaxTradeID=self._to_bytes(i_tuple[18])
    self.MaxOrderMessageReference=self._to_bytes(i_tuple[19])

class QryMDTraderOfferField(Base):
  """查询行情报盘机"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
]

  def __init__(self,ExchangeID= '',ParticipantID='',TraderID=''):

    super(QryMDTraderOfferField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.TraderID=self._to_bytes(TraderID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.TraderID=self._to_bytes(i_tuple[3])

class QryNoticeField(Base):
  """查询客户通知"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
]

  def __init__(self,BrokerID= ''):

    super(QryNoticeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])

class NoticeField(Base):
  """客户通知"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('Content',ctypes.c_char*501)# 消息正文
    ,('SequenceLabel',ctypes.c_char*2)# 经纪公司通知内容序列号
]

  def __init__(self,BrokerID= '',Content='',SequenceLabel=''):

    super(NoticeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.Content=self._to_bytes(Content)
    self.SequenceLabel=self._to_bytes(SequenceLabel)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.Content=self._to_bytes(i_tuple[2])
    self.SequenceLabel=self._to_bytes(i_tuple[3])

class UserRightField(Base):
  """用户权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserRightType',ctypes.c_char)# 客户权限类型
    ,('IsForbidden',ctypes.c_int)# 是否禁止
]

  def __init__(self,BrokerID= '',UserID='',UserRightType='',IsForbidden=0):

    super(UserRightField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserRightType=self._to_bytes(UserRightType)
    self.IsForbidden=int(IsForbidden)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserRightType=self._to_bytes(i_tuple[3])
    self.IsForbidden=int(i_tuple[4])

class QrySettlementInfoConfirmField(Base):
  """查询结算信息确认域"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',InvestorID='',AccountID='',CurrencyID=''):

    super(QrySettlementInfoConfirmField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.AccountID=self._to_bytes(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])

class LoadSettlementInfoField(Base):
  """装载结算信息"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
]

  def __init__(self,BrokerID= ''):

    super(LoadSettlementInfoField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])

class BrokerWithdrawAlgorithmField(Base):
  """经纪公司可提资金算法表"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('WithdrawAlgorithm',ctypes.c_char)# 可提资金算法
    ,('UsingRatio',ctypes.c_double)# 资金使用率
    ,('IncludeCloseProfit',ctypes.c_char)# 可提是否包含平仓盈利
    ,('AllWithoutTrade',ctypes.c_char)# 本日无仓且无成交客户是否受可提比例限制
    ,('AvailIncludeCloseProfit',ctypes.c_char)# 可用是否包含平仓盈利
    ,('IsBrokerUserEvent',ctypes.c_int)# 是否启用用户事件
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('FundMortgageRatio',ctypes.c_double)# 货币质押比率
    ,('BalanceAlgorithm',ctypes.c_char)# 权益算法
]

  def __init__(self,BrokerID= '',WithdrawAlgorithm='',UsingRatio=0.0,IncludeCloseProfit='',AllWithoutTrade='',AvailIncludeCloseProfit='',IsBrokerUserEvent=0,CurrencyID='',FundMortgageRatio=0.0,BalanceAlgorithm=''):

    super(BrokerWithdrawAlgorithmField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.WithdrawAlgorithm=self._to_bytes(WithdrawAlgorithm)
    self.UsingRatio=float(UsingRatio)
    self.IncludeCloseProfit=self._to_bytes(IncludeCloseProfit)
    self.AllWithoutTrade=self._to_bytes(AllWithoutTrade)
    self.AvailIncludeCloseProfit=self._to_bytes(AvailIncludeCloseProfit)
    self.IsBrokerUserEvent=int(IsBrokerUserEvent)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.FundMortgageRatio=float(FundMortgageRatio)
    self.BalanceAlgorithm=self._to_bytes(BalanceAlgorithm)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.WithdrawAlgorithm=self._to_bytes(i_tuple[2])
    self.UsingRatio=float(i_tuple[3])
    self.IncludeCloseProfit=self._to_bytes(i_tuple[4])
    self.AllWithoutTrade=self._to_bytes(i_tuple[5])
    self.AvailIncludeCloseProfit=self._to_bytes(i_tuple[6])
    self.IsBrokerUserEvent=int(i_tuple[7])
    self.CurrencyID=self._to_bytes(i_tuple[8])
    self.FundMortgageRatio=float(i_tuple[9])
    self.BalanceAlgorithm=self._to_bytes(i_tuple[10])

class TradingAccountPasswordUpdateV1Field(Base):
  """资金账户口令变更域"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OldPassword',ctypes.c_char*41)# 原来的口令
    ,('NewPassword',ctypes.c_char*41)# 新的口令
]

  def __init__(self,BrokerID= '',InvestorID='',OldPassword='',NewPassword=''):

    super(TradingAccountPasswordUpdateV1Field,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OldPassword=self._to_bytes(OldPassword)
    self.NewPassword=self._to_bytes(NewPassword)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OldPassword=self._to_bytes(i_tuple[3])
    self.NewPassword=self._to_bytes(i_tuple[4])

class TradingAccountPasswordUpdateField(Base):
  """资金账户口令变更域"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('OldPassword',ctypes.c_char*41)# 原来的口令
    ,('NewPassword',ctypes.c_char*41)# 新的口令
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',OldPassword='',NewPassword='',CurrencyID=''):

    super(TradingAccountPasswordUpdateField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.OldPassword=self._to_bytes(OldPassword)
    self.NewPassword=self._to_bytes(NewPassword)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.OldPassword=self._to_bytes(i_tuple[3])
    self.NewPassword=self._to_bytes(i_tuple[4])
    self.CurrencyID=self._to_bytes(i_tuple[5])

class QryCombinationLegField(Base):
  """查询组合合约分腿"""
  _fields_ = [
    ('CombInstrumentID',ctypes.c_char*31)# ///组合合约代码
    ,('LegID',ctypes.c_int)# 单腿编号
    ,('LegInstrumentID',ctypes.c_char*31)# 单腿合约代码
]

  def __init__(self,CombInstrumentID= '',LegID=0,LegInstrumentID=''):

    super(QryCombinationLegField,self).__init__()

    self.CombInstrumentID=self._to_bytes(CombInstrumentID)
    self.LegID=int(LegID)
    self.LegInstrumentID=self._to_bytes(LegInstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.CombInstrumentID=self._to_bytes(i_tuple[1])
    self.LegID=int(i_tuple[2])
    self.LegInstrumentID=self._to_bytes(i_tuple[3])

class QrySyncStatusField(Base):
  """查询组合合约分腿"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
]

  def __init__(self,TradingDay= ''):

    super(QrySyncStatusField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])

class CombinationLegField(Base):
  """组合交易合约的单腿"""
  _fields_ = [
    ('CombInstrumentID',ctypes.c_char*31)# ///组合合约代码
    ,('LegID',ctypes.c_int)# 单腿编号
    ,('LegInstrumentID',ctypes.c_char*31)# 单腿合约代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('LegMultiple',ctypes.c_int)# 单腿乘数
    ,('ImplyLevel',ctypes.c_int)# 派生层数
]

  def __init__(self,CombInstrumentID= '',LegID=0,LegInstrumentID='',Direction='',LegMultiple=0,ImplyLevel=0):

    super(CombinationLegField,self).__init__()

    self.CombInstrumentID=self._to_bytes(CombInstrumentID)
    self.LegID=int(LegID)
    self.LegInstrumentID=self._to_bytes(LegInstrumentID)
    self.Direction=self._to_bytes(Direction)
    self.LegMultiple=int(LegMultiple)
    self.ImplyLevel=int(ImplyLevel)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.CombInstrumentID=self._to_bytes(i_tuple[1])
    self.LegID=int(i_tuple[2])
    self.LegInstrumentID=self._to_bytes(i_tuple[3])
    self.Direction=self._to_bytes(i_tuple[4])
    self.LegMultiple=int(i_tuple[5])
    self.ImplyLevel=int(i_tuple[6])

class SyncStatusField(Base):
  """数据同步状态"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('DataSyncStatus',ctypes.c_char)# 数据同步状态
]

  def __init__(self,TradingDay= '',DataSyncStatus=''):

    super(SyncStatusField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.DataSyncStatus=self._to_bytes(DataSyncStatus)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.DataSyncStatus=self._to_bytes(i_tuple[2])

class QryLinkManField(Base):
  """查询联系人"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryLinkManField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class LinkManField(Base):
  """联系人"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('PersonType',ctypes.c_char)# 联系人类型
    ,('IdentifiedCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('PersonName',ctypes.c_char*81)# 名称
    ,('Telephone',ctypes.c_char*41)# 联系电话
    ,('Address',ctypes.c_char*101)# 通讯地址
    ,('ZipCode',ctypes.c_char*7)# 邮政编码
    ,('Priority',ctypes.c_int)# 优先级
    ,('UOAZipCode',ctypes.c_char*11)# 开户邮政编码
    ,('PersonFullName',ctypes.c_char*101)# 全称
]

  def __init__(self,BrokerID= '',InvestorID='',PersonType='',IdentifiedCardType='',IdentifiedCardNo='',PersonName='',Telephone='',Address='',ZipCode='',Priority=0,UOAZipCode='',PersonFullName=''):

    super(LinkManField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.PersonType=self._to_bytes(PersonType)
    self.IdentifiedCardType=self._to_bytes(IdentifiedCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.PersonName=self._to_bytes(PersonName)
    self.Telephone=self._to_bytes(Telephone)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Priority=int(Priority)
    self.UOAZipCode=self._to_bytes(UOAZipCode)
    self.PersonFullName=self._to_bytes(PersonFullName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.PersonType=self._to_bytes(i_tuple[3])
    self.IdentifiedCardType=self._to_bytes(i_tuple[4])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[5])
    self.PersonName=self._to_bytes(i_tuple[6])
    self.Telephone=self._to_bytes(i_tuple[7])
    self.Address=self._to_bytes(i_tuple[8])
    self.ZipCode=self._to_bytes(i_tuple[9])
    self.Priority=int(i_tuple[10])
    self.UOAZipCode=self._to_bytes(i_tuple[11])
    self.PersonFullName=self._to_bytes(i_tuple[12])

class QryBrokerUserEventField(Base):
  """查询经纪公司用户事件"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserEventType',ctypes.c_char)# 用户事件类型
]

  def __init__(self,BrokerID= '',UserID='',UserEventType=''):

    super(QryBrokerUserEventField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserEventType=self._to_bytes(UserEventType)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserEventType=self._to_bytes(i_tuple[3])

class BrokerUserEventField(Base):
  """查询经纪公司用户事件"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('UserEventType',ctypes.c_char)# 用户事件类型
    ,('EventSequenceNo',ctypes.c_int)# 用户事件序号
    ,('EventDate',ctypes.c_char*9)# 事件发生日期
    ,('EventTime',ctypes.c_char*9)# 事件发生时间
    ,('UserEventInfo',ctypes.c_char*1025)# 用户事件信息
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',UserID='',UserEventType='',EventSequenceNo=0,EventDate='',EventTime='',UserEventInfo='',InvestorID='',InstrumentID=''):

    super(BrokerUserEventField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.UserEventType=self._to_bytes(UserEventType)
    self.EventSequenceNo=int(EventSequenceNo)
    self.EventDate=self._to_bytes(EventDate)
    self.EventTime=self._to_bytes(EventTime)
    self.UserEventInfo=self._to_bytes(UserEventInfo)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.UserEventType=self._to_bytes(i_tuple[3])
    self.EventSequenceNo=int(i_tuple[4])
    self.EventDate=self._to_bytes(i_tuple[5])
    self.EventTime=self._to_bytes(i_tuple[6])
    self.UserEventInfo=self._to_bytes(i_tuple[7])
    self.InvestorID=self._to_bytes(i_tuple[8])
    self.InstrumentID=self._to_bytes(i_tuple[9])

class QryContractBankField(Base):
  """查询签约银行请求"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBrchID',ctypes.c_char*5)# 银行分中心代码
]

  def __init__(self,BrokerID= '',BankID='',BankBrchID=''):

    super(QryContractBankField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.BankID=self._to_bytes(BankID)
    self.BankBrchID=self._to_bytes(BankBrchID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBrchID=self._to_bytes(i_tuple[3])

class ContractBankField(Base):
  """查询签约银行响应"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBrchID',ctypes.c_char*5)# 银行分中心代码
    ,('BankName',ctypes.c_char*101)# 银行名称
]

  def __init__(self,BrokerID= '',BankID='',BankBrchID='',BankName=''):

    super(ContractBankField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.BankID=self._to_bytes(BankID)
    self.BankBrchID=self._to_bytes(BankBrchID)
    self.BankName=self._to_bytes(BankName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBrchID=self._to_bytes(i_tuple[3])
    self.BankName=self._to_bytes(i_tuple[4])

class InvestorPositionCombineDetailField(Base):
  """投资者组合持仓明细"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日
    ,('OpenDate',ctypes.c_char*9)# 开仓日期
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ComTradeID',ctypes.c_char*21)# 组合编号
    ,('TradeID',ctypes.c_char*21)# 撮合编号
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('Direction',ctypes.c_char)# 买卖
    ,('TotalAmt',ctypes.c_int)# 持仓量
    ,('Margin',ctypes.c_double)# 投资者保证金
    ,('ExchMargin',ctypes.c_double)# 交易所保证金
    ,('MarginRateByMoney',ctypes.c_double)# 保证金率
    ,('MarginRateByVolume',ctypes.c_double)# 保证金率(按手数)
    ,('LegID',ctypes.c_int)# 单腿编号
    ,('LegMultiple',ctypes.c_int)# 单腿乘数
    ,('CombInstrumentID',ctypes.c_char*31)# 组合持仓合约编码
    ,('TradeGroupID',ctypes.c_int)# 成交组号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,TradingDay= '',OpenDate='',ExchangeID='',SettlementID=0,BrokerID='',InvestorID='',ComTradeID='',TradeID='',InstrumentID='',HedgeFlag='',Direction='',TotalAmt=0,Margin=0.0,ExchMargin=0.0,MarginRateByMoney=0.0,MarginRateByVolume=0.0,LegID=0,LegMultiple=0,CombInstrumentID='',TradeGroupID=0,InvestUnitID=''):

    super(InvestorPositionCombineDetailField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.OpenDate=self._to_bytes(OpenDate)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.SettlementID=int(SettlementID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ComTradeID=self._to_bytes(ComTradeID)
    self.TradeID=self._to_bytes(TradeID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.Direction=self._to_bytes(Direction)
    self.TotalAmt=int(TotalAmt)
    self.Margin=float(Margin)
    self.ExchMargin=float(ExchMargin)
    self.MarginRateByMoney=float(MarginRateByMoney)
    self.MarginRateByVolume=float(MarginRateByVolume)
    self.LegID=int(LegID)
    self.LegMultiple=int(LegMultiple)
    self.CombInstrumentID=self._to_bytes(CombInstrumentID)
    self.TradeGroupID=int(TradeGroupID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.OpenDate=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.SettlementID=int(i_tuple[4])
    self.BrokerID=self._to_bytes(i_tuple[5])
    self.InvestorID=self._to_bytes(i_tuple[6])
    self.ComTradeID=self._to_bytes(i_tuple[7])
    self.TradeID=self._to_bytes(i_tuple[8])
    self.InstrumentID=self._to_bytes(i_tuple[9])
    self.HedgeFlag=self._to_bytes(i_tuple[10])
    self.Direction=self._to_bytes(i_tuple[11])
    self.TotalAmt=int(i_tuple[12])
    self.Margin=float(i_tuple[13])
    self.ExchMargin=float(i_tuple[14])
    self.MarginRateByMoney=float(i_tuple[15])
    self.MarginRateByVolume=float(i_tuple[16])
    self.LegID=int(i_tuple[17])
    self.LegMultiple=int(i_tuple[18])
    self.CombInstrumentID=self._to_bytes(i_tuple[19])
    self.TradeGroupID=int(i_tuple[20])
    self.InvestUnitID=self._to_bytes(i_tuple[21])

class ParkedOrderField(Base):
  """预埋单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OrderPriceType',ctypes.c_char)# 报单价格条件
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('CombOffsetFlag',ctypes.c_char*5)# 组合开平标志
    ,('CombHedgeFlag',ctypes.c_char*5)# 组合投机套保标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeTotalOriginal',ctypes.c_int)# 数量
    ,('TimeCondition',ctypes.c_char)# 有效期类型
    ,('GTDDate',ctypes.c_char*9)# GTD日期
    ,('VolumeCondition',ctypes.c_char)# 成交量类型
    ,('MinVolume',ctypes.c_int)# 最小成交量
    ,('ContingentCondition',ctypes.c_char)# 触发条件
    ,('StopPrice',ctypes.c_double)# 止损价
    ,('ForceCloseReason',ctypes.c_char)# 强平原因
    ,('IsAutoSuspend',ctypes.c_int)# 自动挂起标志
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('UserForceClose',ctypes.c_int)# 用户强评标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParkedOrderID',ctypes.c_char*13)# 预埋报单编号
    ,('UserType',ctypes.c_char)# 用户类型
    ,('Status',ctypes.c_char)# 预埋单状态
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('IsSwapOrder',ctypes.c_int)# 互换单标志
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OrderRef='',UserID='',OrderPriceType='',Direction='',CombOffsetFlag='',CombHedgeFlag='',LimitPrice=0.0,VolumeTotalOriginal=0,TimeCondition='',GTDDate='',VolumeCondition='',MinVolume=0,ContingentCondition='',StopPrice=0.0,ForceCloseReason='',IsAutoSuspend=0,BusinessUnit='',RequestID=0,UserForceClose=0,ExchangeID='',ParkedOrderID='',UserType='',Status='',ErrorID=0,ErrorMsg='',IsSwapOrder=0,AccountID='',CurrencyID='',ClientID='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(ParkedOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OrderRef=self._to_bytes(OrderRef)
    self.UserID=self._to_bytes(UserID)
    self.OrderPriceType=self._to_bytes(OrderPriceType)
    self.Direction=self._to_bytes(Direction)
    self.CombOffsetFlag=self._to_bytes(CombOffsetFlag)
    self.CombHedgeFlag=self._to_bytes(CombHedgeFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeTotalOriginal=int(VolumeTotalOriginal)
    self.TimeCondition=self._to_bytes(TimeCondition)
    self.GTDDate=self._to_bytes(GTDDate)
    self.VolumeCondition=self._to_bytes(VolumeCondition)
    self.MinVolume=int(MinVolume)
    self.ContingentCondition=self._to_bytes(ContingentCondition)
    self.StopPrice=float(StopPrice)
    self.ForceCloseReason=self._to_bytes(ForceCloseReason)
    self.IsAutoSuspend=int(IsAutoSuspend)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.RequestID=int(RequestID)
    self.UserForceClose=int(UserForceClose)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParkedOrderID=self._to_bytes(ParkedOrderID)
    self.UserType=self._to_bytes(UserType)
    self.Status=self._to_bytes(Status)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.IsSwapOrder=int(IsSwapOrder)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.ClientID=self._to_bytes(ClientID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.OrderPriceType=self._to_bytes(i_tuple[6])
    self.Direction=self._to_bytes(i_tuple[7])
    self.CombOffsetFlag=self._to_bytes(i_tuple[8])
    self.CombHedgeFlag=self._to_bytes(i_tuple[9])
    self.LimitPrice=float(i_tuple[10])
    self.VolumeTotalOriginal=int(i_tuple[11])
    self.TimeCondition=self._to_bytes(i_tuple[12])
    self.GTDDate=self._to_bytes(i_tuple[13])
    self.VolumeCondition=self._to_bytes(i_tuple[14])
    self.MinVolume=int(i_tuple[15])
    self.ContingentCondition=self._to_bytes(i_tuple[16])
    self.StopPrice=float(i_tuple[17])
    self.ForceCloseReason=self._to_bytes(i_tuple[18])
    self.IsAutoSuspend=int(i_tuple[19])
    self.BusinessUnit=self._to_bytes(i_tuple[20])
    self.RequestID=int(i_tuple[21])
    self.UserForceClose=int(i_tuple[22])
    self.ExchangeID=self._to_bytes(i_tuple[23])
    self.ParkedOrderID=self._to_bytes(i_tuple[24])
    self.UserType=self._to_bytes(i_tuple[25])
    self.Status=self._to_bytes(i_tuple[26])
    self.ErrorID=int(i_tuple[27])
    self.ErrorMsg=self._to_bytes(i_tuple[28])
    self.IsSwapOrder=int(i_tuple[29])
    self.AccountID=self._to_bytes(i_tuple[30])
    self.CurrencyID=self._to_bytes(i_tuple[31])
    self.ClientID=self._to_bytes(i_tuple[32])
    self.InvestUnitID=self._to_bytes(i_tuple[33])
    self.IPAddress=self._to_bytes(i_tuple[34])
    self.MacAddress=self._to_bytes(i_tuple[35])

class ParkedOrderActionField(Base):
  """输入预埋单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OrderActionRef',ctypes.c_int)# 报单操作引用
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeChange',ctypes.c_int)# 数量变化
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ParkedOrderActionID',ctypes.c_char*13)# 预埋撤单单编号
    ,('UserType',ctypes.c_char)# 用户类型
    ,('Status',ctypes.c_char)# 预埋撤单状态
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',OrderActionRef=0,OrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',OrderSysID='',ActionFlag='',LimitPrice=0.0,VolumeChange=0,UserID='',InstrumentID='',ParkedOrderActionID='',UserType='',Status='',ErrorID=0,ErrorMsg='',InvestUnitID='',IPAddress='',MacAddress=''):

    super(ParkedOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OrderActionRef=int(OrderActionRef)
    self.OrderRef=self._to_bytes(OrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeChange=int(VolumeChange)
    self.UserID=self._to_bytes(UserID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ParkedOrderActionID=self._to_bytes(ParkedOrderActionID)
    self.UserType=self._to_bytes(UserType)
    self.Status=self._to_bytes(Status)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OrderActionRef=int(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.OrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.LimitPrice=float(i_tuple[11])
    self.VolumeChange=int(i_tuple[12])
    self.UserID=self._to_bytes(i_tuple[13])
    self.InstrumentID=self._to_bytes(i_tuple[14])
    self.ParkedOrderActionID=self._to_bytes(i_tuple[15])
    self.UserType=self._to_bytes(i_tuple[16])
    self.Status=self._to_bytes(i_tuple[17])
    self.ErrorID=int(i_tuple[18])
    self.ErrorMsg=self._to_bytes(i_tuple[19])
    self.InvestUnitID=self._to_bytes(i_tuple[20])
    self.IPAddress=self._to_bytes(i_tuple[21])
    self.MacAddress=self._to_bytes(i_tuple[22])

class QryParkedOrderField(Base):
  """查询预埋单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryParkedOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class QryParkedOrderActionField(Base):
  """查询预埋撤单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryParkedOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class RemoveParkedOrderField(Base):
  """删除预埋单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ParkedOrderID',ctypes.c_char*13)# 预埋报单编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',ParkedOrderID='',InvestUnitID=''):

    super(RemoveParkedOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ParkedOrderID=self._to_bytes(ParkedOrderID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ParkedOrderID=self._to_bytes(i_tuple[3])
    self.InvestUnitID=self._to_bytes(i_tuple[4])

class RemoveParkedOrderActionField(Base):
  """删除预埋撤单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ParkedOrderActionID',ctypes.c_char*13)# 预埋撤单编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',ParkedOrderActionID='',InvestUnitID=''):

    super(RemoveParkedOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ParkedOrderActionID=self._to_bytes(ParkedOrderActionID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ParkedOrderActionID=self._to_bytes(i_tuple[3])
    self.InvestUnitID=self._to_bytes(i_tuple[4])

class InvestorWithdrawAlgorithmField(Base):
  """经纪公司可提资金算法表"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('UsingRatio',ctypes.c_double)# 可提资金比例
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('FundMortgageRatio',ctypes.c_double)# 货币质押比率
]

  def __init__(self,BrokerID= '',InvestorRange='',InvestorID='',UsingRatio=0.0,CurrencyID='',FundMortgageRatio=0.0):

    super(InvestorWithdrawAlgorithmField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.InvestorID=self._to_bytes(InvestorID)
    self.UsingRatio=float(UsingRatio)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.FundMortgageRatio=float(FundMortgageRatio)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.UsingRatio=float(i_tuple[4])
    self.CurrencyID=self._to_bytes(i_tuple[5])
    self.FundMortgageRatio=float(i_tuple[6])

class QryInvestorPositionCombineDetailField(Base):
  """查询组合持仓明细"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('CombInstrumentID',ctypes.c_char*31)# 组合持仓合约编码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',CombInstrumentID='',ExchangeID='',InvestUnitID=''):

    super(QryInvestorPositionCombineDetailField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.CombInstrumentID=self._to_bytes(CombInstrumentID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.CombInstrumentID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class MarketDataAveragePriceField(Base):
  """成交均价"""
  _fields_ = [
    ('AveragePrice',ctypes.c_double)# ///当日均价
]

  def __init__(self,AveragePrice= 0.0):

    super(MarketDataAveragePriceField,self).__init__()

    self.AveragePrice=float(AveragePrice)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.AveragePrice=float(i_tuple[1])

class VerifyInvestorPasswordField(Base):
  """校验投资者密码"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Password',ctypes.c_char*41)# 密码
]

  def __init__(self,BrokerID= '',InvestorID='',Password=''):

    super(VerifyInvestorPasswordField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Password=self._to_bytes(Password)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.Password=self._to_bytes(i_tuple[3])

class UserIPField(Base):
  """用户IP"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('IPMask',ctypes.c_char*16)# IP地址掩码
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',UserID='',IPAddress='',IPMask='',MacAddress=''):

    super(UserIPField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.IPMask=self._to_bytes(IPMask)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.IPAddress=self._to_bytes(i_tuple[3])
    self.IPMask=self._to_bytes(i_tuple[4])
    self.MacAddress=self._to_bytes(i_tuple[5])

class TradingNoticeInfoField(Base):
  """用户事件通知信息"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('SendTime',ctypes.c_char*9)# 发送时间
    ,('FieldContent',ctypes.c_char*501)# 消息正文
    ,('SequenceSeries',ctypes.c_short)# 序列系列号
    ,('SequenceNo',ctypes.c_int)# 序列号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',SendTime='',FieldContent='',SequenceSeries=0,SequenceNo=0,InvestUnitID=''):

    super(TradingNoticeInfoField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.SendTime=self._to_bytes(SendTime)
    self.FieldContent=self._to_bytes(FieldContent)
    self.SequenceSeries=int(SequenceSeries)
    self.SequenceNo=int(SequenceNo)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.SendTime=self._to_bytes(i_tuple[3])
    self.FieldContent=self._to_bytes(i_tuple[4])
    self.SequenceSeries=int(i_tuple[5])
    self.SequenceNo=int(i_tuple[6])
    self.InvestUnitID=self._to_bytes(i_tuple[7])

class TradingNoticeField(Base):
  """用户事件通知"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorRange',ctypes.c_char)# 投资者范围
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('SequenceSeries',ctypes.c_short)# 序列系列号
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('SendTime',ctypes.c_char*9)# 发送时间
    ,('SequenceNo',ctypes.c_int)# 序列号
    ,('FieldContent',ctypes.c_char*501)# 消息正文
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorRange='',InvestorID='',SequenceSeries=0,UserID='',SendTime='',SequenceNo=0,FieldContent='',InvestUnitID=''):

    super(TradingNoticeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorRange=self._to_bytes(InvestorRange)
    self.InvestorID=self._to_bytes(InvestorID)
    self.SequenceSeries=int(SequenceSeries)
    self.UserID=self._to_bytes(UserID)
    self.SendTime=self._to_bytes(SendTime)
    self.SequenceNo=int(SequenceNo)
    self.FieldContent=self._to_bytes(FieldContent)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorRange=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.SequenceSeries=int(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.SendTime=self._to_bytes(i_tuple[6])
    self.SequenceNo=int(i_tuple[7])
    self.FieldContent=self._to_bytes(i_tuple[8])
    self.InvestUnitID=self._to_bytes(i_tuple[9])

class QryTradingNoticeField(Base):
  """查询交易事件通知"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InvestUnitID=''):

    super(QryTradingNoticeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InvestUnitID=self._to_bytes(i_tuple[3])

class QryErrOrderField(Base):
  """查询错误报单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryErrOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class ErrOrderField(Base):
  """错误报单"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OrderPriceType',ctypes.c_char)# 报单价格条件
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('CombOffsetFlag',ctypes.c_char*5)# 组合开平标志
    ,('CombHedgeFlag',ctypes.c_char*5)# 组合投机套保标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeTotalOriginal',ctypes.c_int)# 数量
    ,('TimeCondition',ctypes.c_char)# 有效期类型
    ,('GTDDate',ctypes.c_char*9)# GTD日期
    ,('VolumeCondition',ctypes.c_char)# 成交量类型
    ,('MinVolume',ctypes.c_int)# 最小成交量
    ,('ContingentCondition',ctypes.c_char)# 触发条件
    ,('StopPrice',ctypes.c_double)# 止损价
    ,('ForceCloseReason',ctypes.c_char)# 强平原因
    ,('IsAutoSuspend',ctypes.c_int)# 自动挂起标志
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('UserForceClose',ctypes.c_int)# 用户强评标志
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('IsSwapOrder',ctypes.c_int)# 互换单标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('ClientID',ctypes.c_char*11)# 交易编码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OrderRef='',UserID='',OrderPriceType='',Direction='',CombOffsetFlag='',CombHedgeFlag='',LimitPrice=0.0,VolumeTotalOriginal=0,TimeCondition='',GTDDate='',VolumeCondition='',MinVolume=0,ContingentCondition='',StopPrice=0.0,ForceCloseReason='',IsAutoSuspend=0,BusinessUnit='',RequestID=0,UserForceClose=0,ErrorID=0,ErrorMsg='',IsSwapOrder=0,ExchangeID='',InvestUnitID='',AccountID='',CurrencyID='',ClientID='',IPAddress='',MacAddress=''):

    super(ErrOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OrderRef=self._to_bytes(OrderRef)
    self.UserID=self._to_bytes(UserID)
    self.OrderPriceType=self._to_bytes(OrderPriceType)
    self.Direction=self._to_bytes(Direction)
    self.CombOffsetFlag=self._to_bytes(CombOffsetFlag)
    self.CombHedgeFlag=self._to_bytes(CombHedgeFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeTotalOriginal=int(VolumeTotalOriginal)
    self.TimeCondition=self._to_bytes(TimeCondition)
    self.GTDDate=self._to_bytes(GTDDate)
    self.VolumeCondition=self._to_bytes(VolumeCondition)
    self.MinVolume=int(MinVolume)
    self.ContingentCondition=self._to_bytes(ContingentCondition)
    self.StopPrice=float(StopPrice)
    self.ForceCloseReason=self._to_bytes(ForceCloseReason)
    self.IsAutoSuspend=int(IsAutoSuspend)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.RequestID=int(RequestID)
    self.UserForceClose=int(UserForceClose)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.IsSwapOrder=int(IsSwapOrder)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.ClientID=self._to_bytes(ClientID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.OrderPriceType=self._to_bytes(i_tuple[6])
    self.Direction=self._to_bytes(i_tuple[7])
    self.CombOffsetFlag=self._to_bytes(i_tuple[8])
    self.CombHedgeFlag=self._to_bytes(i_tuple[9])
    self.LimitPrice=float(i_tuple[10])
    self.VolumeTotalOriginal=int(i_tuple[11])
    self.TimeCondition=self._to_bytes(i_tuple[12])
    self.GTDDate=self._to_bytes(i_tuple[13])
    self.VolumeCondition=self._to_bytes(i_tuple[14])
    self.MinVolume=int(i_tuple[15])
    self.ContingentCondition=self._to_bytes(i_tuple[16])
    self.StopPrice=float(i_tuple[17])
    self.ForceCloseReason=self._to_bytes(i_tuple[18])
    self.IsAutoSuspend=int(i_tuple[19])
    self.BusinessUnit=self._to_bytes(i_tuple[20])
    self.RequestID=int(i_tuple[21])
    self.UserForceClose=int(i_tuple[22])
    self.ErrorID=int(i_tuple[23])
    self.ErrorMsg=self._to_bytes(i_tuple[24])
    self.IsSwapOrder=int(i_tuple[25])
    self.ExchangeID=self._to_bytes(i_tuple[26])
    self.InvestUnitID=self._to_bytes(i_tuple[27])
    self.AccountID=self._to_bytes(i_tuple[28])
    self.CurrencyID=self._to_bytes(i_tuple[29])
    self.ClientID=self._to_bytes(i_tuple[30])
    self.IPAddress=self._to_bytes(i_tuple[31])
    self.MacAddress=self._to_bytes(i_tuple[32])

class ErrorConditionalOrderField(Base):
  """查询错误报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OrderPriceType',ctypes.c_char)# 报单价格条件
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('CombOffsetFlag',ctypes.c_char*5)# 组合开平标志
    ,('CombHedgeFlag',ctypes.c_char*5)# 组合投机套保标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeTotalOriginal',ctypes.c_int)# 数量
    ,('TimeCondition',ctypes.c_char)# 有效期类型
    ,('GTDDate',ctypes.c_char*9)# GTD日期
    ,('VolumeCondition',ctypes.c_char)# 成交量类型
    ,('MinVolume',ctypes.c_int)# 最小成交量
    ,('ContingentCondition',ctypes.c_char)# 触发条件
    ,('StopPrice',ctypes.c_double)# 止损价
    ,('ForceCloseReason',ctypes.c_char)# 强平原因
    ,('IsAutoSuspend',ctypes.c_int)# 自动挂起标志
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('ExchangeInstID',ctypes.c_char*31)# 合约在交易所的代码
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderSubmitStatus',ctypes.c_char)# 报单提交状态
    ,('NotifySequence',ctypes.c_int)# 报单提示序号
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('OrderSource',ctypes.c_char)# 报单来源
    ,('OrderStatus',ctypes.c_char)# 报单状态
    ,('OrderType',ctypes.c_char)# 报单类型
    ,('VolumeTraded',ctypes.c_int)# 今成交数量
    ,('VolumeTotal',ctypes.c_int)# 剩余数量
    ,('InsertDate',ctypes.c_char*9)# 报单日期
    ,('InsertTime',ctypes.c_char*9)# 委托时间
    ,('ActiveTime',ctypes.c_char*9)# 激活时间
    ,('SuspendTime',ctypes.c_char*9)# 挂起时间
    ,('UpdateTime',ctypes.c_char*9)# 最后修改时间
    ,('CancelTime',ctypes.c_char*9)# 撤销时间
    ,('ActiveTraderID',ctypes.c_char*21)# 最后修改交易所交易员代码
    ,('ClearingPartID',ctypes.c_char*11)# 结算会员编号
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('UserProductInfo',ctypes.c_char*11)# 用户端产品信息
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('UserForceClose',ctypes.c_int)# 用户强评标志
    ,('ActiveUserID',ctypes.c_char*16)# 操作用户代码
    ,('BrokerOrderSeq',ctypes.c_int)# 经纪公司报单编号
    ,('RelativeOrderSysID',ctypes.c_char*21)# 相关报单
    ,('ZCETotalTradedVolume',ctypes.c_int)# 郑商所成交数量
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('IsSwapOrder',ctypes.c_int)# 互换单标志
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('AccountID',ctypes.c_char*13)# 资金账号
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',OrderRef='',UserID='',OrderPriceType='',Direction='',CombOffsetFlag='',CombHedgeFlag='',LimitPrice=0.0,VolumeTotalOriginal=0,TimeCondition='',GTDDate='',VolumeCondition='',MinVolume=0,ContingentCondition='',StopPrice=0.0,ForceCloseReason='',IsAutoSuspend=0,BusinessUnit='',RequestID=0,OrderLocalID='',ExchangeID='',ParticipantID='',ClientID='',ExchangeInstID='',TraderID='',InstallID=0,OrderSubmitStatus='',NotifySequence=0,TradingDay='',SettlementID=0,OrderSysID='',OrderSource='',OrderStatus='',OrderType='',VolumeTraded=0,VolumeTotal=0,InsertDate='',InsertTime='',ActiveTime='',SuspendTime='',UpdateTime='',CancelTime='',ActiveTraderID='',ClearingPartID='',SequenceNo=0,FrontID=0,SessionID=0,UserProductInfo='',StatusMsg='',UserForceClose=0,ActiveUserID='',BrokerOrderSeq=0,RelativeOrderSysID='',ZCETotalTradedVolume=0,ErrorID=0,ErrorMsg='',IsSwapOrder=0,BranchID='',InvestUnitID='',AccountID='',CurrencyID='',IPAddress='',MacAddress=''):

    super(ErrorConditionalOrderField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.OrderRef=self._to_bytes(OrderRef)
    self.UserID=self._to_bytes(UserID)
    self.OrderPriceType=self._to_bytes(OrderPriceType)
    self.Direction=self._to_bytes(Direction)
    self.CombOffsetFlag=self._to_bytes(CombOffsetFlag)
    self.CombHedgeFlag=self._to_bytes(CombHedgeFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeTotalOriginal=int(VolumeTotalOriginal)
    self.TimeCondition=self._to_bytes(TimeCondition)
    self.GTDDate=self._to_bytes(GTDDate)
    self.VolumeCondition=self._to_bytes(VolumeCondition)
    self.MinVolume=int(MinVolume)
    self.ContingentCondition=self._to_bytes(ContingentCondition)
    self.StopPrice=float(StopPrice)
    self.ForceCloseReason=self._to_bytes(ForceCloseReason)
    self.IsAutoSuspend=int(IsAutoSuspend)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.RequestID=int(RequestID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.ExchangeInstID=self._to_bytes(ExchangeInstID)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderSubmitStatus=self._to_bytes(OrderSubmitStatus)
    self.NotifySequence=int(NotifySequence)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.OrderSource=self._to_bytes(OrderSource)
    self.OrderStatus=self._to_bytes(OrderStatus)
    self.OrderType=self._to_bytes(OrderType)
    self.VolumeTraded=int(VolumeTraded)
    self.VolumeTotal=int(VolumeTotal)
    self.InsertDate=self._to_bytes(InsertDate)
    self.InsertTime=self._to_bytes(InsertTime)
    self.ActiveTime=self._to_bytes(ActiveTime)
    self.SuspendTime=self._to_bytes(SuspendTime)
    self.UpdateTime=self._to_bytes(UpdateTime)
    self.CancelTime=self._to_bytes(CancelTime)
    self.ActiveTraderID=self._to_bytes(ActiveTraderID)
    self.ClearingPartID=self._to_bytes(ClearingPartID)
    self.SequenceNo=int(SequenceNo)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.UserProductInfo=self._to_bytes(UserProductInfo)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.UserForceClose=int(UserForceClose)
    self.ActiveUserID=self._to_bytes(ActiveUserID)
    self.BrokerOrderSeq=int(BrokerOrderSeq)
    self.RelativeOrderSysID=self._to_bytes(RelativeOrderSysID)
    self.ZCETotalTradedVolume=int(ZCETotalTradedVolume)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.IsSwapOrder=int(IsSwapOrder)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.UserID=self._to_bytes(i_tuple[5])
    self.OrderPriceType=self._to_bytes(i_tuple[6])
    self.Direction=self._to_bytes(i_tuple[7])
    self.CombOffsetFlag=self._to_bytes(i_tuple[8])
    self.CombHedgeFlag=self._to_bytes(i_tuple[9])
    self.LimitPrice=float(i_tuple[10])
    self.VolumeTotalOriginal=int(i_tuple[11])
    self.TimeCondition=self._to_bytes(i_tuple[12])
    self.GTDDate=self._to_bytes(i_tuple[13])
    self.VolumeCondition=self._to_bytes(i_tuple[14])
    self.MinVolume=int(i_tuple[15])
    self.ContingentCondition=self._to_bytes(i_tuple[16])
    self.StopPrice=float(i_tuple[17])
    self.ForceCloseReason=self._to_bytes(i_tuple[18])
    self.IsAutoSuspend=int(i_tuple[19])
    self.BusinessUnit=self._to_bytes(i_tuple[20])
    self.RequestID=int(i_tuple[21])
    self.OrderLocalID=self._to_bytes(i_tuple[22])
    self.ExchangeID=self._to_bytes(i_tuple[23])
    self.ParticipantID=self._to_bytes(i_tuple[24])
    self.ClientID=self._to_bytes(i_tuple[25])
    self.ExchangeInstID=self._to_bytes(i_tuple[26])
    self.TraderID=self._to_bytes(i_tuple[27])
    self.InstallID=int(i_tuple[28])
    self.OrderSubmitStatus=self._to_bytes(i_tuple[29])
    self.NotifySequence=int(i_tuple[30])
    self.TradingDay=self._to_bytes(i_tuple[31])
    self.SettlementID=int(i_tuple[32])
    self.OrderSysID=self._to_bytes(i_tuple[33])
    self.OrderSource=self._to_bytes(i_tuple[34])
    self.OrderStatus=self._to_bytes(i_tuple[35])
    self.OrderType=self._to_bytes(i_tuple[36])
    self.VolumeTraded=int(i_tuple[37])
    self.VolumeTotal=int(i_tuple[38])
    self.InsertDate=self._to_bytes(i_tuple[39])
    self.InsertTime=self._to_bytes(i_tuple[40])
    self.ActiveTime=self._to_bytes(i_tuple[41])
    self.SuspendTime=self._to_bytes(i_tuple[42])
    self.UpdateTime=self._to_bytes(i_tuple[43])
    self.CancelTime=self._to_bytes(i_tuple[44])
    self.ActiveTraderID=self._to_bytes(i_tuple[45])
    self.ClearingPartID=self._to_bytes(i_tuple[46])
    self.SequenceNo=int(i_tuple[47])
    self.FrontID=int(i_tuple[48])
    self.SessionID=int(i_tuple[49])
    self.UserProductInfo=self._to_bytes(i_tuple[50])
    self.StatusMsg=self._to_bytes(i_tuple[51])
    self.UserForceClose=int(i_tuple[52])
    self.ActiveUserID=self._to_bytes(i_tuple[53])
    self.BrokerOrderSeq=int(i_tuple[54])
    self.RelativeOrderSysID=self._to_bytes(i_tuple[55])
    self.ZCETotalTradedVolume=int(i_tuple[56])
    self.ErrorID=int(i_tuple[57])
    self.ErrorMsg=self._to_bytes(i_tuple[58])
    self.IsSwapOrder=int(i_tuple[59])
    self.BranchID=self._to_bytes(i_tuple[60])
    self.InvestUnitID=self._to_bytes(i_tuple[61])
    self.AccountID=self._to_bytes(i_tuple[62])
    self.CurrencyID=self._to_bytes(i_tuple[63])
    self.IPAddress=self._to_bytes(i_tuple[64])
    self.MacAddress=self._to_bytes(i_tuple[65])

class QryErrOrderActionField(Base):
  """查询错误报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryErrOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class ErrOrderActionField(Base):
  """错误报单操作"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('OrderActionRef',ctypes.c_int)# 报单操作引用
    ,('OrderRef',ctypes.c_char*13)# 报单引用
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('FrontID',ctypes.c_int)# 前置编号
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('OrderSysID',ctypes.c_char*21)# 报单编号
    ,('ActionFlag',ctypes.c_char)# 操作标志
    ,('LimitPrice',ctypes.c_double)# 价格
    ,('VolumeChange',ctypes.c_int)# 数量变化
    ,('ActionDate',ctypes.c_char*9)# 操作日期
    ,('ActionTime',ctypes.c_char*9)# 操作时间
    ,('TraderID',ctypes.c_char*21)# 交易所交易员代码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('OrderLocalID',ctypes.c_char*13)# 本地报单编号
    ,('ActionLocalID',ctypes.c_char*13)# 操作本地编号
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ClientID',ctypes.c_char*11)# 客户代码
    ,('BusinessUnit',ctypes.c_char*21)# 业务单元
    ,('OrderActionStatus',ctypes.c_char)# 报单操作状态
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('StatusMsg',ctypes.c_char*81)# 状态信息
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('BranchID',ctypes.c_char*9)# 营业部编号
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
    ,('MacAddress',ctypes.c_char*21)# Mac地址
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,BrokerID= '',InvestorID='',OrderActionRef=0,OrderRef='',RequestID=0,FrontID=0,SessionID=0,ExchangeID='',OrderSysID='',ActionFlag='',LimitPrice=0.0,VolumeChange=0,ActionDate='',ActionTime='',TraderID='',InstallID=0,OrderLocalID='',ActionLocalID='',ParticipantID='',ClientID='',BusinessUnit='',OrderActionStatus='',UserID='',StatusMsg='',InstrumentID='',BranchID='',InvestUnitID='',IPAddress='',MacAddress='',ErrorID=0,ErrorMsg=''):

    super(ErrOrderActionField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.OrderActionRef=int(OrderActionRef)
    self.OrderRef=self._to_bytes(OrderRef)
    self.RequestID=int(RequestID)
    self.FrontID=int(FrontID)
    self.SessionID=int(SessionID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.OrderSysID=self._to_bytes(OrderSysID)
    self.ActionFlag=self._to_bytes(ActionFlag)
    self.LimitPrice=float(LimitPrice)
    self.VolumeChange=int(VolumeChange)
    self.ActionDate=self._to_bytes(ActionDate)
    self.ActionTime=self._to_bytes(ActionTime)
    self.TraderID=self._to_bytes(TraderID)
    self.InstallID=int(InstallID)
    self.OrderLocalID=self._to_bytes(OrderLocalID)
    self.ActionLocalID=self._to_bytes(ActionLocalID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ClientID=self._to_bytes(ClientID)
    self.BusinessUnit=self._to_bytes(BusinessUnit)
    self.OrderActionStatus=self._to_bytes(OrderActionStatus)
    self.UserID=self._to_bytes(UserID)
    self.StatusMsg=self._to_bytes(StatusMsg)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.BranchID=self._to_bytes(BranchID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
    self.IPAddress=self._to_bytes(IPAddress)
    self.MacAddress=self._to_bytes(MacAddress)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.OrderActionRef=int(i_tuple[3])
    self.OrderRef=self._to_bytes(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.FrontID=int(i_tuple[6])
    self.SessionID=int(i_tuple[7])
    self.ExchangeID=self._to_bytes(i_tuple[8])
    self.OrderSysID=self._to_bytes(i_tuple[9])
    self.ActionFlag=self._to_bytes(i_tuple[10])
    self.LimitPrice=float(i_tuple[11])
    self.VolumeChange=int(i_tuple[12])
    self.ActionDate=self._to_bytes(i_tuple[13])
    self.ActionTime=self._to_bytes(i_tuple[14])
    self.TraderID=self._to_bytes(i_tuple[15])
    self.InstallID=int(i_tuple[16])
    self.OrderLocalID=self._to_bytes(i_tuple[17])
    self.ActionLocalID=self._to_bytes(i_tuple[18])
    self.ParticipantID=self._to_bytes(i_tuple[19])
    self.ClientID=self._to_bytes(i_tuple[20])
    self.BusinessUnit=self._to_bytes(i_tuple[21])
    self.OrderActionStatus=self._to_bytes(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.StatusMsg=self._to_bytes(i_tuple[24])
    self.InstrumentID=self._to_bytes(i_tuple[25])
    self.BranchID=self._to_bytes(i_tuple[26])
    self.InvestUnitID=self._to_bytes(i_tuple[27])
    self.IPAddress=self._to_bytes(i_tuple[28])
    self.MacAddress=self._to_bytes(i_tuple[29])
    self.ErrorID=int(i_tuple[30])
    self.ErrorMsg=self._to_bytes(i_tuple[31])

class QryExchangeSequenceField(Base):
  """查询交易所状态"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
]

  def __init__(self,ExchangeID= ''):

    super(QryExchangeSequenceField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])

class ExchangeSequenceField(Base):
  """交易所状态"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('SequenceNo',ctypes.c_int)# 序号
    ,('MarketStatus',ctypes.c_char)# 合约交易状态
]

  def __init__(self,ExchangeID= '',SequenceNo=0,MarketStatus=''):

    super(ExchangeSequenceField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.SequenceNo=int(SequenceNo)
    self.MarketStatus=self._to_bytes(MarketStatus)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.SequenceNo=int(i_tuple[2])
    self.MarketStatus=self._to_bytes(i_tuple[3])

class QueryMaxOrderVolumeWithPriceField(Base):
  """根据价格查询最大报单数量"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('OffsetFlag',ctypes.c_char)# 开平标志
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('MaxVolume',ctypes.c_int)# 最大允许报单数量
    ,('Price',ctypes.c_double)# 报单价格
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InstrumentID='',Direction='',OffsetFlag='',HedgeFlag='',MaxVolume=0,Price=0.0,ExchangeID='',InvestUnitID=''):

    super(QueryMaxOrderVolumeWithPriceField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.Direction=self._to_bytes(Direction)
    self.OffsetFlag=self._to_bytes(OffsetFlag)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.MaxVolume=int(MaxVolume)
    self.Price=float(Price)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.Direction=self._to_bytes(i_tuple[4])
    self.OffsetFlag=self._to_bytes(i_tuple[5])
    self.HedgeFlag=self._to_bytes(i_tuple[6])
    self.MaxVolume=int(i_tuple[7])
    self.Price=float(i_tuple[8])
    self.ExchangeID=self._to_bytes(i_tuple[9])
    self.InvestUnitID=self._to_bytes(i_tuple[10])

class QryBrokerTradingParamsField(Base):
  """查询经纪公司交易参数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
]

  def __init__(self,BrokerID= '',InvestorID='',CurrencyID='',AccountID=''):

    super(QryBrokerTradingParamsField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.AccountID=self._to_bytes(AccountID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.CurrencyID=self._to_bytes(i_tuple[3])
    self.AccountID=self._to_bytes(i_tuple[4])

class BrokerTradingParamsField(Base):
  """经纪公司交易参数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('MarginPriceType',ctypes.c_char)# 保证金价格类型
    ,('Algorithm',ctypes.c_char)# 盈亏算法
    ,('AvailIncludeCloseProfit',ctypes.c_char)# 可用是否包含平仓盈利
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('OptionRoyaltyPriceType',ctypes.c_char)# 期权权利金价格类型
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
]

  def __init__(self,BrokerID= '',InvestorID='',MarginPriceType='',Algorithm='',AvailIncludeCloseProfit='',CurrencyID='',OptionRoyaltyPriceType='',AccountID=''):

    super(BrokerTradingParamsField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.MarginPriceType=self._to_bytes(MarginPriceType)
    self.Algorithm=self._to_bytes(Algorithm)
    self.AvailIncludeCloseProfit=self._to_bytes(AvailIncludeCloseProfit)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.OptionRoyaltyPriceType=self._to_bytes(OptionRoyaltyPriceType)
    self.AccountID=self._to_bytes(AccountID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.MarginPriceType=self._to_bytes(i_tuple[3])
    self.Algorithm=self._to_bytes(i_tuple[4])
    self.AvailIncludeCloseProfit=self._to_bytes(i_tuple[5])
    self.CurrencyID=self._to_bytes(i_tuple[6])
    self.OptionRoyaltyPriceType=self._to_bytes(i_tuple[7])
    self.AccountID=self._to_bytes(i_tuple[8])

class QryBrokerTradingAlgosField(Base):
  """查询经纪公司交易算法"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
]

  def __init__(self,BrokerID= '',ExchangeID='',InstrumentID=''):

    super(QryBrokerTradingAlgosField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InstrumentID=self._to_bytes(InstrumentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])

class BrokerTradingAlgosField(Base):
  """经纪公司交易算法"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('HandlePositionAlgoID',ctypes.c_char)# 持仓处理算法编号
    ,('FindMarginRateAlgoID',ctypes.c_char)# 寻找保证金率算法编号
    ,('HandleTradingAccountAlgoID',ctypes.c_char)# 资金处理算法编号
]

  def __init__(self,BrokerID= '',ExchangeID='',InstrumentID='',HandlePositionAlgoID='',FindMarginRateAlgoID='',HandleTradingAccountAlgoID=''):

    super(BrokerTradingAlgosField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.HandlePositionAlgoID=self._to_bytes(HandlePositionAlgoID)
    self.FindMarginRateAlgoID=self._to_bytes(FindMarginRateAlgoID)
    self.HandleTradingAccountAlgoID=self._to_bytes(HandleTradingAccountAlgoID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.InstrumentID=self._to_bytes(i_tuple[3])
    self.HandlePositionAlgoID=self._to_bytes(i_tuple[4])
    self.FindMarginRateAlgoID=self._to_bytes(i_tuple[5])
    self.HandleTradingAccountAlgoID=self._to_bytes(i_tuple[6])

class QueryBrokerDepositField(Base):
  """查询经纪公司资金"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,BrokerID= '',ExchangeID=''):

    super(QueryBrokerDepositField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])

class BrokerDepositField(Base):
  """经纪公司资金"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日期
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('ParticipantID',ctypes.c_char*11)# 会员代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('PreBalance',ctypes.c_double)# 上次结算准备金
    ,('CurrMargin',ctypes.c_double)# 当前保证金总额
    ,('CloseProfit',ctypes.c_double)# 平仓盈亏
    ,('Balance',ctypes.c_double)# 期货结算准备金
    ,('Deposit',ctypes.c_double)# 入金金额
    ,('Withdraw',ctypes.c_double)# 出金金额
    ,('Available',ctypes.c_double)# 可提资金
    ,('Reserve',ctypes.c_double)# 基本准备金
    ,('FrozenMargin',ctypes.c_double)# 冻结的保证金
]

  def __init__(self,TradingDay= '',BrokerID='',ParticipantID='',ExchangeID='',PreBalance=0.0,CurrMargin=0.0,CloseProfit=0.0,Balance=0.0,Deposit=0.0,Withdraw=0.0,Available=0.0,Reserve=0.0,FrozenMargin=0.0):

    super(BrokerDepositField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.BrokerID=self._to_bytes(BrokerID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.PreBalance=float(PreBalance)
    self.CurrMargin=float(CurrMargin)
    self.CloseProfit=float(CloseProfit)
    self.Balance=float(Balance)
    self.Deposit=float(Deposit)
    self.Withdraw=float(Withdraw)
    self.Available=float(Available)
    self.Reserve=float(Reserve)
    self.FrozenMargin=float(FrozenMargin)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.ParticipantID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.PreBalance=float(i_tuple[5])
    self.CurrMargin=float(i_tuple[6])
    self.CloseProfit=float(i_tuple[7])
    self.Balance=float(i_tuple[8])
    self.Deposit=float(i_tuple[9])
    self.Withdraw=float(i_tuple[10])
    self.Available=float(i_tuple[11])
    self.Reserve=float(i_tuple[12])
    self.FrozenMargin=float(i_tuple[13])

class QryCFMMCBrokerKeyField(Base):
  """查询保证金监管系统经纪公司密钥"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
]

  def __init__(self,BrokerID= ''):

    super(QryCFMMCBrokerKeyField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])

class CFMMCBrokerKeyField(Base):
  """保证金监管系统经纪公司密钥"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ParticipantID',ctypes.c_char*11)# 经纪公司统一编码
    ,('CreateDate',ctypes.c_char*9)# 密钥生成日期
    ,('CreateTime',ctypes.c_char*9)# 密钥生成时间
    ,('KeyID',ctypes.c_int)# 密钥编号
    ,('CurrentKey',ctypes.c_char*21)# 动态密钥
    ,('KeyKind',ctypes.c_char)# 动态密钥类型
]

  def __init__(self,BrokerID= '',ParticipantID='',CreateDate='',CreateTime='',KeyID=0,CurrentKey='',KeyKind=''):

    super(CFMMCBrokerKeyField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.CreateDate=self._to_bytes(CreateDate)
    self.CreateTime=self._to_bytes(CreateTime)
    self.KeyID=int(KeyID)
    self.CurrentKey=self._to_bytes(CurrentKey)
    self.KeyKind=self._to_bytes(KeyKind)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.CreateDate=self._to_bytes(i_tuple[3])
    self.CreateTime=self._to_bytes(i_tuple[4])
    self.KeyID=int(i_tuple[5])
    self.CurrentKey=self._to_bytes(i_tuple[6])
    self.KeyKind=self._to_bytes(i_tuple[7])

class CFMMCTradingAccountKeyField(Base):
  """保证金监管系统经纪公司资金账户密钥"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ParticipantID',ctypes.c_char*11)# 经纪公司统一编码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('KeyID',ctypes.c_int)# 密钥编号
    ,('CurrentKey',ctypes.c_char*21)# 动态密钥
]

  def __init__(self,BrokerID= '',ParticipantID='',AccountID='',KeyID=0,CurrentKey=''):

    super(CFMMCTradingAccountKeyField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.AccountID=self._to_bytes(AccountID)
    self.KeyID=int(KeyID)
    self.CurrentKey=self._to_bytes(CurrentKey)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.AccountID=self._to_bytes(i_tuple[3])
    self.KeyID=int(i_tuple[4])
    self.CurrentKey=self._to_bytes(i_tuple[5])

class QryCFMMCTradingAccountKeyField(Base):
  """请求查询保证金监管系统经纪公司资金账户密钥"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QryCFMMCTradingAccountKeyField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

class BrokerUserOTPParamField(Base):
  """用户动态令牌参数"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OTPVendorsID',ctypes.c_char*2)# 动态令牌提供商
    ,('SerialNumber',ctypes.c_char*17)# 动态令牌序列号
    ,('AuthKey',ctypes.c_char*41)# 令牌密钥
    ,('LastDrift',ctypes.c_int)# 漂移值
    ,('LastSuccess',ctypes.c_int)# 成功值
    ,('OTPType',ctypes.c_char)# 动态令牌类型
]

  def __init__(self,BrokerID= '',UserID='',OTPVendorsID='',SerialNumber='',AuthKey='',LastDrift=0,LastSuccess=0,OTPType=''):

    super(BrokerUserOTPParamField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.OTPVendorsID=self._to_bytes(OTPVendorsID)
    self.SerialNumber=self._to_bytes(SerialNumber)
    self.AuthKey=self._to_bytes(AuthKey)
    self.LastDrift=int(LastDrift)
    self.LastSuccess=int(LastSuccess)
    self.OTPType=self._to_bytes(OTPType)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.OTPVendorsID=self._to_bytes(i_tuple[3])
    self.SerialNumber=self._to_bytes(i_tuple[4])
    self.AuthKey=self._to_bytes(i_tuple[5])
    self.LastDrift=int(i_tuple[6])
    self.LastSuccess=int(i_tuple[7])
    self.OTPType=self._to_bytes(i_tuple[8])

class ManualSyncBrokerUserOTPField(Base):
  """手工同步用户动态令牌"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('OTPType',ctypes.c_char)# 动态令牌类型
    ,('FirstOTP',ctypes.c_char*41)# 第一个动态密码
    ,('SecondOTP',ctypes.c_char*41)# 第二个动态密码
]

  def __init__(self,BrokerID= '',UserID='',OTPType='',FirstOTP='',SecondOTP=''):

    super(ManualSyncBrokerUserOTPField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.OTPType=self._to_bytes(OTPType)
    self.FirstOTP=self._to_bytes(FirstOTP)
    self.SecondOTP=self._to_bytes(SecondOTP)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.OTPType=self._to_bytes(i_tuple[3])
    self.FirstOTP=self._to_bytes(i_tuple[4])
    self.SecondOTP=self._to_bytes(i_tuple[5])

class CommRateModelField(Base):
  """投资者手续费率模板"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('CommModelID',ctypes.c_char*13)# 手续费率模板代码
    ,('CommModelName',ctypes.c_char*161)# 模板名称
]

  def __init__(self,BrokerID= '',CommModelID='',CommModelName=''):

    super(CommRateModelField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.CommModelID=self._to_bytes(CommModelID)
    self.CommModelName=self._to_bytes(CommModelName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.CommModelID=self._to_bytes(i_tuple[2])
    self.CommModelName=self._to_bytes(i_tuple[3])

class QryCommRateModelField(Base):
  """请求查询投资者手续费率模板"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('CommModelID',ctypes.c_char*13)# 手续费率模板代码
]

  def __init__(self,BrokerID= '',CommModelID=''):

    super(QryCommRateModelField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.CommModelID=self._to_bytes(CommModelID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.CommModelID=self._to_bytes(i_tuple[2])

class MarginModelField(Base):
  """投资者保证金率模板"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('MarginModelID',ctypes.c_char*13)# 保证金率模板代码
    ,('MarginModelName',ctypes.c_char*161)# 模板名称
]

  def __init__(self,BrokerID= '',MarginModelID='',MarginModelName=''):

    super(MarginModelField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.MarginModelID=self._to_bytes(MarginModelID)
    self.MarginModelName=self._to_bytes(MarginModelName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.MarginModelID=self._to_bytes(i_tuple[2])
    self.MarginModelName=self._to_bytes(i_tuple[3])

class QryMarginModelField(Base):
  """请求查询投资者保证金率模板"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('MarginModelID',ctypes.c_char*13)# 保证金率模板代码
]

  def __init__(self,BrokerID= '',MarginModelID=''):

    super(QryMarginModelField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.MarginModelID=self._to_bytes(MarginModelID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.MarginModelID=self._to_bytes(i_tuple[2])

class EWarrantOffsetField(Base):
  """仓单折抵信息"""
  _fields_ = [
    ('TradingDay',ctypes.c_char*9)# ///交易日期
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('Direction',ctypes.c_char)# 买卖方向
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('Volume',ctypes.c_int)# 数量
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,TradingDay= '',BrokerID='',InvestorID='',ExchangeID='',InstrumentID='',Direction='',HedgeFlag='',Volume=0,InvestUnitID=''):

    super(EWarrantOffsetField,self).__init__()

    self.TradingDay=self._to_bytes(TradingDay)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.Direction=self._to_bytes(Direction)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.Volume=int(Volume)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradingDay=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.ExchangeID=self._to_bytes(i_tuple[4])
    self.InstrumentID=self._to_bytes(i_tuple[5])
    self.Direction=self._to_bytes(i_tuple[6])
    self.HedgeFlag=self._to_bytes(i_tuple[7])
    self.Volume=int(i_tuple[8])
    self.InvestUnitID=self._to_bytes(i_tuple[9])

class QryEWarrantOffsetField(Base):
  """查询仓单折抵信息"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InstrumentID',ctypes.c_char*31)# 合约代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',ExchangeID='',InstrumentID='',InvestUnitID=''):

    super(QryEWarrantOffsetField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InstrumentID=self._to_bytes(InstrumentID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ExchangeID=self._to_bytes(i_tuple[3])
    self.InstrumentID=self._to_bytes(i_tuple[4])
    self.InvestUnitID=self._to_bytes(i_tuple[5])

class QryInvestorProductGroupMarginField(Base):
  """查询投资者品种/跨品种保证金"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('ProductGroupID',ctypes.c_char*31)# 品种/跨品种标示
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',ProductGroupID='',HedgeFlag='',ExchangeID='',InvestUnitID=''):

    super(QryInvestorProductGroupMarginField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.ProductGroupID=self._to_bytes(ProductGroupID)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.ProductGroupID=self._to_bytes(i_tuple[3])
    self.HedgeFlag=self._to_bytes(i_tuple[4])
    self.ExchangeID=self._to_bytes(i_tuple[5])
    self.InvestUnitID=self._to_bytes(i_tuple[6])

class InvestorProductGroupMarginField(Base):
  """投资者品种/跨品种保证金"""
  _fields_ = [
    ('ProductGroupID',ctypes.c_char*31)# ///品种/跨品种标示
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('SettlementID',ctypes.c_int)# 结算编号
    ,('FrozenMargin',ctypes.c_double)# 冻结的保证金
    ,('LongFrozenMargin',ctypes.c_double)# 多头冻结的保证金
    ,('ShortFrozenMargin',ctypes.c_double)# 空头冻结的保证金
    ,('UseMargin',ctypes.c_double)# 占用的保证金
    ,('LongUseMargin',ctypes.c_double)# 多头保证金
    ,('ShortUseMargin',ctypes.c_double)# 空头保证金
    ,('ExchMargin',ctypes.c_double)# 交易所保证金
    ,('LongExchMargin',ctypes.c_double)# 交易所多头保证金
    ,('ShortExchMargin',ctypes.c_double)# 交易所空头保证金
    ,('CloseProfit',ctypes.c_double)# 平仓盈亏
    ,('FrozenCommission',ctypes.c_double)# 冻结的手续费
    ,('Commission',ctypes.c_double)# 手续费
    ,('FrozenCash',ctypes.c_double)# 冻结的资金
    ,('CashIn',ctypes.c_double)# 资金差额
    ,('PositionProfit',ctypes.c_double)# 持仓盈亏
    ,('OffsetAmount',ctypes.c_double)# 折抵总金额
    ,('LongOffsetAmount',ctypes.c_double)# 多头折抵总金额
    ,('ShortOffsetAmount',ctypes.c_double)# 空头折抵总金额
    ,('ExchOffsetAmount',ctypes.c_double)# 交易所折抵总金额
    ,('LongExchOffsetAmount',ctypes.c_double)# 交易所多头折抵总金额
    ,('ShortExchOffsetAmount',ctypes.c_double)# 交易所空头折抵总金额
    ,('HedgeFlag',ctypes.c_char)# 投机套保标志
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,ProductGroupID= '',BrokerID='',InvestorID='',TradingDay='',SettlementID=0,FrozenMargin=0.0,LongFrozenMargin=0.0,ShortFrozenMargin=0.0,UseMargin=0.0,LongUseMargin=0.0,ShortUseMargin=0.0,ExchMargin=0.0,LongExchMargin=0.0,ShortExchMargin=0.0,CloseProfit=0.0,FrozenCommission=0.0,Commission=0.0,FrozenCash=0.0,CashIn=0.0,PositionProfit=0.0,OffsetAmount=0.0,LongOffsetAmount=0.0,ShortOffsetAmount=0.0,ExchOffsetAmount=0.0,LongExchOffsetAmount=0.0,ShortExchOffsetAmount=0.0,HedgeFlag='',ExchangeID='',InvestUnitID=''):

    super(InvestorProductGroupMarginField,self).__init__()

    self.ProductGroupID=self._to_bytes(ProductGroupID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.TradingDay=self._to_bytes(TradingDay)
    self.SettlementID=int(SettlementID)
    self.FrozenMargin=float(FrozenMargin)
    self.LongFrozenMargin=float(LongFrozenMargin)
    self.ShortFrozenMargin=float(ShortFrozenMargin)
    self.UseMargin=float(UseMargin)
    self.LongUseMargin=float(LongUseMargin)
    self.ShortUseMargin=float(ShortUseMargin)
    self.ExchMargin=float(ExchMargin)
    self.LongExchMargin=float(LongExchMargin)
    self.ShortExchMargin=float(ShortExchMargin)
    self.CloseProfit=float(CloseProfit)
    self.FrozenCommission=float(FrozenCommission)
    self.Commission=float(Commission)
    self.FrozenCash=float(FrozenCash)
    self.CashIn=float(CashIn)
    self.PositionProfit=float(PositionProfit)
    self.OffsetAmount=float(OffsetAmount)
    self.LongOffsetAmount=float(LongOffsetAmount)
    self.ShortOffsetAmount=float(ShortOffsetAmount)
    self.ExchOffsetAmount=float(ExchOffsetAmount)
    self.LongExchOffsetAmount=float(LongExchOffsetAmount)
    self.ShortExchOffsetAmount=float(ShortExchOffsetAmount)
    self.HedgeFlag=self._to_bytes(HedgeFlag)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductGroupID=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.TradingDay=self._to_bytes(i_tuple[4])
    self.SettlementID=int(i_tuple[5])
    self.FrozenMargin=float(i_tuple[6])
    self.LongFrozenMargin=float(i_tuple[7])
    self.ShortFrozenMargin=float(i_tuple[8])
    self.UseMargin=float(i_tuple[9])
    self.LongUseMargin=float(i_tuple[10])
    self.ShortUseMargin=float(i_tuple[11])
    self.ExchMargin=float(i_tuple[12])
    self.LongExchMargin=float(i_tuple[13])
    self.ShortExchMargin=float(i_tuple[14])
    self.CloseProfit=float(i_tuple[15])
    self.FrozenCommission=float(i_tuple[16])
    self.Commission=float(i_tuple[17])
    self.FrozenCash=float(i_tuple[18])
    self.CashIn=float(i_tuple[19])
    self.PositionProfit=float(i_tuple[20])
    self.OffsetAmount=float(i_tuple[21])
    self.LongOffsetAmount=float(i_tuple[22])
    self.ShortOffsetAmount=float(i_tuple[23])
    self.ExchOffsetAmount=float(i_tuple[24])
    self.LongExchOffsetAmount=float(i_tuple[25])
    self.ShortExchOffsetAmount=float(i_tuple[26])
    self.HedgeFlag=self._to_bytes(i_tuple[27])
    self.ExchangeID=self._to_bytes(i_tuple[28])
    self.InvestUnitID=self._to_bytes(i_tuple[29])

class QueryCFMMCTradingAccountTokenField(Base):
  """查询监控中心用户令牌"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('InvestUnitID',ctypes.c_char*17)# 投资单元代码
]

  def __init__(self,BrokerID= '',InvestorID='',InvestUnitID=''):

    super(QueryCFMMCTradingAccountTokenField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.InvestUnitID=self._to_bytes(InvestUnitID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])
    self.InvestUnitID=self._to_bytes(i_tuple[3])

class CFMMCTradingAccountTokenField(Base):
  """监控中心用户令牌"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('ParticipantID',ctypes.c_char*11)# 经纪公司统一编码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('KeyID',ctypes.c_int)# 密钥编号
    ,('Token',ctypes.c_char*21)# 动态令牌
]

  def __init__(self,BrokerID= '',ParticipantID='',AccountID='',KeyID=0,Token=''):

    super(CFMMCTradingAccountTokenField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.ParticipantID=self._to_bytes(ParticipantID)
    self.AccountID=self._to_bytes(AccountID)
    self.KeyID=int(KeyID)
    self.Token=self._to_bytes(Token)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.ParticipantID=self._to_bytes(i_tuple[2])
    self.AccountID=self._to_bytes(i_tuple[3])
    self.KeyID=int(i_tuple[4])
    self.Token=self._to_bytes(i_tuple[5])

class QryProductGroupField(Base):
  """查询产品组"""
  _fields_ = [
    ('ProductID',ctypes.c_char*31)# ///产品代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
]

  def __init__(self,ProductID= '',ExchangeID=''):

    super(QryProductGroupField,self).__init__()

    self.ProductID=self._to_bytes(ProductID)
    self.ExchangeID=self._to_bytes(ExchangeID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])

class ProductGroupField(Base):
  """投资者品种/跨品种保证金产品组"""
  _fields_ = [
    ('ProductID',ctypes.c_char*31)# ///产品代码
    ,('ExchangeID',ctypes.c_char*9)# 交易所代码
    ,('ProductGroupID',ctypes.c_char*31)# 产品组代码
]

  def __init__(self,ProductID= '',ExchangeID='',ProductGroupID=''):

    super(ProductGroupField,self).__init__()

    self.ProductID=self._to_bytes(ProductID)
    self.ExchangeID=self._to_bytes(ExchangeID)
    self.ProductGroupID=self._to_bytes(ProductGroupID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ProductID=self._to_bytes(i_tuple[1])
    self.ExchangeID=self._to_bytes(i_tuple[2])
    self.ProductGroupID=self._to_bytes(i_tuple[3])

class BulletinField(Base):
  """交易所公告"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('TradingDay',ctypes.c_char*9)# 交易日
    ,('BulletinID',ctypes.c_int)# 公告编号
    ,('SequenceNo',ctypes.c_int)# 序列号
    ,('NewsType',ctypes.c_char*3)# 公告类型
    ,('NewsUrgency',ctypes.c_char)# 紧急程度
    ,('SendTime',ctypes.c_char*9)# 发送时间
    ,('Abstract',ctypes.c_char*81)# 消息摘要
    ,('ComeFrom',ctypes.c_char*21)# 消息来源
    ,('Content',ctypes.c_char*501)# 消息正文
    ,('URLLink',ctypes.c_char*201)# WEB地址
    ,('MarketID',ctypes.c_char*31)# 市场代码
]

  def __init__(self,ExchangeID= '',TradingDay='',BulletinID=0,SequenceNo=0,NewsType='',NewsUrgency='',SendTime='',Abstract='',ComeFrom='',Content='',URLLink='',MarketID=''):

    super(BulletinField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.TradingDay=self._to_bytes(TradingDay)
    self.BulletinID=int(BulletinID)
    self.SequenceNo=int(SequenceNo)
    self.NewsType=self._to_bytes(NewsType)
    self.NewsUrgency=self._to_bytes(NewsUrgency)
    self.SendTime=self._to_bytes(SendTime)
    self.Abstract=self._to_bytes(Abstract)
    self.ComeFrom=self._to_bytes(ComeFrom)
    self.Content=self._to_bytes(Content)
    self.URLLink=self._to_bytes(URLLink)
    self.MarketID=self._to_bytes(MarketID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.TradingDay=self._to_bytes(i_tuple[2])
    self.BulletinID=int(i_tuple[3])
    self.SequenceNo=int(i_tuple[4])
    self.NewsType=self._to_bytes(i_tuple[5])
    self.NewsUrgency=self._to_bytes(i_tuple[6])
    self.SendTime=self._to_bytes(i_tuple[7])
    self.Abstract=self._to_bytes(i_tuple[8])
    self.ComeFrom=self._to_bytes(i_tuple[9])
    self.Content=self._to_bytes(i_tuple[10])
    self.URLLink=self._to_bytes(i_tuple[11])
    self.MarketID=self._to_bytes(i_tuple[12])

class QryBulletinField(Base):
  """查询交易所公告"""
  _fields_ = [
    ('ExchangeID',ctypes.c_char*9)# ///交易所代码
    ,('BulletinID',ctypes.c_int)# 公告编号
    ,('SequenceNo',ctypes.c_int)# 序列号
    ,('NewsType',ctypes.c_char*3)# 公告类型
    ,('NewsUrgency',ctypes.c_char)# 紧急程度
]

  def __init__(self,ExchangeID= '',BulletinID=0,SequenceNo=0,NewsType='',NewsUrgency=''):

    super(QryBulletinField,self).__init__()

    self.ExchangeID=self._to_bytes(ExchangeID)
    self.BulletinID=int(BulletinID)
    self.SequenceNo=int(SequenceNo)
    self.NewsType=self._to_bytes(NewsType)
    self.NewsUrgency=self._to_bytes(NewsUrgency)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ExchangeID=self._to_bytes(i_tuple[1])
    self.BulletinID=int(i_tuple[2])
    self.SequenceNo=int(i_tuple[3])
    self.NewsType=self._to_bytes(i_tuple[4])
    self.NewsUrgency=self._to_bytes(i_tuple[5])

class ReqOpenAccountField(Base):
  """转帐开户请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('CashExchangeCode',ctypes.c_char)# 汇钞标志
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('TID',ctypes.c_int)# 交易ID
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',CashExchangeCode='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',TID=0,UserID='',LongCustomerName=''):

    super(ReqOpenAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.CashExchangeCode=self._to_bytes(CashExchangeCode)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.TID=int(TID)
    self.UserID=self._to_bytes(UserID)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.AccountID=self._to_bytes(i_tuple[28])
    self.Password=self._to_bytes(i_tuple[29])
    self.InstallID=int(i_tuple[30])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.CashExchangeCode=self._to_bytes(i_tuple[33])
    self.Digest=self._to_bytes(i_tuple[34])
    self.BankAccType=self._to_bytes(i_tuple[35])
    self.DeviceID=self._to_bytes(i_tuple[36])
    self.BankSecuAccType=self._to_bytes(i_tuple[37])
    self.BrokerIDByBank=self._to_bytes(i_tuple[38])
    self.BankSecuAcc=self._to_bytes(i_tuple[39])
    self.BankPwdFlag=self._to_bytes(i_tuple[40])
    self.SecuPwdFlag=self._to_bytes(i_tuple[41])
    self.OperNo=self._to_bytes(i_tuple[42])
    self.TID=int(i_tuple[43])
    self.UserID=self._to_bytes(i_tuple[44])
    self.LongCustomerName=self._to_bytes(i_tuple[45])

class ReqCancelAccountField(Base):
  """转帐销户请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('CashExchangeCode',ctypes.c_char)# 汇钞标志
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('TID',ctypes.c_int)# 交易ID
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',CashExchangeCode='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',TID=0,UserID='',LongCustomerName=''):

    super(ReqCancelAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.CashExchangeCode=self._to_bytes(CashExchangeCode)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.TID=int(TID)
    self.UserID=self._to_bytes(UserID)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.AccountID=self._to_bytes(i_tuple[28])
    self.Password=self._to_bytes(i_tuple[29])
    self.InstallID=int(i_tuple[30])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.CashExchangeCode=self._to_bytes(i_tuple[33])
    self.Digest=self._to_bytes(i_tuple[34])
    self.BankAccType=self._to_bytes(i_tuple[35])
    self.DeviceID=self._to_bytes(i_tuple[36])
    self.BankSecuAccType=self._to_bytes(i_tuple[37])
    self.BrokerIDByBank=self._to_bytes(i_tuple[38])
    self.BankSecuAcc=self._to_bytes(i_tuple[39])
    self.BankPwdFlag=self._to_bytes(i_tuple[40])
    self.SecuPwdFlag=self._to_bytes(i_tuple[41])
    self.OperNo=self._to_bytes(i_tuple[42])
    self.TID=int(i_tuple[43])
    self.UserID=self._to_bytes(i_tuple[44])
    self.LongCustomerName=self._to_bytes(i_tuple[45])

class ReqChangeAccountField(Base):
  """变更银行账户请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('NewBankAccount',ctypes.c_char*41)# 新银行帐号
    ,('NewBankPassWord',ctypes.c_char*41)# 新银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('TID',ctypes.c_int)# 交易ID
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',NewBankAccount='',NewBankPassWord='',AccountID='',Password='',BankAccType='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',BrokerIDByBank='',BankPwdFlag='',SecuPwdFlag='',TID=0,Digest='',LongCustomerName=''):

    super(ReqChangeAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.NewBankAccount=self._to_bytes(NewBankAccount)
    self.NewBankPassWord=self._to_bytes(NewBankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.BankAccType=self._to_bytes(BankAccType)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.TID=int(TID)
    self.Digest=self._to_bytes(Digest)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.NewBankAccount=self._to_bytes(i_tuple[28])
    self.NewBankPassWord=self._to_bytes(i_tuple[29])
    self.AccountID=self._to_bytes(i_tuple[30])
    self.Password=self._to_bytes(i_tuple[31])
    self.BankAccType=self._to_bytes(i_tuple[32])
    self.InstallID=int(i_tuple[33])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[34])
    self.CurrencyID=self._to_bytes(i_tuple[35])
    self.BrokerIDByBank=self._to_bytes(i_tuple[36])
    self.BankPwdFlag=self._to_bytes(i_tuple[37])
    self.SecuPwdFlag=self._to_bytes(i_tuple[38])
    self.TID=int(i_tuple[39])
    self.Digest=self._to_bytes(i_tuple[40])
    self.LongCustomerName=self._to_bytes(i_tuple[41])

class ReqTransferField(Base):
  """转账请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 转帐金额
    ,('FutureFetchAmount',ctypes.c_double)# 期货可取金额
    ,('FeePayFlag',ctypes.c_char)# 费用支付标志
    ,('CustFee',ctypes.c_double)# 应收客户费用
    ,('BrokerFee',ctypes.c_double)# 应收期货公司费用
    ,('Message',ctypes.c_char*129)# 发送方给接收方的消息
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('TransferStatus',ctypes.c_char)# 转账交易状态
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,FutureSerial=0,UserID='',VerifyCertNoFlag='',CurrencyID='',TradeAmount=0.0,FutureFetchAmount=0.0,FeePayFlag='',CustFee=0.0,BrokerFee=0.0,Message='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,TransferStatus='',LongCustomerName=''):

    super(ReqTransferField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.FutureSerial=int(FutureSerial)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.FutureFetchAmount=float(FutureFetchAmount)
    self.FeePayFlag=self._to_bytes(FeePayFlag)
    self.CustFee=float(CustFee)
    self.BrokerFee=float(BrokerFee)
    self.Message=self._to_bytes(Message)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.TransferStatus=self._to_bytes(TransferStatus)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.CustType=self._to_bytes(i_tuple[16])
    self.BankAccount=self._to_bytes(i_tuple[17])
    self.BankPassWord=self._to_bytes(i_tuple[18])
    self.AccountID=self._to_bytes(i_tuple[19])
    self.Password=self._to_bytes(i_tuple[20])
    self.InstallID=int(i_tuple[21])
    self.FutureSerial=int(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[24])
    self.CurrencyID=self._to_bytes(i_tuple[25])
    self.TradeAmount=float(i_tuple[26])
    self.FutureFetchAmount=float(i_tuple[27])
    self.FeePayFlag=self._to_bytes(i_tuple[28])
    self.CustFee=float(i_tuple[29])
    self.BrokerFee=float(i_tuple[30])
    self.Message=self._to_bytes(i_tuple[31])
    self.Digest=self._to_bytes(i_tuple[32])
    self.BankAccType=self._to_bytes(i_tuple[33])
    self.DeviceID=self._to_bytes(i_tuple[34])
    self.BankSecuAccType=self._to_bytes(i_tuple[35])
    self.BrokerIDByBank=self._to_bytes(i_tuple[36])
    self.BankSecuAcc=self._to_bytes(i_tuple[37])
    self.BankPwdFlag=self._to_bytes(i_tuple[38])
    self.SecuPwdFlag=self._to_bytes(i_tuple[39])
    self.OperNo=self._to_bytes(i_tuple[40])
    self.RequestID=int(i_tuple[41])
    self.TID=int(i_tuple[42])
    self.TransferStatus=self._to_bytes(i_tuple[43])
    self.LongCustomerName=self._to_bytes(i_tuple[44])

class RspTransferField(Base):
  """银行发起银行资金转期货响应"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 转帐金额
    ,('FutureFetchAmount',ctypes.c_double)# 期货可取金额
    ,('FeePayFlag',ctypes.c_char)# 费用支付标志
    ,('CustFee',ctypes.c_double)# 应收客户费用
    ,('BrokerFee',ctypes.c_double)# 应收期货公司费用
    ,('Message',ctypes.c_char*129)# 发送方给接收方的消息
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('TransferStatus',ctypes.c_char)# 转账交易状态
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,FutureSerial=0,UserID='',VerifyCertNoFlag='',CurrencyID='',TradeAmount=0.0,FutureFetchAmount=0.0,FeePayFlag='',CustFee=0.0,BrokerFee=0.0,Message='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,TransferStatus='',ErrorID=0,ErrorMsg='',LongCustomerName=''):

    super(RspTransferField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.FutureSerial=int(FutureSerial)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.FutureFetchAmount=float(FutureFetchAmount)
    self.FeePayFlag=self._to_bytes(FeePayFlag)
    self.CustFee=float(CustFee)
    self.BrokerFee=float(BrokerFee)
    self.Message=self._to_bytes(Message)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.TransferStatus=self._to_bytes(TransferStatus)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.CustType=self._to_bytes(i_tuple[16])
    self.BankAccount=self._to_bytes(i_tuple[17])
    self.BankPassWord=self._to_bytes(i_tuple[18])
    self.AccountID=self._to_bytes(i_tuple[19])
    self.Password=self._to_bytes(i_tuple[20])
    self.InstallID=int(i_tuple[21])
    self.FutureSerial=int(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[24])
    self.CurrencyID=self._to_bytes(i_tuple[25])
    self.TradeAmount=float(i_tuple[26])
    self.FutureFetchAmount=float(i_tuple[27])
    self.FeePayFlag=self._to_bytes(i_tuple[28])
    self.CustFee=float(i_tuple[29])
    self.BrokerFee=float(i_tuple[30])
    self.Message=self._to_bytes(i_tuple[31])
    self.Digest=self._to_bytes(i_tuple[32])
    self.BankAccType=self._to_bytes(i_tuple[33])
    self.DeviceID=self._to_bytes(i_tuple[34])
    self.BankSecuAccType=self._to_bytes(i_tuple[35])
    self.BrokerIDByBank=self._to_bytes(i_tuple[36])
    self.BankSecuAcc=self._to_bytes(i_tuple[37])
    self.BankPwdFlag=self._to_bytes(i_tuple[38])
    self.SecuPwdFlag=self._to_bytes(i_tuple[39])
    self.OperNo=self._to_bytes(i_tuple[40])
    self.RequestID=int(i_tuple[41])
    self.TID=int(i_tuple[42])
    self.TransferStatus=self._to_bytes(i_tuple[43])
    self.ErrorID=int(i_tuple[44])
    self.ErrorMsg=self._to_bytes(i_tuple[45])
    self.LongCustomerName=self._to_bytes(i_tuple[46])

class ReqRepealField(Base):
  """冲正请求"""
  _fields_ = [
    ('RepealTimeInterval',ctypes.c_int)# ///冲正时间间隔
    ,('RepealedTimes',ctypes.c_int)# 已经冲正次数
    ,('BankRepealFlag',ctypes.c_char)# 银行冲正标志
    ,('BrokerRepealFlag',ctypes.c_char)# 期商冲正标志
    ,('PlateRepealSerial',ctypes.c_int)# 被冲正平台流水号
    ,('BankRepealSerial',ctypes.c_char*13)# 被冲正银行流水号
    ,('FutureRepealSerial',ctypes.c_int)# 被冲正期货流水号
    ,('TradeCode',ctypes.c_char*7)# 业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 转帐金额
    ,('FutureFetchAmount',ctypes.c_double)# 期货可取金额
    ,('FeePayFlag',ctypes.c_char)# 费用支付标志
    ,('CustFee',ctypes.c_double)# 应收客户费用
    ,('BrokerFee',ctypes.c_double)# 应收期货公司费用
    ,('Message',ctypes.c_char*129)# 发送方给接收方的消息
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('TransferStatus',ctypes.c_char)# 转账交易状态
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,RepealTimeInterval= 0,RepealedTimes=0,BankRepealFlag='',BrokerRepealFlag='',PlateRepealSerial=0,BankRepealSerial='',FutureRepealSerial=0,TradeCode='',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,FutureSerial=0,UserID='',VerifyCertNoFlag='',CurrencyID='',TradeAmount=0.0,FutureFetchAmount=0.0,FeePayFlag='',CustFee=0.0,BrokerFee=0.0,Message='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,TransferStatus='',LongCustomerName=''):

    super(ReqRepealField,self).__init__()

    self.RepealTimeInterval=int(RepealTimeInterval)
    self.RepealedTimes=int(RepealedTimes)
    self.BankRepealFlag=self._to_bytes(BankRepealFlag)
    self.BrokerRepealFlag=self._to_bytes(BrokerRepealFlag)
    self.PlateRepealSerial=int(PlateRepealSerial)
    self.BankRepealSerial=self._to_bytes(BankRepealSerial)
    self.FutureRepealSerial=int(FutureRepealSerial)
    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.FutureSerial=int(FutureSerial)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.FutureFetchAmount=float(FutureFetchAmount)
    self.FeePayFlag=self._to_bytes(FeePayFlag)
    self.CustFee=float(CustFee)
    self.BrokerFee=float(BrokerFee)
    self.Message=self._to_bytes(Message)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.TransferStatus=self._to_bytes(TransferStatus)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.RepealTimeInterval=int(i_tuple[1])
    self.RepealedTimes=int(i_tuple[2])
    self.BankRepealFlag=self._to_bytes(i_tuple[3])
    self.BrokerRepealFlag=self._to_bytes(i_tuple[4])
    self.PlateRepealSerial=int(i_tuple[5])
    self.BankRepealSerial=self._to_bytes(i_tuple[6])
    self.FutureRepealSerial=int(i_tuple[7])
    self.TradeCode=self._to_bytes(i_tuple[8])
    self.BankID=self._to_bytes(i_tuple[9])
    self.BankBranchID=self._to_bytes(i_tuple[10])
    self.BrokerID=self._to_bytes(i_tuple[11])
    self.BrokerBranchID=self._to_bytes(i_tuple[12])
    self.TradeDate=self._to_bytes(i_tuple[13])
    self.TradeTime=self._to_bytes(i_tuple[14])
    self.BankSerial=self._to_bytes(i_tuple[15])
    self.TradingDay=self._to_bytes(i_tuple[16])
    self.PlateSerial=int(i_tuple[17])
    self.LastFragment=self._to_bytes(i_tuple[18])
    self.SessionID=int(i_tuple[19])
    self.CustomerName=self._to_bytes(i_tuple[20])
    self.IdCardType=self._to_bytes(i_tuple[21])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[22])
    self.CustType=self._to_bytes(i_tuple[23])
    self.BankAccount=self._to_bytes(i_tuple[24])
    self.BankPassWord=self._to_bytes(i_tuple[25])
    self.AccountID=self._to_bytes(i_tuple[26])
    self.Password=self._to_bytes(i_tuple[27])
    self.InstallID=int(i_tuple[28])
    self.FutureSerial=int(i_tuple[29])
    self.UserID=self._to_bytes(i_tuple[30])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.TradeAmount=float(i_tuple[33])
    self.FutureFetchAmount=float(i_tuple[34])
    self.FeePayFlag=self._to_bytes(i_tuple[35])
    self.CustFee=float(i_tuple[36])
    self.BrokerFee=float(i_tuple[37])
    self.Message=self._to_bytes(i_tuple[38])
    self.Digest=self._to_bytes(i_tuple[39])
    self.BankAccType=self._to_bytes(i_tuple[40])
    self.DeviceID=self._to_bytes(i_tuple[41])
    self.BankSecuAccType=self._to_bytes(i_tuple[42])
    self.BrokerIDByBank=self._to_bytes(i_tuple[43])
    self.BankSecuAcc=self._to_bytes(i_tuple[44])
    self.BankPwdFlag=self._to_bytes(i_tuple[45])
    self.SecuPwdFlag=self._to_bytes(i_tuple[46])
    self.OperNo=self._to_bytes(i_tuple[47])
    self.RequestID=int(i_tuple[48])
    self.TID=int(i_tuple[49])
    self.TransferStatus=self._to_bytes(i_tuple[50])
    self.LongCustomerName=self._to_bytes(i_tuple[51])

class RspRepealField(Base):
  """冲正响应"""
  _fields_ = [
    ('RepealTimeInterval',ctypes.c_int)# ///冲正时间间隔
    ,('RepealedTimes',ctypes.c_int)# 已经冲正次数
    ,('BankRepealFlag',ctypes.c_char)# 银行冲正标志
    ,('BrokerRepealFlag',ctypes.c_char)# 期商冲正标志
    ,('PlateRepealSerial',ctypes.c_int)# 被冲正平台流水号
    ,('BankRepealSerial',ctypes.c_char*13)# 被冲正银行流水号
    ,('FutureRepealSerial',ctypes.c_int)# 被冲正期货流水号
    ,('TradeCode',ctypes.c_char*7)# 业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 转帐金额
    ,('FutureFetchAmount',ctypes.c_double)# 期货可取金额
    ,('FeePayFlag',ctypes.c_char)# 费用支付标志
    ,('CustFee',ctypes.c_double)# 应收客户费用
    ,('BrokerFee',ctypes.c_double)# 应收期货公司费用
    ,('Message',ctypes.c_char*129)# 发送方给接收方的消息
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('TransferStatus',ctypes.c_char)# 转账交易状态
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,RepealTimeInterval= 0,RepealedTimes=0,BankRepealFlag='',BrokerRepealFlag='',PlateRepealSerial=0,BankRepealSerial='',FutureRepealSerial=0,TradeCode='',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,FutureSerial=0,UserID='',VerifyCertNoFlag='',CurrencyID='',TradeAmount=0.0,FutureFetchAmount=0.0,FeePayFlag='',CustFee=0.0,BrokerFee=0.0,Message='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,TransferStatus='',ErrorID=0,ErrorMsg='',LongCustomerName=''):

    super(RspRepealField,self).__init__()

    self.RepealTimeInterval=int(RepealTimeInterval)
    self.RepealedTimes=int(RepealedTimes)
    self.BankRepealFlag=self._to_bytes(BankRepealFlag)
    self.BrokerRepealFlag=self._to_bytes(BrokerRepealFlag)
    self.PlateRepealSerial=int(PlateRepealSerial)
    self.BankRepealSerial=self._to_bytes(BankRepealSerial)
    self.FutureRepealSerial=int(FutureRepealSerial)
    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.FutureSerial=int(FutureSerial)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.FutureFetchAmount=float(FutureFetchAmount)
    self.FeePayFlag=self._to_bytes(FeePayFlag)
    self.CustFee=float(CustFee)
    self.BrokerFee=float(BrokerFee)
    self.Message=self._to_bytes(Message)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.TransferStatus=self._to_bytes(TransferStatus)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.RepealTimeInterval=int(i_tuple[1])
    self.RepealedTimes=int(i_tuple[2])
    self.BankRepealFlag=self._to_bytes(i_tuple[3])
    self.BrokerRepealFlag=self._to_bytes(i_tuple[4])
    self.PlateRepealSerial=int(i_tuple[5])
    self.BankRepealSerial=self._to_bytes(i_tuple[6])
    self.FutureRepealSerial=int(i_tuple[7])
    self.TradeCode=self._to_bytes(i_tuple[8])
    self.BankID=self._to_bytes(i_tuple[9])
    self.BankBranchID=self._to_bytes(i_tuple[10])
    self.BrokerID=self._to_bytes(i_tuple[11])
    self.BrokerBranchID=self._to_bytes(i_tuple[12])
    self.TradeDate=self._to_bytes(i_tuple[13])
    self.TradeTime=self._to_bytes(i_tuple[14])
    self.BankSerial=self._to_bytes(i_tuple[15])
    self.TradingDay=self._to_bytes(i_tuple[16])
    self.PlateSerial=int(i_tuple[17])
    self.LastFragment=self._to_bytes(i_tuple[18])
    self.SessionID=int(i_tuple[19])
    self.CustomerName=self._to_bytes(i_tuple[20])
    self.IdCardType=self._to_bytes(i_tuple[21])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[22])
    self.CustType=self._to_bytes(i_tuple[23])
    self.BankAccount=self._to_bytes(i_tuple[24])
    self.BankPassWord=self._to_bytes(i_tuple[25])
    self.AccountID=self._to_bytes(i_tuple[26])
    self.Password=self._to_bytes(i_tuple[27])
    self.InstallID=int(i_tuple[28])
    self.FutureSerial=int(i_tuple[29])
    self.UserID=self._to_bytes(i_tuple[30])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.TradeAmount=float(i_tuple[33])
    self.FutureFetchAmount=float(i_tuple[34])
    self.FeePayFlag=self._to_bytes(i_tuple[35])
    self.CustFee=float(i_tuple[36])
    self.BrokerFee=float(i_tuple[37])
    self.Message=self._to_bytes(i_tuple[38])
    self.Digest=self._to_bytes(i_tuple[39])
    self.BankAccType=self._to_bytes(i_tuple[40])
    self.DeviceID=self._to_bytes(i_tuple[41])
    self.BankSecuAccType=self._to_bytes(i_tuple[42])
    self.BrokerIDByBank=self._to_bytes(i_tuple[43])
    self.BankSecuAcc=self._to_bytes(i_tuple[44])
    self.BankPwdFlag=self._to_bytes(i_tuple[45])
    self.SecuPwdFlag=self._to_bytes(i_tuple[46])
    self.OperNo=self._to_bytes(i_tuple[47])
    self.RequestID=int(i_tuple[48])
    self.TID=int(i_tuple[49])
    self.TransferStatus=self._to_bytes(i_tuple[50])
    self.ErrorID=int(i_tuple[51])
    self.ErrorMsg=self._to_bytes(i_tuple[52])
    self.LongCustomerName=self._to_bytes(i_tuple[53])

class ReqQueryAccountField(Base):
  """查询账户信息请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',FutureSerial=0,InstallID=0,UserID='',VerifyCertNoFlag='',CurrencyID='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,LongCustomerName=''):

    super(ReqQueryAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.FutureSerial=int(FutureSerial)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.CustType=self._to_bytes(i_tuple[16])
    self.BankAccount=self._to_bytes(i_tuple[17])
    self.BankPassWord=self._to_bytes(i_tuple[18])
    self.AccountID=self._to_bytes(i_tuple[19])
    self.Password=self._to_bytes(i_tuple[20])
    self.FutureSerial=int(i_tuple[21])
    self.InstallID=int(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[24])
    self.CurrencyID=self._to_bytes(i_tuple[25])
    self.Digest=self._to_bytes(i_tuple[26])
    self.BankAccType=self._to_bytes(i_tuple[27])
    self.DeviceID=self._to_bytes(i_tuple[28])
    self.BankSecuAccType=self._to_bytes(i_tuple[29])
    self.BrokerIDByBank=self._to_bytes(i_tuple[30])
    self.BankSecuAcc=self._to_bytes(i_tuple[31])
    self.BankPwdFlag=self._to_bytes(i_tuple[32])
    self.SecuPwdFlag=self._to_bytes(i_tuple[33])
    self.OperNo=self._to_bytes(i_tuple[34])
    self.RequestID=int(i_tuple[35])
    self.TID=int(i_tuple[36])
    self.LongCustomerName=self._to_bytes(i_tuple[37])

class RspQueryAccountField(Base):
  """查询账户信息响应"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('BankUseAmount',ctypes.c_double)# 银行可用金额
    ,('BankFetchAmount',ctypes.c_double)# 银行可取金额
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',FutureSerial=0,InstallID=0,UserID='',VerifyCertNoFlag='',CurrencyID='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,BankUseAmount=0.0,BankFetchAmount=0.0,LongCustomerName=''):

    super(RspQueryAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.FutureSerial=int(FutureSerial)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.BankUseAmount=float(BankUseAmount)
    self.BankFetchAmount=float(BankFetchAmount)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.CustType=self._to_bytes(i_tuple[16])
    self.BankAccount=self._to_bytes(i_tuple[17])
    self.BankPassWord=self._to_bytes(i_tuple[18])
    self.AccountID=self._to_bytes(i_tuple[19])
    self.Password=self._to_bytes(i_tuple[20])
    self.FutureSerial=int(i_tuple[21])
    self.InstallID=int(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[24])
    self.CurrencyID=self._to_bytes(i_tuple[25])
    self.Digest=self._to_bytes(i_tuple[26])
    self.BankAccType=self._to_bytes(i_tuple[27])
    self.DeviceID=self._to_bytes(i_tuple[28])
    self.BankSecuAccType=self._to_bytes(i_tuple[29])
    self.BrokerIDByBank=self._to_bytes(i_tuple[30])
    self.BankSecuAcc=self._to_bytes(i_tuple[31])
    self.BankPwdFlag=self._to_bytes(i_tuple[32])
    self.SecuPwdFlag=self._to_bytes(i_tuple[33])
    self.OperNo=self._to_bytes(i_tuple[34])
    self.RequestID=int(i_tuple[35])
    self.TID=int(i_tuple[36])
    self.BankUseAmount=float(i_tuple[37])
    self.BankFetchAmount=float(i_tuple[38])
    self.LongCustomerName=self._to_bytes(i_tuple[39])

class FutureSignIOField(Base):
  """期商签到签退"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Digest='',CurrencyID='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0):

    super(FutureSignIOField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Digest=self._to_bytes(Digest)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Digest=self._to_bytes(i_tuple[15])
    self.CurrencyID=self._to_bytes(i_tuple[16])
    self.DeviceID=self._to_bytes(i_tuple[17])
    self.BrokerIDByBank=self._to_bytes(i_tuple[18])
    self.OperNo=self._to_bytes(i_tuple[19])
    self.RequestID=int(i_tuple[20])
    self.TID=int(i_tuple[21])

class RspFutureSignInField(Base):
  """期商签到响应"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('PinKey',ctypes.c_char*129)# PIN密钥
    ,('MacKey',ctypes.c_char*129)# MAC密钥
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Digest='',CurrencyID='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0,ErrorID=0,ErrorMsg='',PinKey='',MacKey=''):

    super(RspFutureSignInField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Digest=self._to_bytes(Digest)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.PinKey=self._to_bytes(PinKey)
    self.MacKey=self._to_bytes(MacKey)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Digest=self._to_bytes(i_tuple[15])
    self.CurrencyID=self._to_bytes(i_tuple[16])
    self.DeviceID=self._to_bytes(i_tuple[17])
    self.BrokerIDByBank=self._to_bytes(i_tuple[18])
    self.OperNo=self._to_bytes(i_tuple[19])
    self.RequestID=int(i_tuple[20])
    self.TID=int(i_tuple[21])
    self.ErrorID=int(i_tuple[22])
    self.ErrorMsg=self._to_bytes(i_tuple[23])
    self.PinKey=self._to_bytes(i_tuple[24])
    self.MacKey=self._to_bytes(i_tuple[25])

class ReqFutureSignOutField(Base):
  """期商签退请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Digest='',CurrencyID='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0):

    super(ReqFutureSignOutField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Digest=self._to_bytes(Digest)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Digest=self._to_bytes(i_tuple[15])
    self.CurrencyID=self._to_bytes(i_tuple[16])
    self.DeviceID=self._to_bytes(i_tuple[17])
    self.BrokerIDByBank=self._to_bytes(i_tuple[18])
    self.OperNo=self._to_bytes(i_tuple[19])
    self.RequestID=int(i_tuple[20])
    self.TID=int(i_tuple[21])

class RspFutureSignOutField(Base):
  """期商签退响应"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Digest='',CurrencyID='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0,ErrorID=0,ErrorMsg=''):

    super(RspFutureSignOutField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Digest=self._to_bytes(Digest)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Digest=self._to_bytes(i_tuple[15])
    self.CurrencyID=self._to_bytes(i_tuple[16])
    self.DeviceID=self._to_bytes(i_tuple[17])
    self.BrokerIDByBank=self._to_bytes(i_tuple[18])
    self.OperNo=self._to_bytes(i_tuple[19])
    self.RequestID=int(i_tuple[20])
    self.TID=int(i_tuple[21])
    self.ErrorID=int(i_tuple[22])
    self.ErrorMsg=self._to_bytes(i_tuple[23])

class ReqQueryTradeResultBySerialField(Base):
  """查询指定流水号的交易结果请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('Reference',ctypes.c_int)# 流水号
    ,('RefrenceIssureType',ctypes.c_char)# 本流水号发布者的机构类型
    ,('RefrenceIssure',ctypes.c_char*36)# 本流水号发布者机构编码
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 转帐金额
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,Reference=0,RefrenceIssureType='',RefrenceIssure='',CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',CurrencyID='',TradeAmount=0.0,Digest='',LongCustomerName=''):

    super(ReqQueryTradeResultBySerialField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.Reference=int(Reference)
    self.RefrenceIssureType=self._to_bytes(RefrenceIssureType)
    self.RefrenceIssure=self._to_bytes(RefrenceIssure)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.Digest=self._to_bytes(Digest)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.Reference=int(i_tuple[13])
    self.RefrenceIssureType=self._to_bytes(i_tuple[14])
    self.RefrenceIssure=self._to_bytes(i_tuple[15])
    self.CustomerName=self._to_bytes(i_tuple[16])
    self.IdCardType=self._to_bytes(i_tuple[17])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[18])
    self.CustType=self._to_bytes(i_tuple[19])
    self.BankAccount=self._to_bytes(i_tuple[20])
    self.BankPassWord=self._to_bytes(i_tuple[21])
    self.AccountID=self._to_bytes(i_tuple[22])
    self.Password=self._to_bytes(i_tuple[23])
    self.CurrencyID=self._to_bytes(i_tuple[24])
    self.TradeAmount=float(i_tuple[25])
    self.Digest=self._to_bytes(i_tuple[26])
    self.LongCustomerName=self._to_bytes(i_tuple[27])

class RspQueryTradeResultBySerialField(Base):
  """查询指定流水号的交易结果响应"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('Reference',ctypes.c_int)# 流水号
    ,('RefrenceIssureType',ctypes.c_char)# 本流水号发布者的机构类型
    ,('RefrenceIssure',ctypes.c_char*36)# 本流水号发布者机构编码
    ,('OriginReturnCode',ctypes.c_char*7)# 原始返回代码
    ,('OriginDescrInfoForReturnCode',ctypes.c_char*129)# 原始返回码描述
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 转帐金额
    ,('Digest',ctypes.c_char*36)# 摘要
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,ErrorID=0,ErrorMsg='',Reference=0,RefrenceIssureType='',RefrenceIssure='',OriginReturnCode='',OriginDescrInfoForReturnCode='',BankAccount='',BankPassWord='',AccountID='',Password='',CurrencyID='',TradeAmount=0.0,Digest=''):

    super(RspQueryTradeResultBySerialField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.Reference=int(Reference)
    self.RefrenceIssureType=self._to_bytes(RefrenceIssureType)
    self.RefrenceIssure=self._to_bytes(RefrenceIssure)
    self.OriginReturnCode=self._to_bytes(OriginReturnCode)
    self.OriginDescrInfoForReturnCode=self._to_bytes(OriginDescrInfoForReturnCode)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.Digest=self._to_bytes(Digest)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.ErrorID=int(i_tuple[13])
    self.ErrorMsg=self._to_bytes(i_tuple[14])
    self.Reference=int(i_tuple[15])
    self.RefrenceIssureType=self._to_bytes(i_tuple[16])
    self.RefrenceIssure=self._to_bytes(i_tuple[17])
    self.OriginReturnCode=self._to_bytes(i_tuple[18])
    self.OriginDescrInfoForReturnCode=self._to_bytes(i_tuple[19])
    self.BankAccount=self._to_bytes(i_tuple[20])
    self.BankPassWord=self._to_bytes(i_tuple[21])
    self.AccountID=self._to_bytes(i_tuple[22])
    self.Password=self._to_bytes(i_tuple[23])
    self.CurrencyID=self._to_bytes(i_tuple[24])
    self.TradeAmount=float(i_tuple[25])
    self.Digest=self._to_bytes(i_tuple[26])

class ReqDayEndFileReadyField(Base):
  """日终文件就绪请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('FileBusinessCode',ctypes.c_char)# 文件业务功能
    ,('Digest',ctypes.c_char*36)# 摘要
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,FileBusinessCode='',Digest=''):

    super(ReqDayEndFileReadyField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.FileBusinessCode=self._to_bytes(FileBusinessCode)
    self.Digest=self._to_bytes(Digest)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.FileBusinessCode=self._to_bytes(i_tuple[13])
    self.Digest=self._to_bytes(i_tuple[14])

class ReturnResultField(Base):
  """返回结果"""
  _fields_ = [
    ('ReturnCode',ctypes.c_char*7)# ///返回代码
    ,('DescrInfoForReturnCode',ctypes.c_char*129)# 返回码描述
]

  def __init__(self,ReturnCode= '',DescrInfoForReturnCode=''):

    super(ReturnResultField,self).__init__()

    self.ReturnCode=self._to_bytes(ReturnCode)
    self.DescrInfoForReturnCode=self._to_bytes(DescrInfoForReturnCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.ReturnCode=self._to_bytes(i_tuple[1])
    self.DescrInfoForReturnCode=self._to_bytes(i_tuple[2])

class VerifyFuturePasswordField(Base):
  """验证期货资金密码"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,AccountID='',Password='',BankAccount='',BankPassWord='',InstallID=0,TID=0,CurrencyID=''):

    super(VerifyFuturePasswordField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.InstallID=int(InstallID)
    self.TID=int(TID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.AccountID=self._to_bytes(i_tuple[13])
    self.Password=self._to_bytes(i_tuple[14])
    self.BankAccount=self._to_bytes(i_tuple[15])
    self.BankPassWord=self._to_bytes(i_tuple[16])
    self.InstallID=int(i_tuple[17])
    self.TID=int(i_tuple[18])
    self.CurrencyID=self._to_bytes(i_tuple[19])

class VerifyCustInfoField(Base):
  """验证客户信息"""
  _fields_ = [
    ('CustomerName',ctypes.c_char*51)# ///客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,CustomerName= '',IdCardType='',IdentifiedCardNo='',CustType='',LongCustomerName=''):

    super(VerifyCustInfoField,self).__init__()

    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.CustomerName=self._to_bytes(i_tuple[1])
    self.IdCardType=self._to_bytes(i_tuple[2])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[3])
    self.CustType=self._to_bytes(i_tuple[4])
    self.LongCustomerName=self._to_bytes(i_tuple[5])

class VerifyFuturePasswordAndCustInfoField(Base):
  """验证期货资金密码和客户信息"""
  _fields_ = [
    ('CustomerName',ctypes.c_char*51)# ///客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,CustomerName= '',IdCardType='',IdentifiedCardNo='',CustType='',AccountID='',Password='',CurrencyID='',LongCustomerName=''):

    super(VerifyFuturePasswordAndCustInfoField,self).__init__()

    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.CustomerName=self._to_bytes(i_tuple[1])
    self.IdCardType=self._to_bytes(i_tuple[2])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[3])
    self.CustType=self._to_bytes(i_tuple[4])
    self.AccountID=self._to_bytes(i_tuple[5])
    self.Password=self._to_bytes(i_tuple[6])
    self.CurrencyID=self._to_bytes(i_tuple[7])
    self.LongCustomerName=self._to_bytes(i_tuple[8])

class DepositResultInformField(Base):
  """验证期货资金密码和客户信息"""
  _fields_ = [
    ('DepositSeqNo',ctypes.c_char*15)# ///出入金流水号，该流水号为银期报盘返回的流水号
    ,('BrokerID',ctypes.c_char*11)# 经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('Deposit',ctypes.c_double)# 入金金额
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('ReturnCode',ctypes.c_char*7)# 返回代码
    ,('DescrInfoForReturnCode',ctypes.c_char*129)# 返回码描述
]

  def __init__(self,DepositSeqNo= '',BrokerID='',InvestorID='',Deposit=0.0,RequestID=0,ReturnCode='',DescrInfoForReturnCode=''):

    super(DepositResultInformField,self).__init__()

    self.DepositSeqNo=self._to_bytes(DepositSeqNo)
    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.Deposit=float(Deposit)
    self.RequestID=int(RequestID)
    self.ReturnCode=self._to_bytes(ReturnCode)
    self.DescrInfoForReturnCode=self._to_bytes(DescrInfoForReturnCode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.DepositSeqNo=self._to_bytes(i_tuple[1])
    self.BrokerID=self._to_bytes(i_tuple[2])
    self.InvestorID=self._to_bytes(i_tuple[3])
    self.Deposit=float(i_tuple[4])
    self.RequestID=int(i_tuple[5])
    self.ReturnCode=self._to_bytes(i_tuple[6])
    self.DescrInfoForReturnCode=self._to_bytes(i_tuple[7])

class ReqSyncKeyField(Base):
  """交易核心向银期报盘发出密钥同步请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Message',ctypes.c_char*129)# 交易核心给银期报盘的消息
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Message='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0):

    super(ReqSyncKeyField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Message=self._to_bytes(Message)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Message=self._to_bytes(i_tuple[15])
    self.DeviceID=self._to_bytes(i_tuple[16])
    self.BrokerIDByBank=self._to_bytes(i_tuple[17])
    self.OperNo=self._to_bytes(i_tuple[18])
    self.RequestID=int(i_tuple[19])
    self.TID=int(i_tuple[20])

class RspSyncKeyField(Base):
  """交易核心向银期报盘发出密钥同步响应"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Message',ctypes.c_char*129)# 交易核心给银期报盘的消息
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Message='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0,ErrorID=0,ErrorMsg=''):

    super(RspSyncKeyField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Message=self._to_bytes(Message)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Message=self._to_bytes(i_tuple[15])
    self.DeviceID=self._to_bytes(i_tuple[16])
    self.BrokerIDByBank=self._to_bytes(i_tuple[17])
    self.OperNo=self._to_bytes(i_tuple[18])
    self.RequestID=int(i_tuple[19])
    self.TID=int(i_tuple[20])
    self.ErrorID=int(i_tuple[21])
    self.ErrorMsg=self._to_bytes(i_tuple[22])

class NotifyQueryAccountField(Base):
  """查询账户信息通知"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('BankUseAmount',ctypes.c_double)# 银行可用金额
    ,('BankFetchAmount',ctypes.c_double)# 银行可取金额
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',CustType='',BankAccount='',BankPassWord='',AccountID='',Password='',FutureSerial=0,InstallID=0,UserID='',VerifyCertNoFlag='',CurrencyID='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',RequestID=0,TID=0,BankUseAmount=0.0,BankFetchAmount=0.0,ErrorID=0,ErrorMsg='',LongCustomerName=''):

    super(NotifyQueryAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustType=self._to_bytes(CustType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.FutureSerial=int(FutureSerial)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.BankUseAmount=float(BankUseAmount)
    self.BankFetchAmount=float(BankFetchAmount)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.CustType=self._to_bytes(i_tuple[16])
    self.BankAccount=self._to_bytes(i_tuple[17])
    self.BankPassWord=self._to_bytes(i_tuple[18])
    self.AccountID=self._to_bytes(i_tuple[19])
    self.Password=self._to_bytes(i_tuple[20])
    self.FutureSerial=int(i_tuple[21])
    self.InstallID=int(i_tuple[22])
    self.UserID=self._to_bytes(i_tuple[23])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[24])
    self.CurrencyID=self._to_bytes(i_tuple[25])
    self.Digest=self._to_bytes(i_tuple[26])
    self.BankAccType=self._to_bytes(i_tuple[27])
    self.DeviceID=self._to_bytes(i_tuple[28])
    self.BankSecuAccType=self._to_bytes(i_tuple[29])
    self.BrokerIDByBank=self._to_bytes(i_tuple[30])
    self.BankSecuAcc=self._to_bytes(i_tuple[31])
    self.BankPwdFlag=self._to_bytes(i_tuple[32])
    self.SecuPwdFlag=self._to_bytes(i_tuple[33])
    self.OperNo=self._to_bytes(i_tuple[34])
    self.RequestID=int(i_tuple[35])
    self.TID=int(i_tuple[36])
    self.BankUseAmount=float(i_tuple[37])
    self.BankFetchAmount=float(i_tuple[38])
    self.ErrorID=int(i_tuple[39])
    self.ErrorMsg=self._to_bytes(i_tuple[40])
    self.LongCustomerName=self._to_bytes(i_tuple[41])

class TransferSerialField(Base):
  """银期转账交易流水表"""
  _fields_ = [
    ('PlateSerial',ctypes.c_int)# ///平台流水号
    ,('TradeDate',ctypes.c_char*9)# 交易发起方日期
    ,('TradingDay',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('TradeCode',ctypes.c_char*7)# 交易代码
    ,('SessionID',ctypes.c_int)# 会话编号
    ,('BankID',ctypes.c_char*4)# 银行编码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构编码
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('BrokerID',ctypes.c_char*11)# 期货公司编码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('FutureAccType',ctypes.c_char)# 期货公司帐号类型
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
    ,('FutureSerial',ctypes.c_int)# 期货公司流水号
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('TradeAmount',ctypes.c_double)# 交易金额
    ,('CustFee',ctypes.c_double)# 应收客户费用
    ,('BrokerFee',ctypes.c_double)# 应收期货公司费用
    ,('AvailabilityFlag',ctypes.c_char)# 有效标志
    ,('OperatorCode',ctypes.c_char*17)# 操作员
    ,('BankNewAccount',ctypes.c_char*41)# 新银行帐号
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,PlateSerial= 0,TradeDate='',TradingDay='',TradeTime='',TradeCode='',SessionID=0,BankID='',BankBranchID='',BankAccType='',BankAccount='',BankSerial='',BrokerID='',BrokerBranchID='',FutureAccType='',AccountID='',InvestorID='',FutureSerial=0,IdCardType='',IdentifiedCardNo='',CurrencyID='',TradeAmount=0.0,CustFee=0.0,BrokerFee=0.0,AvailabilityFlag='',OperatorCode='',BankNewAccount='',ErrorID=0,ErrorMsg=''):

    super(TransferSerialField,self).__init__()

    self.PlateSerial=int(PlateSerial)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradingDay=self._to_bytes(TradingDay)
    self.TradeTime=self._to_bytes(TradeTime)
    self.TradeCode=self._to_bytes(TradeCode)
    self.SessionID=int(SessionID)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BankAccType=self._to_bytes(BankAccType)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankSerial=self._to_bytes(BankSerial)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.FutureAccType=self._to_bytes(FutureAccType)
    self.AccountID=self._to_bytes(AccountID)
    self.InvestorID=self._to_bytes(InvestorID)
    self.FutureSerial=int(FutureSerial)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.TradeAmount=float(TradeAmount)
    self.CustFee=float(CustFee)
    self.BrokerFee=float(BrokerFee)
    self.AvailabilityFlag=self._to_bytes(AvailabilityFlag)
    self.OperatorCode=self._to_bytes(OperatorCode)
    self.BankNewAccount=self._to_bytes(BankNewAccount)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.PlateSerial=int(i_tuple[1])
    self.TradeDate=self._to_bytes(i_tuple[2])
    self.TradingDay=self._to_bytes(i_tuple[3])
    self.TradeTime=self._to_bytes(i_tuple[4])
    self.TradeCode=self._to_bytes(i_tuple[5])
    self.SessionID=int(i_tuple[6])
    self.BankID=self._to_bytes(i_tuple[7])
    self.BankBranchID=self._to_bytes(i_tuple[8])
    self.BankAccType=self._to_bytes(i_tuple[9])
    self.BankAccount=self._to_bytes(i_tuple[10])
    self.BankSerial=self._to_bytes(i_tuple[11])
    self.BrokerID=self._to_bytes(i_tuple[12])
    self.BrokerBranchID=self._to_bytes(i_tuple[13])
    self.FutureAccType=self._to_bytes(i_tuple[14])
    self.AccountID=self._to_bytes(i_tuple[15])
    self.InvestorID=self._to_bytes(i_tuple[16])
    self.FutureSerial=int(i_tuple[17])
    self.IdCardType=self._to_bytes(i_tuple[18])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[19])
    self.CurrencyID=self._to_bytes(i_tuple[20])
    self.TradeAmount=float(i_tuple[21])
    self.CustFee=float(i_tuple[22])
    self.BrokerFee=float(i_tuple[23])
    self.AvailabilityFlag=self._to_bytes(i_tuple[24])
    self.OperatorCode=self._to_bytes(i_tuple[25])
    self.BankNewAccount=self._to_bytes(i_tuple[26])
    self.ErrorID=int(i_tuple[27])
    self.ErrorMsg=self._to_bytes(i_tuple[28])

class QryTransferSerialField(Base):
  """请求查询转帐流水"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('BankID',ctypes.c_char*4)# 银行编码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',BankID='',CurrencyID=''):

    super(QryTransferSerialField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.BankID=self._to_bytes(BankID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.BankID=self._to_bytes(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])

class NotifyFutureSignInField(Base):
  """期商签到通知"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('PinKey',ctypes.c_char*129)# PIN密钥
    ,('MacKey',ctypes.c_char*129)# MAC密钥
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Digest='',CurrencyID='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0,ErrorID=0,ErrorMsg='',PinKey='',MacKey=''):

    super(NotifyFutureSignInField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Digest=self._to_bytes(Digest)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.PinKey=self._to_bytes(PinKey)
    self.MacKey=self._to_bytes(MacKey)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Digest=self._to_bytes(i_tuple[15])
    self.CurrencyID=self._to_bytes(i_tuple[16])
    self.DeviceID=self._to_bytes(i_tuple[17])
    self.BrokerIDByBank=self._to_bytes(i_tuple[18])
    self.OperNo=self._to_bytes(i_tuple[19])
    self.RequestID=int(i_tuple[20])
    self.TID=int(i_tuple[21])
    self.ErrorID=int(i_tuple[22])
    self.ErrorMsg=self._to_bytes(i_tuple[23])
    self.PinKey=self._to_bytes(i_tuple[24])
    self.MacKey=self._to_bytes(i_tuple[25])

class NotifyFutureSignOutField(Base):
  """期商签退通知"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Digest='',CurrencyID='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0,ErrorID=0,ErrorMsg=''):

    super(NotifyFutureSignOutField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Digest=self._to_bytes(Digest)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Digest=self._to_bytes(i_tuple[15])
    self.CurrencyID=self._to_bytes(i_tuple[16])
    self.DeviceID=self._to_bytes(i_tuple[17])
    self.BrokerIDByBank=self._to_bytes(i_tuple[18])
    self.OperNo=self._to_bytes(i_tuple[19])
    self.RequestID=int(i_tuple[20])
    self.TID=int(i_tuple[21])
    self.ErrorID=int(i_tuple[22])
    self.ErrorMsg=self._to_bytes(i_tuple[23])

class NotifySyncKeyField(Base):
  """交易核心向银期报盘发出密钥同步处理结果的通知"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('Message',ctypes.c_char*129)# 交易核心给银期报盘的消息
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('RequestID',ctypes.c_int)# 请求编号
    ,('TID',ctypes.c_int)# 交易ID
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,InstallID=0,UserID='',Message='',DeviceID='',BrokerIDByBank='',OperNo='',RequestID=0,TID=0,ErrorID=0,ErrorMsg=''):

    super(NotifySyncKeyField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.InstallID=int(InstallID)
    self.UserID=self._to_bytes(UserID)
    self.Message=self._to_bytes(Message)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.OperNo=self._to_bytes(OperNo)
    self.RequestID=int(RequestID)
    self.TID=int(TID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.InstallID=int(i_tuple[13])
    self.UserID=self._to_bytes(i_tuple[14])
    self.Message=self._to_bytes(i_tuple[15])
    self.DeviceID=self._to_bytes(i_tuple[16])
    self.BrokerIDByBank=self._to_bytes(i_tuple[17])
    self.OperNo=self._to_bytes(i_tuple[18])
    self.RequestID=int(i_tuple[19])
    self.TID=int(i_tuple[20])
    self.ErrorID=int(i_tuple[21])
    self.ErrorMsg=self._to_bytes(i_tuple[22])

class QryAccountregisterField(Base):
  """请求查询银期签约关系"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('BankID',ctypes.c_char*4)# 银行编码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构编码
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',BankID='',BankBranchID='',CurrencyID=''):

    super(QryAccountregisterField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.BankID=self._to_bytes(i_tuple[3])
    self.BankBranchID=self._to_bytes(i_tuple[4])
    self.CurrencyID=self._to_bytes(i_tuple[5])

class AccountregisterField(Base):
  """客户开销户信息表"""
  _fields_ = [
    ('TradeDay',ctypes.c_char*9)# ///交易日期
    ,('BankID',ctypes.c_char*4)# 银行编码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构编码
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BrokerID',ctypes.c_char*11)# 期货公司编码
    ,('BrokerBranchID',ctypes.c_char*31)# 期货公司分支机构编码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('OpenOrDestroy',ctypes.c_char)# 开销户类别
    ,('RegDate',ctypes.c_char*9)# 签约日期
    ,('OutDate',ctypes.c_char*9)# 解约日期
    ,('TID',ctypes.c_int)# 交易ID
    ,('CustType',ctypes.c_char)# 客户类型
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeDay= '',BankID='',BankBranchID='',BankAccount='',BrokerID='',BrokerBranchID='',AccountID='',IdCardType='',IdentifiedCardNo='',CustomerName='',CurrencyID='',OpenOrDestroy='',RegDate='',OutDate='',TID=0,CustType='',BankAccType='',LongCustomerName=''):

    super(AccountregisterField,self).__init__()

    self.TradeDay=self._to_bytes(TradeDay)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.AccountID=self._to_bytes(AccountID)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.CustomerName=self._to_bytes(CustomerName)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.OpenOrDestroy=self._to_bytes(OpenOrDestroy)
    self.RegDate=self._to_bytes(RegDate)
    self.OutDate=self._to_bytes(OutDate)
    self.TID=int(TID)
    self.CustType=self._to_bytes(CustType)
    self.BankAccType=self._to_bytes(BankAccType)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeDay=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BankAccount=self._to_bytes(i_tuple[4])
    self.BrokerID=self._to_bytes(i_tuple[5])
    self.BrokerBranchID=self._to_bytes(i_tuple[6])
    self.AccountID=self._to_bytes(i_tuple[7])
    self.IdCardType=self._to_bytes(i_tuple[8])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[9])
    self.CustomerName=self._to_bytes(i_tuple[10])
    self.CurrencyID=self._to_bytes(i_tuple[11])
    self.OpenOrDestroy=self._to_bytes(i_tuple[12])
    self.RegDate=self._to_bytes(i_tuple[13])
    self.OutDate=self._to_bytes(i_tuple[14])
    self.TID=int(i_tuple[15])
    self.CustType=self._to_bytes(i_tuple[16])
    self.BankAccType=self._to_bytes(i_tuple[17])
    self.LongCustomerName=self._to_bytes(i_tuple[18])

class OpenAccountField(Base):
  """银期开户信息"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('CashExchangeCode',ctypes.c_char)# 汇钞标志
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('TID',ctypes.c_int)# 交易ID
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',CashExchangeCode='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',TID=0,UserID='',ErrorID=0,ErrorMsg='',LongCustomerName=''):

    super(OpenAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.CashExchangeCode=self._to_bytes(CashExchangeCode)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.TID=int(TID)
    self.UserID=self._to_bytes(UserID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.AccountID=self._to_bytes(i_tuple[28])
    self.Password=self._to_bytes(i_tuple[29])
    self.InstallID=int(i_tuple[30])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.CashExchangeCode=self._to_bytes(i_tuple[33])
    self.Digest=self._to_bytes(i_tuple[34])
    self.BankAccType=self._to_bytes(i_tuple[35])
    self.DeviceID=self._to_bytes(i_tuple[36])
    self.BankSecuAccType=self._to_bytes(i_tuple[37])
    self.BrokerIDByBank=self._to_bytes(i_tuple[38])
    self.BankSecuAcc=self._to_bytes(i_tuple[39])
    self.BankPwdFlag=self._to_bytes(i_tuple[40])
    self.SecuPwdFlag=self._to_bytes(i_tuple[41])
    self.OperNo=self._to_bytes(i_tuple[42])
    self.TID=int(i_tuple[43])
    self.UserID=self._to_bytes(i_tuple[44])
    self.ErrorID=int(i_tuple[45])
    self.ErrorMsg=self._to_bytes(i_tuple[46])
    self.LongCustomerName=self._to_bytes(i_tuple[47])

class CancelAccountField(Base):
  """银期销户信息"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('CashExchangeCode',ctypes.c_char)# 汇钞标志
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('DeviceID',ctypes.c_char*3)# 渠道标志
    ,('BankSecuAccType',ctypes.c_char)# 期货单位帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankSecuAcc',ctypes.c_char*41)# 期货单位帐号
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('OperNo',ctypes.c_char*17)# 交易柜员
    ,('TID',ctypes.c_int)# 交易ID
    ,('UserID',ctypes.c_char*16)# 用户标识
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',AccountID='',Password='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',CashExchangeCode='',Digest='',BankAccType='',DeviceID='',BankSecuAccType='',BrokerIDByBank='',BankSecuAcc='',BankPwdFlag='',SecuPwdFlag='',OperNo='',TID=0,UserID='',ErrorID=0,ErrorMsg='',LongCustomerName=''):

    super(CancelAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.CashExchangeCode=self._to_bytes(CashExchangeCode)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.DeviceID=self._to_bytes(DeviceID)
    self.BankSecuAccType=self._to_bytes(BankSecuAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankSecuAcc=self._to_bytes(BankSecuAcc)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.OperNo=self._to_bytes(OperNo)
    self.TID=int(TID)
    self.UserID=self._to_bytes(UserID)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.AccountID=self._to_bytes(i_tuple[28])
    self.Password=self._to_bytes(i_tuple[29])
    self.InstallID=int(i_tuple[30])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[31])
    self.CurrencyID=self._to_bytes(i_tuple[32])
    self.CashExchangeCode=self._to_bytes(i_tuple[33])
    self.Digest=self._to_bytes(i_tuple[34])
    self.BankAccType=self._to_bytes(i_tuple[35])
    self.DeviceID=self._to_bytes(i_tuple[36])
    self.BankSecuAccType=self._to_bytes(i_tuple[37])
    self.BrokerIDByBank=self._to_bytes(i_tuple[38])
    self.BankSecuAcc=self._to_bytes(i_tuple[39])
    self.BankPwdFlag=self._to_bytes(i_tuple[40])
    self.SecuPwdFlag=self._to_bytes(i_tuple[41])
    self.OperNo=self._to_bytes(i_tuple[42])
    self.TID=int(i_tuple[43])
    self.UserID=self._to_bytes(i_tuple[44])
    self.ErrorID=int(i_tuple[45])
    self.ErrorMsg=self._to_bytes(i_tuple[46])
    self.LongCustomerName=self._to_bytes(i_tuple[47])

class ChangeAccountField(Base):
  """银期变更银行账号信息"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*51)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('NewBankAccount',ctypes.c_char*41)# 新银行帐号
    ,('NewBankPassWord',ctypes.c_char*41)# 新银行密码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('BankPwdFlag',ctypes.c_char)# 银行密码标志
    ,('SecuPwdFlag',ctypes.c_char)# 期货资金密码核对标志
    ,('TID',ctypes.c_int)# 交易ID
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
    ,('LongCustomerName',ctypes.c_char*161)# 长客户姓名
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',NewBankAccount='',NewBankPassWord='',AccountID='',Password='',BankAccType='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',BrokerIDByBank='',BankPwdFlag='',SecuPwdFlag='',TID=0,Digest='',ErrorID=0,ErrorMsg='',LongCustomerName=''):

    super(ChangeAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.NewBankAccount=self._to_bytes(NewBankAccount)
    self.NewBankPassWord=self._to_bytes(NewBankPassWord)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.BankAccType=self._to_bytes(BankAccType)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.BankPwdFlag=self._to_bytes(BankPwdFlag)
    self.SecuPwdFlag=self._to_bytes(SecuPwdFlag)
    self.TID=int(TID)
    self.Digest=self._to_bytes(Digest)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
    self.LongCustomerName=self._to_bytes(LongCustomerName)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.NewBankAccount=self._to_bytes(i_tuple[28])
    self.NewBankPassWord=self._to_bytes(i_tuple[29])
    self.AccountID=self._to_bytes(i_tuple[30])
    self.Password=self._to_bytes(i_tuple[31])
    self.BankAccType=self._to_bytes(i_tuple[32])
    self.InstallID=int(i_tuple[33])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[34])
    self.CurrencyID=self._to_bytes(i_tuple[35])
    self.BrokerIDByBank=self._to_bytes(i_tuple[36])
    self.BankPwdFlag=self._to_bytes(i_tuple[37])
    self.SecuPwdFlag=self._to_bytes(i_tuple[38])
    self.TID=int(i_tuple[39])
    self.Digest=self._to_bytes(i_tuple[40])
    self.ErrorID=int(i_tuple[41])
    self.ErrorMsg=self._to_bytes(i_tuple[42])
    self.LongCustomerName=self._to_bytes(i_tuple[43])

class SecAgentACIDMapField(Base):
  """二级代理操作员银期权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('AccountID',ctypes.c_char*13)# 资金账户
    ,('CurrencyID',ctypes.c_char*4)# 币种
    ,('BrokerSecAgentID',ctypes.c_char*13)# 境外中介机构资金帐号
]

  def __init__(self,BrokerID= '',UserID='',AccountID='',CurrencyID='',BrokerSecAgentID=''):

    super(SecAgentACIDMapField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.BrokerSecAgentID=self._to_bytes(BrokerSecAgentID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.AccountID=self._to_bytes(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])
    self.BrokerSecAgentID=self._to_bytes(i_tuple[5])

class QrySecAgentACIDMapField(Base):
  """二级代理操作员银期权限查询"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('AccountID',ctypes.c_char*13)# 资金账户
    ,('CurrencyID',ctypes.c_char*4)# 币种
]

  def __init__(self,BrokerID= '',UserID='',AccountID='',CurrencyID=''):

    super(QrySecAgentACIDMapField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.AccountID=self._to_bytes(AccountID)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.AccountID=self._to_bytes(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])

class UserRightsAssignField(Base):
  """灾备中心交易权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///应用单元代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('DRIdentityID',ctypes.c_int)# 交易中心代码
]

  def __init__(self,BrokerID= '',UserID='',DRIdentityID=0):

    super(UserRightsAssignField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.DRIdentityID=int(DRIdentityID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.DRIdentityID=int(i_tuple[3])

class BrokerUserRightAssignField(Base):
  """经济公司是否有在本标示的交易权限"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///应用单元代码
    ,('DRIdentityID',ctypes.c_int)# 交易中心代码
    ,('Tradeable',ctypes.c_int)# 能否交易
]

  def __init__(self,BrokerID= '',DRIdentityID=0,Tradeable=0):

    super(BrokerUserRightAssignField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.DRIdentityID=int(DRIdentityID)
    self.Tradeable=int(Tradeable)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.DRIdentityID=int(i_tuple[2])
    self.Tradeable=int(i_tuple[3])

class DRTransferField(Base):
  """灾备交易转换报文"""
  _fields_ = [
    ('OrigDRIdentityID',ctypes.c_int)# ///原交易中心代码
    ,('DestDRIdentityID',ctypes.c_int)# 目标交易中心代码
    ,('OrigBrokerID',ctypes.c_char*11)# 原应用单元代码
    ,('DestBrokerID',ctypes.c_char*11)# 目标易用单元代码
]

  def __init__(self,OrigDRIdentityID= 0,DestDRIdentityID=0,OrigBrokerID='',DestBrokerID=''):

    super(DRTransferField,self).__init__()

    self.OrigDRIdentityID=int(OrigDRIdentityID)
    self.DestDRIdentityID=int(DestDRIdentityID)
    self.OrigBrokerID=self._to_bytes(OrigBrokerID)
    self.DestBrokerID=self._to_bytes(DestBrokerID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.OrigDRIdentityID=int(i_tuple[1])
    self.DestDRIdentityID=int(i_tuple[2])
    self.OrigBrokerID=self._to_bytes(i_tuple[3])
    self.DestBrokerID=self._to_bytes(i_tuple[4])

class FensUserInfoField(Base):
  """Fens用户信息"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('LoginMode',ctypes.c_char)# 登录模式
]

  def __init__(self,BrokerID= '',UserID='',LoginMode=''):

    super(FensUserInfoField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.LoginMode=self._to_bytes(LoginMode)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.LoginMode=self._to_bytes(i_tuple[3])

class CurrTransferIdentityField(Base):
  """当前银期所属交易中心"""
  _fields_ = [
    ('IdentityID',ctypes.c_int)# ///交易中心代码
]

  def __init__(self,IdentityID= 0):

    super(CurrTransferIdentityField,self).__init__()

    self.IdentityID=int(IdentityID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.IdentityID=int(i_tuple[1])

class LoginForbiddenUserField(Base):
  """禁止登录用户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
    ,('IPAddress',ctypes.c_char*16)# IP地址
]

  def __init__(self,BrokerID= '',UserID='',IPAddress=''):

    super(LoginForbiddenUserField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
    self.IPAddress=self._to_bytes(IPAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])
    self.IPAddress=self._to_bytes(i_tuple[3])

class QryLoginForbiddenUserField(Base):
  """查询禁止登录用户"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,BrokerID= '',UserID=''):

    super(QryLoginForbiddenUserField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])

class MulticastGroupInfoField(Base):
  """UDP组播组信息"""
  _fields_ = [
    ('GroupIP',ctypes.c_char*16)# ///组播组IP地址
    ,('GroupPort',ctypes.c_int)# 组播组IP端口
    ,('SourceIP',ctypes.c_char*16)# 源地址
]

  def __init__(self,GroupIP= '',GroupPort=0,SourceIP=''):

    super(MulticastGroupInfoField,self).__init__()

    self.GroupIP=self._to_bytes(GroupIP)
    self.GroupPort=int(GroupPort)
    self.SourceIP=self._to_bytes(SourceIP)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.GroupIP=self._to_bytes(i_tuple[1])
    self.GroupPort=int(i_tuple[2])
    self.SourceIP=self._to_bytes(i_tuple[3])

class TradingAccountReserveField(Base):
  """资金账户基本准备金"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Reserve',ctypes.c_double)# 基本准备金
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',Reserve=0.0,CurrencyID=''):

    super(TradingAccountReserveField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.Reserve=float(Reserve)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.Reserve=float(i_tuple[3])
    self.CurrencyID=self._to_bytes(i_tuple[4])

class QryLoginForbiddenIPField(Base):
  """查询禁止登录IP"""
  _fields_ = [
    ('IPAddress',ctypes.c_char*16)# ///IP地址
]

  def __init__(self,IPAddress= ''):

    super(QryLoginForbiddenIPField,self).__init__()

    self.IPAddress=self._to_bytes(IPAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.IPAddress=self._to_bytes(i_tuple[1])

class QryIPListField(Base):
  """查询IP列表"""
  _fields_ = [
    ('IPAddress',ctypes.c_char*16)# ///IP地址
]

  def __init__(self,IPAddress= ''):

    super(QryIPListField,self).__init__()

    self.IPAddress=self._to_bytes(IPAddress)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.IPAddress=self._to_bytes(i_tuple[1])

class QryUserRightsAssignField(Base):
  """查询用户下单权限分配表"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///应用单元代码
    ,('UserID',ctypes.c_char*16)# 用户代码
]

  def __init__(self,BrokerID= '',UserID=''):

    super(QryUserRightsAssignField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.UserID=self._to_bytes(UserID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.UserID=self._to_bytes(i_tuple[2])

class ReserveOpenAccountConfirmField(Base):
  """银期预约开户确认请求"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*161)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('TID',ctypes.c_int)# 交易ID
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('Password',ctypes.c_char*41)# 期货密码
    ,('BankReserveOpenSeq',ctypes.c_char*13)# 预约开户银行流水号
    ,('BookDate',ctypes.c_char*9)# 预约开户日期
    ,('BookPsw',ctypes.c_char*41)# 预约开户验证密码
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',Digest='',BankAccType='',BrokerIDByBank='',TID=0,AccountID='',Password='',BankReserveOpenSeq='',BookDate='',BookPsw='',ErrorID=0,ErrorMsg=''):

    super(ReserveOpenAccountConfirmField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.TID=int(TID)
    self.AccountID=self._to_bytes(AccountID)
    self.Password=self._to_bytes(Password)
    self.BankReserveOpenSeq=self._to_bytes(BankReserveOpenSeq)
    self.BookDate=self._to_bytes(BookDate)
    self.BookPsw=self._to_bytes(BookPsw)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.InstallID=int(i_tuple[28])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[29])
    self.CurrencyID=self._to_bytes(i_tuple[30])
    self.Digest=self._to_bytes(i_tuple[31])
    self.BankAccType=self._to_bytes(i_tuple[32])
    self.BrokerIDByBank=self._to_bytes(i_tuple[33])
    self.TID=int(i_tuple[34])
    self.AccountID=self._to_bytes(i_tuple[35])
    self.Password=self._to_bytes(i_tuple[36])
    self.BankReserveOpenSeq=self._to_bytes(i_tuple[37])
    self.BookDate=self._to_bytes(i_tuple[38])
    self.BookPsw=self._to_bytes(i_tuple[39])
    self.ErrorID=int(i_tuple[40])
    self.ErrorMsg=self._to_bytes(i_tuple[41])

class ReserveOpenAccountField(Base):
  """银期预约开户"""
  _fields_ = [
    ('TradeCode',ctypes.c_char*7)# ///业务功能码
    ,('BankID',ctypes.c_char*4)# 银行代码
    ,('BankBranchID',ctypes.c_char*5)# 银行分支机构代码
    ,('BrokerID',ctypes.c_char*11)# 期商代码
    ,('BrokerBranchID',ctypes.c_char*31)# 期商分支机构代码
    ,('TradeDate',ctypes.c_char*9)# 交易日期
    ,('TradeTime',ctypes.c_char*9)# 交易时间
    ,('BankSerial',ctypes.c_char*13)# 银行流水号
    ,('TradingDay',ctypes.c_char*9)# 交易系统日期
    ,('PlateSerial',ctypes.c_int)# 银期平台消息流水号
    ,('LastFragment',ctypes.c_char)# 最后分片标志
    ,('SessionID',ctypes.c_int)# 会话号
    ,('CustomerName',ctypes.c_char*161)# 客户姓名
    ,('IdCardType',ctypes.c_char)# 证件类型
    ,('IdentifiedCardNo',ctypes.c_char*51)# 证件号码
    ,('Gender',ctypes.c_char)# 性别
    ,('CountryCode',ctypes.c_char*21)# 国家代码
    ,('CustType',ctypes.c_char)# 客户类型
    ,('Address',ctypes.c_char*101)# 地址
    ,('ZipCode',ctypes.c_char*7)# 邮编
    ,('Telephone',ctypes.c_char*41)# 电话号码
    ,('MobilePhone',ctypes.c_char*21)# 手机
    ,('Fax',ctypes.c_char*41)# 传真
    ,('EMail',ctypes.c_char*41)# 电子邮件
    ,('MoneyAccountStatus',ctypes.c_char)# 资金账户状态
    ,('BankAccount',ctypes.c_char*41)# 银行帐号
    ,('BankPassWord',ctypes.c_char*41)# 银行密码
    ,('InstallID',ctypes.c_int)# 安装编号
    ,('VerifyCertNoFlag',ctypes.c_char)# 验证客户证件号码标志
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
    ,('Digest',ctypes.c_char*36)# 摘要
    ,('BankAccType',ctypes.c_char)# 银行帐号类型
    ,('BrokerIDByBank',ctypes.c_char*33)# 期货公司银行编码
    ,('TID',ctypes.c_int)# 交易ID
    ,('ReserveOpenAccStas',ctypes.c_char)# 预约开户状态
    ,('ErrorID',ctypes.c_int)# 错误代码
    ,('ErrorMsg',ctypes.c_char*81)# 错误信息
]

  def __init__(self,TradeCode= '',BankID='',BankBranchID='',BrokerID='',BrokerBranchID='',TradeDate='',TradeTime='',BankSerial='',TradingDay='',PlateSerial=0,LastFragment='',SessionID=0,CustomerName='',IdCardType='',IdentifiedCardNo='',Gender='',CountryCode='',CustType='',Address='',ZipCode='',Telephone='',MobilePhone='',Fax='',EMail='',MoneyAccountStatus='',BankAccount='',BankPassWord='',InstallID=0,VerifyCertNoFlag='',CurrencyID='',Digest='',BankAccType='',BrokerIDByBank='',TID=0,ReserveOpenAccStas='',ErrorID=0,ErrorMsg=''):

    super(ReserveOpenAccountField,self).__init__()

    self.TradeCode=self._to_bytes(TradeCode)
    self.BankID=self._to_bytes(BankID)
    self.BankBranchID=self._to_bytes(BankBranchID)
    self.BrokerID=self._to_bytes(BrokerID)
    self.BrokerBranchID=self._to_bytes(BrokerBranchID)
    self.TradeDate=self._to_bytes(TradeDate)
    self.TradeTime=self._to_bytes(TradeTime)
    self.BankSerial=self._to_bytes(BankSerial)
    self.TradingDay=self._to_bytes(TradingDay)
    self.PlateSerial=int(PlateSerial)
    self.LastFragment=self._to_bytes(LastFragment)
    self.SessionID=int(SessionID)
    self.CustomerName=self._to_bytes(CustomerName)
    self.IdCardType=self._to_bytes(IdCardType)
    self.IdentifiedCardNo=self._to_bytes(IdentifiedCardNo)
    self.Gender=self._to_bytes(Gender)
    self.CountryCode=self._to_bytes(CountryCode)
    self.CustType=self._to_bytes(CustType)
    self.Address=self._to_bytes(Address)
    self.ZipCode=self._to_bytes(ZipCode)
    self.Telephone=self._to_bytes(Telephone)
    self.MobilePhone=self._to_bytes(MobilePhone)
    self.Fax=self._to_bytes(Fax)
    self.EMail=self._to_bytes(EMail)
    self.MoneyAccountStatus=self._to_bytes(MoneyAccountStatus)
    self.BankAccount=self._to_bytes(BankAccount)
    self.BankPassWord=self._to_bytes(BankPassWord)
    self.InstallID=int(InstallID)
    self.VerifyCertNoFlag=self._to_bytes(VerifyCertNoFlag)
    self.CurrencyID=self._to_bytes(CurrencyID)
    self.Digest=self._to_bytes(Digest)
    self.BankAccType=self._to_bytes(BankAccType)
    self.BrokerIDByBank=self._to_bytes(BrokerIDByBank)
    self.TID=int(TID)
    self.ReserveOpenAccStas=self._to_bytes(ReserveOpenAccStas)
    self.ErrorID=int(ErrorID)
    self.ErrorMsg=self._to_bytes(ErrorMsg)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.TradeCode=self._to_bytes(i_tuple[1])
    self.BankID=self._to_bytes(i_tuple[2])
    self.BankBranchID=self._to_bytes(i_tuple[3])
    self.BrokerID=self._to_bytes(i_tuple[4])
    self.BrokerBranchID=self._to_bytes(i_tuple[5])
    self.TradeDate=self._to_bytes(i_tuple[6])
    self.TradeTime=self._to_bytes(i_tuple[7])
    self.BankSerial=self._to_bytes(i_tuple[8])
    self.TradingDay=self._to_bytes(i_tuple[9])
    self.PlateSerial=int(i_tuple[10])
    self.LastFragment=self._to_bytes(i_tuple[11])
    self.SessionID=int(i_tuple[12])
    self.CustomerName=self._to_bytes(i_tuple[13])
    self.IdCardType=self._to_bytes(i_tuple[14])
    self.IdentifiedCardNo=self._to_bytes(i_tuple[15])
    self.Gender=self._to_bytes(i_tuple[16])
    self.CountryCode=self._to_bytes(i_tuple[17])
    self.CustType=self._to_bytes(i_tuple[18])
    self.Address=self._to_bytes(i_tuple[19])
    self.ZipCode=self._to_bytes(i_tuple[20])
    self.Telephone=self._to_bytes(i_tuple[21])
    self.MobilePhone=self._to_bytes(i_tuple[22])
    self.Fax=self._to_bytes(i_tuple[23])
    self.EMail=self._to_bytes(i_tuple[24])
    self.MoneyAccountStatus=self._to_bytes(i_tuple[25])
    self.BankAccount=self._to_bytes(i_tuple[26])
    self.BankPassWord=self._to_bytes(i_tuple[27])
    self.InstallID=int(i_tuple[28])
    self.VerifyCertNoFlag=self._to_bytes(i_tuple[29])
    self.CurrencyID=self._to_bytes(i_tuple[30])
    self.Digest=self._to_bytes(i_tuple[31])
    self.BankAccType=self._to_bytes(i_tuple[32])
    self.BrokerIDByBank=self._to_bytes(i_tuple[33])
    self.TID=int(i_tuple[34])
    self.ReserveOpenAccStas=self._to_bytes(i_tuple[35])
    self.ErrorID=int(i_tuple[36])
    self.ErrorMsg=self._to_bytes(i_tuple[37])

class AccountPropertyField(Base):
  """银行账户属性"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('AccountID',ctypes.c_char*13)# 投资者帐号
    ,('BankID',ctypes.c_char*4)# 银行统一标识类型
    ,('BankAccount',ctypes.c_char*41)# 银行账户
    ,('OpenName',ctypes.c_char*101)# 银行账户的开户人名称
    ,('OpenBank',ctypes.c_char*101)# 银行账户的开户行
    ,('IsActive',ctypes.c_int)# 是否活跃
    ,('AccountSourceType',ctypes.c_char)# 账户来源
    ,('OpenDate',ctypes.c_char*9)# 开户日期
    ,('CancelDate',ctypes.c_char*9)# 注销日期
    ,('OperatorID',ctypes.c_char*65)# 录入员代码
    ,('OperateDate',ctypes.c_char*9)# 录入日期
    ,('OperateTime',ctypes.c_char*9)# 录入时间
    ,('CurrencyID',ctypes.c_char*4)# 币种代码
]

  def __init__(self,BrokerID= '',AccountID='',BankID='',BankAccount='',OpenName='',OpenBank='',IsActive=0,AccountSourceType='',OpenDate='',CancelDate='',OperatorID='',OperateDate='',OperateTime='',CurrencyID=''):

    super(AccountPropertyField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.AccountID=self._to_bytes(AccountID)
    self.BankID=self._to_bytes(BankID)
    self.BankAccount=self._to_bytes(BankAccount)
    self.OpenName=self._to_bytes(OpenName)
    self.OpenBank=self._to_bytes(OpenBank)
    self.IsActive=int(IsActive)
    self.AccountSourceType=self._to_bytes(AccountSourceType)
    self.OpenDate=self._to_bytes(OpenDate)
    self.CancelDate=self._to_bytes(CancelDate)
    self.OperatorID=self._to_bytes(OperatorID)
    self.OperateDate=self._to_bytes(OperateDate)
    self.OperateTime=self._to_bytes(OperateTime)
    self.CurrencyID=self._to_bytes(CurrencyID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.AccountID=self._to_bytes(i_tuple[2])
    self.BankID=self._to_bytes(i_tuple[3])
    self.BankAccount=self._to_bytes(i_tuple[4])
    self.OpenName=self._to_bytes(i_tuple[5])
    self.OpenBank=self._to_bytes(i_tuple[6])
    self.IsActive=int(i_tuple[7])
    self.AccountSourceType=self._to_bytes(i_tuple[8])
    self.OpenDate=self._to_bytes(i_tuple[9])
    self.CancelDate=self._to_bytes(i_tuple[10])
    self.OperatorID=self._to_bytes(i_tuple[11])
    self.OperateDate=self._to_bytes(i_tuple[12])
    self.OperateTime=self._to_bytes(i_tuple[13])
    self.CurrencyID=self._to_bytes(i_tuple[14])

class QryCurrDRIdentityField(Base):
  """查询当前交易中心"""
  _fields_ = [
    ('DRIdentityID',ctypes.c_int)# ///交易中心代码
]

  def __init__(self,DRIdentityID= 0):

    super(QryCurrDRIdentityField,self).__init__()

    self.DRIdentityID=int(DRIdentityID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.DRIdentityID=int(i_tuple[1])

class CurrDRIdentityField(Base):
  """当前交易中心"""
  _fields_ = [
    ('DRIdentityID',ctypes.c_int)# ///交易中心代码
]

  def __init__(self,DRIdentityID= 0):

    super(CurrDRIdentityField,self).__init__()

    self.DRIdentityID=int(DRIdentityID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.DRIdentityID=int(i_tuple[1])

class QrySecAgentCheckModeField(Base):
  """查询二级代理商资金校验模式"""
  _fields_ = [
    ('BrokerID',ctypes.c_char*11)# ///经纪公司代码
    ,('InvestorID',ctypes.c_char*13)# 投资者代码
]

  def __init__(self,BrokerID= '',InvestorID=''):

    super(QrySecAgentCheckModeField,self).__init__()

    self.BrokerID=self._to_bytes(BrokerID)
    self.InvestorID=self._to_bytes(InvestorID)
     
  def towhere(self):
    l_where = ""
    l_dict  = self.to_dict()
    
    for k,v in l_dict.items():
      if not v is None and len(self._to_str(v)) > 0:
        if len(l_where) > 0:
          l_where = l_where + " and " + k + "=" + self._to_str4where(v)
        else:
          l_where =   k + "=" + self._to_str4where(v)     
    
    if len(l_where) > 0:
      l_where = " WHERE " + l_where
    return l_where


  def from_tuple(self, i_tuple):

    self.BrokerID=self._to_bytes(i_tuple[1])
    self.InvestorID=self._to_bytes(i_tuple[2])

