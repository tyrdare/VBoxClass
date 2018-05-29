from typing import Dict


class VMDevice:
    pass


class VMController:
    controller_types: Dict = {
        "IDE": ["PIIX4", "PIIX3", "ICH6"],
        "SATA": ["ACHI"],
        "SCSI": ["Lsilogic", "Buslogic"],
        "SAS": ["Lsilogic"],
        "Floppy": ["I82078"],
        "USB": ["USB"],
        "NVMe": ["NVMe"],
    }

    def __init__(self):
        self.__controller_type: str = None
        self.__controller_subtype: str = None
        self.__has_multiple_ports: bool = False
        self.__port_count: int = 0
        self.__use_host_io_cache: bool = False
        self.__devices = None

    @property
    def controller_type(self) -> str:
        return self.__controller_type

    @controller_type.setter
    def controller_type(self, controller_type: str):
        if controller_type in list(self.controller_types.keys()):
            self.__controller_type = controller_type
            if controller_type in ["SATA", "SAS"]:
                self.__has_multiple_ports = True
                # Defaults to having one port adding disks to the controller should also add ports
                self.__port_count = 1
            if controller_type in ["Floppy", "USB", "SAS", "SATA", "NVMe"]:
                self.__controller_subtype = self.controller_types.get(controller_type)[
                    0
                ]
        else:
            raise VMControllerError(
                "Invalid controller type: {}".format(controller_type)
            )

    @property
    def controller_subtype(self) -> str:
        return self.__controller_subtype

    @controller_subtype.setter
    def controller_subtype(self, controller_subtype: str):
        if not self.__controller_type:
            raise VMControllerError(
                "Controller type must be set before setting subtype"
            )

        if controller_subtype in self.controller_types[self.__controller_type]:
            self.__controller_subtype = controller_subtype
        else:
            raise VMControllerError(
                "Invalid subtype for {} controller: >>{}<<".format(
                    self.__controller_type, controller_subtype
                )
            )

    @property
    def use_host_io_cache(self) -> bool:
        return self.__use_host_io_cache

    @use_host_io_cache.setter
    def use_host_io_cache(self, enable: bool):
        self.__use_host_io_cache = enable

    @property
    def port_count(self) -> int:
        return self.__port_count

    @port_count.setter
    def port_count(self, num_ports: int):
        assert num_ports > 0
        if self.__controller_type:
            if self.__controller_type in ["SATA", "SCSI"]:
                self.__port_count = num_ports
            else:
                raise VMControllerError(
                    "Controller type {} does not require setting a port count".format(
                        self.__controller_type
                    )
                )
        else:
            raise VMControllerError("Controller type has not yet been set")

    def add_device(self, device: VMDevice):
        if isinstance(device, VMDevice):
            if not self.__devices:
                self.__devices = list()
            self.__devices.append(device)

    def remove_device(self, device):
        if device in self.__devices:
            del self.__devices[self.__disks.index(device)]
        else:
            raise DeviceNotFoundError("No such disk on the controller")


class VMDevice:
    DEVICE_TYPES = ["Hard", "Floppy", "ISO", "DVD/CDROM", "USB"]

    def __init__(self, parent_controller):
        self.__parent_controller = None
        self.__controller_port = None
        self.__title = ""
        self.__name = None
        self.__path = None
        self.__bytes_allocated = 0
        self.__size = 0
        self.__is_dynamic = None
        self.__uuid = None
        self.disk_type = None

    def __repr__(self):
        device_info = dict(
            title=self.__title,
            name=self.__name,
            uuid=self.__uuid,
            path=self.__path,
            bytes=self.__size,
            allocated=self.__bytes_allocated,
            dynamic="Yes" if self.__is_dynamic else "No",
        )
        repr_text = "Title:{title}\nName:{name}\nUuid:{uuid}\nPath:{path}\n"
        "Defined bytes{bytes}\nAllocated Bytes{allocated}\nDynamic{dynamic}"
        output = repr_text.format(device_info)
        return output


class DeviceNotFoundError(Exception):
    pass


class VMControllerError(Exception):
    pass
