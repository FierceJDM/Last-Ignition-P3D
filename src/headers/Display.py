from .misc.MiscFunctions import *
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage


class Display():

    class Game():
        def __init__(self):
            base.setBackgroundColor(0, 0.5, 1)
            self.EverythingNP.reparentTo(self.render)

            self.SpeedNP = aspect2d.attachNewNode(TextNode('currentspeed'))
            self.SpeedNP.node().setText("0")
            self.SpeedNP.node().setTextColor(0, 0, 0, 1)
            self.SpeedNP.node().setAlign(TextNode.ACenter)
            self.SpeedNP.setScale(0.2)
            self.SpeedNP.setPos(1.36, 0, -0.65)
            
            self.SpeedometerNP = aspect2d.attachNewNode(CardMaker('speedometer').generate())
            self.SpeedometerNP.setTexture(loader.loadTexture('../assets/media/speedo1.png'))
            self.SpeedometerNP.setTransparency(TransparencyAttrib.MAlpha)
            self.SpeedometerNP.setScale(1.25, 1, 1.0)
            self.SpeedometerNP.setPos(0.75, 0, -1.10)


        def Update(self):
            self.SpeedNP.node().setText(f"{abs(round(self.Vehicle.getCurrentSpeedKmHour()))}")

        def Close(self):
            self.EverythingNP.detachNode()
            self.SpeedometerNP.detachNode()
            self.SpeedNP.detachNode()


    class Home():
        def __init__(self):
            base.setBackgroundColor(0, 0, 0)
            
            self.WelcomeNP = pixel2d.attachNewNode(TextNode('welcome'))
            self.WelcomeNP.node().setText("Welcome")
            self.WelcomeNP.node().setTextColor(1, 1, 1, 1)
            self.WelcomeNP.node().setAlign(TextNode.ACenter)
            self.WelcomeNP.setScale(150)
            
            self.buttontex = loader.loadTexture('../assets/media/Home-Button.png')
            self.ButtonNP = pixel2d.attachNewNode(CardMaker('button').generate())
            self.ButtonNP.setTexture(self.buttontex)
            self.ButtonNP.setScale(self.buttontex.getXSize(), 0, self.buttontex.getYSize())

        def Update(self):
            if self.Width != 0:
                if ThreeConv(ThreeConv(50, 100, self.Width) - (self.buttontex.getXSize()/2),
                             self.Width,
                             2
                )-1 < self.MouseX < ThreeConv(ThreeConv(50, 100, self.Width) + (self.buttontex.getXSize()/2),
                                              self.Width,
                                              2
                )-1 and -((75*self.Height/100  -  self.buttontex.getYSize()/2)*2/self.Height-1) > self.MouseY > -((75*self.Height/100  +  self.buttontex.getYSize()/2)*2/self.Height-1):
                    base.setBackgroundColor(1, 0, 0)
                else:
                    base.setBackgroundColor(0, 0, 0)
            
            self.ButtonNP.setPos((50*self.Width/100)-(self.buttontex.getXSize()/2),
                                 0, 
                                 -(75*self.Height/100)-(self.buttontex.getYSize()/2)
            )
            self.WelcomeNP.setPos((50*self.Width/100),
                                  0,
                                  -(50*self.Height/100)
            )

        def Close(self):
            self.WelcomeNP.detachNode()
            self.ButtonNP.detachNode()



    def __init__(self):
        self.CurrentDisplay = "Home"
        self.ChangeDisplay = False


    def ChangeDisplay(self, display):
        self.ChangeDisplay = True

        # Close Current Display
        if self.CurrentDisplay == "Home":
            Display.Home.Close(self)
        elif self.CurrentDisplay == "Game":
            Display.Game.Close(self)
        
        # Init Desired Display
        if display == "Home":
            Display.Home.__init__(self)
        elif display == "Game":
            Display.Game.__init__(self)
        
        # Change Variables to Desired State
        self.ChangeDisplay = False
        self.CurrentDisplay = display


    def Update(self):
        if self.ChangeDisplay == False:
            if self.CurrentDisplay == "Home":
                Display.Home.Update(self)
            elif self.CurrentDisplay == "Game":
                Display.Game.Update(self)