import unittest
from forwardedport import FPRules, ForwardedPort


class PortForwardingRulesTestCase(unittest.TestCase):

    def setUp(self):
        self.fpr = FPRules()

    def test_add_rule(self):
        fp = ForwardedPort()
        fp.set_fp_rule("SSH", "", 12222, "", 22)
        self.fpr.add_rule(fp)
        self.assertEqual(self.fpr.rule_count(), 1)
        # self.assertEqual(self.fpr.rules_names[0].rule_name)

    def test_add_rule_with_empty_title(self):
        # Adding a rule with an empty title should result in the FPRule assigning the title 'Rule X'
        # depending on the number of rules
        fp = ForwardedPort()
        fp.set_fp_rule(None, None, 12222, None, 22)
        self.fpr.add_rule(fp)
        self.assertTrue(self.fpr.list_rules().startswith("Rule 1"))

    def test_remove_rule(self):
        fp = ForwardedPort()
        fp.set_fp_rule(None, None, 12222, None, 22)
        self.fpr.add_rule(fp)
        self.assertEqual(self.fpr.rule_count(), 1)
        self.fpr.remove_rule("Rule 1")
        self.assertEqual(self.fpr.rule_count(), 0)

    def test_added_rule_has_fpr_instance_as_parent(self):
        fp = ForwardedPort()
        fp.set_fp_rule(None, None, 12222, None, 22)
        self.fpr.add_rule(fp)
        self.assertEqual(self.fpr, fp.rule_parent)

    def test_removed_rule_is_prev_added_rule(self):
        fp = ForwardedPort()
        fp.set_fp_rule(None, None, 12222, None, 22)
        self.fpr.add_rule(fp)
        removed_fp = self.fpr.remove_rule('Rule 1')
        self.assertEqual(removed_fp, fp)

    def test_adding_multiple_rules(self):
        host_port_start = 12222
        guest_port_start = 22
        for i in range(0,5):
            fp = ForwardedPort()
            fp.set_fp_rule(None, None, host_port_start + i, None, guest_port_start + i)
            self.fpr.add_rule(fp)
        self.assertEqual(self.fpr.rule_count(), 5)
        self.assertEqual(
            self.fpr.list_rules(),
            "Rule 1:12222->22\nRule 2:12223->23\nRule 3:12224->24\nRule 4:12225->25\nRule 5:12226->26"
        )

    def test_removing_multiple_rules(self):
        host_port_start = 12222
        guest_port_start = 22
        for i in range(0, 3):
            fp = ForwardedPort()
            fp.set_fp_rule(None, None, host_port_start + i, None, guest_port_start + i)
            self.fpr.add_rule(fp)
        self.assertEqual(self.fpr.rule_count(), 3)
        for i in range(0,3):
            self.fpr.remove_rule('Rule {}'.format(i + 1))
        self.assertEqual(self.fpr.rule_count(), 0)


