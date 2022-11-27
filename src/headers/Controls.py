from panda3d.core import *
from .Camera import *
from .Steering import *
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
        self.PedalsStatus = 0
        self.Steering = 0.0
        self.SteerLimit = 0.0
        self.engineForce = 0.0
        self.brakeForce = 0.0

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

        if KeyMap["w"]: # Respawn
            self.ChassisNP.node().setLinearVelocity(Point3(0, 0, 0))
            self.ChassisNP.node().setAngularVelocity(Point3(0, 0, 0))
            self.ChassisNP.setPos(0, 200, 12)
            self.ChassisNP.setHpr(0, 0, 0)


        if KeyMap["f1"]: # Debug Mode
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()


        if KeyMap["up"]: # Forward
            self.PedalsStatus = 0.05
            self.engineForce = SetSpeedKmHour(self.Vehicle.getCurrentSpeedKmHour())
            self.brakeForce = 0.0
        elif KeyMap["down"]: # Backward
            self.PedalsStatus = -0.05
            self.engineForce = -4000.0
            self.brakeForce = 50
        else:
            self.PedalsStatus = 0
            self.engineForce = 0
            self.brakeForce = 5

        if KeyMap["left"]:
            Steer.Left(self)

            if -1 < self.Vehicle.getCurrentSpeedKmHour() < 1:
                Camera.FirstPerson.Zero(self, True)
            else:
                Camera.FirstPerson.Turn(self, self.SteerLimit)
    
        elif KeyMap["right"]:
            Steer.Right(self)
            
            if -1 < self.Vehicle.getCurrentSpeedKmHour() < 1:
                Camera.FirstPerson.Zero(self, True)
            else:
                Camera.FirstPerson.Turn(self, self.SteerLimit)

        else: # Bring values to Zero
            if -5 < self.Steering < 5:
                self.Steering = 0.0
            elif self.Steering < 0:
                self.Steering += self.dt * 60
            elif self.Steering > 0:
                self.Steering -= self.dt * 60
            
            Camera.FirstPerson.Zero(self, False)

        self.Vehicle.setSteeringValue(self.Steering, 0)
        self.Vehicle.setSteeringValue(self.Steering, 1)
        self.Vehicle.applyEngineForce(self.engineForce, 2)
        self.Vehicle.applyEngineForce(self.engineForce, 3)
        self.Vehicle.setBrake(self.brakeForce, 2)
        self.Vehicle.setBrake(self.brakeForce, 3)