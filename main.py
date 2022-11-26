import machine
from machine import Pin
import time
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE, STATUS_GAS_VALID
from pimoroni_i2c import PimoroniI2C
import breakout_bme68x

import gc
import machine

from local.connected_wlan import ConnectedWLAN
from local.bme68x import BME68X
from local.dweeter import Dweeter

    
def init_components():
    global bme
    bme = BME68X()
    global wlan
    wlan = ConnectedWLAN()
    global dweeter
    dweeter = Dweeter(wlan.get_mac_address())
    
def do_dweet():
    dweet = {
        "bme" : {
            "description" : bme.describe(),
            "value" : bme.read()
            }
        }
    dweeter.dweet(dweet)

def deep_sleep(seconds):
    print(f"going into deep sleep for {seconds}s")
    time.sleep(1)
    machine.deepsleep(seconds)

def toggle_onboard_led():
    Pin("LED", Pin.OUT).toggle()

def blinking_sleep(seconds, rate=5):
    print(f"sleeping for {seconds}s")
    for i in range(seconds*rate):
        toggle_onboard_led()
        time.sleep(1/rate)


# check if the device woke from a deep sleep
reset_cause = machine.reset_cause()
print(f"reset cause: {reset_cause}")
blinking_sleep(reset_cause, 2)
time.sleep(1)
blinking_sleep(5)

try:
    init_components()
    while True:
        do_dweet()
        blinking_sleep(60,0.5)
except Exception as e:
    print(e)
    blinking_sleep(10, 1)
    raise e
#    raise e


machine.reset()
#deep_sleep(20)
#time.sleep(1)
#print("resetting")
#time.sleep(1)
#machine.reset()