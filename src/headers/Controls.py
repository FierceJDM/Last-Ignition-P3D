from panda3d.core import *
from math import *
from MiscFunctions import *

keyMap = {
    "f1" : False,
    "w" : False,
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False,
    "y" : False,
    "g" : False,
    "h" : False,
    "j" : False
}
def updateKeyMap(key, state):
    keyMap[key] = state

class Controls():
    def __init__(self):


        self.accept("f1", updateKeyMap, ["f1", True])
        self.accept("w", updateKeyMap, ["w", True])
        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("y", updateKeyMap, ["y", True])
        self.accept("g", updateKeyMap, ["g", True])
        self.accept("h", updateKeyMap, ["h", True])
        self.accept("j", updateKeyMap, ["j", True])

        self.accept("f1-up", updateKeyMap, ["f1", False])
        self.accept("w-up", updateKeyMap, ["w", False])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])
        self.accept("y-up", updateKeyMap, ["y", False])
        self.accept("g-up", updateKeyMap, ["g", False])
        self.accept("h-up", updateKeyMap, ["h", False])
        self.accept("j-up", updateKeyMap, ["j", False])

    def Update(self):
        SmileyPos = self.ChassisNP.getPos()
        SmileyVel = self.ChassisNP.node().getLinearVelocity()
        SmileyHPR = self.ChassisNP.getHpr()

        self.steering = 0.0
        self.steeringClamp = 45.0
        self.steeringIncrement = 10000.0


        if keyMap["w"]:
            SmileyPos.z = 5
            SmileyPos.x = -6
            SmileyPos.y = -8
            self.ChassisNP.node().setLinearVelocity(Point3(0, 0, 0))
            self.ChassisNP.node().setAngularVelocity(Point3(0, 0, 0))
            self.ChassisNP.setPos(SmileyPos)
            self.ChassisNP.setHpr(0, 0, 0)

        if keyMap["f1"]:
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()

        if keyMap["up"]:
            self.engineForce = 2000.0
            self.brakeForce = 0.0
        
        if keyMap["down"]:
            self.engineForce = 0.0
            self.brakeForce = 50.0
        

        if keyMap["left"]:
            if self.Vehicle.getCurrentSpeedKmHour() < 0:
                self.RelaxedCamPos = TranslatePercentage(-(-self.Vehicle.getCurrentSpeedKmHour()/10),
                                                         15, 
                                                         self.RelaxedCamPos
                )
            else:
                self.RelaxedCamPos = TranslatePercentage(-(self.Vehicle.getCurrentSpeedKmHour()/10),
                                                         15, 
                                                         self.RelaxedCamPos
                )

            self.CamPosResetTotal = self.RelaxedCamPos
            self.CamPosResetProgress = 0
            self.steering += self.dt * self.steeringIncrement
            self.steering = min(self.steering, self.steeringClamp)
        

        elif keyMap["right"]:
            if self.Vehicle.getCurrentSpeedKmHour() < 0:
                self.RelaxedCamPos = TranslatePercentage(-self.Vehicle.getCurrentSpeedKmHour()/10,
                                                         15, 
                                                         self.RelaxedCamPos
                )
            else:
                self.RelaxedCamPos = TranslatePercentage(self.Vehicle.getCurrentSpeedKmHour()/10,
                                                         15, 
                                                         self.RelaxedCamPos
                )
            self.CamPosResetTotal = self.RelaxedCamPos
            self.CamPosResetProgress = 0

            self.steering -= self.dt * self.steeringIncrement
            self.steering = max(self.steering, -self.steeringClamp)
        
        else:
            if self.RelaxedCamPos < -2:
                self.CamPosResetProgress = TranslatePercentage(self.dt*-25,
                                                               -self.CamPosResetTotal, 
                                                               self.CamPosResetProgress
                )
                self.RelaxedCamPos = self.RelaxedCamPos - self.CamPosResetProgress
            elif self.RelaxedCamPos > 2:
                self.CamPosResetProgress = TranslatePercentage(self.dt*25, 
                                                               self.CamPosResetTotal, 
                                                               self.CamPosResetProgress
                )
                self.RelaxedCamPos = self.RelaxedCamPos - self.CamPosResetProgress
            else:
                self.CamPosResetProgress = 0
                self.RelaxedCamPos = 0