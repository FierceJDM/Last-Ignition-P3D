from panda3d.core import *
from .MiscFunctions import *

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
            # Add Power to Engine
            self.engineForce = 2000.0
            self.brakeForce = 0.0
            

        if keyMap["down"]:
            self.engineForce = -1700.0
        

        if keyMap["left"]:
            self.Steering += self.dt * self.SteeringIncrement
            self.Steering = min(self.Steering, self.SteeringClamp)

            if -3 < self.Vehicle.getCurrentSpeedKmHour() < 3:
                if self.CamOffset < 0:
                    self.CamOffset += 14*self.dt*(6/30)
                if self.CamOffset > 0:
                    self.CamOffset -= 14*self.dt*(6/30)
            else:
                if self.CamOffset > -10:
                    self.CamOffset -= 14*self.dt*(abs(DivByZero(self.Steering, 6))/30)
    

        elif keyMap["right"]:
            self.Steering -= self.dt * self.SteeringIncrement
            self.Steering = max(self.Steering, -self.SteeringClamp)
            
            if -3 < self.Vehicle.getCurrentSpeedKmHour() < 3:
                if self.CamOffset < 0:
                    self.CamOffset += 14*self.dt*(6/30)
                if self.CamOffset > 0:
                    self.CamOffset -= 14*self.dt*(6/30)
            else:
                if self.CamOffset < 10:
                    self.CamOffset += 14*self.dt*(abs(DivByZero(self.Steering, 6))/30)


        else:
            # Bring Steering near 0
            if -0.1 < self.Steering < 0.1:
                self.Steering = 0.0
            elif self.Steering < 0:
                self.Steering += self.dt * self.SteeringIncrement
            elif self.Steering > 0:
                self.Steering -= self.dt * self.SteeringIncrement
            
            #Bring camoffset near 0
            if self.CamOffset < 0:
                self.CamOffset += 14*self.dt*(abs(DivByZero(self.Steering, 6))/30)
            
            if self.CamOffset > 0:
                self.CamOffset -= 14*self.dt*(abs(DivByZero(self.Steering, 6))/30)







# TODO : Tweak values of Camera dynamics and add dynamics for Yaw rotation.
# TODO : Decrease Steering power and speed when Speed gets higher.