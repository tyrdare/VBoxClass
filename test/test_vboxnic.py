import unittest
import logging
from vboxvm import VBoxVM
from forwardedport import FPRules

logging.basicConfig(level=logging.INFO)

class TestVmNicTestCase(unittest.TestCase):

    def setUp(self):
        # A Nic is always instantiated having a VM
        self.vm = VBoxVM()
        self.nic = self.vm.nics[0]

    def test_nic_default_net_attach_type(self):
        self.assertEqual(self.nic.net_attach_type, "NAT")

    def test_nic_default_nic_type(self):
        self.assertEqual(self.nic.nic_type, "PCnet-PC II (Am79C970A)")

    def test_nic_default_port_forwarding_status(self):
        self.assertTrue(self.nic.port_forwarding_active)
        self.assertTrue(self.nic.port_forwarding_enabled)
        self.assertIsInstance(self.nic.forwarding_rules, FPRules)

    def test_change_to_nic_type(self):
        # It's a property, not an attribute, so we test setting and getting
        nic_brand = "Intel PRO/1000 T Server (82543GC)"
        self.nic.nic_type = nic_brand
        self.assertEqual(self.nic.nic_type, nic_brand)

    def test_change_to_net_attach_type(self):
        # It's a property, not an attribute, so we test setting and getting
        # Also, port forwarding should only be active when the attach_type is 'NAT'
        # and there should be no Forwarded Port Rules object
        attach_type = "Bridged Adapter"
        self.nic.net_attach_type = attach_type
        self.assertEqual(self.nic.net_attach_type, attach_type)
        self.assertFalse(self.nic.port_forwarding_enabled)
        self.assertFalse(self.nic.port_forwarding_active)
        self.assertIsNone(self.nic.forwarding_rules)

    def test_mac_address_not_hexadecimal_chars(self):
        with self.assertRaises(ValueError):
            self.nic.mac_address = 'oa;eiwfn;cnc'

    def test_mac_address_not_string(self):
        with self.assertRaises(TypeError):
            self.nic.mac_address = 0xa1b2c3d4e5f66

    def test_mac_address_too_short(self):
        # Mac addresses must be 12 characters
        with self.assertRaises(ValueError):
            self.nic.mac_address = 'EABFD94C7F1'

    def test_mac_address_leading_0x(self):
        m_addr = '0xa1b2c3d4e5f6'
        self.nic.mac_address = m_addr
        self.assertEqual(self.nic.mac_address, m_addr[2:])

    def test_mac_address_assign_removes_colons(self):
        addr_colons = 'EA:BF:D9:4C:7F:12'
        addr_no_colons = "EABFD94C7F12".lower()
        self.nic.mac_address = addr_colons
        self.assertEqual(self.nic.mac_address, addr_no_colons)

    def test_mac_address_generator(self):
        import re
        mac_addr = self.nic.generate_mac_address()
        self.assertIsInstance(mac_addr, str)
        self.assertEqual(len(mac_addr), 12)
        self.assertTrue(re.search(r'[0-9a-f]{12}', mac_addr), )
        logging.info(mac_addr)

    def test_nic__nic_types(self):
        self.assertIsInstance(self.nic.nic_types(), list)
        self.assertEqual(self.nic.nic_types(), self.nic.nic_brands)
        logging.info(self.nic.nic_types())

    def test_nic__net_attach_types(self):
        self.assertIsInstance(self.nic.net_attach_types(), list)
        self.assertEqual(self.nic.net_attach_types(), self.nic.network_attach_types)
        logging.info(self.nic.net_attach_types())


