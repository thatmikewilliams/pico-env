import machine
import time

from local.connected_wlan import ConnectedWLAN
from local.bme68x import BME68X
from local.power_monitor import PowerMonitor
from local.dweeter import Dweeter

run_count = 0
exception_count = 0
last_exception = "n/a"

def init_components():
    global bme
    bme = BME68X()
    global power_monitor
    power_monitor = PowerMonitor()
    global wlan
    wlan = ConnectedWLAN()
    global dweeter
    dweeter = Dweeter(wlan.get_mac_address())
    
def do_dweet():
    dweet = {
        "bme" : {
            "description" : bme.describe(),
            "value" : bme.read()
            },
        "power_monitor" : {
            "description" : power_monitor.describe(),
            "value" : power_monitor.read()
            },
        "run_count" : run_count,
        "exception_count" : exception_count,
        "last_exception" : last_exception
        }
    dweeter.dweet(dweet)

def deep_sleep(seconds):
    print(f"going into deep sleep for {seconds}s")
    time.sleep(1)
    machine.deepsleep(seconds)

def toggle_onboard_led():
    machine.Pin("LED", machine.Pin.OUT).toggle()

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

init_components()
while True:
    blinking_sleep(2,10)
    try:
        run_count = run_count + 1
        do_dweet()
    except Exception as e:
        print(e)
        exception_count = exception_count + 1
        last_exception = str(e)
        blinking_sleep(10, 1)

machine.reset()

