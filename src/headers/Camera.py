from .MiscFunctions import *
from math import *

class Camera():
    def __init__(self):
        self.CamOffset = 0
        

    class FirstPerson():
        def Zero(self, turn):
            if turn==True:
                if self.CamOffset < 0:
                    self.CamOffset += Dampen( 25*self.dt*(13/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= Dampen( 25*self.dt*(13/30) , self.CamOffset)
            else:
                if self.CamOffset < 0:
                    self.CamOffset += Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset)
            

        def Turn(self, limitpos):
            if limitpos > 0:
                if self.CamOffset < limitpos:
                    self.CamOffset += Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset, limitpos)
            elif limitpos < 0:
                if self.CamOffset > limitpos:
                    self.CamOffset -= Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset, limitpos)
        
    
    
    def Update(self):
        ChassisPos = self.ChassisNP.getPos()
        ChassisHPR = self.ChassisNP.getHpr()
        if self.Vehicle.getCurrentSpeedKmHour() < 50:
            self.camera.setPos( ChassisPos.getX()  +  (7 + (0.7*self.Vehicle.getCurrentSpeedKmHour()/50) ) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getY()  -  (7 + (0.7*self.Vehicle.getCurrentSpeedKmHour()/50) ) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.8
            )
        elif 50 < self.Vehicle.getCurrentSpeedKmHour() < 100:
            self.camera.setPos( ChassisPos.getX()  +  (7.7 + (0.5*(self.Vehicle.getCurrentSpeedKmHour()-50)/50) ) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getY()  -  (7.7 + (0.5*(self.Vehicle.getCurrentSpeedKmHour()-50)/50) ) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.8
            )
        elif 100 < self.Vehicle.getCurrentSpeedKmHour() < 200:
            self.camera.setPos( ChassisPos.getX()  +  (8.2 + (0.3*(self.Vehicle.getCurrentSpeedKmHour()-100)/100) ) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getY()  -  (8.2 + (0.3*(self.Vehicle.getCurrentSpeedKmHour()-100)/100) ) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.8
            )
        else:
            self.camera.setPos( ChassisPos.getX()  +  8.5 * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                ChassisPos.getY()  -  8.5 * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.8
            )


        self.camera.setHpr( ChassisHPR.getX()+self.CamOffset ,
                            0 ,
                            0)