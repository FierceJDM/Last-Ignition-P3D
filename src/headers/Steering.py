class Steer():
    def Left(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 135:
            self.Steering += self.dt * (40 - (39*self.Vehicle.getCurrentSpeedKmHour()/135))
            self.Steering = min(self.Steering, (35 - (33*self.Vehicle.getCurrentSpeedKmHour()/135)))
            self.SteerLimit = (-19 + (14*self.Vehicle.getCurrentSpeedKmHour()/135))
        else:
            self.Steering += self.dt * 1
            self.Steering = min(self.Steering, 2)
            self.SteerLimit = -5





    def Right(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 135:
            self.Steering -= self.dt * (40 - (39*self.Vehicle.getCurrentSpeedKmHour()/135))
            self.Steering = max(self.Steering, (-35 + (33*self.Vehicle.getCurrentSpeedKmHour()/135)))
            self.SteerLimit = (19 - (14*self.Vehicle.getCurrentSpeedKmHour()/135))
        else:
            self.Steering -= self.dt * 1
            self.Steering = max(self.Steering, -2)
            self.SteerLimit = 5