import ctypes

lstepdll = '.\lstep64'
dll = ctypes.WinDLL(lstepdll+'.dll')

def CreateLSID () -> int:
    '''Create an ID Value for a controller'''
    c_value = ctypes.c_int32()
    return dll.LSX_CreateLSID(ctypes.byref(c_value))

def LoadConfig (LSID: int, FileName: str) -> int:
    '''Loads a Config file fron the given config path string'''
    return dll.LSX_LoadConfig(LSID, FileName)

def SetControlPars(LSID: int) -> int:
    '''Sends the loaded Cofig Parameters to the given controller'''
    return dll.LSX_SetControlPars(LSID)

def Connect (LSID: int) -> int:
    '''Connect to the given controller using the
      parameters in the previously loaded Config file'''
    return dll.LSX_Connect(LSID)

def Disconnect (LSID: int) -> int:
    '''Disconnect from the given controller'''
    return dll.LSX_Disconnect(LSID)

def SetCommandTimeout (
        LSID: int,
        AtoRead: int,
        AtoMove: int,
        AtoCalibrate: int
        ) -> int:
    '''Set the timeout for general API calls.
    AtoRead: response wait time to general calls in ms
    AtoMove: timeout for positionion calls in ms
    AtoCalibrate: timeout for calibration calls in ms'''

#TODO: figure out datatypes and how to implement conditional/optional arguments) 
def SendString (
        LSID: int,
        Ret: str,
        MaxLen: int,
        ReadLine: bool,
        TimeOut: int
        ) -> int:
    c_MaxLen = ctypes.c_bool(MaxLen)
    return dll.LSX_SendString(LSID, Ret, MaxLen, ReadLine, TimeOut)

def SetShowCmdList (LSID: int, ShowCmdList: bool) -> int:
    c_ShowCmdList = ctypes.c_bool(ShowCmdList)
    return dll.LSX_SetShowCmdList(LSID, c_ShowCmdList)
