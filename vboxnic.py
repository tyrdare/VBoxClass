from typing import List
from forwardedports import ForwardedPort

class VMNic:
    nic_brands: List[str] = [
        "PCnet-PC II (Am79C970A)",
        "PCnet-FAST III (Am97C973)",
        "Intel PRO/1000 MT Desktop (82540EM)",
        "Intel Pro/1000 T Server (82543GC)",
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

    def __init__(self):
        self.attached_to: str = None
        self.nic_brand: str = None
        self.mac_address: str = None
        self.adapter_number: int = 1
        self.port_forwarding: bool = False
        self.cable_connected: bool = True
        self.forwarded_ports: List[ForwardedPort] = []
        self.transparent_proxying = False

    def generate_mac_address(self) -> str:
        if self.mac_address:
            return self.mac_address
        else:
            # TODO - code to generate a MAC address
            return ''

    def update_network_attach_type(self, attach_type: str):
        if attach_type in self.network_attach_types:
           self.attached_to = attach_type