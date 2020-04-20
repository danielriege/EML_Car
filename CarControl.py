import RPi.GPIO as GPIO
import time

# throttle_zero might also be configured on the ESC
class CarControl:
    def __init__(self, steering_zero, steering_trim = 0, throttle_zero, throttle_trim = 0, pwm_frequency = 50, steering_pin, throttle_pin):
        self.steering_value = steering_zero
        self.throttle_value = throttle_zero
        self.steering_trim = steering_trim
        self.throttle_trim = throttle_trim
        self.pwm_frequency = pwm_frequency
        self.steering_pin = steering_pin
        self.throttle_pin = throttle_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.steering_pin, GPIO.OUT)
        GPIO.setup(self.throttle_pin, GPIO.OUT)

        self.steering = GPIO.PWM(self.steering_pin, self.pwm_frequency)
        self.throttle = GPIO.PWM(self.throttle_pin, self.pwm_frequency)
    def __del__(self):
        self.stop()
        GPIO.cleanup()
        print('CarControl deleted')
    def start(self):
        self.steering.start(self.__relativePWM(self.steering_value))
        self.throttle.start(self.__relativePWM(self.throttle_value))
    def stop(self):
        self.steering.stop()
        self.throttle.stop()
    # angle as PWM %
    def steer(self, angle):
        if self.steering_value = self.__relativePWM(angle) > 0:
            self.steering_value += self.steering_trim
        self.steering.ChangeDutyCycle(self.steering_value)
    def accelerate(self, throttle):
        if self.throttle_value = self.__relativePWM(throttle) > 0:
            self.throttle_value += self.throttle_trim
        self.throttle.ChangeDutyCycle(self.throttle_value)
    def __relativePWM(self, pwm_value):
        return pwm_value*self.pwm_frequency/10000.0
