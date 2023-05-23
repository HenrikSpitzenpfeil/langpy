import ctypes

lstepdll = '.\lstep64.dll'
dll = ctypes.WinDLL(lstepdll)
encoding = 'utf8'

#TODO: Find all argument that need to be passed by reference
# Cast all strings to bytstrings if necessary

def CreateLSID () -> tuple:

    '''Create an ID Value for a controller.
    Tuple: Error Code: int, LSID: ctypes.c_int32'''

    c_LSID = ctypes.c_int32()
    return dll.LSX_CreateLSID(ctypes.byref(c_LSID)), c_LSID

def LoadConfig (LSID: int, FileName: str) -> int:

    '''Loads a Config file fron the given config path string'''

    return dll.LSX_LoadConfig(LSID, bytes(FileName, encoding))

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
    
    '''Connect to the given controller.
    Interface settings are passed as arguments.'''

    return dll.LSX_ConnectSimple(LSID,
                                 AnInterfaceType,
                                 bytes(AComName, encoding),
                                 ABR,
                                 AShowProt
                                 )

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
    c_Ret = ctypes.c_int32()
    return dll.LSX_SendString(LSID,
                              ctypes.byref(c_Ret),
                              c_MaxLen,
                              ReadLine,
                              TimeOut,
                              ), c_Ret

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
    tuple: error code: int, X: ctypes.c_double, 
    Y: ctypes.c_double, Z: ctypes.c_double, A: ctypes.c_double'''

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

def SetPos (LSID: int, X: float, Y: float, Z: float, A: float) -> int:
    
    '''Set a new postion value. Current Position will be set to passed values.
    Origin of the coordinate system will be adjusted accordingly.'''

    c_X = ctypes.c_double(X)
    c_Y = ctypes.c_double(Y)
    c_Z = ctypes.c_double(Z)
    c_A = ctypes.c_double(A)
    return dll.LSX_SetPos(LSID, c_X, c_Y, c_Z, c_A)

def MoveAbs (LSID: int,
             X: float,
             Y: float,
             Z: float,
             A: float,
             Wait: bool = True
             ) -> int:
    
    '''Move to an absolute position from the current position.
    Movement is linearly interpolated.'''

    c_X = ctypes.c_double(X)
    c_Y = ctypes.c_double(Y)
    c_Z = ctypes.c_double(Z)
    c_A = ctypes.c_double(A)
    c_wait = ctypes.c_bool(Wait)
    return dll.LSX_MoveAbs(LSID, c_X, c_Y, c_Z, c_A, c_wait)

def MoveAbsSingleAxis (LSID: int,
                       Axis: int,
                       Value: float,
                       Wait: bool = True
                       ) -> int:

    ''' Move a single axis to an absolute position from the current position
    Axis: 1 = X, 2 = Y, 3 = Z ...'''

    c_Value = ctypes.c_double(Value)
    c_Wait = ctypes.c_bool(Wait)
    return dll.LSX_MoveAbsSingleAxis(LSID, Axis, c_Value, c_Wait)

def MoveRel (LSID: int,
             X: float,
             Y: float,
             Z: float,
             A: float,
             Wait: bool = True
             ) -> int:
    
    ''' Move by a relative vector from current position.'''

    c_X = ctypes.c_double(X)
    c_Y = ctypes.c_double(Y)
    c_Z = ctypes.c_double(Z)
    c_A = ctypes.c_double(A)
    c_Wait = ctypes.c_bool(Wait)
    
    return dll.LSX_MoveRel(LSID, c_X, c_Y, c_Z, c_A, c_Wait)

def MoveRelSingleAxis (LSID: int,
                       Axis: int,
                       Value: float,
                       Wait: bool = True
                       ) -> int:
    
    ''' Move a single axis relative to current position
    Axis: 1 = X, 2 = Y, 3 = Z ...'''

    c_Value = ctypes.c_double(Value)
    c_Wait = ctypes.c_bool(Wait)
    return dll.LSX_MoveSingleAxis(LSID, Axis, c_Value, c_Wait)

def GetDistance (LSID: int,
                 X: float,
                 Y: float,
                 Z: float,
                 A: float
                 ) -> tuple:
    
    '''Get the Distance of MoveRelShort
    Tuple: error code: int, 
            X: ctypes.c_float
            Y: ctypes.c_float
            Z: ctypes.c_float
            A: ctypes.c_float'''

    c_X = ctypes.c_float(X)
    c_Y = ctypes.c_float(Y)
    c_Z = ctypes.c_float(Z)
    c_A = ctypes.c_float(A)
    return dll.LSX_GetDistance(LSID,
                           c_X,
                           c_Y,
                           c_Z,
                           c_A
                           ), c_X, c_Y, c_Z, c_A

def SetDistance (LSID: int, X: float, Y: float, Z: float, A: float) -> int:

    '''Set distance for MoveRelShort'''

    c_X = ctypes.c_float(X)
    c_Y = ctypes.c_float(Y)
    c_Z = ctypes.c_float(Z)
    c_A = ctypes.c_float(A)
    return dll.LSX_SetDistance(LSID, c_X, c_Y, c_Z, c_A)

def MoveRelShort (LSID: int) -> int:

    '''Moves by a relative vector to current position. 
    Vector is set with LSX_SetDistance.
    Use when multiple moves by the same distance in succession are needed.'''

    return dll.LSX_MoveRelShort(LSID)

def StopAxes (LSID: int) -> int:

    '''Interrupts all movement commands'''

    return dll.LSX_StopAxes(LSID)