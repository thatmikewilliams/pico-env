import machine
import time

from local.connected_wlan import ConnectedWLAN
from local.bme68x import BME68X
from local.power_monitor import PowerMonitor
from local.dweeter import Dweeter
from local.system_stats import SystemStats

def init_components():
    global bme
    bme = BME68X()
    global power_monitor
    power_monitor = PowerMonitor()
    global wlan
    wlan = ConnectedWLAN()
    global dweeter
    dweeter = Dweeter(wlan.get_mac_address())
    global system_stats
    system_stats = SystemStats()
    
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
        "system_stats" : {
            "description" : system_stats.describe(),
            "value" : system_stats.read()
            }
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


blinking_sleep(5)
init_components()

while True:
    blinking_sleep(2,10)
    try:
        system_stats.add_run()
        do_dweet()
    except Exception as e:
        system_stats.add_exception(e)
        print(e)
        blinking_sleep(10, 1)

machine.reset()