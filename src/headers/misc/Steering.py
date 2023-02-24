#  Definitive values for realistic steering (11/02/2023)

class Steer():
    def Left(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 35:
            self.Steering += self.dt * (15 - (13*self.Vehicle.getCurrentSpeedKmHour()/35))
            self.Steering = min(self.Steering, (22 - (14*self.Vehicle.getCurrentSpeedKmHour()/35)))
            self.SteerLimit = (-23 - (-9*self.Vehicle.getCurrentSpeedKmHour()/35))
        elif self.Vehicle.getCurrentSpeedKmHour() < 135:
            self.Steering += self.dt * (15 - (13*self.Vehicle.getCurrentSpeedKmHour()/135))
            self.Steering = min(self.Steering, (8 - (7.8*self.Vehicle.getCurrentSpeedKmHour()/135)))
            self.SteerLimit = (-17 - (-14*self.Vehicle.getCurrentSpeedKmHour()/135))
        else:
            self.Steering += self.dt * 1
            self.Steering = min(self.Steering, 2)
            self.SteerLimit = -5





    def Right(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 35:
            self.Steering += self.dt * (-15 - (-13*self.Vehicle.getCurrentSpeedKmHour()/35))
            self.Steering = max(self.Steering, (-22 - (-14*self.Vehicle.getCurrentSpeedKmHour()/35)))
            self.SteerLimit = (23 - (9*self.Vehicle.getCurrentSpeedKmHour()/35))
        elif self.Vehicle.getCurrentSpeedKmHour() < 135:
            self.Steering += self.dt * (-15 - (-13*self.Vehicle.getCurrentSpeedKmHour()/135))
            self.Steering = max(self.Steering, (-8 - (-7.8*self.Vehicle.getCurrentSpeedKmHour()/135)))
            self.SteerLimit = (17 - (14*self.Vehicle.getCurrentSpeedKmHour()/135))
        else:
            self.Steering += self.dt * -1
            self.Steering = max(self.Steering, -2)
            self.SteerLimit = 5