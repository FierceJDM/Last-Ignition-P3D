class Steer():
    def Left(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 10:
            self.Steering += self.dt * (self.SteeringIncrement)
            self.Steering = min(self.Steering, self.SteeringClamp)
        elif self.Vehicle.getCurrentSpeedKmHour() < 25:
            self.Steering += self.dt * (self.SteeringIncrement)
            self.Steering = min(self.Steering, self.SteeringClamp)
        elif self.Vehicle.getCurrentSpeedKmHour() < 40:
            self.Steering += self.dt * (self.SteeringIncrement)
            self.Steering = min(self.Steering, self.SteeringClamp)
        elif self.Vehicle.getCurrentSpeedKmHour() < 75:
            self.Steering += self.dt * (self.SteeringIncrement)
            self.Steering = min(self.Steering, self.SteeringClamp)
        else:
            self.Steering += self.dt * (self.SteeringIncrement)
            self.Steering = min(self.Steering, self.SteeringClamp)


    def Right(self):
        if self.Vehicle.getCurrentSpeedKmHour() < 10:
            self.Steering -= self.dt * (self.SteeringIncrement)
            self.Steering = max(self.Steering, -self.SteeringClamp)
        elif self.Vehicle.getCurrentSpeedKmHour() < 25:
            self.Steering -= self.dt * (self.SteeringIncrement)
            self.Steering = max(self.Steering, -self.SteeringClamp)
        elif self.Vehicle.getCurrentSpeedKmHour() < 40:
            self.Steering -= self.dt * (self.SteeringIncrement)
            self.Steering = max(self.Steering, -self.SteeringClamp)
        elif self.Vehicle.getCurrentSpeedKmHour() < 75:
            self.Steering -= self.dt * (self.SteeringIncrement)
            self.Steering = max(self.Steering, -self.SteeringClamp)
        else:
            self.Steering -= self.dt * (self.SteeringIncrement)
            self.Steering = max(self.Steering, -self.SteeringClamp)