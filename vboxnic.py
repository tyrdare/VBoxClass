import re
from random import randint
from typing import List
# from vboxvm import VBoxVM
from forwardedport import FPRules
#from vboxvm import VBoxVM


# class VBoxVM:
#     pass

class VMNic:
    nic_brands: List[str] = [
        "PCnet-PC II (Am79C970A)",
        "PCnet-FAST III (Am97C973)",
        "Intel PRO/1000 MT Desktop (82540EM)",
        "Intel PRO/1000 T Server (82543GC)",
        "Intel PRO/1000 MT Server (82545EM)",
        "Paravirtualized Network (virtio-net)",
    ]
    network_attach_types: List[str] = [
        "NAT",
        "NAT Network",
        "Bridged Adapter",
        "Internal Network",
        "Host-only Adapter",
        "Generic Driver",
    ]

    def __init__(self, vm):
        self.__vm = vm
        self.__net_attach_type: str = 'NAT'
        self.__nic_type: str = self.nic_brands[0]
        self.__mac_address: str = self.generate_mac_address()
        if len(self.__vm.nics) > 0:
            self.__adapter_number = len(self.__vm.nics)
        else:
            self.__adapter_number = 1
        # Since default net attach type is "NAT"
        if self.__net_attach_type == 'NAT':
            self.__port_forwarding_possible: bool = True
            self.__port_forwarding_active: bool = True
            self.__pf_rules: FPRules = FPRules()
        else:
            self.__port_forwarding_possible: bool = False
            self.__port_forwarding_active: bool = False
            self.__pf_rules: FPRules = None
        self.__cable_connected: bool = True
        self.__transparent_proxying = False
        self.__enabled = True

    def generate_mac_address(self) -> str:
        hex_num: str = ''
        for i in range(0, 12):
            hex_num += hex(randint(0, 15))
        return hex_num.replace("0x", "")

    @property
    def mac_address(self):
        return self.__mac_address

    @mac_address.setter
    def mac_address(self, mac_address: str):
        if isinstance(mac_address, str):
            m_addr = mac_address.lower()
            # must be a 12-character hexadecimal string
            if ":" in m_addr:
                m_addr = m_addr.replace(':', '')
            if m_addr.startswith('0x'):
                m_addr = m_addr[2:]

            if len(m_addr) == 12:
                if re.search(r'[0-9a-f]{12}', m_addr):
                    self.__mac_address = m_addr
                else:
                    raise ValueError('Mac address is not in the proper format')
            else:
                raise ValueError('MAC address must be a 12 digit hexadecimal string')
        else:
            raise TypeError('MAC address must be a 12 digit hexadecimal string')

    @property
    def net_attach_type(self):
        return self.__net_attach_type

    @net_attach_type.setter
    def net_attach_type(self, attach_type: str):
        if attach_type in self.network_attach_types:
            self.__net_attach_type = attach_type
            if attach_type == "NAT":
                self.enable_port_forwarding()
            else:
                self.disable_port_forwarding()
        else:
            raise ValueError('Invalid network attachment type: {}'.format(attach_type))

    @property
    def nic_type(self):
        return self.__nic_type

    @nic_type.setter
    def nic_type(self, nic_type: str):
        if isinstance(nic_type, str):
            if nic_type in self.nic_brands:
                self.__nic_type = nic_type
            else:
                raise ValueError('Invalid NIC type: {}'.format(nic_type))
        else:
            raise TypeError('Property nic_type is str')

    @property
    def connect_cable(self):
        return self.__cable_connected

    @connect_cable.setter
    def connect_cable(self, connect: bool):
        if isinstance(connect, bool):
            self.__cable_connected = connect
        else:
            raise TypeError("Property 'connect_cable' is bool")

    def _port_forwarding(self, enable: bool):
        if self.__net_attach_type == 'NAT' and enable:
            self.__port_forwarding_possible = enable
            self.__port_forwarding_active = enable
            self.__pf_rules = [FPRules()]
        else:
            self.__port_forwarding_possible = False
            self.__port_forwarding_active = False
            self.__pf_rules = None

    def enable_port_forwarding(self):
        self._port_forwarding(True)

    def disable_port_forwarding(self):
        self._port_forwarding(False)

    @property
    def forwarding_rules(self):
        return self.__pf_rules

    @forwarding_rules.setter
    def add_forwarding_rule(self, fprule_obj):
        if self.__port_forwarding_possible and self.__port_forwarding_active:
            if isinstance(fprule_obj, FPRules):
                self.__pf_rules = fprule_obj
            else:
                raise TypeError('forwarding_rules accepts only an FPRules type')

    @property
    def port_forwarding_active(self):
        return self.__port_forwarding_active

    @property
    def port_forwarding_enabled(self):
        return self.__port_forwarding_possible

    def remove_forwarding_rule(self, rule_name):
        if self.__port_forwarding_possible and self.__port_forwarding_active:
            self.__pf_rules.remove_rule(rule_name)

    @classmethod
    def net_attach_types(cls):
        return cls.network_attach_types

    @classmethod
    def nic_types(cls):
        return cls.nic_brands