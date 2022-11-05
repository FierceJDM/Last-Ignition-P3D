from .MiscFunctions import *


class Camera():
    def __init__(self):
        self.CamOffset = 0

    class FirstPerson():
        def Zero(self, turn):
            if turn==True:
                if self.CamOffset < 0:
                    self.CamOffset += Dampen( 25*self.dt*(13/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= Dampen( 25*self.dt*(13/30) , self.CamOffset)
            else:
                if self.CamOffset < 0:
                    self.CamOffset += Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset)
                if self.CamOffset > 0:
                    self.CamOffset -= Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset)
            

        def Turn(self, limitpos):
            if limitpos > 0:
                if self.CamOffset < limitpos:
                    self.CamOffset += Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset, limitpos)
            elif limitpos < 0:
                if self.CamOffset > limitpos:
                    self.CamOffset -= Dampen( 25*self.dt*(abs(DivByZero(self.Steering, 13))/30) , self.CamOffset, limitpos)
