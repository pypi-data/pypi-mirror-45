import win32com.client

class _XASessionEvents:
    def __init__(self):
        self.reset()

    def reset(self):
        self.OnLoginReturn = None
        self.OnLogoutReturn = None
        self.OnDisconnectReturn = None

    def OnLogin(self, szCode, szMsg):
        self.OnLoginReturn = dict(szCode=szCode, szMsg=szMsg)
    def OnLogout(self):
        self.OnLogoutReturn = dict()
    def OnDisconnect(self):
        self.OnDisconnectReturn = dict()

class _XAQueryEvents:
    def __init__(self):
        self.reset()

    def reset(self):
        self.OnReceiveDataReturn = None
        self.OnReceiveMessageReturn = None
        self.OnReceiveChartRealDataReturn = None
        self.OnReceiveSearchRealDataReturn = None

    def OnReceiveData(self, szTrCode):
        self.OnReceiveDataReturn = dict(szTrCode=szTrCode)
    def OnReceiveMessage(self, bIsSystemError, nMessageCode, szMessage):
        self.OnReceiveMessageReturn = dict(bIsSystemError=bIsSystemError, nMessageCode=nMessageCode, szMessage=szMessage)
    def OnReceiveChartRealData(self, szTrCode):
        self.OnReceiveChartRealDataReturn = dict(szTrCode=szTrCode)
    def OnReceiveSearchRealData(self, szTrCode):
        self.OnReceiveSearchRealDataReturn = dict(szTrCode=szTrCode)

class _XARealEvents:
    def __init__(self):
        self.reset()

    def reset(self):
        self.OnReceiveRealDataReturn = None
        self.OnRecieveLinkDataReturn = None

    def OnReceiveRealData(self, szTrCode):
        self.OnReceiveRealDataReturn = dict(szTrCode=szTrCode)
    def OnRecieveLinkData(self, szLinkName, szData, szFiller):
        self.OnRecieveLinkDataReturn = dict(szLinkName=szLinkName, szData=szData, szFiller=szFiller)

class Session:
    def __init__(self):
        self.session = win32com.client.DispatchWithEvents("XA_Session.XASession", _XASessionEvents)

    @property
    def SendPacketSize(self):
        return self.session.SendPacketSize

    @property
    def ConnectTimeOut(self):
        return self.session.ConnectTimeOut

    def ConnectServer(self, szServerIP, nServerPort):
        return self.session.ConnectServer(szServerIP, nServerPort)
    
    def DisconnectServer(self):
        return self.session.DisconnectServer()

    def IsConnected(self):
        return self.session.IsConnected()

    def Login(self, szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg):
        return self.session.Login(szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg)

    def Logout(self):
        return self.session.Logout()

    def GetAccountListCount(self):
        return self.session.GetAccountListCount()

    def GetAccountList(self, nIndex):
        return self.session.GetAccountList(nIndex)

    def GetAcctDetailName(self, szAcc):
        return self.session.GetAcctDetailName(szAcc)

    def GetAcctNickName(self, szAcc):
        return self.session.GetAcctNickName(szAcc)

    def GetLastError(self):
        return self.session.GetLastError()

    def GetErrorMessage(self, nErrorCode):
        return self.session.GetErrorMessage(nErrorCode)

    def IsLoadAPI(self):
        return self.session.IsLoadAPI()

    def GetServerName(self):
        return self.session.GetServerName()

    @property
    def OnLogin(self):
        return self.session.OnLoginReturn

    @property
    def OnLogout(self, reset=True):
        return self.session.OnLogoutReturn

    @property
    def OnDisconnect(self):
        return self.session.OnDisconnectReturn
    
    def reset(self):
        self.session.reset()

class Query:
    def __init__(self):
        self.query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", _XAQueryEvents)
    
    @property
    def ResFileName(self):
        return self.query.ResFileName

    @property
    def IsNext(self):
        return self.query.IsNext

    def Request(self, bNext):
        return self.query.Request(bNext)

    def GetFieldData(self, szBlockName, szFieldName, nOccursIndex):
        return self.query.GetFieldData(szBlockName, szFieldName, nOccursIndex)

    def SetFieldData(self, szBlockName, szFieldName, nOccursIndex, szData):
        return self.query.SetFieldData(szBlockName, szFieldName, nOccursIndex, szData)

    def GetBlockCount(self, szBlockName):
        return self.query.GetBlockCount(szBlockName)

    def SetBlockCount(self, szBlockName, nCount):
        return self.query.SetBlockCount(szBlockName, nCount)

    def LoadFromResFile(self, szFileName):
        return self.query.LoadFromResFile(szFileName)

    def ClearBlockdata(self, szBlockName):
        return self.query.ClearBlockdata(szBlockName)

    def GetBlockData(self, szBlockName):
        return self.query.GetBlockData(szBlockName)

    def GetTRCountPerSec(self, szCode):
        return self.query.GetTRCountPerSec(szCode)

    def RequestService(self, szCode, szData):
        return self.query.RequestService(szCode, szData)

    def RemoveService(self, szCode, szData):
        return self.query.RemoveService(szCode, szData)

    def RequestLinkToHTS(self, szLinkName, szData, szFiller):
        return self.query.RequestLinkToHTS(szLinkName, szData, szFiller)

    def Decompress(self, szBlockName):
        return self.query.Decompress(szBlockName)

    def GetFieldChartRealData(self, szBlockName, szFieldName):
        return self.query.GetFieldChartRealData(szBlockName, szFieldName)

    def GetAttribute(self, szBlockName, szFieldName, szAttribute, nOccursIndex):
        return self.query.GetAttribute(szBlockName, szFieldName, szAttribute, nOccursIndex)

    def GetTRCountBaseSec(self, szCode):
        return self.query.GetTRCountBaseSec(szCode)

    def GetTRCountRequest(self, szCode):
        return self.query.GetTRCountRequest(szCode)

    def GetTRCountLimit(self, szCode):
        return self.query.GetTRCountLimit(szCode)

    @property
    def OnReceiveData(self):
        return self.query.OnReceiveDataReturn
    
    @property
    def OnReceiveMessage(self):
        return self.query.OnReceiveMessageReturn

    @property
    def OnReceiveSearchRealData(self):
        return self.query.OnReceiveSearchRealDataReturn

    @property
    def OnReceiveChartRealData(self):
        return self.query.OnReceiveChartRealDataReturn

    def reset(self):
        self.query.reset()

class Real:
    def __init__(self):
        self.real = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", _XARealEvents)
    
    @property
    def ResFileName(self):
        return self.real.ResFileName

    def AdviseRealData(self):
        return self.real.AdviseRealData()

    def UnadviseRealData(self):
        return self.real.UnadviseRealData()

    def UnAdviseRealDataWithKey(self, szCode):
        return self.real.UnAdviseRealDataWithKey()

    def AdviseLinkFromHTS(self):
        return self.real.AdviseLinkFromHTS()

    def UnadviseLinkFromHTS(self):
        return self.real.UnadviseLinkFromHTS()

    def GetFieldData(self, szBlockName, szFieldName):
        return self.real.GetFieldData(szBlockName, szFieldName)

    def SetFieldData(self, szBlockName, szFieldName, szData):
        return self.real.SetFieldData(szBlockName, szFieldName, szData)

    def LoadFromResFile(self, szFileName):
        return self.real.LoadFromResFile(szFileName)

    def GetBlockData(self, szBlockName):
        return self.real.GetBlockData(szBlockName)

    @property
    def OnReceiveRealData(self):
        return self.real.OnReceiveRealDataReturn

    @property
    def OnRecieveLinkData(self):
        return self.real.OnRecieveLinkDataReturn

    def reset(self):
        self.real.reset()
