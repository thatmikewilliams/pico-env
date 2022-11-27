import machine
import gc
from local.logger import Logger

__log = Logger("SystemStats")
class SystemStats:
    def __init__(self):
        __log.debug("__init__")
        self.reset()
        
    def reset(self):
        self.start_datetime = machine.RTC().datetime()
        self.run_count = 0
        self.exception_count = 0
        self.last_exception = "n/a"
        self.reset_cause = machine.reset_cause()

    def add_run(self):
        self.run_count = self.run_count + 1
        
    def add_exception(self, ex):
        self.exception_count = self.exception_count + 1
        self.last_exception = str(ex)
        
    def __formatted_start_date(self):
        return f"{self.start_datetime[2]:02d}/{self.start_datetime[1]:02d}/{self.start_datetime[0]:04d}"
    
    def __formatted_start_time(self):
        return f"{self.start_datetime[4]:02d}:{self.start_datetime[5]:02d}:{self.start_datetime[6]:02d}"
        
    def __get_cpu_temperature_degrees_c(self):
        temp_sensor = machine.ADC(4)
        voltage_conversion_factor = 3.3 / 65535
        temp_sensor_voltage = temp_sensor.read_u16() * voltage_conversion_factor
        # From the datasheet, a temperature of 27 degrees Celsius delivers a
        # voltage of 0.706 V. With each additional degree the voltage reduces
        # by 1.721 mV or 0.001721 V
        temperature = 27 - (temp_sensor_voltage - 0.706)/0.001721
        return temperature
        
    def __read_gc(self):
        d = {
            "mem_free" : gc.mem_free(),
            "mem_alloc" : gc.mem_alloc(),
            "threshold" : gc.threshold()
            }
        return d
             
    def read(self):
        __log.debug("read()")
        sm_dict = {
            "start_date" : self.__formatted_start_date(),
            "start_time" : self.__formatted_start_time(),
            "run_count" : self.run_count,
            "exception_count" : self.exception_count,
            "last_exception" : self.last_exception,
            "cpu_temperature" : self.__get_cpu_temperature_degrees_c(),
            "reset_cause" : self.reset_cause,
            "gc" : self.__read_gc()
            }
        __log.debug("read(): ", sm_dict)
        return sm_dict

    def describe(self):
        __log.debug("describe")
        desc = {
            "hrd" : "Internal system monitoring",
            }
        __log.debug("describe:", desc)
        return desc
