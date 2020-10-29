import pigpio
import time
pi = pigpio.pi()
pi.set_PWM_dutycycle(17,0)
for i in range(10):
    pi = pigpio.pi()
    pi.set_PWM_dutycycle(17,255) #red
    pi.set_PWM_dutycycle(22,0) #red
    time.sleep(1)
    pi.set_PWM_dutycycle(22,255)#green
    time.sleep(1)
    pi.set_PWM_dutycycle(17,0) #off
    pi.set_PWM_dutycycle(22,0) #off
    pi.set_PWM_dutycycle(23,0) #off
    time.sleep(1)
    

pi.stop()