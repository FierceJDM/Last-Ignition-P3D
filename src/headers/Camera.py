from .misc.MiscFunctions import *
from math import *

class Camera():
    def __init__(self):
        self.CurrentCam = 0
        self.CamList = ["ThirdPerson", "Far", "Hood"]
        self.CrashOffset = 0
        self.CamOffset = 0
        self.SpeedB, self.SpeedA = 0, 0
        self.CarCrashed = False

    class ThirdPerson():
        def Zero(self, turn):
            if turn==True:
                if self.CamOffset < 0:
                    self.CamOffset += MiscFunctions.Dampen(self,  25*self.dt*(13/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= MiscFunctions.Dampen(self,  25*self.dt*(13/30) , self.CamOffset)
            else:
                if self.CamOffset < 0:
                    self.CamOffset += MiscFunctions.Dampen(self,  25*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= MiscFunctions.Dampen(self,  25*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset)
            
        def Turn(self, limitpos):
            if limitpos > 0:
                if self.CamOffset < limitpos:
                    self.CamOffset += MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
                else:
                    self.CamOffset -= MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
            elif limitpos < 0:
                if self.CamOffset > limitpos:
                    self.CamOffset -= MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
                else:
                    self.CamOffset += MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
        
        def Update(self):
            ChassisPos = self.ChassisNP.getPos()
            ChassisHPR = self.ChassisNP.getHpr()

            # Check if car has crashed :
            self.SpeedA = self.Vehicle.getCurrentSpeedKmHour()
            if self.SpeedA-self.SpeedB < 0 and abs(self.SpeedA-self.SpeedB) > 8:
                self.CarCrashed = True
                self.CrashOffset = (1*self.SpeedB/100)
            self.SpeedB = self.Vehicle.getCurrentSpeedKmHour()



            if self.CarCrashed: # If yes, bring camera position near ideal 
                self.CrashOffset -= 0.01
                if self.CrashOffset < 0.05:
                    self.CrashOffset = 0
                    self.CarCrashed = False

                self.camera.setPos( ChassisPos.getX()  +  (7 + self.CrashOffset ) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getY()  -  (7 + self.CrashOffset ) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                )


            else: # If not, execute normal camera positioning

                if self.CrashOffset < self.PedalsStatus:
                    self.CrashOffset += 0.005
                elif self.CrashOffset > self.PedalsStatus:
                    self.CrashOffset -= 0.005


                if self.Vehicle.getCurrentSpeedKmHour() < 100:
                    self.camera.setPos( ChassisPos.getX()  +  (7 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.CrashOffset) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                        ChassisPos.getY()  -  (7 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.CrashOffset) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                        ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                    )
                else:
                    self.camera.setPos( ChassisPos.getX()  +  (8 + self.CrashOffset) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                        ChassisPos.getY()  -  (8 + self.CrashOffset) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                        ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                    )


            self.camera.setHpr( ChassisHPR.getX()+self.CamOffset ,
                                0 ,
                                0)
    
    class Far():
        def Zero(self, turn):
            if turn==True:
                if self.CamOffset < 0:
                    self.CamOffset += MiscFunctions.Dampen(self,  25*self.dt*(13/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= MiscFunctions.Dampen(self,  25*self.dt*(13/30) , self.CamOffset)
            else:
                if self.CamOffset < 0:
                    self.CamOffset += MiscFunctions.Dampen(self,  25*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= MiscFunctions.Dampen(self,  25*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset)
            
        def Turn(self, limitpos):
            if limitpos > 0:
                if self.CamOffset < limitpos:
                    self.CamOffset += MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
                else:
                    self.CamOffset -= MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
            elif limitpos < 0:
                if self.CamOffset > limitpos:
                    self.CamOffset -= MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
                else:
                    self.CamOffset += MiscFunctions.Dampen(self,  70*self.dt*(abs(MiscFunctions.DivByZero(self, self.Steering, 13))/30) , self.CamOffset, limitpos)
        
        def Update(self):
            ChassisPos = self.ChassisNP.getPos()
            ChassisHPR = self.ChassisNP.getHpr()

            # Check if car has crashed :
            self.SpeedA = self.Vehicle.getCurrentSpeedKmHour()
            if self.SpeedA-self.SpeedB < 0 and abs(self.SpeedA-self.SpeedB) > 8:
                self.CarCrashed = True
                self.CrashOffset = (1*self.SpeedB/100)
            self.SpeedB = self.Vehicle.getCurrentSpeedKmHour()



            if self.CarCrashed: # If yes, bring camera position near ideal 
                self.CrashOffset -= 0.01
                if self.CrashOffset < 0.05:
                    self.CrashOffset = 0
                    self.CarCrashed = False

                self.camera.setPos( ChassisPos.getX()  +  (8 + self.CrashOffset ) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getY()  -  (8 + self.CrashOffset ) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                )


            else: # If not, execute normal camera positioning

                if self.CrashOffset < self.PedalsStatus:
                    self.CrashOffset += 0.005
                elif self.CrashOffset > self.PedalsStatus:
                    self.CrashOffset -= 0.005


                if self.Vehicle.getCurrentSpeedKmHour() < 100:
                    self.camera.setPos( ChassisPos.getX()  +  (8 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.CrashOffset) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                        ChassisPos.getY()  -  (8 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.CrashOffset) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                        ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                    )
                else:
                    self.camera.setPos( ChassisPos.getX()  +  (9 + self.CrashOffset) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                        ChassisPos.getY()  -  (9 + self.CrashOffset) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                        ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                    )


            self.camera.setHpr( ChassisHPR.getX()+self.CamOffset ,
                                0 ,
                                0)

    class Hood():
        def Update(self):
            ChassisPos = self.ChassisNP.getPos()
            ChassisHPR = self.ChassisNP.getHpr()

            self.camera.setPos( ChassisPos.getX()  +  0.34 * MiscFunctions.Truncate(self, sin((ChassisHPR.getX())*(pi/180)), 5)  , 
                                ChassisPos.getY()  -  0.34 * MiscFunctions.Truncate(self, cos((ChassisHPR.getX())*(pi/180)), 5)  , 
                                ChassisPos.getZ()  -  MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
            )

            self.camera.setHpr( ChassisHPR.getX(),
                                ChassisHPR.getY()-7,
                                ChassisHPR.getZ())

    class Rotate():
        def Update(self, angle):
            ChassisPos = self.ChassisNP.getPos()
            ChassisHPR = self.ChassisNP.getHpr()


            if self.Vehicle.getCurrentSpeedKmHour() < 100:
                self.camera.setPos( ChassisPos.getX()  +  (8 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.CrashOffset) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+angle-self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getY()  -  (8 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.CrashOffset) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+angle-self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                )
            else:
                self.camera.setPos( ChassisPos.getX()  +  (9 + self.CrashOffset) * MiscFunctions.Truncate(self, sin((ChassisHPR.getX()+angle)*(pi/180)), 5)  , 
                                    ChassisPos.getY()  -  (9 + self.CrashOffset) * MiscFunctions.Truncate(self, cos((ChassisHPR.getX()+angle)*(pi/180)), 5)  , 
                                    ChassisPos.getZ()  -  2.5 * MiscFunctions.Truncate(self, sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                )


            self.camera.setHpr( ChassisHPR.getX()+angle-self.CamOffset ,
                                0 ,
                                0)


    def Update(self):
        if self.CamList[self.CurrentCam] == "ThirdPerson":
            Camera.ThirdPerson.Update(self)
        elif self.CamList[self.CurrentCam] == "Far":
            Camera.Far.Update(self)
        elif self.CamList[self.CurrentCam] == "Hood":
            Camera.Hood.Update(self)


    def Zero(self, turn):
        if self.CamList[self.CurrentCam] == "ThirdPerson":
            Camera.ThirdPerson.Zero(self, turn)
        elif self.CamList[self.CurrentCam] == "Far":
            Camera.Far.Zero(self, turn)
    
    def Turn(self, limitpos):
        if self.CamList[self.CurrentCam] == "ThirdPerson":
            Camera.ThirdPerson.Turn(self, limitpos)
        elif self.CamList[self.CurrentCam] == "Far":
            Camera.Far.Turn(self, limitpos)

    def CycleCameras(self):
        if self.CurrentCam == len(self.CamList)-1:
            self.CurrentCam = 0
        else:
            self.CurrentCam += 1
