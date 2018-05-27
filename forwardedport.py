from typing import List


# empty class def so ForwardedPort works
class FPRules:
    pass


class ForwardedPort:

    def __init__(self):
        self.__rule_name = None
        self.__host_ip: str = None
        self.__guest_ip: str = None
        self.__host_port: int = None
        self.__guest_port: int = None
        self.__rule_name = None
        self.__rule_parent = None

    @property
    def rule_parent(self) -> FPRules:
        return self.__rule_parent

    @rule_parent.setter
    def rule_parent(self, rule_parent: FPRules):
        if isinstance(rule_parent, FPRules) or rule_parent is None:
            self.__rule_parent = rule_parent
        else:
            raise TypeError(
                "ForwardedPort.rule_parent can only be an FPRules type or None"
            )

    @property
    def rule_name(self) -> str:
        return self.__rule_name

    @rule_name.setter
    def rule_name(self, rule_str: str):
        if isinstance(rule_str, str):
            self.__rule_name = rule_str
        else:
            raise TypeError("Rule name must be a string")

    @property
    def host_ip(self) -> str:
        return self.__host_ip

    @host_ip.setter
    def host_ip(self, ip_addr: str):
        """It's okay that the host ip is blank, though...why are you trying to set it to nothing?"""
        self._set_ip("host", ip_addr)

    def _set_ip(self, which, address):

        if address and address != "":
            if isinstance(address, str):
                # make sure it's in proper IPv4 format
                num_dots = address.count(".")
                if num_dots != 3:
                    raise ValueError("Address is not in proper IPv4 format")
                if which == "host":
                    self.__host_ip = address
                elif which == "guest":
                    self.__guest_ip = address
                else:
                    raise ValueError("Value must be applied to 'host' or 'guest'")
            else:
                raise TypeError("IP address must be a string")

    @property
    def guest_ip(self) -> str:
        return self.__guest_ip

    @guest_ip.setter
    def guest_ip(self, ip_addr):
        self._set_ip("guest", ip_addr)

    def set_fp_rule(self, rule_name, host_ip, host_port, guest_ip, guest_port):
        """
        Rules can be created with no ip addresses under NAT adapters.
        """
        self.__rule_name = rule_name
        self._set_ip("host", host_ip)
        self.__host_port = host_port
        self._set_ip("guest", guest_ip)
        self.__guest_port = guest_port

    @property
    def host_port(self) -> int:
        return self.__host_port

    @host_port.setter
    def host_port(self, port: int):
        if port and port > 0:
            if isinstance(port, int):
                self.__host_port = port
            else:
                raise TypeError("Port must be an integer")
        else:
            raise ValueError("Port must be a positive integer")

    @property
    def guest_port(self) -> int:
        return self.__guest_port

    @guest_port.setter
    def guest_port(self, port: int):
        if port and port > 0:
            if isinstance(port, int):
                self.__guest_port = port
            else:
                raise TypeError("Port must be an integer")
        else:
            raise ValueError("Port must be a positive integer")

    def __repr__(self):
        return "{}::(HOST){}:{}->(GUEST){}:{}".format(
            self.__rule_name,
            self.__host_ip,
            self.__host_port,
            self.__guest_ip,
            self.__guest_port,
        )


class FPRules:
    """Bag to hold Forwarded Ports"""

    def __init__(self):
        self.__rules: List[ForwardedPort] = list()
        self.__rule_names = list()

    def add_rule(self, rule: ForwardedPort):
        rule_name = ""
        if isinstance(rule, ForwardedPort):
            self.__rules.append(rule)
        else:
            raise TypeError("A rule must be a ForwardedPort")

        if rule.rule_name:
            rule_name = rule.rule_name
        else:
            # get length of current rules list
            num_rules = len(self.__rules)
            rule_name = "Rule {}".format(num_rules)
        self.__rule_names.append(rule_name)

        rule.rule_parent = self

    def remove_rule(self, rule_name) -> ForwardedPort:
        """
        Removing a non-existent rule has no effect.
        Removing from a zero length rule list has no effect
        """
        if self.__rules and self.__rule_names:
            rule_index = self.__rule_names.index(rule_name)
            self.__rules[rule_index].rule_parent = None
            del self.__rule_names[rule_index]
            return self.__rules.pop(rule_index)

    def get_rule_by_name(self, rule_name: str) -> ForwardedPort:
        pass

    def get_rule_by_index(self, rule_index: int) -> ForwardedPort:
        pass

    def list_rules(self) -> str:
        return self.__repr__()

    def rule_count(self) -> int:
        return len(self.__rules)

    def __repr__(self) -> str:
        rules_list = list()
        for index, rule in enumerate(self.__rules):
            rule_name = rule.rule_name if rule.rule_name else self.__rule_names[index]
            rules_list.append(
                "{}:{}->{}".format(rule_name, rule.host_port, rule.guest_port)
            )
        return "\n".join(rules_list)
