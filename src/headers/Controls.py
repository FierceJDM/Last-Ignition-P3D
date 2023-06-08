from panda3d.core import *
from .misc.Steering import *
from .misc.MiscFunctions import *
from .Display import *
from .LoadObjects import *
from .Camera import *

InputMap = {
    "f1" : False,
    "e" : False,
    "r" : False,
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False,
    "c" : False,
    "mouse1" : False,
    "page_up" : False,
    "page_down" : False,
    "enter" : False
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
        self.GearList = []
        for gear in self.VehicleMetadata['GearList']:
            self.GearList.append((gear['gearduration'], gear['coef']))
        self.CurrentRPM = 100
        self.CurrentGear = 1

        self.accept("page_up", UpdateInputMap, ["page_up", True])
        self.accept("page_down", UpdateInputMap, ["page_down", True])
        self.accept("arrow_up", UpdateInputMap, ["up", True])
        self.accept("arrow_down", UpdateInputMap, ["down", True])
        self.accept("arrow_left", UpdateInputMap, ["left", True])
        self.accept("arrow_right", UpdateInputMap, ["right", True])
        self.accept("e", UpdateInputMap, ["e", True])
        self.accept("mouse1-up", UpdateInputMap, ["mouse1", True])
        self.accept("c-up", UpdateInputMap, ["c", True])
        self.accept("r-up", UpdateInputMap, ["r", True])
        self.accept("f1-up", UpdateInputMap, ["f1", True])
        self.accept("enter-up", UpdateInputMap, ["enter", True])

        self.accept("page_up-up", UpdateInputMap, ["page_up", False])
        self.accept("page_down-up", UpdateInputMap, ["page_down", False])
        self.accept("arrow_up-up", UpdateInputMap, ["up", False])
        self.accept("arrow_down-up", UpdateInputMap, ["down", False])
        self.accept("arrow_left-up", UpdateInputMap, ["left", False])
        self.accept("arrow_right-up", UpdateInputMap, ["right", False])
        self.accept("e-up", UpdateInputMap, ["e", False])

    def Update(self):
        self.Width, self.Height = base.win.getXSize(), base.win.getYSize()
        








        #-------------------------------TODO : Terrain Switch (WIP)------------------------------------------


        
        if 315 < round(self.ChassisNP.getPos().getY())%(128*6) < 453:

            if round(self.ChassisNP.getPos().getY())%(128*6) <= 384 and self.TerrainsStatus != 1:

                if self.Terrain2 != None and round(abs(self.ChassisNP.getPos().getY() - self.Terrain1.BTerrainNP.getPos().getY()))  >  round(abs(self.ChassisNP.getPos().getY() - self.Terrain2.BTerrainNP.getPos().getY())):
                    # Replaces Terrain1 with Terrain2
                    TempTerrain = self.Terrain1
                    self.Terrain1 = self.Terrain2
                    self.Terrain2 = TempTerrain
                    self.TerrainsStatus = 1
                elif self.Terrain2 != None and round(abs(self.ChassisNP.getPos().getY() - self.Terrain1.BTerrainNP.getPos().getY()))  ==  round(abs(self.ChassisNP.getPos().getY() - self.Terrain2.BTerrainNP.getPos().getY())):
                    print("same distance")
                else:
                    # Creates Terrain2
                    self.Terrain2 = NewTerrain('Terrain2', [0, self.Terrain1.BTerrainNP.getPos().getY()+768, 0], "../assets/media/output_COP30.png", "../assets/media/output_COP301.png", self.EverythingNP, self.world, self.loader, self.camera)
                    self.TerrainsStatus = 1


            elif round(self.ChassisNP.getPos().getY())%(128*6) > 384 and self.TerrainsStatus != 2:

                if self.Terrain2 != None and round(abs(self.ChassisNP.getPos().getY() - self.Terrain1.BTerrainNP.getPos().getY()))  >  round(abs(self.ChassisNP.getPos().getY() - self.Terrain2.BTerrainNP.getPos().getY())):
                    # Replaces Terrain1 with Terrain2
                    TempTerrain = self.Terrain1
                    self.Terrain1 = self.Terrain2
                    self.Terrain2 = TempTerrain
                    self.TerrainsStatus = 2
                elif self.Terrain2 != None and round(abs(self.ChassisNP.getPos().getY() - self.Terrain1.BTerrainNP.getPos().getY()))  ==  round(abs(self.ChassisNP.getPos().getY() - self.Terrain2.BTerrainNP.getPos().getY())):
                    print("same distance")
                else:
                    # Creates Terrain2
                    self.Terrain2 = NewTerrain('Terrain2', [0, self.Terrain1.BTerrainNP.getPos().getY()-768, 0], "../assets/media/output_COP30.png", "../assets/media/output_COP301.png", self.EverythingNP, self.world, self.loader, self.camera)
                    self.TerrainsStatus = 2


        else:
            self.TerrainsStatus = 0
            if self.Terrain2 != None:
                self.Terrain2.Unload(self.world)
                self.Terrain2 = None

        

        #if X is in-between:
            #if its here:
                #do this
            #if its there:
                #do that
        #else:
            #idk




        # TODO : Study Possible Conflict between Y and X Terrain Check





        #-------------------------------     Terrain Switch (WIP)      ------------------------------------------













        if base.mouseWatcherNode.hasMouse():    
            self.MouseX = (base.mouseWatcherNode.getMouseX()+1)*self.Width/2
            self.MouseY = (-base.mouseWatcherNode.getMouseY()+1)*self.Height/2

        if InputMap["mouse1"]:
            if self.CurrentDisplay == "Home":
                for i in range(len(self.MenuNP)-3): # Cycle through all buttons of the group
                    BGPos = Display.ButtonGroup.GetButtonPos(self, self.MenuNP[i+1])

                    if(BGPos[0] < self.MouseX < BGPos[1] and BGPos[2] < self.MouseY < BGPos[3]):
                        if self.HomeState == "Main":
                            if i+1 == 1:
                                Display.ChangeDisplay(self, "Game")
                            if i+1 == 2:
                                self.HomeState = "Multiplayer"
                        elif self.HomeState == "Multiplayer":
                            if i+1 == 2:
                                self.HomeState = "Main"
            UpdateInputMap("mouse1", False)

        if InputMap["enter"]:
            if self.CurrentDisplay == "Splash":
                if self.SplashState == [1, 1]:
                    self.SplashState = [1, 2]
            UpdateInputMap("enter", False)


        if InputMap["page_up"]:
            Camera.Rotate.Update(self, -90)
        elif InputMap["page_down"]:
            Camera.Rotate.Update(self, 90)
        elif InputMap["e"]:
            Camera.Rotate.Update(self, 180)
        else:
            if InputMap["c"]: # Cycle Cam
                if self.CurrentDisplay == "Game":
                    Camera.CycleCameras(self)
                UpdateInputMap("c", False)
            Camera.Update(self)

        if InputMap["r"]: # Respawn
            self.ChassisNP.node().setLinearVelocity(Point3(0, 0, 0))
            self.ChassisNP.node().setAngularVelocity(Point3(0, 0, 0))
            self.ChassisNP.setPos(0, 300, 12)
            self.ChassisNP.setHpr(0, 0, 0)
            UpdateInputMap("r", False)

        if InputMap["f1"]: # Debug Mode
            if self.DebugNP.isHidden():
                self.DebugNP.show()
            else:
                self.DebugNP.hide()
            UpdateInputMap("f1", False)



        if InputMap["up"]: # Forward
            self.engineForce = MiscFunctions.SetSpeedKmHour(self, True, 5000, self.GearList)

            if self.Vehicle.getCurrentSpeedKmHour() != 0:
                self.PedalsStatus = 0.03
            self.brakeForce = 0.0
        elif InputMap["down"]: # Backward
            MiscFunctions.SetSpeedKmHour(self, False, 5000, self.GearList)

            if self.Vehicle.getCurrentSpeedKmHour() >= -15:
                self.engineForce = -3500.0
                if self.Vehicle.getCurrentSpeedKmHour() != 0:
                    self.PedalsStatus = -0.03
            else:
                self.engineForce = 0
            self.brakeForce = 50
        else:
            MiscFunctions.SetSpeedKmHour(self, False, 5000, self.GearList)

            self.PedalsStatus = 0
            self.engineForce = 0
            self.brakeForce = 5


        if InputMap["left"]:
            Steer.Left(self)

            if -1 < self.Vehicle.getCurrentSpeedKmHour() < 1:
                Camera.Zero(self, True)
            else:
                Camera.Turn(self, self.SteerLimit)
        elif InputMap["right"]:
            Steer.Right(self)
            
            if -1 < self.Vehicle.getCurrentSpeedKmHour() < 1:
                Camera.Zero(self, True)
            else:
                Camera.Turn(self, self.SteerLimit)
        else: # Bring values to Zero
            if -5 < self.Steering < 5:
                self.Steering = 0.0
            elif self.Steering < 0:
                self.Steering += self.dt * 60
            elif self.Steering > 0:
                self.Steering -= self.dt * 60
            
            Camera.Zero(self, False)


        self.Vehicle.setSteeringValue(self.Steering, 0)
        self.Vehicle.setSteeringValue(self.Steering, 1)
        self.Vehicle.applyEngineForce(self.engineForce, 2)
        self.Vehicle.applyEngineForce(self.engineForce, 3)
        self.Vehicle.setBrake(self.brakeForce, 2)
        self.Vehicle.setBrake(self.brakeForce, 3)