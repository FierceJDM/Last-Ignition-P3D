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
        self.NotifFont = loader.loadFont('../assets/media/Notificateur.ttf')
        slantfont = TextProperties()
        slantfont.setSlant(0.3)
        textpropMgr = TextPropertiesManager.getGlobalPtr()
        textpropMgr.setProperties("slant", slantfont)
        self.EverythingNP = NodePath('Everything')
        base.camLens.setFov(45)
        
        InitiateAllObjects(self)

        # -----------------------Initiate Classes and Functions Below----------------------------

        Controls.__init__(self)
        Camera.__init__(self)
        Display.__init__(self)

        # ----------------------------Configure Tasks---------------------------------

        self.taskMgr.add(self.update, "update")







    def update(self, task):
        self.dt = globalClock.getDt()
        self.world.doPhysics(self.dt)

        # ------------------------Update Everything Below----------------------------
        
        Display.Update(self)
        Controls.Update(self)

        return task.cont



            

app = MainApp()
app.run()


# ------------------------- Tasks for v1.0.0 : ---------------------------------

# TODO : Setup Entire Map
# TODO : Add Audio (Music, Car Sounds, ...)
# TODO : Add Content (Goal : 10 cars, 10 songs)

# ---------FINISH THE ONES BELOW BEFORE PROCEEDING TO THE ONES ABOVE----------

# TODO : Add UI and Menus (Menus, Video)

# ------------------------- Tasks for v1.1.0 : ------------------------------

# TODO : Add Garage, Customization System
# TODO : Add Drift Physics
# TODO : Add Multiplayer