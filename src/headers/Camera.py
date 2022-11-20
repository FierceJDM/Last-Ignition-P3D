from .MiscFunctions import *
from math import *

class Camera():
    def __init__(self):
        self.CamOffset = 0
        self.SpeedB, self.SpeedA = 0, 0
        self.CarCrashed = False

    class FirstPerson():
        def Zero(self, turn):
            if turn==True:
                if self.CamOffset < 0:
                    self.CamOffset += Dampen( 30*self.dt*(13/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= Dampen( 30*self.dt*(13/30) , self.CamOffset)
            else:
                if self.CamOffset < 0:
                    self.CamOffset += Dampen( 30*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= Dampen( 30*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset)
            

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

        # Check if car has crashed :
        self.SpeedA = self.Vehicle.getCurrentSpeedKmHour()
        if self.SpeedA-self.SpeedB < 0 and abs(self.SpeedA-self.SpeedB) > 10:
            self.CarCrashed = True
            self.Increment = (0.7*self.SpeedB/50)
        self.SpeedB = self.Vehicle.getCurrentSpeedKmHour()



        if self.CarCrashed: # If yes, bring camera position near ideal 
            self.camera.setPos( ChassisPos.getX()  +  (7 + self.Increment ) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getY()  -  (7 + self.Increment ) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.8
            )

            self.Increment -= 0.04
            if self.Increment < 0.05:
                self.CarCrashed = False

        else: # If not, execute normal camera positioning 
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