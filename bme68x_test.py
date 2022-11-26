from breakout_bme68x import BreakoutBME68X
from pimoroni_i2c import PimoroniI2C
import gc
import machine
from utime import sleep

from breakout_bme68x import BreakoutBME68X
from pimoroni_i2c import PimoroniI2C

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

for i in range(50):
    i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
    bme = BreakoutBME68X(i2c)

def toggle_onboard_led():
    machine.Pin("LED", machine.Pin.OUT).toggle()

def blinking_sleep(seconds):
    print(f"sleeping for {seconds}s")
    for i in range(seconds*5):
        toggle_onboard_led()
        sleep(0.2)
        
blinking_sleep(5)
machine.reset()

#i2c = PimoroniI2C(sda = 4, scl = 5)
#for i in range(100):
#    print(f"loop {i}")
#    print(f"gc.mem_free: {gc.mem_free()}")
#    print(f"gc.mem_alloc: {gc.mem_alloc()}")
#    bme = BreakoutBME68X(i2c)
#    bme = 0
