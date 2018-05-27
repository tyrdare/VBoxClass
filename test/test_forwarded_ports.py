import unittest
from forwardedport import FPRules, ForwardedPort


class ForwardedPortTestCase(unittest.TestCase):

    def setUp(self):
        self.fp = ForwardedPort()

    def test_host_bad_ipv4_addr(self):
        with self.assertRaises(ValueError):
            self.fp.host_ip = "11.13.4.11.8"

    def test_host_ip_assigned_nonstr(self):
        with self.assertRaises(TypeError):
            self.fp.host_ip = 10.34535

    def test_guest_bad_ipv4_addr(self):
        with self.assertRaises(ValueError):
            self.fp.guest_ip = "11.2.3"

    def test_guest_ip_assigned_non_str(self):
        with self.assertRaises(TypeError):
            self.fp.guest_ip = 123456

    def test_host_ports_assigned_neg_int(self):
        with self.assertRaises(ValueError):
            self.fp.host_port = -5

    def test_guest_port_assigned_neg_int(self):
        with self.assertRaises(ValueError):
            self.fp.guest_port = -22

    def test_guest_port_assigned_str(self):
        with self.assertRaises(TypeError):
            self.fp.host_port = "A"

    def test_guest_port_assigned_float(self):
        with self.assertRaises(TypeError):
            self.fp.guest_port = 9.776

    def test_host_port_assigned_str(self):
        with self.assertRaises(TypeError):
            self.fp.host_port = "A"

    def test_host_port_assigned_float(self):
        with self.assertRaises(TypeError):
            self.fp.host_port = 9.776

    def test_rule_name_is_not_str(self):
        with self.assertRaises(TypeError):
            self.fp.rule_name = 99

    def test_set_ip_fn_for_host(self):
        ip = "10.10.10.10"
        self.fp._set_ip("host", ip)
        self.assertEqual(self.fp.host_ip, ip)

    def test_set_ip_fn_for_guest(self):
        ip = "11.11.11.11"
        self.fp._set_ip("guest", ip)
        self.assertEqual(self.fp.guest_ip, ip)

    def test_set_ip_fn_bad_which(self):
        # Not that you would ever use an underscore method like this...would you?  WOULD YOU!
        with self.assertRaises(ValueError):
            self.fp._set_ip("elmer", "12.12.12.12")

    def test_repr_output(self):
        self.fp.rule_name = "First Port Forwarding Rule"
        self.fp.host_ip = "11.11.11.11"
        self.fp.host_port = 12222
        self.fp.guest_ip = "12.12.12.12"
        self.fp.guest_port = 22
        result_str = "{}::(HOST){}:{}->(GUEST){}:{}".format(
            self.fp.rule_name,
            self.fp.host_ip,
            self.fp.host_port,
            self.fp.guest_ip,
            self.fp.guest_port,
        )
        self.assertEqual(self.fp.__repr__(), result_str)

    def test_host_ip_assigned_none(self):
        self.fp.host_ip = None
        self.assertIsNone(self.fp.host_ip)

    def test_guest_ip_assigned_none(self):
        self.fp.guest_ip = None
        self.assertIsNone(self.fp.guest_ip)


if __name__ == "__main__":
    unittest.main()
