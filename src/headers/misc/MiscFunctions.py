from math import *

class MiscFunctions():
    def Truncate(self, n, decimals = 0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def DivByZero(self, variable, replace): # Avoid Division by Zero
        if variable == 0:
            return replace
        return variable

    def Dampen(self, currentpos, camoffset, limitpos=0): # Dampen Camera when approaching limit pos
        if limitpos-0.5 < camoffset < limitpos+0.5:
            return currentpos/8
        if limitpos-1.5 < camoffset < limitpos+1.5:
            return currentpos/4
        if limitpos-2.5 < camoffset < limitpos+2.5:
            return currentpos/2

        return currentpos


    def SetSpeedKmHour(self, throttle, maxrpm, gearlist): #Set next speed (in km/h) based on current speed
        desiredspeed = 0
        
        
        if throttle:
            if self.CurrentGear < len(gearlist) : # Shift Gear
                if self.CurrentRPM > maxrpm-500:
                    self.CurrentGear += 1
                    self.CurrentRPM = self.Vehicle.getCurrentSpeedKmHour()*gearlist[self.CurrentGear-1][1]

            gearduration = gearlist[self.CurrentGear-1][0] # Calculate Desired Speed
            if self.CurrentRPM < maxrpm:
                self.CurrentRPM += maxrpm/gearduration * self.dt
            desiredspeed = self.CurrentRPM/gearlist[self.CurrentGear-1][1]

            # -----------------------------------------------------------------------------------------

            if self.Vehicle.getCurrentSpeedKmHour() < desiredspeed:
                return 3000
            elif self.Vehicle.getCurrentSpeedKmHour() > desiredspeed:
                return -3000
            else:
                return 0

        
        else:
            # If Automatic, Constantly Shift to Corresponding Gears
            for i in range(len(gearlist)):
                if i == 0:
                    if self.Vehicle.getCurrentSpeedKmHour() < round(maxrpm/gearlist[i][1])-3:
                        self.CurrentGear = i+1
                else:
                    if (maxrpm/gearlist[i-1][1])-3 <= self.Vehicle.getCurrentSpeedKmHour() < (maxrpm/gearlist[i][1])-3:
                        self.CurrentGear = i+1

            # -----------------------------------------------------------------------------------------

            if self.CurrentRPM > 1000: # Slowly Lower RPM
                self.CurrentRPM = gearlist[self.CurrentGear-1][1]*self.Vehicle.getCurrentSpeedKmHour()