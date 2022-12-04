from panda3d.core import *
from .Camera import *

class Display():
    class Game():
        def __init__(self):
            self.EverythingNP.reparentTo(self.render)

            self.SpeedNP = aspect2d.attachNewNode(TextNode("speed"))
            self.SpeedNP.node().setText("0")
            self.SpeedNP.node().setTextColor(0, 0, 0, 1)
            self.SpeedNP.node().setAlign(TextNode.ACenter)
            self.SpeedNP.setScale(0.2)
            self.SpeedNP.setPos(1.36, 0, -0.65)
            
            self.SpeedometerNP = aspect2d.attachNewNode(CardMaker('speedometer').generate())
            self.SpeedometerNP.setTexture(loader.loadTexture('../assets/media/speedo1.png'))
            self.SpeedometerNP.setTransparency(TransparencyAttrib.MAlpha)
            self.SpeedometerNP.setScale(1.25, 1, 1.1)
            self.SpeedometerNP.setPos(0.75, 0, -1.15)


        def Update(self):
            self.SpeedNP.node().setText(f"{abs(round(self.Vehicle.getCurrentSpeedKmHour()))}")

        def Close(self):
            self.EverythingNP.detachNode()
            self.SpeedometerNP.detachNode()
            self.SpeedNP.detachNode()
            