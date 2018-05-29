import os
import sys
from typing import Dict, List, Tuple
from vboxnic import VMNic


class VBoxVM:
    """
    A class which basically holds configuration information for a VM
    """

    def __init__(self):
        self.boot_from = None
        self.system_settings: VMSystem = VMSystem()
        self.general_settings: VMGeneral = VMGeneral()
        self.controllers: List[VMController] = [VMController()]
        self.nics = list()
        self.nics.append(VMNic(self))


class VMGeneral:
    os_classes: List[str] = [
        "Linux",
        "Solaris",
        "Mac OS X",
        "BSD",
        "IBM OS/2",
        "Microsoft Windows",
        "Other",
    ]
    os_class_flavors: Dict = {
        "linux": [],
        "Windows": [],
        "Solaris": [],
        "BSD": [],
        "IBM OS/2": [],
        "Mac OS X": [],
        "Other": [],
    }

    def __init__(self):
        self.vmname: str = None
        self.vm_friendly_name: str = None
        self.vm_os_type: str = None
        self.vm_os_detail: str = None


class VMSystem:
    MEM_MIN = 0
    MEM_MAX = "16GB"
    CPU_MIN = 1
    CPU_MAX = 8

    def __init__(self):
        self.vm_mem: int = 1024  # MB
        self.cpus: int = None


class VMDisplay:
    VID_MEM_MIN = 0
    VID_MEM_MAX = 128
    AUTH_METHODS = ["Null", "External", "Guest"]

    def __init__(self):
        self.video_mem_size: int = 16  # MB
        self.monitor_count: int = 1
        self.use_3d_acceleration: bool = True
        self.use_2d_acceleration: bool = False  # Don't use this, most of the time.

        # remote connections
        self.enable_rdp_server: bool = False
        self.server_port: int = 3389
        self.authentication_method: str = None
        self.authentication_timeout: int = 5000
        self.allow_multiple_connections: bool = False


class VMMedia:

    def __init__(self):
        self.__media_type = None
        self.__controller = None
        hard_disks: List[VMHardDisk] = None

from vboxctlr import VMController


class VMNetAdapters:
    """Basically a bag to hold VMNics"""

    def __init__(self):
        self.nics: List[VMNic] = []







