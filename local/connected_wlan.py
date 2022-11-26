import machine
import network
import binascii
from time import sleep
from secrets import ssid_secrets
from local.logger import Logger

__log = Logger("ConnectedWLAN")

class ConnectedWLAN:
    def __init__(self):
        __log.debug("__init__")
    
        machine.Pin("LED", machine.Pin.OUT, value=0)
        wlan = self.__activate()
        networks = self.__get_networks_by_rssi(wlan)
        wlan_creds_list = self.__filter_wlan_creds(ssid_secrets, networks)
        self.__connect_or_throw(wlan, wlan_creds_list)
        machine.Pin("LED", machine.Pin.OUT, value=1)
        
    def __activate(self):
        __log.debug("__activate")
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)
        wlan.active(True)
        return wlan

    def __filter_wlan_creds(self, wlan_creds, networks):
        __log.debug("__filter_wlan_creds")
        available = []
        for network in networks:
            ssid = network[0].decode()
            __log.debug("checking wlan_creds for:", ssid)
            if ssid in list(wlan_creds.keys()):
                available.append(wlan_creds.get(ssid))
        __log.debug("__filter_wlan_creds result:", *map(lambda x: x['ssid'], available))
        return available

    def __get_networks_by_rssi(self, wlan):
        __log.debug("__get_networks_by_rssi")
        networks = wlan.scan()
        networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)
        self.__log_networks(networks)
        return networks;

    def __log_networks(self, networks):
        for network in networks:
            __log.debug("available network: ssid:'{ssid}' bssid:0x{bssid} channel:{channel} RSSI:{rssi} security:{security} hidden:{hidden}"
                      .format(ssid = network[0].decode(),
                              bssid = binascii.hexlify(network[1]).decode(),
                              channel = network[2],
                              rssi = network[3],
                              security = self.__security_to_str(network[4]),
                              hidden = network[5]))

    def __security_to_str(self, security):
        if (security == 0): return "open"
        if (security == 1): return "WEP"
        if (security == 2): return "WPA-PSK"
        if (security == 3): return "WPA2-PSK"
        if (security == 4): return "WPA/WPA2-PSK"
        return "unknown: {}".format(security)

    def __status_to_str(self, status):
        if (status == network.STAT_IDLE): return "STAT_IDLE"
        if (status == network.STAT_CONNECTING): return "STAT_CONNECTING"
        if (status == network.STAT_WRONG_PASSWORD): return "STAT_WRONG_PASSWORD"
        if (status == network.STAT_NO_AP_FOUND): return "STAT_NO_AP_FOUND"
        if (status == network.STAT_CONNECT_FAIL): return "STAT_CONNECT_FAIL"
        if (status == network.STAT_GOT_IP): return "STAT_GOT_IP"
        return "unknown: {}".format(status)

    def __connect_or_throw(self, wlan, wlan_creds_list):
        for wlan_creds in wlan_creds_list:
            if self.__connect(wlan, wlan_creds):
                return;
        raise Exception("Failed to connect to any of the configured SSIDs")

    def __connect(self, wlan, wlan_creds):
        __log.debug("__connect", wlan_creds['ssid'])
        wlan.connect(wlan_creds['ssid'], wlan_creds['password'])
        for wait_loop in range(10):
            __log.debug("checking if connected...status: {}".format(self.__status_to_str(wlan.status())))
            if wlan.isconnected() == True:
                __log.debug(wlan.ifconfig())
                break;
            sleep(1)
        __log.debug("__connect result:", "{ssid}={connected}".format(ssid = wlan_creds['ssid'], connected = wlan.isconnected()))
        return wlan.isconnected()

    def get_mac_address(self):
        __log.debug("get_mac_address")
        mac = binascii.hexlify(network.WLAN().config('mac')).decode()
        __log.debug("get_mac_address:", mac)
        return mac

    def describe(self):
        __log.debug("describe")
        desc = {
            "device" : "bme688"
            }
        __log.debug("describe:", desc)
        return desc