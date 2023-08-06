#ifndef CMdSpi_H
#define CMdSpi_H

#include "ThostFtdcMdApi.h"


#include "MyTools.h"

//声明静态函数，并没有实现，在Cython中实现，以实现回调 python 代码
//目的就是解决 C 回调 python 代码，才能实现在python中实现编写业务逻辑





static inline int MdSpi_OnFrontConnected(PyObject *);

static inline int MdSpi_OnFrontDisconnected(PyObject *, int);

static inline int MdSpi_OnHeartBeatWarning(PyObject *, int);

static inline int MdSpi_OnRspUserLogin(PyObject *, CThostFtdcRspUserLoginField *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRspUserLogout(PyObject *, CThostFtdcUserLogoutField *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRspError(PyObject *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRspSubMarketData(PyObject *, CThostFtdcSpecificInstrumentField *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRspUnSubMarketData(PyObject *, CThostFtdcSpecificInstrumentField *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRspSubForQuoteRsp(PyObject *, CThostFtdcSpecificInstrumentField *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRspUnSubForQuoteRsp(PyObject *, CThostFtdcSpecificInstrumentField *, CThostFtdcRspInfoField *, int, bool);

static inline int MdSpi_OnRtnDepthMarketData(PyObject *, CThostFtdcDepthMarketDataField *);

static inline int MdSpi_OnRtnForQuoteRsp(PyObject *, CThostFtdcForQuoteRspField *);

#define Python_GIL(func) \
  do { \
    PyGILState_STATE gil_state = PyGILState_Ensure(); \
    if ((func) == -1) PyErr_Print();  \
    PyGILState_Release(gil_state); \
  } while (false)

class CMdSpi : public CThostFtdcMdSpi{
public:

    CMdSpi(PyObject *obj):self(obj) {};

  virtual ~CMdSpi() {};



  ///当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
  virtual void  OnFrontConnected() {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    MdSpi_OnFrontConnected(self);

    printString("MdSpiOnFrontConnected","null","null",dwTime);

  };

  ///当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
///@param nReason 错误原因
///        0x1001 网络读失败
///        0x1002 网络写失败
///        0x2001 接收心跳超时
///        0x2002 发送心跳失败
///        0x2003 收到错误报文
  virtual void  OnFrontDisconnected(int nReason) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    MdSpi_OnFrontDisconnected(self, nReason);

    printNumber("MdSpiOnFrontDisconnected","nReason",nReason,dwTime);

  };

  ///心跳超时警告。当长时间未收到报文时，该方法被调用。
///@param nTimeLapse 距离上次接收报文的时间
  virtual void  OnHeartBeatWarning(int nTimeLapse) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    MdSpi_OnHeartBeatWarning(self, nTimeLapse);

    printNumber("MdSpiOnHeartBeatWarning","nTimeLapse",nTimeLapse,dwTime);

  };

  ///登录请求响应
  virtual void  OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspUserLogin", "Enter", dwTime);

    if (NULL==pRspUserLogin)
    {
      printString("pRspUserLogin","CThostFtdcRspUserLoginField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pRspUserLogin","TradingDay",pRspUserLogin->TradingDay,dwTime);
      printString("pRspUserLogin","LoginTime",pRspUserLogin->LoginTime,dwTime);
      printString("pRspUserLogin","BrokerID",pRspUserLogin->BrokerID,dwTime);
      printString("pRspUserLogin","UserID",pRspUserLogin->UserID,dwTime);
      printString("pRspUserLogin","SystemName",pRspUserLogin->SystemName,dwTime);
      printNumber("pRspUserLogin","FrontID",pRspUserLogin->FrontID,dwTime);
      printNumber("pRspUserLogin","SessionID",pRspUserLogin->SessionID,dwTime);
      printString("pRspUserLogin","MaxOrderRef",pRspUserLogin->MaxOrderRef,dwTime);
      printString("pRspUserLogin","SHFETime",pRspUserLogin->SHFETime,dwTime);
      printString("pRspUserLogin","DCETime",pRspUserLogin->DCETime,dwTime);
      printString("pRspUserLogin","CZCETime",pRspUserLogin->CZCETime,dwTime);
      printString("pRspUserLogin","FFEXTime",pRspUserLogin->FFEXTime,dwTime);
      printString("pRspUserLogin","INETime",pRspUserLogin->INETime,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspUserLogin", "Leave", dwTime);

    if (NULL==pRspInfo)
        {
            printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
        }
        else
        {
            printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
            printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);
        }

    MdSpi_OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast);

  };

  ///登出请求响应
  virtual void  OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspUserLogout", "Enter", dwTime);

    if (NULL==pUserLogout)
    {
      printString("pUserLogout","CThostFtdcUserLogoutField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pUserLogout","BrokerID",pUserLogout->BrokerID,dwTime);
      printString("pUserLogout","UserID",pUserLogout->UserID,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspUserLogout", "Leave", dwTime);

    if (NULL==pRspInfo)
        {
            printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
        }
        else
        {
            printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
            printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);
        }

    MdSpi_OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast);

  };

  ///错误应答
  virtual void  OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspError", "Enter", dwTime);

    if (NULL==pRspInfo)
    {
      printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
      return;
    }
    else
    {
      printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
      printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspError", "Leave", dwTime);

    MdSpi_OnRspError(self, pRspInfo, nRequestID, bIsLast);

  };

  ///订阅行情应答
  virtual void  OnRspSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspSubMarketData", "Enter", dwTime);

    if (NULL==pSpecificInstrument)
    {
      printString("pSpecificInstrument","CThostFtdcSpecificInstrumentField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pSpecificInstrument","InstrumentID",pSpecificInstrument->InstrumentID,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspSubMarketData", "Leave", dwTime);

    if (NULL==pRspInfo)
        {
            printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
        }
        else
        {
            printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
            printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);
        }

    MdSpi_OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast);

  };

  ///取消订阅行情应答
  virtual void  OnRspUnSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspUnSubMarketData", "Enter", dwTime);

    if (NULL==pSpecificInstrument)
    {
      printString("pSpecificInstrument","CThostFtdcSpecificInstrumentField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pSpecificInstrument","InstrumentID",pSpecificInstrument->InstrumentID,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspUnSubMarketData", "Leave", dwTime);

    if (NULL==pRspInfo)
        {
            printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
        }
        else
        {
            printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
            printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);
        }

    MdSpi_OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast);

  };

  ///订阅询价应答
  virtual void  OnRspSubForQuoteRsp(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspSubForQuoteRsp", "Enter", dwTime);

    if (NULL==pSpecificInstrument)
    {
      printString("pSpecificInstrument","CThostFtdcSpecificInstrumentField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pSpecificInstrument","InstrumentID",pSpecificInstrument->InstrumentID,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspSubForQuoteRsp", "Leave", dwTime);

    if (NULL==pRspInfo)
        {
            printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
        }
        else
        {
            printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
            printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);
        }

    MdSpi_OnRspSubForQuoteRsp(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast);

  };

  ///取消订阅询价应答
  virtual void  OnRspUnSubForQuoteRsp(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRspUnSubForQuoteRsp", "Enter", dwTime);

    if (NULL==pSpecificInstrument)
    {
      printString("pSpecificInstrument","CThostFtdcSpecificInstrumentField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pSpecificInstrument","InstrumentID",pSpecificInstrument->InstrumentID,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRspUnSubForQuoteRsp", "Leave", dwTime);

    if (NULL==pRspInfo)
        {
            printString("pRspInfo","CThostFtdcRspInfoField","NULL",dwTime);
        }
        else
        {
            printNumber("pRspInfo","ErrorID",pRspInfo->ErrorID,dwTime);
            printString("pRspInfo","ErrorMsg",pRspInfo->ErrorMsg,dwTime);
        }

    MdSpi_OnRspUnSubForQuoteRsp(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast);

  };

  ///深度行情通知
  virtual void  OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRtnDepthMarketData", "Enter", dwTime);

    if (NULL==pDepthMarketData)
    {
      printString("pDepthMarketData","CThostFtdcDepthMarketDataField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pDepthMarketData","TradingDay",pDepthMarketData->TradingDay,dwTime);
      printString("pDepthMarketData","InstrumentID",pDepthMarketData->InstrumentID,dwTime);
      printString("pDepthMarketData","ExchangeID",pDepthMarketData->ExchangeID,dwTime);
      printString("pDepthMarketData","ExchangeInstID",pDepthMarketData->ExchangeInstID,dwTime);
      printNumber("pDepthMarketData","LastPrice",pDepthMarketData->LastPrice,dwTime);
      printNumber("pDepthMarketData","PreSettlementPrice",pDepthMarketData->PreSettlementPrice,dwTime);
      printNumber("pDepthMarketData","PreClosePrice",pDepthMarketData->PreClosePrice,dwTime);
      printNumber("pDepthMarketData","PreOpenInterest",pDepthMarketData->PreOpenInterest,dwTime);
      printNumber("pDepthMarketData","OpenPrice",pDepthMarketData->OpenPrice,dwTime);
      printNumber("pDepthMarketData","HighestPrice",pDepthMarketData->HighestPrice,dwTime);
      printNumber("pDepthMarketData","LowestPrice",pDepthMarketData->LowestPrice,dwTime);
      printNumber("pDepthMarketData","Volume",pDepthMarketData->Volume,dwTime);
      printNumber("pDepthMarketData","Turnover",pDepthMarketData->Turnover,dwTime);
      printNumber("pDepthMarketData","OpenInterest",pDepthMarketData->OpenInterest,dwTime);
      printNumber("pDepthMarketData","ClosePrice",pDepthMarketData->ClosePrice,dwTime);
      printNumber("pDepthMarketData","SettlementPrice",pDepthMarketData->SettlementPrice,dwTime);
      printNumber("pDepthMarketData","UpperLimitPrice",pDepthMarketData->UpperLimitPrice,dwTime);
      printNumber("pDepthMarketData","LowerLimitPrice",pDepthMarketData->LowerLimitPrice,dwTime);
      printNumber("pDepthMarketData","PreDelta",pDepthMarketData->PreDelta,dwTime);
      printNumber("pDepthMarketData","CurrDelta",pDepthMarketData->CurrDelta,dwTime);
      printString("pDepthMarketData","UpdateTime",pDepthMarketData->UpdateTime,dwTime);
      printNumber("pDepthMarketData","UpdateMillisec",pDepthMarketData->UpdateMillisec,dwTime);
      printNumber("pDepthMarketData","BidPrice1",pDepthMarketData->BidPrice1,dwTime);
      printNumber("pDepthMarketData","BidVolume1",pDepthMarketData->BidVolume1,dwTime);
      printNumber("pDepthMarketData","AskPrice1",pDepthMarketData->AskPrice1,dwTime);
      printNumber("pDepthMarketData","AskVolume1",pDepthMarketData->AskVolume1,dwTime);
      printNumber("pDepthMarketData","BidPrice2",pDepthMarketData->BidPrice2,dwTime);
      printNumber("pDepthMarketData","BidVolume2",pDepthMarketData->BidVolume2,dwTime);
      printNumber("pDepthMarketData","AskPrice2",pDepthMarketData->AskPrice2,dwTime);
      printNumber("pDepthMarketData","AskVolume2",pDepthMarketData->AskVolume2,dwTime);
      printNumber("pDepthMarketData","BidPrice3",pDepthMarketData->BidPrice3,dwTime);
      printNumber("pDepthMarketData","BidVolume3",pDepthMarketData->BidVolume3,dwTime);
      printNumber("pDepthMarketData","AskPrice3",pDepthMarketData->AskPrice3,dwTime);
      printNumber("pDepthMarketData","AskVolume3",pDepthMarketData->AskVolume3,dwTime);
      printNumber("pDepthMarketData","BidPrice4",pDepthMarketData->BidPrice4,dwTime);
      printNumber("pDepthMarketData","BidVolume4",pDepthMarketData->BidVolume4,dwTime);
      printNumber("pDepthMarketData","AskPrice4",pDepthMarketData->AskPrice4,dwTime);
      printNumber("pDepthMarketData","AskVolume4",pDepthMarketData->AskVolume4,dwTime);
      printNumber("pDepthMarketData","BidPrice5",pDepthMarketData->BidPrice5,dwTime);
      printNumber("pDepthMarketData","BidVolume5",pDepthMarketData->BidVolume5,dwTime);
      printNumber("pDepthMarketData","AskPrice5",pDepthMarketData->AskPrice5,dwTime);
      printNumber("pDepthMarketData","AskVolume5",pDepthMarketData->AskVolume5,dwTime);
      printNumber("pDepthMarketData","AveragePrice",pDepthMarketData->AveragePrice,dwTime);
      printString("pDepthMarketData","ActionDay",pDepthMarketData->ActionDay,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRtnDepthMarketData", "Leave", dwTime);

    MdSpi_OnRtnDepthMarketData(self, pDepthMarketData);

  };

  ///询价通知
  virtual void  OnRtnForQuoteRsp(CThostFtdcForQuoteRspField *pForQuoteRsp) {
    double dwTime = get_tick_count();
    PyGILLock gilLock;

    printString("CThostFtdcMdSpi","OnRtnForQuoteRsp", "Enter", dwTime);

    if (NULL==pForQuoteRsp)
    {
      printString("pForQuoteRsp","CThostFtdcForQuoteRspField","NULL",dwTime);
      return;
    }
    else
    {
      printString("pForQuoteRsp","TradingDay",pForQuoteRsp->TradingDay,dwTime);
      printString("pForQuoteRsp","InstrumentID",pForQuoteRsp->InstrumentID,dwTime);
      printString("pForQuoteRsp","ForQuoteSysID",pForQuoteRsp->ForQuoteSysID,dwTime);
      printString("pForQuoteRsp","ForQuoteTime",pForQuoteRsp->ForQuoteTime,dwTime);
      printString("pForQuoteRsp","ActionDay",pForQuoteRsp->ActionDay,dwTime);
      printString("pForQuoteRsp","ExchangeID",pForQuoteRsp->ExchangeID,dwTime);

    }

    printString("CThostFtdcMdSpi","OnRtnForQuoteRsp", "Leave", dwTime);

    MdSpi_OnRtnForQuoteRsp(self, pForQuoteRsp);

  };
private:
    PyObject *self;
};

#endif /* CMdSpi_H */
