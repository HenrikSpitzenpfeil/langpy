import ctypes

lstepdll = '.\lstep64.dll'
dll = ctypes.WinDLL(lstepdll)

#TODO: figure out if current byref pass in is correctly writes into variables

def CreateLSID () -> tuple:

    '''Create an ID Value for a controller.
    Tuple: Error Code: int, LSID: ctypes.c_int32'''

    c_LSID = ctypes.c_int32()
    return dll.LSX_CreateLSID(ctypes.byref(c_LSID)), c_LSID

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

def ConnectSimple (LSID: int, AnInterfaceType: int,
                   AComName: str,
                   ABR: int,
                   AShowProt: bool
                   ) -> int:
    
    '''Connect to the given controller. Interface settings are passed as arguments.'''

    c_AnInterfaceType = ctypes.c_int32(AnInterfaceType)
    c_ABR = ctypes.c_int32(ABR)
    c_AShowProt = ctypes.c_bool(AShowProt)
    return dll.LSX_ConnectSimple(LSID, c_AnInterfaceType, AComName, c_ABR, c_AShowProt)

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

    return dll.LSX_SetCommandTimeout(LSID, AtoRead, AtoMove, AtoCalibrate)


def SendString (LSID: int,
                MaxLen: int,
                ReadLine: bool,
                TimeOut: int,
                ) -> tuple:
    
    '''Send commands that a have no api method as a string.
    tuple: error code: int, Ret: ctypes.c_int32'''

    c_MaxLen = ctypes.c_bool(MaxLen)
    c_Ret = ctypes.c_int32(Ret)
    return dll.LSX_SendString(LSID, ctypes.byref(c_Ret), c_MaxLen, ReadLine, TimeOut), c_Ret

def SetShowCmdList (LSID: int, ShowCmdList: bool) -> int:

    ''' Toggle the command list window'''
    
    c_ShowCmdList = ctypes.c_bool(ShowCmdList)
    return dll.LSX_SetShowCmdList(LSID, c_ShowCmdList)

def Calibrate (LSID: int) -> int:
    
    '''Moves all axis to smaller position values.
    Move is interrupted when limit switch is reached.
    All positions are set to zero '''

    return dll.LSX_Calibrate(LSID)

def RMeasure (LSID: int) -> int:
    
    '''Moves all axis to larger position values. 
    Move is interrupted when limit switch is reached.'''

    dll.LSX_RMeasure(LSID)

def GetPos (LSID: int, X: float, Y: float, Z: float, A: float) -> tuple:
    
    '''Gets current postion of all axis. Position is written into the variable 
    that are passed to the function- Non existent axis return zero
    tuple: error code: int, X: ctypes.c_double, Y: ctypes.c_double, Z: ctypes.c_double, A: ctypes.c_double'''

    c_X = ctypes.c_double(X)
    c_Y = ctypes.c_double(Y)
    c_Z = ctypes.c_double(Z)
    c_A = ctypes.c_double(A)
    return dll.LSX_GetPos(LSID, ctypes.byref(c_X),
                          ctypes.byref(c_Y),
                          ctypes.byref(c_Z),
                          ctypes.byref(c_A)
                          ), c_X, c_Y, c_Z, c_A

def GetPosSingleAxis (LSID: int, Axis: int, Pos: float) -> tuple:

    '''Get current position of specified axis.
    Position is written into Pos variable passed into function.
    Axis: 1 = X, 2 = Y, 3 = Z ...
    tuple: error code: int, Pos: ctypes.c_double'''

    c_Pos = ctypes.c_double(Pos)
    return dll.GetPosSingleAxis(LSID, Axis, ctypes.byref(c_Pos)), c_Pos