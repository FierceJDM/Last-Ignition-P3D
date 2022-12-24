from panda3d.core import *
from .misc.Steering import *
from .misc.MiscFunctions import *
from .Display import *
from .Camera import *

InputMap = {
    "f1" : False,
    "w" : False,
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False,
    "y" : False,
    "g" : False,
    "h" : False,
    "j" : False,
    "escape" : False,
    "mouse1" : False
}

def UpdateInputMap(key, state):
    InputMap[key] = state

class Controls():
    def __init__(self):
        self.Width, self.Height = 0, 0
        self.MouseX, self.MouseY = 0, 0
        self.PedalsStatus = 0
        self.Steering = 0.0
        self.SteerLimit = 0.0
        self.engineForce = 0.0
        self.brakeForce = 0.0

        self.accept("f1", UpdateInputMap, ["f1", True])
        self.accept("w", UpdateInputMap, ["w", True])
        self.accept("arrow_up", UpdateInputMap, ["up", True])
        self.accept("arrow_down", UpdateInputMap, ["down", True])
        self.accept("arrow_left", UpdateInputMap, ["left", True])
        self.accept("arrow_right", UpdateInputMap, ["right", True])
        self.accept("y", UpdateInputMap, ["y", True])
        self.accept("g", UpdateInputMap, ["g", True])
        self.accept("h", UpdateInputMap, ["h", True])
        self.accept("j", UpdateInputMap, ["j", True])
        self.accept("escape", UpdateInputMap, ["escape", True])
        self.accept("mouse1", UpdateInputMap, ["mouse1", True])

        self.accept("f1-up", UpdateInputMap, ["f1", False])
        self.accept("w-up", UpdateInputMap, ["w", False])
        self.accept("arrow_up-up", UpdateInputMap, ["up", False])
        self.accept("arrow_down-up", UpdateInputMap, ["down", False])
        self.accept("arrow_left-up", UpdateInputMap, ["left", False])
        self.accept("arrow_right-up", UpdateInputMap, ["right", False])
        self.accept("y-up", UpdateInputMap, ["y", False])
        self.accept("g-up", UpdateInputMap, ["g", False])
        self.accept("h-up", UpdateInputMap, ["h", False])
        self.accept("j-up", UpdateInputMap, ["j", False])
        self.accept("escape-up", UpdateInputMap, ["escape", False])
        self.accept("mouse1-up", UpdateInputMap, ["mouse1", False])

    def Update(self):
        self.Width, self.Height = base.win.getXSize(), base.win.getYSize()

        if base.mouseWatcherNode.hasMouse():
            self.MouseX = base.mouseWatcherNode.getMouseX()
            self.MouseY = base.mouseWatcherNode.getMouseY()

        if InputMap["mouse1"]:
            if (50*self.Width/100  -  self.buttontex.getXSize()/2)*2/self.Width-1 < self.MouseX < (50*self.Width/100  +  self.buttontex.getXSize()/2)*2/self.Width-1 and -((75*self.Height/100  -  self.buttontex.getYSize()/2)*2/self.Height-1) > self.MouseY > -((75*self.Height/100  +  self.buttontex.getYSize()/2)*2/self.Height-1):
                Display.ChangeDisplay(self, "Game")


        if InputMap["w"]: # Respawn
            self.ChassisNP.node().setLinearVelocity(Point3(0, 0, 0))
            self.ChassisNP.node().setAngularVelocity(Point3(0, 0, 0))
            self.ChassisNP.setPos(0, 200, 12)
            self.ChassisNP.setHpr(0, 0, 0)


        if InputMap["f1"]: # Debug Mode
            if self.DebugNP.isHidden():
                self.DebugNP.show()
            else:
                self.DebugNP.hide()


        if InputMap["up"]: # Forward
            if self.Vehicle.getCurrentSpeedKmHour() != 0:
                self.PedalsStatus = 0.03
            self.engineForce = SetSpeedKmHour(self.Vehicle.getCurrentSpeedKmHour())
            self.brakeForce = 0.0
        elif InputMap["down"]: # Backward
            if self.Vehicle.getCurrentSpeedKmHour() != 0:
                self.PedalsStatus = -0.03
            self.engineForce = -4000.0
            self.brakeForce = 50
        else:
            self.PedalsStatus = 0
            self.engineForce = 0
            self.brakeForce = 5

        if InputMap["left"]:
            Steer.Left(self)

            if -1 < self.Vehicle.getCurrentSpeedKmHour() < 1:
                Camera.FirstPerson.Zero(self, True)
            else:
                Camera.FirstPerson.Turn(self, self.SteerLimit)
    
        elif InputMap["right"]:
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