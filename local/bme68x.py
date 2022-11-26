from breakout_bme68x import BreakoutBME68X, STATUS_GAS_VALID, STATUS_HEATER_STABLE
from pimoroni_i2c import PimoroniI2C
from local.logger import Logger

__log = Logger("bme68x")
class BME68X:
    def __init__(self, sda = 4, scl = 5):
        __log.debug(f"__init__(sda={sda}, scl={scl})")
        i2c = PimoroniI2C(sda = sda, scl = scl)
        self.bme = BreakoutBME68X(i2c)

    def read(self):
        __log.debug("read()")
        temperature, pressure, humidity, gas_resistance, status, gas_index, meas_index = self.bme.read()
        bme_dict = {
            "temperature" : "{:0.2f}".format(temperature),
            "pressure" : "{:0.2f}".format(pressure),
            "humidity" : "{:0.2f}".format(humidity),
            "gas_resistance" : "{:0.2f}".format(gas_resistance),
            "gas_index" : "{:d}".format(gas_index),
            "meas_index" : "{:d}".format(meas_index),
            "status" : "{:d}".format(status),
            "new_data" : ("true" if status & 0x80 != 0 else "false"),
            "gasm_valid" : ("true" if status & STATUS_GAS_VALID != 0 else "false"),
            "heater_stable" : ("true" if status & STATUS_HEATER_STABLE != 0 else "false")
            }
        __log.debug("read(): ", bme_dict)
        return bme_dict

    def describe(self):
        __log.debug("describe")
        desc = {
            "hrd" : "Pimoroni bme688 breakout board",
            "device" : "bme688",
            }
        __log.debug("describe:", desc)
        return desc

