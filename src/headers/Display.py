from .misc.MiscFunctions import *
from panda3d.core import *
from direct.gui.OnscreenImage import OnscreenImage
import time

class Display():

    class Splash():
        def __init__(self):
            base.setBackgroundColor(0, 0, 0)
            self.SplashState = [0, 0]
            self.StartTime = 0

            self.MadeUsingNP = pixel2d.attachNewNode(TextNode('MadeWith'))
            self.MadeUsingNP.node().setText("\1slant\1Made using :\2")
            self.MadeUsingNP.node().setTextColor(1, 1, 1, 1)
            self.MadeUsingNP.node().setAlign(TextNode.ACenter)
            self.MadeUsingNP.node().setFont(self.NotifFont)

            self.PandaLogoTEX = loader.loadTexture('../assets/media/P3DLogo.png')
            self.PandaLogoNP = pixel2d.attachNewNode(CardMaker('pandalogo').generate())
            self.PandaLogoNP.setTexture(self.PandaLogoTEX)
            self.PandaLogoNP.setTransparency(True)

            self.LogoTEX = loader.loadTexture('../assets/media/Logo2.png')
            self.LogoNP = pixel2d.attachNewNode(CardMaker('logo').generate())
            self.LogoNP.setTexture(self.LogoTEX)
            self.LogoNP.setTransparency(True)

            self.CurtainsAlpha = 1
            self.CurtainsTEX = loader.loadTexture('../assets/media/Curtains.png')
            self.CurtainsNP = pixel2d.attachNewNode(CardMaker('curtains').generate())
            self.CurtainsNP.setTexture(self.CurtainsTEX)
            self.CurtainsNP.setTransparency(True)

        def Update(self):
            if self.SplashState[0] == 0:
                self.MadeUsingNP.setScale((75*self.Width/1920), 0, (75*self.Height/1080))
                self.MadeUsingNP.setPos((50*self.Width/100), 0, -(25*self.Height/100))

                self.PandaLogoNP.setScale(self.PandaLogoTEX.getXSize()*self.Width/1920,
                                          0, 
                                          self.PandaLogoTEX.getYSize()*self.Height/1080
                )
                self.PandaLogoNP.setPos((50*self.Width/100)-((self.PandaLogoTEX.getXSize()*self.Width/1920)/2),
                                        0, 
                                        -(55*self.Height/100)-((self.PandaLogoTEX.getYSize()*self.Height/1080)/2)
                )

                if self.SplashState[1] == 0:
                    self.CurtainsAlpha -= 0.02
                    if self.CurtainsAlpha < 0:
                        self.SplashState = [0, 1]
                if self.SplashState[1] == 1:
                    if self.StartTime == 0:
                        self.StartTime = time.time()
                    if (time.time() - self.StartTime) > 2:
                        self.StartTime = 0
                        self.SplashState = [0, 2]
                if self.SplashState[1] == 2:
                    self.CurtainsAlpha += 0.02
                    if self.CurtainsAlpha > 1 :
                        self.SplashState = [0, 3]
                if self.SplashState[1] == 3:
                    self.PandaLogoNP.detachNode()
                    self.MadeUsingNP.detachNode()
                    if self.StartTime == 0:
                        self.StartTime = time.time()
                    if (time.time() - self.StartTime) > 1.5:
                        self.StartTime = 0
                        self.SplashState = [1, 0]
            
            elif self.SplashState[0] == 1:
                self.LogoNP.setScale(self.LogoTEX.getXSize()*self.Width/1920,
                                     0, 
                                     self.LogoTEX.getYSize()*self.Height/1080
                )
                self.LogoNP.setPos((50*self.Width/100)-((self.LogoTEX.getXSize()*self.Width/1920)/2),
                                    0, 
                                    -(25*self.Height/100)-((self.LogoTEX.getYSize()*self.Height/1080)/2)
                )

                if self.SplashState[1] == 0:
                    self.CurtainsAlpha -= 0.02
                    if self.CurtainsAlpha < 0:
                        self.SplashState = [1, 1]
                if self.SplashState[1] == 2:
                    self.CurtainsAlpha += 0.02
                    if self.CurtainsAlpha > 1 :
                        self.SplashState = [1, 3]
                if self.SplashState[1] == 3:
                    self.PandaLogoNP.detachNode()
                    self.MadeUsingNP.detachNode()
                    if self.StartTime == 0:
                        self.StartTime = time.time()
                    if (time.time() - self.StartTime) > 1.5:
                        self.StartTime = 0
                        self.SplashState = [1, 4]
                if self.SplashState[1] == 4:
                    self.LogoNP.detachNode()
                    Display.ChangeDisplay(self, "Home")
            
            self.CurtainsNP.setScale(self.Width, 0, self.Height)
            self.CurtainsNP.setPos(0, 0, -self.Height)
            self.CurtainsNP.setAlphaScale(self.CurtainsAlpha)
            


        def Close(self):
            self.SplashState = [0, 0]
            self.StartTime = 0
            self.CurtainsAlpha = 0
            self.PandaLogoNP.detachNode()


    class Game():
        def __init__(self):
            base.setBackgroundColor(0, 0.5, 1)
            self.EverythingNP.reparentTo(self.render)

            self.SpeedNP = pixel2d.attachNewNode(TextNode('currentspeed'))
            self.SpeedNP.node().setText("0")
            self.SpeedNP.node().setTextColor(0, 0, 1, 1)
            self.SpeedNP.node().setAlign(TextNode.ACenter)
            self.SpeedNP.node().setFont(self.NotifFont)

            self.GearNP = pixel2d.attachNewNode(TextNode('currentspeed'))
            self.GearNP.node().setText("0")
            self.GearNP.node().setTextColor(0, 0, 0, 1)
            self.GearNP.node().setAlign(TextNode.ACenter)
            self.GearNP.node().setFont(self.NotifFont)
            
            self.SpeedometerTEX = loader.loadTexture('../assets/media/Speedometer.png')
            self.SpeedometerNP = pixel2d.attachNewNode(CardMaker('speedometer').generate())
            self.SpeedometerNP.setTexture(self.SpeedometerTEX)
            self.SpeedometerNP.setTransparency(TransparencyAttrib.MAlpha)

        def Update(self):
            self.SpeedNP.node().setText(f"{abs(round(self.Vehicle.getCurrentSpeedKmHour()))}")
            self.SpeedNP.setScale(70*self.Width/1920, 0, 70*self.Height/1080)
            self.SpeedNP.setPos((85*self.Width/100),
                                 0, 
                                 -(85*self.Height/100)
            )

            self.GearNP.node().setText(f"{self.CurrentGear}")
            self.GearNP.setScale(65*self.Width/1920, 0, 65*self.Height/1080)
            self.GearNP.setPos((85*self.Width/100),
                                 0, 
                                 -(95*self.Height/100)
            )

            self.SpeedometerNP.setScale(self.SpeedometerTEX.getXSize()*self.Width/1920, 
                                        0, 
                                        self.SpeedometerTEX.getYSize()*self.Height/1080
            )
            self.SpeedometerNP.setPos((85*self.Width/100)-((self.SpeedometerTEX.getXSize()*self.Width/1920)/2),
                                  0,
                                  -(85*self.Height/100)-((self.SpeedometerTEX.getYSize()*self.Height/1080)/2.5)
            )

        def Close(self):
            self.EverythingNP.detachNode()
            self.SpeedometerNP.detachNode()
            self.SpeedNP.detachNode()
            self.GearNP.detachNode()


    class Home():
        def __init__(self):
            self.HomeState = "Main"
            self.InitState = 0
            base.setBackgroundColor(0, 0, 0)
            #-------------------------------------------------------------------------------------------------------------------
            self.MenuVideoTEX = loader.loadTexture('../assets/media/MenuVideo.avi')
            self.MenuVideoNP = pixel2d.attachNewNode(CardMaker('MenuVideo').generate())
            self.MenuVideoNP.setTexture(self.MenuVideoTEX)
            #-------------------------------------------------------------------------------------------------------------------
            self.HomeFadeTEX = loader.loadTexture('../assets/media/HomeFade.png')
            self.HomeFadeNP = pixel2d.attachNewNode(CardMaker('HomeFade').generate())
            self.HomeFadeNP.setTexture(self.HomeFadeTEX)
            self.HomeFadeNP.setTransparency(True)
            #-------------------------------------------------------------------------------------------------------------------
            self.MenuNP = None
            #-------------------------------------------------------------------------------------------------------------------
            self.MenuFrame1TEX = loader.loadTexture('../assets/media/MenuFrame1.png')
            self.MenuFrame1NP = pixel2d.attachNewNode(CardMaker('MenuFrame1').generate())
            self.MenuFrame1NP.setTexture(self.MenuFrame1TEX)
            self.MenuFrame1NP.setTransparency(True)
            #-------------------------------------------------------------------------------------------------------------------
            self.MenuFrame2TEX = loader.loadTexture('../assets/media/MenuFrame2.png')
            self.MenuFrame2NP = pixel2d.attachNewNode(CardMaker('MenuFrame2').generate())
            self.MenuFrame2NP.setTexture(self.MenuFrame2TEX)
            self.MenuFrame2NP.setTransparency(True)


        def Update(self):
            #-------------------------------------------------------------------------------------------------------------------
            self.MenuVideoNP.setScale(self.MenuVideoTEX.getXSize()   *self.Width/1280,
                                      0,
                                      self.MenuVideoTEX.getYSize()  *self.Height/720
            )
            self.MenuVideoNP.setPos(40*self.Width/100,
                                    0, 
                                    -(100 *self.Height/100)
            )
            #-------------------------------------------------------------------------------------------------------------------
            self.HomeFadeNP.setScale(self.HomeFadeTEX.getXSize()   *self.Width/1920,
                                      0,
                                      self.HomeFadeTEX.getYSize()  *self.Height/1080
            )
            self.HomeFadeNP.setPos(0*self.Width/100,
                                   0, 
                                   -(100 *self.Height/100)
            )
            #-------------------------------------------------------------------------------------------------------------------
            if type(self.MenuNP) == list:
                Display.ButtonGroup.Close(self, self.MenuNP)

            if self.HomeState == "Main":
                self.MenuNP = Display.ButtonGroup.CreateGroup(self, ["World", "Multiplayer", "Challenges", "Credits", "Settings", "Quit"], [5,50], [75,75])
            elif self.HomeState == "Multiplayer":
                self.MenuNP = Display.ButtonGroup.CreateGroup(self, ["Coming Soon !", "Back"], [5,60], [75,75])


            Display.ButtonGroup.Update(self, self.MenuNP)
            #-------------------------------------------------------------------------------------------------------------------
            for i in range(len(self.MenuNP)-3):
                BGPos = Display.ButtonGroup.GetButtonPos(self, self.MenuNP[i+1])

                if(BGPos[0] < self.MouseX < BGPos[1] and BGPos[2] < self.MouseY < BGPos[3]):
                    self.MenuFrame1NP.setScale(self.MenuFrame1TEX.getXSize()   *self.Width/1920,
                                              0,
                                              self.MenuFrame1TEX.getYSize()  *self.Height/1080
                    )
                    self.MenuFrame1NP.setPos(BGPos[0],
                                             0, 
                                             -BGPos[2] - (self.MenuFrame1TEX.getYSize()  *self.Height/1080)
                    )
                    self.MenuFrame2NP.setScale(self.MenuFrame2TEX.getXSize()   *self.Width/1920,
                                              0,
                                              self.MenuFrame2TEX.getYSize()  *self.Height/1080
                    )
                    self.MenuFrame2NP.setPos(BGPos[1] - (self.MenuFrame2TEX.getXSize()   *self.Width/1920),
                                             0, 
                                             -BGPos[3]
                    )
            #-------------------------------------------------------------------------------------------------------------------

        def Close(self):
            self.MenuVideoNP.detachNode()
            self.HomeFadeNP.detachNode()
            Display.ButtonGroup.Close(self, self.MenuNP)
            self.MenuFrame1NP.detachNode()
            self.MenuFrame2NP.detachNode()



    def __init__(self):
        self.BGCount = 0

        self.CurrentDisplay = "Splash"
        self.ChangeDisplay = False
        Display.Splash.__init__(self)


    def ChangeDisplay(self, display):
        self.ChangeDisplay = True

        # Close Current Display
        if self.CurrentDisplay == "Home":
            Display.Home.Close(self)
        elif self.CurrentDisplay == "Game":
            Display.Game.Close(self)
        elif self.CurrentDisplay == "Splash":
            Display.Splash.Close(self)
        
        # Init Desired Display
        if display == "Home":
            Display.Home.__init__(self)
        elif display == "Game":
            Display.Game.__init__(self)
        elif display == "Splash":
            Display.Splash.__init__(self)
        
        # Change Variables to Desired State
        self.ChangeDisplay = False
        self.CurrentDisplay = display


    def Update(self):
        if self.ChangeDisplay == False:
            if self.CurrentDisplay == "Home":
                Display.Home.Update(self)
            elif self.CurrentDisplay == "Game":
                Display.Game.Update(self)
            elif self.CurrentDisplay == "Splash":
                Display.Splash.Update(self)
    

    class ButtonGroup():
        def CreateGroup(self,  list1, pos=[50, 50], scale=[125, 125]):

            BGElements = []

            MenuTitleNP = pixel2d.attachNewNode(TextNode('MenuTitle'))
            MenuTitleNP.node().setTextColor(0, 0, 1, 1)
            MenuTitleNP.node().setAlign(TextNode.ALeft)
            MenuTitleNP.node().setFont(self.NotifFont)

            BGElements.append(MenuTitleNP)


            for i in range(len(list1)):
                Element = pixel2d.attachNewNode(TextNode(f'BGElement {i}'))
                Element.node().setText(f"\1slant\1{list1[i]}\2")
                Element.node().setTextColor(1, 1, 1, 1)
                Element.node().setAlign(TextNode.ALeft)
                Element.node().setFont(self.NotifFont)
                BGElements.append(Element)

            BGElements.append(pos)
            BGElements.append(scale)

            self.BGCount += 1
            return BGElements
        
        def Update(self, BG):
            if self.HomeState != "Main":
                BG[0].node().setText(f"\1slant\1{self.HomeState}\2")
                BG[0].setScale(BG[len(BG)-1][0]*1.5  *(self.Width/1920),
                               0,
                               BG[len(BG)-1][0]*1.5  *(self.Height/1080)
                )
                BG[0].setPos(5  *(self.Width/100),
                             0,
                             -10  *(self.Height/100)
                )



            for i in range(1, len(BG)-2):
                BG[i].setScale(BG[len(BG)-1][0]  *(self.Width/1920),
                               0,  
                               BG[len(BG)-1][1]  *(self.Height/1080)
                )
                BG[i].setPos(BG[len(BG)-2][0]  *(self.Width/100),
                             0,
                             -(BG[len(BG)-2][1]   -   (((len(BG)-3) * (10/(len(BG)-3))  +  (len(BG)-3) * (60/(len(BG)-3))) /2)   +   (i*(10/(len(BG)-3))  +  (i-1)*(60/(len(BG)-3))))   *(self.Height/100)
                )
        
        def Close(self, BG):
            for i in range(len(BG)-2):
                BG[i].detachNode()

        def GetButtonPos(self, Button):
            return (Button.getX(),
                   Button.getX() + (75*7*self.Width/1920),
                   -Button.getZ() - (Button.getScale()[2]),
                   -Button.getZ() + (Button.getScale()[2]/2)
            )
