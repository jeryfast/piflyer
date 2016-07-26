from time import time
class pid:
    def __init__(self, setpoint, measured_value):
        self.previous_error=0
        self.integral=0
        self.Kp=1
        self.Ki=0
        self.Kd=0
        self.dt=time()
    def reset(self):
        self.previous_error = 0
        self.integral = 0
    def run(self, setpoint, measured_value):
        self.dt=time()-self.dt
        if(self.dt>1000):
            self.reset()
        else:
            error = setpoint - measured_value
            self.integral = self.integral + error*self.dt
            derivative = (error - self.previous_error)/self.dt
            output = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
            self.previous_error = error
            return output
        return 0