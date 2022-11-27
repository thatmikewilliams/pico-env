import machine
import time
from local.logger import Logger

__log = Logger("PowerMonitor")

# reads the system input voltage
# original code had ADC(29) but this causes the picow board to hang 
#__vsys = ADC(3)
# on the picow the vbus sense is on the internal pin WL_GUIO2, not on GPIO24
__external_power_indicator = machine.Pin("WL_GPIO2", machine.Pin.IN)
# these are our reference voltages for a full/empty battery, in volts
__full_battery = 4.2
# the values could vary by battery size/manufacturer so you might need to adjust them
__empty_battery = 2.8

class PowerMonitor:
    def __init__(self):
        __log.debug("__init__")
    
    def describe(self):
        __log.debug("describe")
        desc = {
            "hrd" : "Internally implemented power monitor",
            }
        __log.debug("describe:", desc)
        return desc

    def read(self):
        __log.debug("read()")
        power_dict = {}
        power_dict["external_power_indicator"] = __external_power_indicator.value()

        voltage = self.__read_vsys()
        power_dict["voltage"] = voltage
        power_dict["full_battery_voltage"] = __full_battery
        power_dict["empty_battery_voltage"] = __empty_battery
        
        calculated_percentage = 100 * ((voltage - __empty_battery) / (__full_battery - __empty_battery))
        if calculated_percentage > 100:
            percentage = 100.00
        else:
            percentage = calculated_percentage
        power_dict["battery_charge_calculated_percent"] = calculated_percentage
        power_dict["battery_charge_percent"] = percentage

        __log.debug("read(): ", power_dict)
        return power_dict

    def __set_pad(self, gpio, value):
        machine.mem32[0x4001c000 | (4+ (4 * gpio))] = value
    
    def __get_pad(self, gpio):
        return machine.mem32[0x4001c000 | (4+ (4 * gpio))]

    # This code from https://forums.raspberrypi.com/viewtopic.php?t=339994
    # prevents the board crashing while reading vsys
    # Big thanks to danjperron - https://github.com/danjperron/PicoWSolar
    def __read_vsys(self):
        old_pad = self.__get_pad(29)
        self.__set_pad(29, 128)  #no pulls, no output, no input
        adc_vsys = machine.ADC(3)
        conversion_factor = 3 * 3.3 / 65535
        vsys = adc_vsys.read_u16() * conversion_factor
        self.__set_pad(29, old_pad)
        return vsys

def toggle_onboard_led():
    Pin("LED", Pin.OUT).toggle()

def blinking_sleep(seconds, rate=5):
    print(f"sleeping for {seconds}s")
    for i in range(seconds*rate):
        toggle_onboard_led()
        time.sleep(1/rate)



