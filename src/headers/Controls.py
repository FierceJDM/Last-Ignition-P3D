from panda3d.core import *
from .MiscFunctions import *

KeyMap = {
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

def UpdateKeyMap(key, state):
    KeyMap[key] = state

class Controls():
    def __init__(self):


        self.accept("f1", UpdateKeyMap, ["f1", True])
        self.accept("w", UpdateKeyMap, ["w", True])
        self.accept("arrow_up", UpdateKeyMap, ["up", True])
        self.accept("arrow_down", UpdateKeyMap, ["down", True])
        self.accept("arrow_left", UpdateKeyMap, ["left", True])
        self.accept("arrow_right", UpdateKeyMap, ["right", True])
        self.accept("y", UpdateKeyMap, ["y", True])
        self.accept("g", UpdateKeyMap, ["g", True])
        self.accept("h", UpdateKeyMap, ["h", True])
        self.accept("j", UpdateKeyMap, ["j", True])

        self.accept("f1-up", UpdateKeyMap, ["f1", False])
        self.accept("w-up", UpdateKeyMap, ["w", False])
        self.accept("arrow_up-up", UpdateKeyMap, ["up", False])
        self.accept("arrow_down-up", UpdateKeyMap, ["down", False])
        self.accept("arrow_left-up", UpdateKeyMap, ["left", False])
        self.accept("arrow_right-up", UpdateKeyMap, ["right", False])
        self.accept("y-up", UpdateKeyMap, ["y", False])
        self.accept("g-up", UpdateKeyMap, ["g", False])
        self.accept("h-up", UpdateKeyMap, ["h", False])
        self.accept("j-up", UpdateKeyMap, ["j", False])

    def Update(self):
        SmileyPos = self.ChassisNP.getPos()
        SmileyVel = self.ChassisNP.node().getLinearVelocity()
        SmileyHPR = self.ChassisNP.getHpr()

        if KeyMap["w"]:
            SmileyPos.z = 5
            SmileyPos.x = -6
            SmileyPos.y = -8
            self.ChassisNP.node().setLinearVelocity(Point3(0, 0, 0))
            self.ChassisNP.node().setAngularVelocity(Point3(0, 0, 0))
            self.ChassisNP.setPos(SmileyPos)
            self.ChassisNP.setHpr(0, 0, 0)


        if KeyMap["f1"]:
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()


        if KeyMap["up"]:
            # Add Power to Engine
            self.engineForce = 2000.0
            self.brakeForce = 0.0
            

        elif KeyMap["down"]:
            self.engineForce = -1700.0
            self.brakeForce = 0.0
        

        else:
            self.brakeForce = 5


        if KeyMap["left"]:
            self.Steering += self.dt * self.SteeringIncrement
            self.Steering = min(self.Steering, self.SteeringClamp)

            if -3 < self.Vehicle.getCurrentSpeedKmHour() < 3:
                if self.CamOffset < 0:
                    self.CamOffset += 25*self.dt*(15/30)
                if self.CamOffset > 0:
                    self.CamOffset -= 25*self.dt*(15/30)
            else:
                if self.CamOffset > -19:
                    self.CamOffset -= 25*self.dt*(abs(DivByZero(self.Steering, 13))/30)
    

        elif KeyMap["right"]:
            self.Steering -= self.dt * self.SteeringIncrement
            self.Steering = max(self.Steering, -self.SteeringClamp)
            
            if -3 < self.Vehicle.getCurrentSpeedKmHour() < 3:
                if self.CamOffset < 0:
                    self.CamOffset += 25*self.dt*(15/30)
                if self.CamOffset > 0:
                    self.CamOffset -= 25*self.dt*(15/30)
            else:
                if self.CamOffset < 19:
                    self.CamOffset += 25*self.dt*(abs(DivByZero(self.Steering, 13))/30)


        else:
            # Bring Steering near 0
            if -5 < self.Steering < 5:
                self.Steering = 0.0
            elif self.Steering < 0:
                self.Steering += self.dt * 60
            elif self.Steering > 0:
                self.Steering -= self.dt * 60
            
            #Bring camoffset near 0
            if self.CamOffset < 0:
                self.CamOffset += 25*self.dt*(abs(DivByZero(self.Steering, 13))/30)
            
            if self.CamOffset > 0:
                self.CamOffset -= 25*self.dt*(abs(DivByZero(self.Steering, 13))/30)







# TODO : Decrease Steering power and speed when Speed gets higher.