class Steer():
    def Left(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 10:
            self.Steering += self.dt * 40
            self.Steering = min(self.Steering, 35)
            self.SteerLimit = -19
        elif self.Vehicle.getCurrentSpeedKmHour() < 25:
            self.Steering += self.dt * 30
            self.Steering = min(self.Steering, 35)
            self.SteerLimit = -19
        elif self.Vehicle.getCurrentSpeedKmHour() < 40:
            self.Steering += self.dt * 25
            self.Steering = min(self.Steering, 30)
            self.SteerLimit = -15
        elif self.Vehicle.getCurrentSpeedKmHour() < 75:
            self.Steering += self.dt * 15
            self.Steering = min(self.Steering, 20)
            self.SteerLimit = -10
        elif self.Vehicle.getCurrentSpeedKmHour() < 135:
            self.Steering += self.dt * 5
            self.Steering = min(self.Steering, 5)
            self.SteerLimit = -5
        else:
            self.Steering += self.dt * 1
            self.Steering = min(self.Steering, 2)
            self.SteerLimit = -5


    def Right(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 10:
            self.Steering -= self.dt * 40
            self.Steering = max(self.Steering, -35)
            self.SteerLimit = 19
        elif self.Vehicle.getCurrentSpeedKmHour() < 25:
            self.Steering -= self.dt * 30
            self.Steering = max(self.Steering, -35)
            self.SteerLimit = 19
        elif self.Vehicle.getCurrentSpeedKmHour() < 40:
            self.Steering -= self.dt * 25
            self.Steering = max(self.Steering, -30)
            self.SteerLimit = 15
        elif self.Vehicle.getCurrentSpeedKmHour() < 75:
            self.Steering -= self.dt * 15
            self.Steering = max(self.Steering, -20)
            self.SteerLimit = 10
        elif self.Vehicle.getCurrentSpeedKmHour() < 135:
            self.Steering -= self.dt * 5
            self.Steering = max(self.Steering, -5)
            self.SteerLimit = 5
        else:
            self.Steering -= self.dt * 1
            self.Steering = max(self.Steering, -2)
            self.SteerLimit = 5