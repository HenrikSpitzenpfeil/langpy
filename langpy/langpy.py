import ctypes

class LStepController:

    def __init__(self, dll_path):

        self.dll = ctypes.WinDLL(dll_path)
        self._encoding = 'utf8'
        self.LSID = self.CreateLSID()[1]
        
        """Automatically connect and calibrates
        the Controller on initialization"""
        # This is the config for the SECM controller of Palkovits Lab
        # Configuration on init need to be implemented in future
        connection_config = [5, 'COM3', 115200, True]
        self.ConnectSimple(*connection_config)
        #self.Calibrate()
        #self.RMeasure()

        #Find and set current Positions
        self.position = self.GetPos()[1:]

    def __str__(self):
        return f'LStepController with LSID {self.LSID}'

    def CreateLSID(self) -> tuple:

        """Create an ID Value for a controller.
        Tuple: Error Code: int, LSID: ctypes.c_int32"""

        c_LSID = ctypes.c_int32()
        return self.dll.LSX_CreateLSID(ctypes.byref(c_LSID)), c_LSID

    def LoadConfig(self, FileName: str) -> int:

        """Loads a Config file fron the given config path string"""

        return self.dll.LSX_LoadConfig(self.LSID, bytes(FileName, self._encoding))

    def SetControlPars(self) -> int:

        """Sends the loaded Cofig Parameters to the given controller"""

        return self.dll.LSX_SetControlPars(self.LSID)

    def Connect(self) -> int:

        """Connect to the given controller using the
          parameters in the previously loaded Config file"""

        return self.dll.LSX_Connect(self.LSID)

    def ConnectSimple(self, AnInterfaceType: int,
                      AComName: str,
                      ABR: int,
                      AShowProt: bool) -> int:

        """Connect to the given controller.
        Interface settings are passed as arguments."""

        return self.dll.LSX_ConnectSimple(self.LSID,
                                     AnInterfaceType,
                                     bytes(AComName, self._encoding),
                                     ABR,
                                     AShowProt
                                     )

    def Disconnect(self) -> int:

        """Disconnect from the given controller"""

        return self.dll.LSX_Disconnect(self.LSID)

    def SetCommandTimeout(self,
                          AtoRead: int,
                          AtoMove: int,
                          AtoCalibrate: int) -> int:

        """Set the timeout for general API calls.
        AtoRead: response wait time to general calls in ms
        AtoMove: timeout for positionion calls in ms
        AtoCalibrate: timeout for calibration calls in ms"""

        return self.dll.LSX_SetCommandTimeout(self.LSID,
                                         AtoRead,
                                         AtoMove,
                                         AtoCalibrate)

    def SendString(self,
                   MaxLen: int,
                   ReadLine: bool,
                   TimeOut: int) -> tuple:

        """Send commands that a have no api method as a string.
        tuple: error code: int, Ret: ctypes.c_int32"""

        c_MaxLen = ctypes.c_bool(MaxLen)
        c_Ret = ctypes.c_int32()
        return self.dll.LSX_SendString(self.LSID,
                                  ctypes.byref(c_Ret),
                                  c_MaxLen,
                                  ReadLine,
                                  TimeOut,
                                  ), c_Ret

    def SetShowCmdList(self, ShowCmdList: bool) -> int:

        """ Toggle the command list window"""

        c_ShowCmdList = ctypes.c_bool(ShowCmdList)
        return self.dll.LSX_SetShowCmdList(self.LSID, c_ShowCmdList)

    def Calibrate(self) -> int:

        """Moves all axis to smaller position values.
        Move is interrupted when limit switch is reached.
        All positions are set to zero """

        answer = self.dll.LSX_Calibrate(self.LSID)
        self.position = self.GetPos()[1:]
        return answer

    def RMeasure(self) -> int:

        """Moves all axis to larger position values.
        Move is interrupted when limit switch is reached."""
        
        answer = self.dll.LSX_RMeasure(self.LSID)
        self.position = self.GetPos()[1:]
        return answer

    def GetPos(self) -> tuple:

        """Gets current postion of all axis. Position is written into the
        variable that are passed to the function- Non existent axis return zero
        tuple: error code: int, X: ctypes.c_double,
        Y: ctypes.c_double, Z: ctypes.c_double, A: ctypes.c_double"""

        c_X = ctypes.c_double()
        c_Y = ctypes.c_double()
        c_Z = ctypes.c_double()
        c_A = ctypes.c_double()
        return self.dll.LSX_GetPos(self.LSID, 
                                   ctypes.byref(c_X),
                                   ctypes.byref(c_Y),
                                   ctypes.byref(c_Z),
                                   ctypes.byref(c_A)
                                   ), c_X.value, c_Y.value, c_Z.value, c_A.value

    def GetPosSingleAxis(self, Axis: int) -> float:

        """Get current position of specified axis.
        Position is written into Pos variable passed into function.
        Axis: 1 = X, 2 = Y, 3 = Z ..."""

        return self.position[Axis-1]

    def SetPos(self, X: float, Y: float, Z: float, A: float) -> int:

        """Set a new postion value.
        Current Position will be set to passed values.
        Origin of the coordinate system will be
        adjusted accordingly."""

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        
        self.position = X, Y, Z, A
        
        return self.dll.LSX_SetPos(self.LSID, c_X, c_Y, c_Z, c_A)

    def MoveAbs(self,
                X: float,
                Y: float,
                Z: float,
                A: float,
                Wait: bool = True) -> int:

        """Move to an absolute position from the current position.
        Movement is linearly interpolated."""

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        c_wait = ctypes.c_bool(Wait)
        answer = self.dll.LSX_MoveAbs(self.LSID, c_X, c_Y, c_Z, c_A, c_wait)
        self.position = self.GetPos()[1:]
        return answer

    def MoveAbsSingleAxis(self,
                          Axis: int,
                          Value: float,
                          Wait: bool = True) -> int:

        """Move a single axis to an absolute position from the current position
        Axis: 1 = X, 2 = Y, 3 = Z ..."""

        c_Value = ctypes.c_double(Value)
        c_Wait = ctypes.c_bool(Wait)
        answer = self.dll.LSX_MoveAbsSingleAxis(self.LSID, Axis, c_Value, c_Wait)
        self.position = self.GetPos()[1:]
        return answer

    def MoveRel(self,
                X: float,
                Y: float,
                Z: float,
                A: float,
                Wait: bool = True) -> int:

        """Move by a relative vector from current position."""

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        c_Wait = ctypes.c_bool(Wait)
        answer = self.dll.LSX_MoveRel(self.LSID, c_X, c_Y, c_Z, c_A, c_Wait)
        self.position = self.GetPos()[1:]
        return answer

    def MoveRelSingleAxis(self,
                          Axis: int,
                          Value: float,
                          Wait: bool = True) -> int:

        """Move a single axis relative to current position
        Axis: 1 = X, 2 = Y, 3 = Z ..."""

        c_Value = ctypes.c_double(Value)
        c_Wait = ctypes.c_bool(Wait)
        answer = self.dll.LSX_MoveRelSingleAxis(self.LSID, Axis, c_Value, c_Wait)
        self.position = self.GetPos()[1:]
        return answer

    def GetDistance(self,
                    X: float,
                    Y: float,
                    Z: float,
                    A: float) -> tuple:

        """Get the Distance of MoveRelShort
        Tuple: error code: int,
                X: ctypes.c_double
                Y: ctypes.c_double
                Z: ctypes.c_double
                A: ctypes.c_double"""

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        return self.dll.LSX_GetDistance(self.LSID,
                                        ctypes.byref(c_X),
                                        ctypes.byref(c_Y),
                                        ctypes.byref(c_Z),
                                        ctypes.byref(c_A)
                                        ), c_X, c_Y, c_Z, c_A

    def SetDistance(self,
                    X: float,
                    Y: float,
                    Z: float,
                    A: float) -> int:

        '''Set distance for MoveRelShort'''

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        return self.dll.LSX_SetDistance(self.LSID, c_X, c_Y, c_Z, c_A)

    def MoveRelShort(self) -> int:

        """Moves by a relative vector to current position.
        Vector is set with LSX_SetDistance.
        Use when multiple moves by the same distance
        in succession are needed."""
        answer = self.dll.LSX_MoveRelShort(self.LSID)
        self.position = self.GetPos()[1:]
        return answer

    def StopAxes(self) -> int:

        """Interrupts all movement commands"""

        return self.dll.LSX_StopAxes(self.LSID)
    
    def GetVel(self,
                    X: float,
                    Y: float,
                    Z: float,
                    A: float) -> tuple:
        
        """Get the Velocity at which movements are executed
        Tuple: error code: int,
                X: ctypes.c_double
                Y: ctypes.c_double
                Z: ctypes.c_double
                A: ctypes.c_double"""

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        return self.dll.LSX_GetVel(self.LSID,
                                   ctypes.byref(c_X),
                                   ctypes.byref(c_Y),
                                   ctypes.byref(c_Z),
                                   ctypes.byref(c_A)
                                   ), c_X, c_Y, c_Z, c_A
    
    def SetVel(self, X, Y, Z, A) -> int:

        """Set the velocity at which movements are executed"""

        c_X = ctypes.c_double(X)
        c_Y = ctypes.c_double(Y)
        c_Z = ctypes.c_double(Z)
        c_A = ctypes.c_double(A)
        return self.dll.LSX_SetVel(self.LSID, c_X, c_Y, c_Z, c_A)
