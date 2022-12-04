from .misc.MiscFunctions import *
from math import *

class Camera():
    def __init__(self):
        self.BringNear = 0
        self.CamOffset = 0
        self.SpeedB, self.SpeedA = 0, 0
        self.CarCrashed = False

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
                    self.CamOffset += Dampen( 70*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset, limitpos)
            elif limitpos < 0:
                if self.CamOffset > limitpos:
                    self.CamOffset -= Dampen( 70*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset, limitpos)
        
    

        def Update(self):
            ChassisPos = self.ChassisNP.getPos()
            ChassisHPR = self.ChassisNP.getHpr()

            # Check if car has crashed :
            self.SpeedA = self.Vehicle.getCurrentSpeedKmHour()
            if self.SpeedA-self.SpeedB < 0 and abs(self.SpeedA-self.SpeedB) > 8:
                self.CarCrashed = True
                self.BringNear = (1*self.SpeedB/100)
            self.SpeedB = self.Vehicle.getCurrentSpeedKmHour()



            if self.CarCrashed: # If yes, bring camera position near ideal 
                self.BringNear -= 0.01
                if self.BringNear < 0.05:
                    self.BringNear = 0
                    self.CarCrashed = False

                self.camera.setPos( ChassisPos.getX()  +  (7 + self.BringNear ) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getY()  -  (7 + self.BringNear ) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                    ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                )


            else: # If not, execute normal camera positioning

                if self.BringNear < self.PedalsStatus:
                    self.BringNear += 0.005
                elif self.BringNear > self.PedalsStatus:
                    self.BringNear -= 0.005


                if self.Vehicle.getCurrentSpeedKmHour() < 100:
                    self.camera.setPos( ChassisPos.getX()  +  (7 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.BringNear) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                        ChassisPos.getY()  -  (7 + (1*self.Vehicle.getCurrentSpeedKmHour()/100) + self.BringNear) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  ,
                                        ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                    )
                else:
                    self.camera.setPos( ChassisPos.getX()  +  (8 + self.BringNear) * Truncate(sin((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                        ChassisPos.getY()  -  (8 + self.BringNear) * Truncate(cos((ChassisHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                                        ChassisPos.getZ()  -  2.5 * Truncate(sin(ChassisHPR.getY()*(pi/180)), 5)+0.7
                    )


            self.camera.setHpr( ChassisHPR.getX()+self.CamOffset ,
                                0 ,
                                0)