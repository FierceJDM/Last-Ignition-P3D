from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
from headers.Display import *
from headers.Controls import *
from headers.LoadObjects import *
from headers.Camera import *



loadPrcFile("config_file.prc")


class MainApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.EverythingNP = NodePath('Everything')
        
        InitiateAllObjects(self)

        # -----------------------Initiate Classes and Functions Below----------------------------

        Controls.__init__(self)
        Camera.__init__(self)
        Display.__init__(self)
        Display.Home.__init__(self)

        # ----------------------------Configure Tasks---------------------------------

        self.taskMgr.add(self.update, "update")







    def update(self, task):
        self.dt = globalClock.getDt()
        self.world.doPhysics(self.dt)

        # ------------------------Update Everything Below----------------------------
        
        #if <certain cam state>:
        #   update <that cam state>
        Camera.FirstPerson.Update(self)
        Display.Update(self)
        Controls.Update(self)

        return task.cont



            

app = MainApp()
app.run()




# TODO : Add UI and Menus
# TODO : Setup Entire Map
# TODO : Add Drift Physics
# TODO : Add Audio (Music, Car Sounds, ...)

# TODO : Add Other Cameras (Far, 1st, Hood)
# TODO : Refactor Vehicle's Wheels definition